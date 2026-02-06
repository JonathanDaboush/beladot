
# ------------------------------------------------------------------------------
# hashing.py
# ------------------------------------------------------------------------------
# Utility functions for encrypting and decrypting text using Fernet symmetric encryption.
# Used for salting and unsalting sensitive data.
# ------------------------------------------------------------------------------

import os
from cryptography.fernet import Fernet

# Load key from environment or generate one for demo (in production, store securely)
FERNET_KEY = os.environ.get('FERNET_KEY', Fernet.generate_key())
fernet = Fernet(FERNET_KEY)

def salt(text: str) -> str:
    """
    Encrypt (salt) the given text using Fernet symmetric encryption.
    Args:
        text (str): The plain text to encrypt.
    Returns:
        str: The encrypted (salted) text.
    """
    return fernet.encrypt(text.encode()).decode()

def deSalt(salted_text: str) -> str:
    """
    Decrypt (unsalt) the given salted text using Fernet symmetric encryption.
    Args:
        salted_text (str): The encrypted (salted) text to decrypt.
    Returns:
        str: The original plain text.
    """
    return fernet.decrypt(salted_text.encode()).decode()