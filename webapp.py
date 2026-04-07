"""
********************************************************************************************
* Title: Zencrypt dApp             |********************************************************
* Developed by: imaclone.x         |********************************************************
* Date: August 10th 2022           |********************************************************
* Last Updated: November 13th 2025 |********************************************************
* Version: Beta.02                 |*****************************************************
********************************************************************************************
*****************************#*|  Zencrypt Beta.02  |***************************************
<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
********************************#* Description: |*******************************************
<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
*              Zencrypt dApp is a Flask application that can be used to:                *
*       - Generate hashes: using SHA256 hashing algorithm, with an optional salt value.    *
*       - Encrypt text and files: using Fernet symmetric encryption algorithm.             *
<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
""""""********************#* Web-App Implementations: |*************************************
- The CLI and webapp code are separated for clarity, scalability and modularity.           *
- The Web-App uses Flask and cryptography libraries with a HTML interface for the UI/UX.   *
********************************************************************************************
*           #* Some key differences in the dApp are                                        *
- #*Securely connect with Solana wallets (Phantom, Solflare, etc.) for authentication.     *
- #*The users Solana wallet address is used as a unique identifier for user accounts.      *
- #*Token gating is implemented to restrict access to users holding the Solsprite NFT.           *
********************************************************************************************
"""

import sys
from models import db, User, Hash, EncryptedText, Key, PGPKey 
#* Importing the required libraries for the webapp
from flask import Flask, request, render_template_string, redirect, url_for, session, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib
import os
import base64
import secrets
import requests
from functools import wraps
from datetime import timedelta
from dotenv import load_dotenv
from utils import generate_pgp_keypair, pgp_encrypt_message, pgp_decrypt_message
from flask_migrate import Migrate
from io import BytesIO
from flask import make_response

# -- Solana wallet authentication imports --
try:
    import base58
    from nacl.signing import VerifyKey
    from nacl.encoding import RawEncoder
except ImportError as e:
    print(f"Warning: Wallet authentication dependencies not installed: {e}")
    print("Install with: pip install base58 PyNaCl")
    base58 = None
    VerifyKey = None
    RawEncoder = None

# #* ---------------------- | Environment & Database Configuration | ---------------------- #

# Load environment variables from .env file
load_dotenv()

# Flask Configuration and JWT Manager
app = Flask(__name__)

# SQLite Configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', f'sqlite:///{basedir}/zencrypt.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

# Initialize database
db.init_app(app)
migrate = Migrate(app, db)

# Create tables
with app.app_context():
    db.create_all()

# Use SECRET_KEY from environment or generate a stable one for development
secret_key = os.environ.get('SECRET_KEY')
if secret_key:
    # If SECRET_KEY is a file path, read it; otherwise use it directly
    if secret_key.startswith('/') or secret_key.startswith('C:'):
        try:
            with open(secret_key, 'rb') as f:
                app.secret_key = f.read()
        except Exception:
            app.secret_key = secret_key.encode() if isinstance(secret_key, str) else secret_key
    else:
        app.secret_key = secret_key.encode() if isinstance(secret_key, str) else secret_key
else:
    # Fallback for development: use a fixed key derived from hostname
    # This makes sure that the key stays consistent across app restarts
    import hashlib
    fallback_key = hashlib.sha256(b'zencrypt-dev-key').digest()
    app.secret_key = fallback_key
    print("[WARNING] No SECRET_KEY set. Using development key (not secure for production)")

#* ---------------------- | Token Gate For Solsprite Holders | ---------------------- #
RPC_URL = os.getenv("SOLANA_DAS_RPC")  # Helius / provider DAS URL
COLLECTION_MINT = os.getenv("ZENCRYPT_COLLECTION_MINT")  # collection NFT mint

def has_zencrypt_pass(owner_address: str) -> bool:
    payload = {
        "jsonrpc": "2.0",
        "id": "zencrypt-check",
        "method": "searchAssets",
        "params": {
            "ownerAddress": owner_address,
            "grouping": ["collection", COLLECTION_MINT],
            "page": 1,
            "limit": 1
        }
    }
    r = requests.post(RPC_URL, json=payload, timeout=10)
    r.raise_for_status()
    data = r.json()
    assets = data.get("result", {}).get("items", []) or data.get("result", [])
    return len(assets) > 0

#* ---------------------- | Token Gating for SPL Tokens | ---------------------- #
import requests

TOKEN_MINT = os.getenv("ZENCRYPT_TOKEN_MINT", "6THr8etVzksaHHKPBPrUTjYCG6kwhqDVP2xvE5HW6W3B")
TOKEN_DECIMALS = 6
MIN_TOKEN_BALANCE = float(os.getenv("ZENCRYPT_MIN_TOKEN_BALANCE", "1"))
HELIUS_RPC_URL = os.getenv("RPC_URL", "https://mainnet.helius-rpc.com/")

def get_token_accounts_by_owner(owner_pubkey: str) -> list:
    """
    Get all token accounts owned by a wallet using the getTokenAccountsByOwner RPC call.
    Returns a list of token accounts.
    """
    try:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getTokenAccountsByOwner",
            "params": [
                owner_pubkey,
                {
                    "mint": TOKEN_MINT
                },
                {
                    "encoding": "jsonParsed"
                }
            ]
        }
        
        response = requests.post(HELIUS_RPC_URL, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if "error" in data:
            print(f"RPC Error: {data['error']}")
            return []
        
        return data.get("result", {}).get("value", [])
    
    except Exception as e:
        print(f"Error fetching token accounts: {e}")
        return []

def check_token_balance(wallet_address: str) -> tuple[bool, float]:
    """
    Check if a wallet holds the required token balance.
    Returns tuple (has_required_balance, balance_amount)
    """
    try:
        token_accounts = get_token_accounts_by_owner(wallet_address)
        
        if not token_accounts:
            return False, 0.0
        
        total_balance = 0.0
        
        for account in token_accounts:
            try:
                # Parse token amount from account data
                parsed_info = account.get("account", {}).get("data", {}).get("parsed", {})
                token_amount_info = parsed_info.get("info", {}).get("tokenAmount", {})
                amount = float(token_amount_info.get("amount", 0))
                decimals = token_amount_info.get("decimals", 6)
                
                # Convert from smallest unit to display amount
                display_amount = amount / (10 ** decimals)
                total_balance += display_amount
                
            except (ValueError, TypeError, KeyError) as e:
                print(f"Error parsing token account: {e}")
                continue
        
        has_required_balance = total_balance >= MIN_TOKEN_BALANCE
        return has_required_balance, total_balance
    
    except Exception as e:
        print(f"Error checking token balance: {e}")
        return False, 0.0

#* ---------------------- | Decorator for Solsprite Token Gating | ---------------------- #
def requires_zencrypt_pass(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        wallet = request.headers.get("X-Wallet-Address")
        if not wallet:
            return jsonify({"error": "wallet address required"}), 400
        try:
            if not has_zencrypt_pass(wallet):
                return jsonify({"error": "Missing Solsprite NFT"}), 403
        except Exception:
            return jsonify({"error": "NFT check failed"}), 500
        return f(*args, **kwargs)
    return wrapper

# #* ---------------------- | JWT Configuration | ---------------------- #

# secret key and token expiration time of 1 hour
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

# Initialize JWT Manager
jwt = JWTManager(app)

# #* ---------------------- | Key Management | ---------------------- #
def initialize_key(user_id):
    #* Initialize or retrieve encryption key for a user
    # Check for existing active key
    key = Key.query.filter_by(user_id=user_id, active=True).first()
    
    if key:
        return key.key_value.encode()
    
    # Generate new key
    new_key = Fernet.generate_key()
    
    # Store in database
    key_entry = Key(
        key_value=new_key.decode(),
        user_id=user_id
    )
    
    try:
        db.session.add(key_entry)
        db.session.commit()
        return new_key
    except Exception as e:
        db.session.rollback()
        print(f"Error storing key: {e}")
        # Fallback to temporary key if database storage fails
        return Fernet.generate_key()

def get_cipher_suite(user_id):
    #* Get Fernet cipher suite for a user
    key = initialize_key(user_id)
    return Fernet(key)

def rotate_key(user_id):
    #*Rotate encryption key for a user
    try:
        # Deactivate old key
        old_key = Key.query.filter_by(user_id=user_id, active=True).first()
        if old_key:
            old_key.active = False
            
        # Generate and store new key
        new_key = Fernet.generate_key()
        key_entry = Key(
            key_value=new_key.decode(),
            user_id=user_id
        )
        
        db.session.add(key_entry)
        db.session.commit()
        
        return new_key
    
    except Exception as e:
        db.session.rollback()
        print(f"Error rotating key: {e}")
        return None

def initialize_ecc():
    #* Initialize ECC handler for the application
    from crypto_utils import ECCHandler
    return ECCHandler()

def initialize_argon2():
    #* Initialize Argon2 handler for the application
    from crypto_utils import Argon2Handler
    return Argon2Handler()

def get_file_processor():
    #* Get configured file processor instance
    from crypto_utils import ParallelFileProcessor
    return ParallelFileProcessor(num_workers=os.cpu_count())  # Only pass num_workers

# #* ---------------------- | Styling and HTML for the Web-App | ---------------------- #

STYLE_TEMPLATE = """
    body {
        background-color: #1e1e1e;
        color: #ffffff;
        font-family: 'Nunito Sans', sans-serif;
        line-height: 1.6;
        margin: 0;
        padding: 0;
        min-height: 100vh;
        display: flex;
        flex-direction: column;
    }
    .container {
        width: 95%;
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
        flex: 1;
    }
    .form-container {
        width: 95%;
        max-width: 600px;
        margin: 2rem auto;
        padding: 2rem;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .form-container form {
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 1rem;
    }
    .button-wrapper {
        width: 100%;
        display: flex;
        justify-content: center;
        margin: 1rem 0;
    }
    textarea, input[type="text"], input[type="password"], input[type="email"] {
        width: 100%;
        padding: 15px;
        font-size: 16px;
        border-radius: 5px;
        background-color: #2d2d2d;
        color: #ffffff;
        border: 1px solid #444;
        transition: border-color 0.3s ease;
    }
    textarea {
        height: 10vh;
        resize: vertical;
    }
    textarea:focus, input:focus {
        border-color: #0066ff;
        outline: none;
    }
    button {
        width: 100%;
        max-width: 300px;
        padding: 15px;
        font-size: 16px;
        border-radius: 5px;
        background-color: #0066ff;
        color: #ffffff;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    button:hover {
        background-color: #0052cc;
    }
    .menu {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        justify-content: center;
        margin: 20px 0;
    }
    .menu form {
        margin: 0;
    }
    .menu input[type="file"] {
        display: none;
    }
    .menu button {
        margin: 0;
        padding: 8px 16px;
        white-space: nowrap;
    }
    .auth-container {
        width: 100%;
        max-width: 400px;
        margin: 2rem auto;
        padding: 2rem;
    }
    .navbar {
        background-color: #1e1e1e;
        border-bottom: 1px solid #444;
        padding: 1rem;
        width: 100%;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    .navbar-container {
        max-width: 1200px;
        margin: 0 auto;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .navbar-brand {
        font-size: 1.5rem;
        font-weight: bold;
        color: #ffffff;
        cursor: pointer;
        user-select: none;
        padding: 0.5rem;
    }
    .navbar-menu {
        background-color: #1e1e1e;
        border-bottom: 1px solid #444;
        padding: 1rem;
        display: none;
    }
    .navbar-menu.active {
        display: block;
    }
    .main-content {
        padding: 2rem 1rem;
        flex: 1;
    }
    .output {
        width: 95%;
        max-width: 600px;
        margin: 2rem auto;
        padding: 1.5rem;
        background: #2d2d2d;
        border-radius: 5px;
        border: 1px solid #444;
        text-align: center;
        white-space: pre-wrap;
        word-break: break-all;
        font-family: 'Consolas', monospace;
    }
    
    .output-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 2rem;
    }
    @media (max-width: 768px) {
        .container {
            width: 95%;
            padding: 10px;
        }
        .menu {
            flex-direction: column;
            align-items: stretch;
        }
        .menu button {
            width: 100%;
            margin: 5px 0;
        }
        .form-container {
            padding: 1rem;
        }
    }
"""

#* Define header and banner separately because its reused in different pages
HEADER_TEMPLATE = """
    <div class="header">
        <div style="text-align: center; font-family: 'Helvetica', sans-serif; color: #999;">
            <p style="font-size: 1.1em; margin: 0.5em 0;">
                <span style="font-family: 'Consolas', monospace;">© 2025</span> 
                All rights reserved by 
                <span style="font-family: 'Consolas', monospace; color: #0066ff;">imaclone.x</span>
            </p>
        </div>
    </div>
"""

#* Main application template
APP_TEMPLATE = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Zencrypt Web-App</title>
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@400;600&display=swap">
    <style>
        {STYLE_TEMPLATE}
    </style>
    <script crossorigin src="https://unpkg.com/react@17/umd/react.development.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@17/umd/react-dom.development.js"></script>
</head>
<body>
    <div class="main-content">
        {HEADER_TEMPLATE}
        
        {{% if session.get('user_id') %}}
            <nav class="navbar">
                <div class="navbar-container">
                    <div class="navbar-brand" onclick="toggleMenu()">
                        ☰ Zencrypt
                    </div>
                    <div class="navbar-menu" id="navMenu">
                        <div class="menu">
                            {{% if session.get('wallet_address') %}}
                                <span style="padding: 8px 16px; color: #999; font-size: 0.9em;">Wallet: {{{{ session['wallet_address'][:8] }}}}...{{{{ session['wallet_address'][-4:] }}}}</span>
                            {{% endif %}}
                            <a href="/logout"><button>Logout</button></a>  
                            <a href="/export-key"><button>Export Key</button></a>
                            <a href="/import-key"><button>Import Key</button></a>
                        </div>
                        <div>
                            <a href="/"><button>Generate Hash</button></a>
                            <a href="/argon2"><button>Argon2</button></a>
                            <a href="/encrypt"><button>Encrypt Text</button></a>
                            <a href="/decrypt"><button>Decrypt Text</button></a>
                            <a href="/file"><button>Encode Text Files</button></a>
                            <a href="/pgp"><button>PGP</button></a>
                        </div>
                    </div>
                </div>
            </nav>
            <hr style="border: 0; height: 1px; background-image: linear-gradient(to right, rgba(0, 102, 255, 0), rgba(0, 102, 255, 0.75), rgba(0, 102, 255, 0));">
            {{{{ content | safe }}}}
            {{% if output %}}
                <div class="output-container">
                    <div class="output">{{{{ output }}}}</div>
                </div>
            {{% endif %}}
        {{% else %}}
            <div class="auth-container">
                <h2>{{% if request.path == '/register' %}}Register{{% else %}}Login{{% endif %}}</h2>
                {{% if error %}}
                    <div class="error-message">{{{{ error }}}}</div>
                {{% endif %}}
                <form method="POST" action="{{% if request.path == '/register' %}}/register{{% else %}}/login{{% endif %}}">
                    <input type="email" name="email" placeholder="Email" required>
                    <br><br>
                    <input type="password" name="password" placeholder="Password" required>
                    <br><br>
                    <button type="submit">{{% if request.path == '/register' %}}Register{{% else %}}Login{{% endif %}}</button>
                </form>
                <hr style="border: 0; height: 1px; background-image: linear-gradient(to right, transparent, #444, transparent); margin: 20px 0;">
                <p style="text-align: center; margin: 10px 0;">
                    <a href="/connect-wallet" style="color: #0066ff; font-weight: bold; text-decoration: none;">Connect Solana Wallet Instead →</a>
                </p>
                {{% if request.path == '/register' %}}
                    <p><code>Already have an account? <a href="/login">Login</code></a></p>
                {{% else %}}
                    <p><code>Don't have an account? <a href="/register">Register</code></a></p>
                {{% endif %}}
            </div>
            <hr style="border: 0; height: 1px; background-image: linear-gradient(to right, rgba(0, 102, 255, 0), rgba(0, 102, 255, 0.75), rgba(0, 102, 255, 0));">
            <h1 style="text-align: center;">Zencrypt Web-App</h1>
            <div class="links">
                <h6 style="text-align: center;">
                <li><b>White Papers</b> - <a href="https://zencrypt.gitbook.io/zencrypt" target="_blank">https://zencrypt.gitbook.io/zencrypt</a></li>
                <li><b>ePortfolio</b> - <a href="https://www.imaclone.x" target="_blank">https://www.imaclone.x</a></li>
                </h6>
            </div>
            <hr style="border: 0; height: 1px; background-image: linear-gradient(to right, rgba(0, 102, 255, 0), rgba(0, 102, 255, 0.75), rgba(0, 102, 255, 0));">
        {{% endif %}}
    </div>
    <script>
        function toggleMenu() {{
            var menu = document.getElementById('navMenu');
            // Guard against pages without a navbar
            if (!menu) return;
            menu.classList.toggle('active');
        }}
        
        document.addEventListener('click', function(event) {{
            var menu = document.getElementById('navMenu');
            var brand = document.querySelector('.navbar-brand');

            // If there's no menu on the page, nothing to do
            if (!menu) return;

            var clickedInsideMenu = menu.contains(event.target);
            var clickedOnBrand = brand && brand.contains(event.target);

            if (!clickedInsideMenu && !clickedOnBrand) {{
                menu.classList.remove('active');
            }}
        }});
        
        window.addEventListener('scroll', function() {{
            var menu = document.getElementById('navMenu');
            if (menu && menu.classList.contains('active')) {{
                menu.classList.remove('active');
            }}
        }});
    </script>
</body>
</html>
"""

# * ---------------------- | Web-App Routes | ---------------------- #
# * Checks if the database is connected and returns an error message if not connected when the webapp is started.
def safe_db_operation(operation): 
    if db is None:                                      # Check if the database is connected
        return None, "Database not connected"           # Return an error message if the database is not connected
    try:
        result = operation()                            # Perform the database operation and store the result
        return result, None                             # Return the result and no error message if the operation is successful
    except Exception as e:                              # Catch any exceptions that occur during the database operation
        print(f"Database operation error: {e}")         # Print an error message if the database operation fails
        return None, str(e)                             # Return no result and an error message if the operation fails

#* ---------------------- | Favicon Route | ---------------------- #
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

# ---------------------- | Wallet Auth (Solana) | ---------------------- #

@app.route('/auth', methods=['GET'])
def auth_page():
    if session.get('user_id'):
        return redirect(url_for('hash_page'))
    return redirect(url_for('connect_wallet_page'))

@app.route('/auth/nonce', methods=['GET'])
def auth_nonce():
    # Generate a random nonce and store in session
    nonce = secrets.token_hex(16)
    session['auth_nonce'] = nonce
    return jsonify({'nonce': nonce})

@app.route('/auth/verify', methods=['POST'])
def auth_verify():
    if not base58 or not VerifyKey or not RawEncoder:
        return jsonify({'error': 'Wallet authentication not available. Install base58 and PyNaCl.'}), 503
    
    data = request.get_json(silent=True) or {}
    public_key_b58 = data.get('public_key', '')
    signature_b64 = data.get('signature_b64', '')
    nonce = data.get('nonce', '')
    expected_nonce = session.get('auth_nonce')
    
    if not (public_key_b58 and signature_b64 and nonce and expected_nonce and nonce == expected_nonce):
        return jsonify({'error': 'Invalid payload'}), 400

    try:
        # Decode wallet public key and signature
        pubkey_bytes = base58.b58decode(public_key_b58)
        signature = base64.b64decode(signature_b64)
        
        # Verify Ed25519 signature
        verify_key = VerifyKey(pubkey_bytes)
        verify_key.verify(nonce.encode('utf-8'), signature, encoder=RawEncoder)
    except Exception as e:
        print(f"Signature verification failed: {e}")
        return jsonify({'error': 'Signature verification failed'}), 400

    # Check token balance - TOKEN GATE CHECK
    has_tokens, balance = check_token_balance(public_key_b58)
    if not has_tokens:
        return jsonify({
            'error': 'Insufficient token balance',
            'message': f'You have {balance} tokens but need at least {MIN_TOKEN_BALANCE} {TOKEN_MINT} token to access Zencrypt.',
            'balance': balance,
            'required': MIN_TOKEN_BALANCE,
            'token_mint': TOKEN_MINT
        }), 403

    # Upsert user by wallet address
    user = User.query.filter_by(wallet_address=public_key_b58).first()
    
    if user is None:
        try:
            # Create new user with wallet address
            user = User(
                wallet_address=public_key_b58,
                email=f"{public_key_b58}@wallet.local",
                password_hash=generate_password_hash(secrets.token_hex(16))
            )
            db.session.add(user)
            db.session.commit()
            
            # Initialize encryption key for new user
            initialize_key(user.id)
        except Exception as e:
            db.session.rollback()
            print(f"User creation failed: {e}")
            return jsonify({'error': 'User creation failed'}), 500

    # Establish session
    session['user_id'] = user.id
    session['wallet_address'] = public_key_b58
    session.pop('auth_nonce', None)
    
    return jsonify({'success': True, 'user_id': user.id}), 200

@app.route('/connect-wallet', methods=['GET'])
def connect_wallet_page():
    """Wallet connection page for Solana wallet authentication (Phantom, Solflare, etc.)."""
    # If already logged in, redirect to hash_page
    if session.get('user_id'):
        return redirect(url_for('hash_page'))
    
    wallet_connect_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Zencrypt dApp</title>
        <link rel="icon" type="image/x-icon" href="/favicon.ico">
        <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@400;600&display=swap">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                background: linear-gradient(135deg, #1e1e1e 0%, #2d2d2d 100%);
                color: #ffffff;
                font-family: 'Nunito Sans', sans-serif;
                line-height: 1.6;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }
            .container {
                max-width: 500px;
                width: 100%;
                background: rgba(45, 45, 45, 0.9);
                border: 1px solid #444;
                border-radius: 10px;
                padding: 40px;
                box-shadow: 0 8px 32px rgba(0, 102, 255, 0.1);
            }
            .header {
                text-align: center;
                margin-bottom: 40px;
            }
            .header h1 {
                font-size: 2em;
                margin-bottom: 10px;
                background: linear-gradient(135deg, #0066ff, #00d4ff);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            .header p {
                color: #999;
                font-size: 0.95em;
            }
            .wallet-buttons {
                display: flex;
                flex-direction: column;
                gap: 15px;
                margin-bottom: 30px;
            }
            .wallet-btn {
                display: flex;
                align-items: center;
                gap: 12px;
                padding: 15px 20px;
                background: #2d2d2d;
                border: 2px solid #444;
                border-radius: 8px;
                color: #fff;
                font-size: 1em;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
            }
            .wallet-btn:hover {
                border-color: #0066ff;
                background: rgba(0, 102, 255, 0.1);
                transform: translateY(-2px);
            }
            .wallet-btn svg {
                width: 24px;
                height: 24px;
            }
            .divider {
                text-align: center;
                margin: 30px 0;
                color: #666;
            }
            .divider span {
                background: #2d2d2d;
                padding: 0 10px;
                position: relative;
                z-index: 1;
            }
            .email-login {
                text-align: center;
            }
            .email-login a {
                color: #0066ff;
                text-decoration: none;
                font-weight: 600;
                transition: color 0.3s ease;
            }
            .email-login a:hover {
                color: #00d4ff;
            }
            .status {
                margin-top: 20px;
                padding: 15px;
                border-radius: 8px;
                text-align: center;
                display: none;
            }
            .status.loading {
                display: block;
                background: rgba(0, 102, 255, 0.1);
                border: 1px solid #0066ff;
                color: #0066ff;
            }
            .status.error {
                display: block;
                background: rgba(255, 0, 0, 0.1);
                border: 1px solid #ff0000;
                color: #ff6b6b;
            }
            .status.success {
                display: block;
                background: rgba(0, 255, 0, 0.1);
                border: 1px solid #00ff00;
                color: #00ff00;
            }
            .footer {
                margin-top: 30px;
                text-align: center;
                color: #666;
                font-size: 0.9em;
            }
            .footer p {
                margin-top: 10px;
            }
            .footer a {
                color: #0066ff;
                text-decoration: none;
            }
            .footer a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Zencrypt</h1>
                <p>Connect your Solana wallet to get started</p>
                <p style="color: #999; font-size: 0.85em; margin-top: 10px;">
                    ⚠️ Requires at least 1 Solsprite NFT from the Zencrypt collection to access the app.
                </p>
            </div>
            
            <div class="wallet-buttons">
                <button class="wallet-btn" id="phantomBtn" onclick="connectPhantom()">
                    <span>🦄</span>
                    <span>Phantom</span>
                </button>
                <button class="wallet-btn" id="solflareBtn" onclick="connectSolflare()">
                    <span>✨</span>
                    <span>Solflare</span>
                </button>
                <button class="wallet-btn" id="ledgerBtn" onclick="connectLedger()">
                    <span>💾</span>
                    <span>Ledger Live</span>
                </button>
            </div>
            
            <div class="divider"><span>or</span></div>
            
            <div class="email-login">
                <p>Don't have the required token? <a href="https://jup.ag/swap/" target="_blank">Get it on Jupiter</a></p>
            </div>
            
            <div class="status" id="status"></div>
            
            <div class="footer">
                <p>© 2025 Zencrypt - Developed by <a href="https://www.imaclone.x" target="_blank">imaclone.x</a></p>
            </div>
        </div>

        <script>
            const statusEl = document.getElementById('status');
            
            function showStatus(message, type = 'loading') {
                statusEl.textContent = message;
                statusEl.className = 'status ' + type;
            }
            
            function hideStatus() {
                statusEl.className = 'status';
            }
            
            async function getNonce() {
                try {
                    const res = await fetch('/auth/nonce');
                    const data = await res.json();
                    return data.nonce;
                } catch (e) {
                    console.error('Failed to get nonce:', e);
                    throw e;
                }
            }
            
            async function verifySignature(publicKey, signature, nonce) {
                try {
                    const res = await fetch('/auth/verify', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            public_key: publicKey,
                            signature_b64: signature,
                            nonce: nonce
                        })
                    });
                    
                    const data = await res.json();
                    
                    if (!res.ok) {
                        // Handle token gating error (403)
                        if (res.status === 403 && data.message) {
                            throw new Error(data.message);
                        }
                        throw new Error(data.error || 'Verification failed');
                    }
                    
                    return data;
                } catch (e) {
                    console.error('Verification error:', e);
                    throw e;
                }
            }
            
            async function connectPhantom() {
                try {
                    if (!window.solana || !window.solana.isPhantom) {
                        showStatus('Phantom wallet not found. Please install the Phantom extension.', 'error');
                        setTimeout(() => window.open('https://phantom.app/', '_blank'), 2000);
                        return;
                    }
                    
                    showStatus('Connecting to Phantom...', 'loading');
                    
                    // Request connection
                    const response = await window.solana.connect();
                    const publicKey = response.publicKey.toString();
                    
                    showStatus('Getting nonce...', 'loading');
                    const nonce = await getNonce();
                    
                    showStatus('Waiting for wallet signature...', 'loading');
                    // Sign the nonce
                    const msg = new TextEncoder().encode(nonce);
                    const signature = await window.solana.signMessage(msg, 'utf8');
                    const signatureB64 = btoa(String.fromCharCode.apply(null, signature.signature));
                    
                    showStatus('Checking token balance...', 'loading');
                    await verifySignature(publicKey, signatureB64, nonce);
                    
                    showStatus('✓ Successfully authenticated!', 'success');
                    setTimeout(() => window.location.href = '/', 1500);
                } catch (e) {
                    console.error('Phantom auth error:', e);
                    showStatus('Error: ' + e.message, 'error');
                }
            }
            
            async function connectSolflare() {
                try {
                    if (!window.solflare) {
                        showStatus('Solflare wallet not found. Please install the Solflare extension.', 'error');
                        setTimeout(() => window.open('https://solflare.com/', '_blank'), 2000);
                        return;
                    }
                    
                    showStatus('Connecting to Solflare...', 'loading');
                    
                    await window.solflare.connect();
                    const publicKey = window.solflare.publicKey.toString();
                    
                    showStatus('Getting nonce...', 'loading');
                    const nonce = await getNonce();
                    
                    showStatus('Waiting for wallet signature...', 'loading');
                    const msg = new TextEncoder().encode(nonce);
                    const signature = await window.solflare.signMessage(msg, 'utf8');
                    const signatureB64 = btoa(String.fromCharCode.apply(null, signature));
                    
                    showStatus('Checking token balance...', 'loading');
                    await verifySignature(publicKey, signatureB64, nonce);
                    
                    showStatus('✓ Successfully authenticated!', 'success');
                    setTimeout(() => window.location.href = '/', 1500);
                } catch (e) {
                    console.error('Solflare auth error:', e);
                    showStatus('Error: ' + e.message, 'error');
                }
            }
            
            function connectLedger() {
                showStatus('Ledger wallet support coming soon!', 'error');
            }
        </script>
    </body>
    </html>
    """
    
    return render_template_string(wallet_connect_html)

#* ---------------------- | Logout Route | ---------------------- #
@app.route('/logout')
def logout():
    user_id = session.get('user_id')
    if user_id:
    #* ---------------------- | Deleting Logged Data | ---------------------- #
        # try:
        #     # Clean up user data
        #     Hash.query.filter_by(user_id=user_id).delete()
        #     EncryptedText.query.filter_by(user_id=user_id).delete()
        #     # Deactivate user's keys
        #     Key.query.filter_by(user_id=user_id, active=True).update({"active": False})
        #     db.session.commit()
        # except Exception as e:
        #     db.session.rollback()
        #     print(f"Error cleaning up user data: {e}")
        pass
    
    session.clear()
    return redirect(url_for('connect_wallet_page'))

#* ---------------------- | Hashing and Main Routes | ---------------------- #

@app.route('/', methods=['GET', 'POST'])
def hash_page():
    if not session.get('user_id'):
        return redirect(url_for('connect_wallet_page'))
    
    content = """
    <div class="form-container">
        <form method="POST">
            <textarea name="text" placeholder="Enter text to hash"></textarea>
            <input type="text" name="salt" placeholder="Salt (optional)">
            <div class="button-wrapper">
                <button type="submit">Generate Hash</button>
            </div>
        </form>
    </div>
    """
    
    if request.method == 'POST':
        text = request.form.get('text', '')
        salt = request.form.get('salt', '')
        if text:
            hash_value = hashlib.sha256((text + salt).encode()).hexdigest()
            
            new_hash = Hash(
                hash_value=hash_value,
                salt=salt,
                user_id=session['user_id']
            )
            db.session.add(new_hash)
            db.session.commit()
            
            return render_template_string(APP_TEMPLATE,
                content=content,
                output=f"SHA256 Hash:\n{hash_value}")
    
    return render_template_string(APP_TEMPLATE, content=content)

#* ---------------------- | Encryption & Decryption Routes | ---------------------- #

@app.route('/encrypt', methods=['GET', 'POST'])
def encrypt_page():
    if not session.get('user_id'):
        return redirect(url_for('connect_wallet_page'))
    
    content = """
    <div class="form-container">
        <form method="POST">
            <textarea name="text" placeholder="Enter text to encrypt"></textarea>
            <div class="button-wrapper">
                <button type="submit">Encrypt</button>
            </div>
        </form>
    </div>
    """
    
    if request.method == 'POST':
        text = request.form.get('text', '')
        if text:
            try:
                cipher_suite = get_cipher_suite(session['user_id'])
                encrypted = cipher_suite.encrypt(text.encode())
                
                # Store in database
                new_encrypted = EncryptedText(
                    encrypted_content=encrypted.decode(),
                    user_id=session['user_id']
                )
                db.session.add(new_encrypted)
                db.session.commit()
                
                return render_template_string(APP_TEMPLATE,
                    content=content,
                    output=f"Encrypted Text:\n{encrypted.decode()}")
            except Exception as e:
                db.session.rollback()
                return render_template_string(APP_TEMPLATE,
                    content=content,
                    output=f"Error: {str(e)}")
    
    return render_template_string(APP_TEMPLATE, content=content)

#* Route to the decrypt text page of the web-app with the decryption function
@app.route('/decrypt', methods=['GET', 'POST'])
def decrypt_page():
    if not session.get('user_id'):
        return redirect(url_for('connect_wallet_page'))
    
    content = """
    <div class="form-container">
        <form method="POST">
            <textarea name="text" placeholder="Enter text to decrypt"></textarea>
            <div class="button-wrapper">
                <button type="submit">Decrypt</button>
            </div>
        </form>
    </div>
    """
    
    if request.method == 'POST':
        text = request.form.get('text', '')
        if text:
            try:
                cipher_suite = get_cipher_suite(session['user_id'])
                decrypted = cipher_suite.decrypt(text.encode())
                return render_template_string(APP_TEMPLATE,
                    content=content,
                    output=f"Decrypted Text:\n{decrypted.decode()}")
            except Exception as e:
                return render_template_string(APP_TEMPLATE,
                    content=content,
                    output=f"Error: {str(e)}")
    
    return render_template_string(APP_TEMPLATE, content=content)

#* ---------------------- | File Operations Route | ---------------------- #

#* Route to the file operations page of the web-app with the file encryption/decryption function
@app.route('/file', methods=['GET', 'POST'])
def file_page():
    if not session.get('user_id'):
        return redirect(url_for('connect_wallet_page'))
    
    content = """
    <div class="form-container">
        <form method="POST" enctype="multipart/form-data" style="text-align: center;">
            <div class="file-upload-wrapper" style="margin: 20px 0;">
                <label for="file-upload" class="custom-file-upload" style="
                    display: inline-block;
                    padding: 10px 20px;
                    background: #2d2d2d;
                    color: #fff;
                    border: 1px solid #444;
                    border-radius: 5px;
                    cursor: pointer;
                    margin-bottom: 10px;">
                    Choose File
                </label>
                <input id="file-upload" type="file" name="file" required style="display: none;">
                <div id="file-name" style="margin-top: 5px; color: #999;"></div>
            </div>
            <input type="password" name="password" placeholder="Enter Password" required style="width: 75%;">
            <select name="operation" style="
                width: 75%;
                padding: 15px;
                margin: 20px 0;
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #444;
                border-radius: 5px;">
                <option value="encrypt">Encrypt File</option>
                <option value="decrypt">Decrypt File</option>
            </select>
            <div class="button-wrapper">
                <button type="submit">Process File</button>
            </div>
        </form>
    </div>
    <script>
        document.getElementById('file-upload').onchange = function() {
            document.getElementById('file-name').textContent = this.files[0] ? this.files[0].name : '';
        };
    </script>
    """
    
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template_string(APP_TEMPLATE,
                content=content,
                output="Please select a file to process")
            
        file = request.files['file']
        if file.filename == '':
            return render_template_string(APP_TEMPLATE,
                content=content,
                output="No file selected")
            
        try:
            file_content = file.read()
            password = request.form.get('password', '').encode()
            operation = request.form.get('operation')
            
            if not password:
                return render_template_string(APP_TEMPLATE,
                    content=content,
                    output="Password is required")
            
            cipher_suite = get_cipher_suite(session['user_id'])
            if operation == 'encrypt':
                encrypted = cipher_suite.encrypt(file_content)
                return render_template_string(APP_TEMPLATE,
                    content=content,
                    output=f"{base64.b64encode(encrypted).decode()}")
            else:
                try:
                    decrypted = cipher_suite.decrypt(base64.b64decode(file_content))
                    return render_template_string(APP_TEMPLATE,
                        content=content,
                        output=f"{decrypted.decode()}")
                except Exception:
                    return render_template_string(APP_TEMPLATE,
                        content=content,
                        output="Invalid encrypted file or wrong password")
                
        except Exception as e:
            return render_template_string(APP_TEMPLATE,
                content=content,
                output=f"Error processing file: {str(e)}")
    
    return render_template_string(APP_TEMPLATE, content=content)

#* ---------------------- | Export / Import Keys Routes | ---------------------- #

@app.route('/export-key')
def export_key():
    if not session.get('user_id'):
        return redirect(url_for('connect_wallet_page'))
    
    try:
        key = Key.query.filter_by(user_id=session['user_id'], active=True).first()
        if key:
            key_name = request.args.get('key_name', 'private')  # Default to 'zen_key' if no name provided
            response = app.response_class(
                key.key_value,
                mimetype='application/octet-stream',
                headers={'Content-Disposition': f'attachment;filename={key_name}.key'}
            )
            return response
        return "No active key found", 404
    except Exception as e:
        return f"Error exporting key: {str(e)}", 500

@app.route('/import-key', methods=['GET', 'POST'])
def import_key():
    if not session.get('user_id'):
        return redirect(url_for('connect_wallet_page'))
    
    if request.method == 'GET':
        # Show the file upload form 
        content = """
        <div class="form-container">
            <form method="POST" action="/import-key" enctype="multipart/form-data">
                <input type="file" name="key_file" style="display: none;" id="key_file" onchange="this.form.submit()">
                <button type="button" onclick="document.getElementById('key_file').click()">Import Key</button>
            </form>
        </div>
        """
        return render_template_string(APP_TEMPLATE, content=content)
    
    # Handle POST request (file upload)
    if 'key_file' not in request.files:
        return redirect(url_for('hash_page'))
        
    file = request.files['key_file']
    if file.filename == '':
        return redirect(url_for('hash_page'))
        
    try:
        key_content = file.read().decode().strip()
        # Deactivate old key
        Key.query.filter_by(user_id=session['user_id'], active=True).update({"active": False})
        
        # Create new key entry
        new_key = Key(
            key_value=key_content,
            user_id=session['user_id'],
            active=True
        )
        db.session.add(new_key)
        db.session.commit()
        return redirect(url_for('hash_page'))
    except Exception as e:
        db.session.rollback()
        return f"Error importing key: {str(e)}", 500
    
#* ---------------------- | PGP Operation Routes | ---------------------- #

@app.route('/pgp', methods=['GET'])
def pgp_page():
    if not session.get('user_id'):
        return redirect(url_for('connect_wallet_page'))
    
    content = """
    <div class="form-container">
        <form method="POST" action="/pgp/generate">
            <div class="button-wrapper">
                <button type="submit">Generate Keys</button>
            </div>
        </form>
        <form method="POST" action="/pgp/encrypt">
            <textarea name="message" placeholder="Message:"></textarea>
            <input type="text" name="recipient_email" placeholder="Email of recipient" required>
            <div class="button-wrapper">
                <button type="submit">Encrypt</button>
            </div>
        </form>
        <form method="POST" action="/pgp/decrypt">
            <textarea name="encrypted_message" placeholder="Message:"></textarea>
            <div class="button-wrapper">
                <button type="submit">Decrypt</button>
            </div>
        </form>
    </div>
    """
    
    return render_template_string(APP_TEMPLATE, content=content)

@app.route('/pgp/generate', methods=['POST'])
def generate_pgp():
    if not session.get('user_id'):
        return redirect(url_for('connect_wallet_page'))
    
    try:
        private_key, public_key = generate_pgp_keypair()
        
        # Deactivate old keys
        PGPKey.query.filter_by(user_id=session['user_id'], active=True).update({"active": False})
        
        # Store new keys
        new_keys = PGPKey(
            public_key=public_key,
            private_key=private_key,
            user_id=session['user_id']
        )
        
        db.session.add(new_keys)
        db.session.commit()
        
        return redirect(url_for('pgp_page'))
    except Exception as e:
        return f"Error generating keys: {str(e)}", 500

@app.route('/pgp/encrypt', methods=['POST'])
def pgp_encrypt():
    if not session.get('user_id'):
        return redirect(url_for('connect_wallet_page'))
    
    message = request.form.get('message')
    recipient_email = request.form.get('recipient_email')
    
    try:
        recipient = User.query.filter_by(email=recipient_email).first()
        if not recipient:
            return "Recipient not found", 404
            
        recipient_key = PGPKey.query.filter_by(user_id=recipient.id, active=True).first()
        if not recipient_key:
            return "Recipient has no active PGP key", 400
            
        encrypted = pgp_encrypt_message(message, recipient_key.public_key)
        return render_template_string(APP_TEMPLATE,
            content="Encrypted message:<br><textarea readonly>%s</textarea>" % encrypted)
    except Exception as e:
        return f"Error encrypting message: {str(e)}", 500

@app.route('/pgp/decrypt', methods=['POST'])
def pgp_decrypt():
    if not session.get('user_id'):
        return redirect(url_for('connect_wallet_page'))
    
    encrypted_message = request.form.get('encrypted_message')
    
    try:
        user_key = PGPKey.query.filter_by(user_id=session['user_id'], active=True).first()
        if not user_key:
            return "No active PGP key found", 400
            
        decrypted = pgp_decrypt_message(encrypted_message, user_key.private_key)
        return render_template_string(APP_TEMPLATE,
            content="Decrypted message:<br><textarea readonly>%s</textarea>" % decrypted)
    except Exception as e:
        return f"Error decrypting message: {str(e)}", 500
    
#* ---------------------- | Argon2 Hashing Routes | ---------------------- #

@app.route('/argon2', methods=['GET', 'POST'])
def advanced_crypto():
    
    #* Handle advanced cryptographic operations
    if not session.get('user_id'):
        return redirect(url_for('connect_wallet_page'))

    # Add this HTML content for the advanced crypto page
    content = """
    <div class="form-container">
        
        <!-- ECC Section -->
        <form method="POST" class="crypto-form">
          <!--  <h3>ECC Key Generation</h3>  -->
            <input type="hidden" name="operation" value="ecc">
            <div class="button-wrapper">
                <button type="submit">Generate Keys</button>
            </div>
        </form>

        <!-- Argon2 Section -->
        <form method="POST" class="crypto-form">
          <!--  <h3>Argon2 Hashing</h3>  -->
            <input type="hidden" name="operation" value="argon2">
            <input type="password" name="password" placeholder="Enter text to hash" required>
            <div class="button-wrapper">
                <button type="submit">Generate Hash</button>
            </div>
        </form>

        <!-- Parallel File Processing 
        <form method="POST" class="crypto-form" enctype="multipart/form-data">
            <h3>Large File Encryption</h3>
            <input type="hidden" name="operation" value="parallel_encrypt">
            <div style="margin: 20px 0;">
                <label for="file-upload" class="custom-file-upload" style="
                    display: inline-block;
                    padding: 10px 20px;
                    background: #2d2d2d;
                    color: #fff;
                    border: 1px solid #444;
                    border-radius: 5px;
                    cursor: pointer;">
                    Choose Large File
                </label>
                <input id="file-upload" type="file" name="file" required style="display: none;">
            </div>
            <div class="button-wrapper">
                <button type="submit">Process Large File</button>
            </div>
        </form>  -->
    </div>
    <style>
        .crypto-form {
            background: #2d2d2d;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .crypto-form h3 {
            margin-top: 0;
            color: #fff;
        }
    </style>
    """
    
    if request.method == 'POST':
        try:
            operation = request.form.get('operation')
            
            if operation == 'ecc':
                ecc = initialize_ecc()
                private_key, public_key = ecc.generate_keypair()
                return render_template_string(APP_TEMPLATE,
                    content=content,
                    output="ECC keys generated successfully!")
                
            elif operation == 'argon2':
                password = request.form.get('password')
                argon2_handler = initialize_argon2()
                hashed = argon2_handler.hash_password(password)
                return render_template_string(APP_TEMPLATE,
                    content=content,
                    output=f"{hashed}")
                    
        except Exception as e:
            return render_template_string(APP_TEMPLATE,
                content=content,
                output=f"Error processing operation: {str(e)}")
    
    return render_template_string(APP_TEMPLATE, content=content)

#* Implementing parallel encryption for large files
            
    #//     elif operation == 'parallel_encrypt':
    #//         if 'file' not in request.files:
    #//             return render_template_string(APP_TEMPLATE,
    #//                 content=content,
    #//                 output="No file provided")
                
    #//         file = request.files['file']
    #//         if not file:
    #//             return render_template_string(APP_TEMPLATE,
    #//                 content=content,
    #//                 output="Invalid file")

    #//         try:
    #//             # Read the entire file into memory
    #//             file_data = file.read()
    #//             processor = get_file_processor()
    #//             cipher_suite = get_cipher_suite(session['user_id'])
                
    #//             def encrypt_chunk(chunk: bytes) -> bytes:
    #//                 return cipher_suite.encrypt(chunk)
                
    #//             # Create a BytesIO object from the file data
    #//             file_obj = BytesIO(file_data)
    #//             encrypted = processor.process_file_parallel(file_obj, encrypt_chunk)
                
    #//             # Create response with encrypted file
    #//             response = make_response(encrypted)
    #//             response.headers['Content-Type'] = 'application/octet-stream'
    #//             response.headers['Content-Disposition'] = f'attachment; filename=encrypted_{file.filename}'
    #//             return response
                
    #//         except Exception as e:
    #//             return render_template_string(APP_TEMPLATE,
    #//                 content=content,
    #//                 output=f"Error processing file: {str(e)}")
    
    #// return render_template_string(APP_TEMPLATE, content=content)

#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
#* TRIFORCE ASCII ART BANNER FOR THE WEB-APP     <><><><><><><><><><><><><><><><><>
#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# #* ---------------------- | Triforce ASCII Art Banner | ---------------------- #
BOLD = '\033[1m'
END = '\033[0m'

ASCII_BANNER = f"""

                           /\\
                          /__\\
                         /\\  /\\
                        /__\\/__\\
                       /\\      /\\
                      /__\\    /__\\
                     /\\  /\\  /\\  /\\
                    /__\\/__\\/__\\/__\\

"""
#* Function to print the Zencrypt banner in the console 
# with the Zencrypt whitepapers and ePortfolio.
def print_startup_banner():
    print(ASCII_BANNER)
    print(f"{BOLD}Zencrypt dApp{END} - Developed And Owned Entirely By imaclone.x{END}\n")
    print(f"Zencrypt {BOLD}Whitepapers and Docs{END} - {BOLD}https://zencrypt.gitbook.io/zencrypt{END}")
    print(f"{BOLD}ePortfolio{END} - {BOLD}https://www.imaclone.x{END}\n")
    print(f"Thank you for using Zencrypt {BOLD}Beta.02{END}\n")
    print(f"{BOLD}The Web App is now successfully up and running: http://localhost:5000/{END}\n\n")
# -- Development helper: inspect session contents --
@app.route('/__session', methods=['GET'])
def _session_inspect():
    """Return a JSON view of the current Flask session for debugging.

    Only enabled when FLASK_ENV is not set to 'production'. This helps
    determine whether `session['user_id']` is actually present after login.
    """
    if os.getenv('FLASK_ENV') == 'production':
        return "Not available in production", 404

    try:
        # Stringify values for safe JSON serialization
        data = {k: (str(v) if not isinstance(v, (int, float, bool, type(None))) else v) for k, v in session.items()}
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)})


#* Main function to run the Flask application
if __name__ == '__main__':
    print_startup_banner()
    if os.getenv('FLASK_ENV') == 'production':
        if not os.getenv('SECRET_KEY'):
            print("Please set the SECRET_KEY environment variable")
            sys.exit(1)                                     # Exit if SECRET_KEY is not set
        initialize_key()                                    # Initialize the encryption key for the user
        app.run(host='0.0.0.0', port=5000, debug=False)     # Let Nginx handle SSL
    else:
        app.run(host='0.0.0.0', port=5000, debug=False)
