#!/usr/bin/env python3
"""
Cleaner Royall - Premium Key Generator

This script generates encrypted keys in the format used by the Cleaner Royall premium system.
The keys use AES-256-CBC encryption with the keys extracted from the APK smali code.

Based on analysis of:
- https://github.com/Eduardob3677/Cleaner_Royall.git
- smali_classes6/Cleaner/Royall/a.smali (contains encryption methods)
- DECRYPTED_KEYS.md (contains all encryption keys)
- assets/Premium/stringMakerKey.txt: "AraafRoyall@1211"

Usage:
    python3 key_generator.py <plain_text_key>

Example:
    python3 key_generator.py "67d93aab"
    
Output will be in the format: $IV<base64_encoded_ciphertext>

The app uses two different keys depending on context:
- For premium key encryption: "AraafRoyall@1211" (stringMakerKey)
- For general file encryption: " Cleaner@Royall#6278 " (note the spaces)
"""

import sys
import hashlib
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes


# Encryption keys from smali analysis of Cleaner_Royall APK
# Primary key for premium key generation (from assets/Premium/stringMakerKey.txt)
STRING_MAKER_KEY = "AraafRoyall@1211"

# Secondary key for file encryption (from smali_classes6/Cleaner/Royall/a.smali line 76)
SECONDARY_KEY = " Cleaner@Royall#6278 "

# Use STRING_MAKER_KEY for premium key generation
ENCRYPTION_KEY = STRING_MAKER_KEY


def generate_key_from_password(password):
    """
    Generate a 32-byte AES key from password using SHA-256.
    This matches the key derivation used in the Android app.
    """
    return hashlib.sha256(password.encode('utf-8')).digest()


def encrypt_key(plain_text):
    """
    Encrypt a plain text key using AES-256-CBC encryption.
    Returns the encrypted key in the format: $IV<base64_encoded_ciphertext>
    
    Args:
        plain_text: The plain text key to encrypt (e.g., "67d93aab")
    
    Returns:
        Encrypted key string with $IV prefix
    """
    # Generate AES key from password
    aes_key = generate_key_from_password(ENCRYPTION_KEY)
    
    # Generate random IV (Initialization Vector)
    iv = get_random_bytes(16)
    
    # Create cipher
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    
    # Pad the plaintext to be a multiple of 16 bytes
    padded_plaintext = pad(plain_text.encode('utf-8'), AES.block_size)
    
    # Encrypt the plaintext
    ciphertext = cipher.encrypt(padded_plaintext)
    
    # Combine IV and ciphertext, then encode to base64
    encrypted_data = iv + ciphertext
    encoded = base64.b64encode(encrypted_data).decode('utf-8')
    
    # Return with $IV prefix
    return f"$IV{encoded}"


def main():
    """Main function to handle command line arguments and generate keys."""
    if len(sys.argv) != 2:
        print("Usage: python3 key_generator.py <plain_text_key>")
        print("\nExample:")
        print("  python3 key_generator.py '67d93aab'")
        print("\nThis will generate an encrypted key in the format:")
        print("  $IV<base64_encoded_ciphertext>")
        sys.exit(1)
    
    plain_text_key = sys.argv[1]
    
    # Validate input
    if not plain_text_key:
        print("Error: Plain text key cannot be empty")
        sys.exit(1)
    
    # Generate encrypted key
    encrypted_key = encrypt_key(plain_text_key)
    
    # Display results
    print("=" * 60)
    print("Cleaner Royall - Key Generator")
    print("=" * 60)
    print(f"\nPlain Text Key:  {plain_text_key}")
    print(f"Encrypted Key:   {encrypted_key}")
    print("\n" + "=" * 60)
    print("\nYou can now use this encrypted key in your server response.")
    print("Example JSON response:")
    print(f'''{{
    "id": "87386",
    "date": "27/06/2025",
    "status": "1",
    "key": "{encrypted_key}",
    "comment": "Thanks For Trying Premium Version\\nKeep Supporting the Project 👍",
    "mode": "Permanent Access",
    "uid": "80680986",
    "pid": "002Aa7r6FBDQxEyT4hPjrA=="
}}''')
    print("=" * 60)


if __name__ == "__main__":
    main()
