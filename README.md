<!--
********************************************************************************************
* Title: Zencrypt dApp              |*******************************************************
* Developed by: Ryan Hatch          |*******************************************************
  Date: August 10th 2022            |*******************************************************
  Last Updated: April 8th 2026      |*******************************************************
  Version: 6.2.2-alpha2             |*******************************************************
********************************************************************************************
*-****************************** Zencrypt v6.2.2-alpha2 |***********************************
<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
|              Zencrypt dApp is a Solana-powered Flask application that can:               |
|       - Authenticate users via Solana wallet signature (no password required).           |
|       - Generate hashes: using SHA256 hashing algorithm, with an optional salt value.    |
|       - Encrypt text and files: using Fernet symmetric encryption algorithm.             |
<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
-->
<!DOCTYPE html>
<!DOCTYPE html>
<html>
  <body>
    <hr>
    <h1 align="center">Zencrypt</h1>
    <hr>
    <br>
    <p align="center">
      <strong>dApp Release - v6.2.2-alpha2</strong>
<!--       <br>
      <strong>By: Ryan Hatch</strong> -->
      <br>
    </p>
    <p align="center">
      <a href="#table-of-contents">Table of Contents</a><br>
       <a href="#introduction">Introduction</a> • <a href="#features">Features</a> • <a href="#installation">Installation</a> • <a href="#usage">Usage</a> • <a href="#examples">Examples</a> • <a href="#contributing">Contributing</a> • <a href="#disclaimer">Disclaimer</a> • <a href="#license">License</a> • <a href="#contact">Contact</a>
    </p>
    <hr>
    <p align="center">
<!--       <br> -->
      <strong>Developed By: Ryan Hatch</strong>
    <p align="center"> &copy; 2026 Ryan Hatch <br> All Rights Reserved.<br><i><br>This software is proprietary and owned by Ryan Hatch. Unauthorized use, modification, or distribution is prohibited.</i> </p>
<p align="center"><img src="https://img.shields.io/badge/Name:-Zencrypt-0A2647?style=for-the-badge" alt="Project Name"><img src="https://img.shields.io/badge/Author-Ryan%20S%20Hatch-0A2647?style=for-the-badge" alt="Project Author"> <img src="https://img.shields.io/badge/Started-January%202021-144272?style=for-the-badge" alt="Project Start Date"> <img src="https://img.shields.io/badge/Updated-Nov%2017%2C%202025-205295?style=for-the-badge" alt="Project Last Updated On"></p>
<p align="center"><img src="https://img.shields.io/badge/Type:-Decentralized%20Application-144272?style=for-the-badge" alt="Project Type"> <img src="https://img.shields.io/badge/Stage:-Alpha%20Web3-205295?style=for-the-badge" alt="Project Stage"> <img src="https://img.shields.io/badge/Version-v6.2.2--alpha2-2C74B3?style=for-the-badge" alt="Project Version"></p>
<hr>
<div class="dapp">
  <h1>dApp v6.2.2-alpha2 and CLI v4.2</h1>
  <ul>
    <li><a href="README.md">What is Zencrypt</a></li>
    <li><a href="cipher/zencrypt-cli.md">Getting To Know About The Zencrypt CLI</a></li>
  </ul>
  <h2>Zencrypt Whitepapers</h2>
  <ul>
    <li>
      <a href="cipher-whitepapers/zencrypt-documentation/README.md">Zencrypt Documentation</a>
      <ul>
        <li>
          <a href="cipher-whitepapers/zencrypt-documentation/a-shorter-description-about-my-enhancement-plan-for-zencrypt-cli/README.md">A Shorter Description About My Enhancement Plans for Zencrypt:</a>
          <ul>
            <li>
              <a href="cipher-whitepapers/zencrypt-documentation/a-shorter-description-about-my-enhancement-plan-for-zencrypt-cli/software-engineering-and-design/README.md">Enhancing and Updating The Software Engineering and Design</a>
              <ul>
                <li><a href="cipher-whitepapers/zencrypt-documentation/a-shorter-description-about-my-enhancement-plan-for-zencrypt-cli/software-engineering-and-design/explanation-of-key-flowchart.md">Key Flowchart Explanation</a></li>
              </ul>
            </li>
            <li>
              <a href="cipher-whitepapers/zencrypt-documentation/a-shorter-description-about-my-enhancement-plan-for-zencrypt-cli/updating-zencrypt-algorithms-and-data-structures/README.md">Updating The Algorithms and Data Structures:</a>
              <ul>
                <li><a href="cipher-whitepapers/zencrypt-documentation/a-shorter-description-about-my-enhancement-plan-for-zencrypt-cli/updating-zencrypt-algorithms-and-data-structures/flowchart-explanation.md">Flowchart Explanation</a></li>
              </ul>
            </li>
            <li>
              <a href="cipher-whitepapers/zencrypt-documentation/a-shorter-description-about-my-enhancement-plan-for-zencrypt-cli/updating-zencrypt-databases/README.md">Enhancing the Database Management For Zencrypt</a>
              <ul>
                <li><a href="cipher-whitepapers/zencrypt-documentation/a-shorter-description-about-my-enhancement-plan-for-zencrypt-cli/updating-zencrypt-databases/flowchart-explanation.md">Flowchart Explanation</a></li>
              </ul>
            </li>
            <li>
              <a href="cipher-whitepapers/zencrypt-documentation/a-shorter-description-about-my-enhancement-plan-for-zencrypt-cli/skills-and-illustrated-outcomes/README.md">Skills and Illustrated Outcomes</a>
              <ul>
                <li><a href="cipher-whitepapers/zencrypt-documentation/a-shorter-description-about-my-enhancement-plan-for-zencrypt-cli/skills-and-illustrated-outcomes/eportfolio-in-current-state.md">ePortfolio</a></li>
              </ul>
            </li>
          </ul>
        </li>
      </ul>
    </li>
  </ul>
</div>
<hr>
<div class="table-of-contents">
  <h1 align="center">Zencrypt <code>v6.2.2-alpha2</code> Decentralized Application:</h1>
<hr>
  <p align="center"><img src="https://img.shields.io/badge/Purpose-Encryption%20Platform-0A2647?style=for-the-badge" alt="Project Purpose"> <img src="https://img.shields.io/badge/Focus-Web3%20Security%20Development-144272?style=for-the-badge" alt="Project Focus"> <img src="https://img.shields.io/badge/Milestones-Web2%20to%20Web3%20Migration-205295?style=for-the-badge" alt="Project Milestones"></p>
  <p align="center"><img src="https://img.shields.io/badge/Testing Code:-Snyk-0A2647?style=for-the-badge" alt="Snyk Tests"> <img src="https://img.shields.io/badge/Testing App:-OWASP%20ZAP-144272?style=for-the-badge" alt="Testing"> <img src="https://img.shields.io/badge/Quality%20Assurance-8.5/10-205295?style=for-the-badge" alt="Quality Assurance">
  <img src="https://img.shields.io/badge/Status-Alpha%20Web3-2C74B3?style=for-the-badge" alt="Project Status"></p>
<hr>

<h4 align="center"><code>
  <a href="#1-project-purpose-and-evolution">Project Purpose and Evolution</code></a> •
  <code><a href="#2-architecture--technology-stack">Architecture & Technology Stack</code></a> •
  <code><a href="#3-features-and-functionalities">Features and Functionalities</code></a>
  <br>
  <code><a href="#4-documentation-flowcharts-and-future-enhancements">Documentation, Flowcharts, and Future Enhancements</code></a> •
  <code><a href="#5-deployment-and-operational-considerations">Deployment and Operational Considerations</code></a> •
  <code><a href="#6-summary">Summary</a>
</code></h4>
<hr>

<h5>I started this project with a CLI script that used core encryption functions and was designed with the purpose of parsing sensitive information offline to be encrypted or decrypted.<br><br> This project was intended to merge the final CLI program into a full fledged webapp that has all of the same functions, and with <code>version 6-alpha</code> that goal was reached — a complete cipher handling everything from hashing, AES, RSA, and fully implemented PGP functionality.
<br><br>
With <code>version 6.2.2-alpha2</code>, I took the next step I had been planning for a while: moving Zencrypt from web2 to web3. This version replaces the traditional email and password login system with Solana wallet-based authentication, meaning users prove their identity by signing a cryptographic challenge with their own wallet instead of storing a password anywhere on the server. No email, no password, no shared secret — just a public key and a signature.</h5>
</p>
<h5>
I restructured the backend from a monolithic <code>webapp.py</code> into a clean set of Flask Blueprints — auth, gate, crypto, and billing — so that each concern is fully separated and independently testable. The wallet authentication flow uses Ed25519 signature verification via PyNaCl, with nonce-based anti-replay protection baked in from the start. On top of that, I integrated Solana Pay so that users can purchase access plans directly with SOL, keeping the entire user journey on-chain.
<br><br>
I learned that moving to web3 is not just a technology swap — it forces you to rethink what identity even means in your system. When a wallet address becomes the primary key for a user record, every assumption about password resets, email lookups, and session expiry has to be revisited. Keeping the encryption core unchanged while swapping out the entire auth layer was a good test of how well the modular design from the previous version had actually held up.
</h5>

> This version represents the transition point I had been writing about since `version 6`. Zencrypt went from a hash generator, to a full cipher suite, to a web platform, and now to a decentralized application. Each step was a deliberate build on the one before it, and this step in particular reinforced why **`keeping it modular`** matters — the encryption engine did not have to change at all, only the door in front of it did.</p>

<hr>


### 1. **Project Purpose and Evolution**

- **Core Functionality:**  
I started Zencrypt as a simple command-line tool focused primarily on SHA-256 hash generation and verification, then steadily expanded its capabilities to include file encryption, RSA-based PGP features, and a full web interface. Version 6-alpha marked the completion of the web2 platform — a modular, scalable Flask app with JWT authentication, SQLAlchemy ORM, and a React front end. Version 6.2.2-alpha2 is the first step into web3: the encryption and hashing features remain unchanged, but the entire authentication layer has been replaced with Solana wallet-based login.

- **Evolutionary Path:**  
The progression from CLI to webapp to dApp followed a consistent philosophy: add capability without breaking what already works. In alpha2, email and password fields on the User model were made nullable and a `wallet_address` column was added to support wallet-only accounts, all while keeping backward compatibility for any existing email-based users. I made sure the cryptographic core — Fernet, AES, PGP — stayed exactly as it was, because the goal was not to rebuild Zencrypt but to give it a new front door.

---

### 2. **Architecture & Technology Stack**

- **Backend Architecture:** I refactored the backend from a single `webapp.py` file into a set of Flask Blueprints, each with a single responsibility: `auth` handles wallet challenge and verification, `gate` protects the encryption routes, `crypto` exposes the hashing and cipher API, and `billing` manages Solana Pay subscriptions. This restructuring made each module independently testable and kept the application factory pattern clean. SQLAlchemy ORM and Flask-Migrate are still used for modeling users, hashes, and encryption keys, and the database remains SQLite in development with a straightforward path to swap it for another backend if needed.

- **Security Implementation:** The authentication model in alpha2 is fundamentally different from the previous version. Instead of storing a password hash and issuing a JWT on credential match, the server now issues a one-time cryptographic nonce, waits for the client to return that nonce signed by their Solana wallet, and verifies the Ed25519 signature server-side using `PyNaCl`'s `VerifyKey`. No private key ever leaves the user's wallet. On successful verification, the user record is upserted by wallet address and a short-lived JWT is issued for the session. Nonces are stored in-memory with a ten-minute expiry and destroyed on use, preventing replay attacks.

- **Cryptographic Foundation:** The existing encryption stack — Fernet for text, AES in CFB mode for files, RSA PGP for asymmetric operations — is carried forward unchanged from version 6-alpha. On the web3 side, Ed25519 is used exclusively for wallet identity verification via `PyNaCl==1.5.0`, and Solana base58 address encoding is handled by `base58==2.1.1`. Keeping these two cryptographic layers cleanly separated — one for identity, one for data — helped me understand how a system can adopt blockchain primitives without having to rewrite its core security logic.

- **Frontend Integration:** The wallet connection UI uses the Phantom browser extension's `window.solana` API. When a user clicks Connect, the frontend calls `window.solana.connect()` to get the public key, fetches a nonce from `GET /auth/nonce`, asks the wallet to sign it with `signMessage`, and posts the result to `POST /auth/verify`. Solflare and Ledger Live are also supported through the same flow. The Navbar component was updated to display a truncated wallet address in place of a username once the user is authenticated via wallet.

- **Solana Pay Integration:** The `billing` Blueprint exposes endpoints for creating and confirming Solana Pay invoices. Subscription plans are priced in lamports — personal, pro, and team tiers — and the payment flow uses a reference key system that is designed to be verified against on-chain transaction data in a production setting. A `WalletManager` class in `static/wallet.js` wraps the Phantom adapter and handles both the connection and the payment creation flows.

---

### 3. **Features and Functionalities**

- **Wallet Authentication:**
  - Supports Phantom, Solflare, and Ledger Live wallets.
  - Nonce-based Ed25519 challenge/response — no password stored anywhere.
  - Wallet address is the primary user identifier; email and password are optional fallbacks.
  - JWT issued on successful verification; session stores wallet address.

- **Solana Pay Subscriptions:**
  - Personal, Pro, and Team plans denominated in lamports.
  - Invoice creation and confirmation endpoints in the `billing` Blueprint.
  - `WalletManager` JS class handles wallet connection and payment creation client-side.

- **Hash Generation:**
  - Uses SHA256 with an optional salt.
  - Hashes can be stored in the database for parsing or later verification.

- **Text Encryption/Decryption:**
  - Implements encryption of text using Fernet.
  - Both encryption and decryption are supported.

- **File Encryption/Decryption:**
  - Encrypts files using AES with a random salt and initialization vector, and decrypts them using the same key.
  - Supports file `uploads`, `processing`, and `download` operations, depending on the user's input.

- **PGP Encryption:**
  - Generates RSA keys for the user and encrypts messages using the recipient's public key.
  - Allows users to encrypt messages using a recipient's public key and decrypt messages using their own private key.
  - Features for exporting and importing public keys are optional but provided to enhance the security of key management.

- **User Authentication & Session Management:**
  - Primary: wallet address + Ed25519 signature via Solana wallet (Phantom / Solflare / Ledger).
  - Fallback: email and password for backward compatibility with existing accounts.
  - JWT-based session management with short-lived tokens.
  - User-specific encryption keys are generated and stored securely to ensure data privacy.

- **Database Operations:**
  - Models are defined for users (with optional wallet address), encryption keys, hashing or encryption event logs, and PGP keys.
  - SQLAlchemy ORM is used for database interactions, making it easy to manage and query data.
  - Database migrations are handled using Flask-Migrate and Alembic, ensuring that the database schema can be updated seamlessly.
  - The modular code structure allows for easy switching to other database systems like MongoDB or MySQL.

---

### 4. **Documentation, Flowcharts, and Future Enhancements**

**Extensive Documentation:** Alpha2 ships with a full set of wallet authentication documents covering setup, quick reference, implementation details, and a migration guide for existing email-based users. I made sure these documents explain both the how and the why behind the design choices, just like the whitepapers in the earlier versions, so that anyone reading the codebase can understand the reasoning without having to reverse-engineer the implementation.

**Whitepapers:** The existing whitepapers from version 6 are carried forward intact because the underlying encryption design has not changed. The new wallet auth documents — `WALLET_AUTH_SETUP.md`, `WALLET_AUTH_QUICK_REFERENCE.md`, `WALLET_AUTH_IMPLEMENTATION_SUMMARY.md`, `MIGRATION_GUIDE.md`, and `DELIVERY_SUMMARY.md` — complement those whitepapers by documenting the web3 layer specifically.

**Enhancement Plans:** The immediate next steps are to replace the in-memory nonce store with a proper database-backed or Redis-backed store for multi-instance deployments, add real on-chain RPC verification to the Solana Pay confirmation endpoint, and expand wallet support beyond Phantom and Solflare. Longer term, the plan is to explore moving encryption key ownership fully on-chain so that users hold their keys in their wallet rather than in the server database.

**Professional Skills and ePortfolio:** Building the web3 layer on top of the existing web2 foundation taught me that a well-structured modular codebase is one of the most valuable things you can invest in early. The fact that the encryption engine required zero changes when the authentication layer was completely replaced is a direct result of the design choices made in version 6.

---

### 5. **Deployment and Operational Considerations**

**Deployment Configuration:** Zencrypt alpha2 is configured for cloud deployment using Gunicorn as the web server, with the same `render.yaml` setup from version 6. The two new runtime dependencies — `PyNaCl==1.5.0` and `base58==2.1.1` — are added to `requirements.txt` and require no special build steps. Environment variables for `JWT_SECRET`, `MERCHANT_WALLET`, and `RPC_URL` must be set before deployment; these are documented in the `.env` template included in the repository.

**Testing and Quality Assurance:** Alpha2 includes a dedicated test suite in `test_wallet_auth.py` that covers nonce generation, Ed25519 key pair creation, server-side signature verification, and session persistence. These tests run without a browser or a real wallet, making them suitable for CI. The existing `test_webapp.py` unit tests for database operations and encryption routes continue to pass unchanged. Security scanning with Snyk and OWASP ZAP from version 6 is carried forward as part of the QA process.

---

### 6. **Summary**

Looking back at Zencrypt's path from a command-line hash tool to a decentralized application, the most important thing I have taken away is that each version had to be built well enough to be a foundation for the next one. Version 6 gave me a solid modular Flask platform with clean separation between the encryption logic, the database models, and the web routes. Alpha2 proved that foundation by swapping the entire authentication layer — from email and password to cryptographic wallet signatures — without touching the encryption engine at all.

The move to web3 is more than a technology choice. It changes what a user account means, what login means, and what trust means. In Zencrypt alpha2, a user is a Solana public key, login is a signature, and trust is cryptographic proof rather than a shared secret. I made sure every part of this version reflected a genuine understanding of those differences, from the nonce-based anti-replay design in the auth flow to the lamport-denominated subscription model in the billing layer. In the end, Zencrypt is still doing the same thing it always did — keeping data secure — but now the door to the system is secured by the same kind of cryptography that secures the data inside it.

<hr>

<h2 id="table-of-contents">Table of Contents</h2>
<h2>Changelog:</h2>
<h3>Logs of Recent Updates:</h3>
<li>Jan 20 2025 - Updated comments and added a more simple structure for the changes to be made.</li>
<li>Jan 21st 2025 - Merged the CLI into a webapp using the Flask framework. The current version is being hosted at <a href="https://zencrypt.app">Zencrypt.app</a></li>
<li>Jan 22nd 2025 - Users can upload files for encryption and decryption.</li>
<li>Jan 26th 2025 - Allows users to manage sessions by creating an account and logging in.</li>
<li>Jan 27th 2025 - Fully merged SQLite and SQLAlchemy into the backend for user authentication and session management.</li>
<li>Jan 28th 2025 - Created new schemas for the database to store user information and session data.</li>
<li>Nov 14th 2025 - Began web2 to web3 migration. Added <code>wallet_address</code> field to User model; made email and password nullable.</li>
<li>Nov 15th 2025 - Implemented Ed25519 wallet signature verification using PyNaCl. Added <code>/auth/nonce</code> and <code>/auth/verify</code> endpoints.</li>
<li>Nov 16th 2025 - Added Phantom and Solflare wallet connection UI. Integrated Solana Pay billing Blueprint with personal, pro, and team plans.</li>
<li>Nov 17th 2025 - Refactored backend from monolithic webapp.py into Flask Blueprints (auth, gate, crypto, billing). dApp v3.1 released as alpha2.</li>
<hr>
<h2 id="introduction">Introduction</h2>
<p> Zencrypt is a decentralized application (dApp) that allows users to hash, encrypt, and decrypt text and files — authenticated entirely through a Solana wallet, with no password required. The dApp runs on the Flask framework and is hosted at <a href="https://zencrypt.app">Here.</a>
    <br>
    <p>The dApp is built for simplicity and security, combining the encryption suite from version 6 with Solana wallet-based authentication. Users connect their Phantom, Solflare, or Ledger wallet, sign a one-time cryptographic nonce, and are issued a session token — no email, no password, no shared secret stored on the server. Subscription access is handled through Solana Pay, keeping the entire user journey on-chain.</p>
<h2 id="features">Features</h2>
<h2>System Overview</h2>
<p>Zencrypt is a Flask-based decentralized application focused on encryption, hashing, and secure file operations with Solana wallet authentication. The project completes the planned migration from the web2 platform in version 6 to a web3 dApp, while maintaining the same strong cryptographic foundations.</p>
<h2>Functions</h2>
<ul>
  <li>Solana wallet authentication — Phantom, Solflare, and Ledger Live</li>
  <li>Ed25519 nonce-based challenge/response login (no password stored)</li>
  <li>Solana Pay subscription billing (personal, pro, and team plans)</li>
  <li>SHA256 hashing with optional salt values</li>
  <li>Fernet symmetric encryption for text</li>
  <li>AES-based file encryption with password protection</li>
  <li>PGP asymmetric encryption with key management</li>
  <li>JWT session management after wallet verification</li>
  <li>Secure key storage in dedicated directory</li>
  <li>SQLite database with encrypted storage</li>
</ul>
<h2 id="installation">Installation</h2>
<p> To install Zencrypt, you will need to follow these steps: </p>
<ol>
  <li>Clone the alpha2 branch of the repository with the command:<br><code>git clone -b alpha2 https://github.com/ryanshatch/zencrypt-v6.2.2-alpha.git</code>. </li>
    <li>Navigate to the project directory with the command: <code>cd zencrypt-v6.2.2-alpha</code>. </li>
    <li>First, you will need to install Python 3.7 or higher. You can download Python from the official website: <a href="https://www.python.org/downloads/">https://www.python.org/downloads/</a>. </li>
        <li>Next, you will need to install pip, the Python package manager. You can install pip by following the instructions on the official website: <a href="https://pip.pypa.io/en/stable/installation/">https://pip.pypa.io/en/stable/installation/</a>. </li>
        <li>Once you have installed Python and pip, you can create a virtual environment with the command: <code>python -m venv venv</code>. </li>
        <li>Activate the virtual environment with the command: <code>source venv/bin/activate</code> on Linux or <code>venv\Scripts\activate</code> on Windows. </li>
  <li>Install the required dependencies with the command: <code>pip install -r requirements.txt</code>. </li>
  <li>Copy <code>.env</code> to your local environment and set <code>JWT_SECRET</code>, <code>MERCHANT_WALLET</code>, and <code>RPC_URL</code> before running. </li>
  <li>Install the <a href="https://phantom.app/">Phantom</a> or <a href="https://solflare.com/">Solflare</a> browser extension to use wallet authentication. </li>
</ol>
<h2 id="usage">How to Run Locally:</h2>
<p> To use the dApp, you will need to follow these steps: </p>
<ol>
  <li>Start the application with the command: <code>python run.py</code>. </li>
  <li>Open a web browser and navigate to <code>http://localhost:5000</code>. </li>
  <li>Click <strong>Connect Phantom</strong> (or Solflare) to authenticate with your Solana wallet. </li>
  <li>Once authenticated, use the dApp to hash, encrypt, and decrypt text and files. </li>
</ol>
<hr>
    <h2 id="examples">Web3 Login and CLI (v4.2-alpha) Examples:</h2>
    <h3 align="center">Web3 Wallet Login:</h3>
    <center>
      <img alt="Web3 Login" src="WEB3-login.JPG" style="width: 100%; height: 100%;" />
    </center>
    <h3 align="center">Hashing:</h3>
    <center>
      <img alt="Hashing Example" src="https://github.com/ryanshatch/zencrypt/blob/v6.2.2-alpha/img/zencrypthash.png" style="width: 100%; height: 100%;" />
    </center>
    <h3 align="center">Cipher:</h3>
    <center>
      <img alt="Cipher Example" src="https://github.com/ryanshatch/zencrypt/blob/v6.2.2-alpha/img/zencrypt.PNG" style="width: 100%; height: 100%;" />
    </center>
    <h3 align="center">Encrypting Parsed Files:</h3>
    <center>
      <img alt="Cipher Example" src="https://github.com/ryanshatch/zencrypt/blob/v6.2.2-alpha/img/encrypt.PNG" style="width: 100%; height: 50%;" />
    </center>
        <h3 align="center">PGP Encryption:</h3>
    <center>
      <img alt="Cipher Example" src="https://github.com/ryanshatch/zencrypt/blob/v6.2.2-alpha/img/pgpencryption.PNG" style="width: 100%; height: 50%;" />
    </center>
    </p>
    <hr><br>
    <h1 align="center" id="disclaimer"><bold>DISCLAIMER!</bold></h1>
    <p align="center">
      <strong>
        <=>
          <=>
            <=>
              <=>
                <=>
                  <=>
                    <=>
                      <=>
                        <=>
                          <=>
                            <=>
                              <=>
                                <=>
                                  <=>
                                    <=>
                                      <=>
                                        <=>
                                          <=>
                                            <=>
                                              <=>
                                                <=>
                                                  <=>
                                                    <=>
                                                      <=>
                                                        <=>
                                                          <=>
                                                            <!-- <=><=><=><=> -->
      </strong>
      </br>
      <!-- <p align="center"><strong><=><=><=></strong></br></p> -->
    <p align="center">
      <strong>
        <code>This script is provided for educational and demonstration purposes only. <br>Use it responsibly and please adhere to all applicable laws and regulations. </code>
      </strong>
      </br>
    </p>
    <!-- <strong>This script is provided for educational and demonstration purposes only. Use it responsibly and adhere to all applicable laws and regulations.</strong></br></p> -->
    <p align="center">
      <strong>
        <code>I am absolutely immune from any responsibility in regards to any damages or loss of data caused by the <br>use, abuse, or misuse of this software. </code>
      </strong>
      </br>
      <!-- <p align="center"><strong><=><=><=></strong></br></p> -->
    <p align="center">
      <strong>
        <=>
          <=>
            <=>
              <=>
                <=>
                  <=>
                    <=>
                      <=>
                        <=>
                          <=>
                            <=>
                              <=>
                                <=>
                                  <=>
                                    <=>
                                      <=>
                                        <=>
                                          <=>
                                            <=>
                                              <=>
                                                <=>
                                                  <=>
                                                    <=>
                                                      <=>
                                                        <=>
                                                          <=>
                                                            <!-- <=><=><=><=> -->
      </strong>
      </br>
    </p><hr>
    <h2 align="center" id="license">license</h2>
    <p> This software is the property of the copyright holder and is protected by copyright laws. All rights are reserved. The copyright holder grants no implied or express license for the use, copying, modification, distribution, or reproduction of this software, in whole or in part, without the prior written permission of the copyright holder. </p>
    <p> Any unauthorized use, copying, modification, distribution, or reproduction of this software, in whole or in part, is strictly prohibited and constitutes a violation of copyright law. Such unauthorized use may result in civil and/or criminal penalties, including but not limited to legal action and monetary damages. </p>
    <p> To obtain permission for any use, copying, modification, distribution, or reproduction of this software, please contact the copyright holder at the following address: <code>ryanshatch@gmail.com</code>
    </p>
    </p>
    <br>
    <p align="center">
      <strong>
        <code>By using this software, you acknowledge that you have read and understood the terms of this license and agree to comply with all applicable copyright laws. <br>Failure to abide by the terms of this license may subject you to legal consequences. </code>
      </strong>
    </p>
  </body>
</html><hr>
<h2 align="center" id="contact">Contact</h2>
<p align="center">For any inquiries or suggestions, please contact me at <a href="mailto:ryanshatch@gmail.com">ryanshatch@gmail.com</a>.
</body>
</html>


