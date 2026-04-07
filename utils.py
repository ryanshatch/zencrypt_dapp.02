"""
********************************************************************************************
* Utils.py                         |********************************************************
* Developed by: Ryan Hatch         |********************************************************
* Date: August 10th 2022           |********************************************************
* Last Updated: Febuary 13th 2025  |********************************************************
* Version: v6.2-A                  |********************************************************
********************************************************************************************
"""

#* Import libraries for the web-app
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization as crypto_serialization
import hashlib
import os
import base64

# Replace collections.Iterable with collections.abc.Iterable
from collections.abc import Iterable

#* Define the key file for the encryption
KEY_FILE = "zen-private.key"                        # The private key is stored in a file called "private.key"
#//KEY_FILE = "zen.key"                        # The private key is stored in a file called "private.key"

#* Initialize the key for encryption
def initialize_key():
    if not os.path.exists(KEY_FILE):            # checks path to see if the key file exists
        key = Fernet.generate_key()             #* generates a new key if the file does not exist named "private.key"
        with open(KEY_FILE, "wb") as key_file:  # opens the file in write mode
            key_file.write(key)                 #* writes the key to the file
    with open(KEY_FILE, "rb") as key_file:      # opens the file in read mode
        return key_file.read()                  #* reads the key from the file

cipher_suite = Fernet(initialize_key())                       #* initializes the cipher suite with the new or old key

def generate_hash(text: str, salt: str = "") -> str:          #* generates a hash of the text using SHA256
    return hashlib.sha256((text + salt).encode()).hexdigest() # Returns the hash of the text and the salt if used

def encrypt_text(text: str) -> str:                     #* encrypts the text using the key
    return cipher_suite.encrypt(text.encode()).decode() # Returns the encrypted text in an encoded format

def decrypt_text(encrypted_text: str) -> str:                     #* decrypts the text using the key
    return cipher_suite.decrypt(encrypted_text.encode()).decode() # Returns the decrypted text in an encoded format

def generate_pgp_keys():                         #* generates a pair of PGP keys using RSA encryption
    private_key = rsa.generate_private_key(      #* generates a private key
        public_exponent=65537,                   # The public exponent is set to 65537 for compatibility and security
        key_size=2048,                           # The key size is set to 2048 bits for security and compatibility
        backend=default_backend()                # uses the default backend for the cryptography library
    )

    return private_key, private_key.public_key() #* returns the private and public keys for the user

def encrypt_file(input_file: str, output_file: str, password: bytes): #* encrypts the file using AES encryption with a password
    salt = os.urandom(16)                   # generates a random salt for the encryption
    key = generate_key(password, salt)      # generates a key from the password and the salt
    iv = os.urandom(16)                     # generates a random iv for the encryption

    with open(input_file, 'rb') as file:    #* opens the file provided in read mode
        plaintext = file.read()             # reads the file into memory

    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend()) # creates a cipher object with the key and iv
    encryptor = cipher.encryptor()                                    # creates an encryptor object from the cipher object
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()   #* encrypts the plaintext and finalizes the encryption

    with open(output_file, 'wb') as file:                             #* opens the output file in write mode
        file.write(salt + iv + ciphertext)                            #* writes the salt, iv, and ciphertext to the output file

def decrypt_file(input_file: str, output_file: str, password: bytes): #* decrypts the file using AES encryption with a password
    with open(input_file, 'rb') as file:                              # opens the file provided in read mode
        data = file.read()                                            # reads the file into memory

    salt = data[:16]                # gets the salt from the file
    iv = data[16:32]                # gets the iv from the file
    ciphertext = data[32:]          # gets the ciphertext from the file

    key = generate_key(password, salt)                   # generates a key from the password and the salt
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend()) # creates a cipher object with the key and iv
    decryptor = cipher.decryptor()                       # creates a decryptor object from the cipher object
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize() #* decrypts the ciphertext and finalizes the decryption

    with open(output_file, 'wb') as file:                #* opens the output file in write mode
        file.write(decrypted_data)                       #* writes the decrypted data to the output file

def generate_key(password: bytes, salt: bytes) -> bytes: #* generates a key from the password and the salt using PBKDF2HMAC - Password Based Key Derivation Function 2
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),  #* uses SHA256 as the hashing algorithm for the key derivation
        length=32,                  # the length of the key is 32 bytes
        salt=salt,                  # the salt is used to make the key derivation more secure
        iterations=100000,          # the number of iterations is set to 100000 for security
        backend=default_backend()   # uses the default backend for the cryptography library
    )

    return kdf.derive(password)     # derives the key from the password and the salt using the KDF - Key Derivation Function

#* PGP Encryption Functions
def generate_pgp_keypair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    
    # Serialize private key
    private_pem = private_key.private_bytes(
        encoding=crypto_serialization.Encoding.PEM,
        format=crypto_serialization.PrivateFormat.PKCS8,
        encryption_algorithm=crypto_serialization.NoEncryption()
    )
    
    # Serialize public key
    public_pem = private_key.public_key().public_bytes(
        encoding=crypto_serialization.Encoding.PEM,
        format=crypto_serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    return private_pem.decode(), public_pem.decode()

def pgp_encrypt_message(message: str, public_key_pem: str) -> str:
    public_key = crypto_serialization.load_pem_public_key(
        public_key_pem.encode(),
        backend=default_backend()
    )
    
    encrypted = public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    return base64.b64encode(encrypted).decode()

def pgp_decrypt_message(encrypted_message: str, private_key_pem: str) -> str:
    private_key = crypto_serialization.load_pem_private_key(
        private_key_pem.encode(),
        password=None,
        backend=default_backend()
    )
    
    encrypted_bytes = base64.b64decode(encrypted_message)
    decrypted = private_key.decrypt(
        encrypted_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    return decrypted.decode()