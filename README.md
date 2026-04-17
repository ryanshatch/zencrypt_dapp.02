# Zencrypt dApp

Zencrypt is a Flask-based cryptography dApp/backend that combines:
- Solana wallet authentication (signature verification),
- wallet/token/NFT-gated access control,
- user-scoped hashing and encryption features,
- persistent key and crypto artifact storage with SQLAlchemy.

This README documents the repository as it currently exists.

---

## Project Snapshot (Current Repository State)

- Primary backend entrypoint: `webapp.py`
- Data models: `models.py`
- Cryptographic helpers: `utils.py`, `crypto_utils.py`
- Python dependency manifest: `requirements.txt`
- Deployment config: `render.yaml`
- Database migrations scaffold: `migrations/`
- Static assets: `static/` (`favicon.ico`, wallet/auth JS files)

The implementation is currently centered on a single Flask application module (`webapp.py`) with inline template rendering for most UI pages.

---

## What Is Implemented

### 1) Authentication and Identity

Zencrypt currently supports wallet-authenticated sessions and also retains email/password routes in the UI flow.

Implemented auth-related behavior in `webapp.py`:
- Session nonce endpoint: `GET /auth/nonce`
- Wallet signature verification endpoint: `POST /auth/verify`
- Wallet connect page: `GET /connect-wallet`
- Session termination: `GET /logout`

Wallet verification path:
- receives base58 public key + base64 signature + nonce,
- verifies Ed25519 signature via `PyNaCl`,
- checks token-gate requirements,
- upserts a `User` row by `wallet_address`,
- creates Flask session state (`user_id`, `wallet_address`).

### 2) Access Gating

Two gate mechanisms are present:

1. NFT collection gate helper (`has_zencrypt_pass`) using DAS `searchAssets`
2. SPL token balance gate (`check_token_balance`) using `getTokenAccountsByOwner`

Runtime gate configuration is environment-driven:
- `ZENCRYPT_COLLECTION_MINT`
- `ZENCRYPT_TOKEN_MINT`
- `ZENCRYPT_MIN_TOKEN_BALANCE`
- `RPC_URL`
- `SOLANA_DAS_RPC`

### 3) Core Crypto Features

Implemented feature routes:
- `GET/POST /` → SHA-256 hash generation (optional salt)
- `GET/POST /encrypt` → text encryption (Fernet, user key)
- `GET/POST /decrypt` → text decryption (Fernet, user key)
- `GET/POST /file` → file processing path using Fernet + base64 handling
- `GET /pgp` + `POST /pgp/generate|encrypt|decrypt` → RSA-based PGP keypair and message encryption/decryption
- `GET/POST /argon2` → Argon2 password hashing and ECC key generation actions

### 4) Key Management

Implemented key lifecycle in `webapp.py` and models:
- per-user active symmetric key initialization (`initialize_key`)
- active key retrieval for cipher operations (`get_cipher_suite`)
- key rotation support (`rotate_key`)
- key export/import routes (`/export-key`, `/import-key`)

### 5) Database Models

`models.py` currently defines:
- `User`
- `Hash`
- `EncryptedText`
- `Key`
- `PGPKey`
- `ECCKey`
- `ProcessingJob`

SQLAlchemy is initialized in-app, and tables are created at startup under app context.

---

## Repository Architecture Notes

Current architecture in this repository is **single-module Flask app orchestration** (`webapp.py`) with helper modules, not a multi-blueprint split.

### Backend Stack

- Flask
- Flask-SQLAlchemy
- Flask-Migrate / Alembic
- Flask-JWT-Extended (configured)
- Cryptography primitives via `cryptography`
- Argon2 (`argon2-cffi`)
- PyNaCl + base58 for wallet verification
- Merkle utilities in `crypto_utils.py`

### Frontend/UI Layer

- Server-rendered HTML via `render_template_string` inside route handlers
- Inline CSS/JS in `webapp.py`
- Additional JS files under `static/js/` and `static/wallet.js` are present in repository as client-side modules/components

---

## Route Inventory (High-Level)

- Auth/session: `/auth`, `/auth/nonce`, `/auth/verify`, `/connect-wallet`, `/logout`
- Crypto UI/actions: `/`, `/encrypt`, `/decrypt`, `/file`, `/pgp`, `/pgp/generate`, `/pgp/encrypt`, `/pgp/decrypt`, `/argon2`
- Key management: `/export-key`, `/import-key`
- Utility/debug: `/favicon.ico`, `/__session` (non-production)

---

## Configuration Surface

### Environment and Secrets

The repository includes `.env.example` documenting variables for:
- database URI and path,
- Flask env flags,
- session/JWT secrets,
- key file path/name options,
- Solana token/NFT gating and RPC settings,
- optional Picket-related values.

### Deployment

`render.yaml` defines a Python web service using:
- build: `pip install --upgrade pip && pip install -r requirements.txt`
- start: `gunicorn webapp:app`
- Python version pin: `3.11.11`

---

## Security and Ownership Notes

- Wallet auth uses challenge-response signatures (no private keys handled by server).
- Session and JWT secret material are expected via environment variables.
- Access gating logic is chain-data-dependent through configured RPC providers.

## Intellectual Property

This repository is proprietary work by the project owner.  
No open contribution policy is provided in this document.

---

## License

See `LICENSE` and `LICENSE.mp3` in this repository for project licensing terms.
