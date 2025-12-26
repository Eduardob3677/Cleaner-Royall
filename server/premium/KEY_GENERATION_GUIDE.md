# Premium Key Generation Guide

## Overview

This guide explains how to generate encrypted premium keys for the Cleaner Royall server response system.

**Based on APK Smali Analysis**: This implementation is based on reverse engineering the actual Cleaner Royall APK from https://github.com/Eduardob3677/Cleaner_Royall.git

## What is an Encrypted Key?

The server returns JSON responses with keys in an encrypted format. For example:

```json
{
    "id": "87386",
    "date": "27/06/2025",
    "status": "1",
    "key": "$IVBB3gUKHdICQiBvQRSjQ8tM4vyc6onNW9R7wygyBVd1Y=",
    "comment": "Thanks For Trying Premium Version\nKeep Supporting the Project 👍",
    "mode": "Permanent Access",
    "uid": "80680986",
    "pid": "002Aa7r6FBDQxEyT4hPjrA=="
}
```

The `key` field contains an encrypted value that starts with `$IV` followed by base64-encoded ciphertext.

## Encryption Details

### Keys Used in the App (from Smali Analysis)

The app uses multiple encryption keys for different purposes:

1. **Main AES Key**: `CleanerRoyall@AraafRoyall`
   - Location: `smali_classes6/Cleaner/Royall/kb.smali`
   - Usage: ECB mode encryption

2. **Secondary AES Key**: ` Cleaner@Royall#6278 ` *(note the leading and trailing spaces)*
   - Location: `smali_classes6/Cleaner/Royall/a.smali` (line 76, 140)
   - Usage: CBC mode encryption with IV for file assets

3. **Premium Key**: `Araaf@Royall$1211`
   - File: `assets/Premium/key`
   - Purpose: Premium feature validation

4. **String Maker Key**: `AraafRoyall@1211`
   - File: `assets/Premium/stringMakerKey.txt`
   - Purpose: **Premium key encryption (THIS IS WHAT WE USE)**

### For Premium Key Generation

- **Algorithm**: AES-256-CBC
- **Encryption Key**: `AraafRoyall@1211` (from stringMakerKey.txt)
- **Key Derivation**: SHA-256 hash of the encryption key
- **Padding**: PKCS5/PKCS7
- **Format**: `$IV` prefix + base64(IV + ciphertext)

## How to Generate Keys

### Prerequisites

```bash
pip3 install pycryptodome
```

### Using the Key Generator Script

The repository includes a Python script to generate encrypted keys:

```bash
cd server/premium
python3 key_generator.py "<plain_text_key>"
```

#### Example 1: Generate a simple alphanumeric key

```bash
python3 key_generator.py "67d93aab"
```

Output:
```
============================================================
Cleaner Royall - Key Generator
============================================================

Plain Text Key:  67d93aab
Encrypted Key:   $IVbgrVjZQiE8EwQI8ZkACk7vmizQLo7xkh2Fxeol/qPJ8=

============================================================
```

#### Example 2: Generate a complex key

```bash
python3 key_generator.py "R3CR700MP4R"
```

#### Example 3: Generate a custom key

```bash
python3 key_generator.py "MyCustomKey123"
```

## Manual Encryption (Alternative Method)

If you prefer to encrypt keys programmatically in your own code, here's how:

### Python Example

```python
import hashlib
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

def encrypt_key(plain_text):
    # Encryption key for premium keys (from assets/Premium/stringMakerKey.txt)
    password = "AraafRoyall@1211"
    
    # Generate AES key from password using SHA-256
    aes_key = hashlib.sha256(password.encode('utf-8')).digest()
    
    # Generate random IV
    iv = get_random_bytes(16)
    
    # Create cipher
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    
    # Pad and encrypt
    padded = pad(plain_text.encode('utf-8'), AES.block_size)
    ciphertext = cipher.encrypt(padded)
    
    # Combine IV and ciphertext, encode to base64
    encrypted_data = iv + ciphertext
    encoded = base64.b64encode(encrypted_data).decode('utf-8')
    
    return f"$IV{encoded}"

# Usage
encrypted = encrypt_key("67d93aab")
print(encrypted)
```

### Java Example (for Android/Server)

```java
import javax.crypto.Cipher;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;
import java.security.MessageDigest;
import java.security.SecureRandom;
import java.util.Base64;

public class KeyGenerator {
    // From assets/Premium/stringMakerKey.txt
    private static final String ENCRYPTION_KEY = "AraafRoyall@1211";
    
    public static String encryptKey(String plainText) throws Exception {
        // Generate AES key from password using SHA-256
        MessageDigest digest = MessageDigest.getInstance("SHA-256");
        byte[] keyBytes = digest.digest(ENCRYPTION_KEY.getBytes("UTF-8"));
        SecretKeySpec key = new SecretKeySpec(keyBytes, "AES");
        
        // Generate random IV
        byte[] iv = new byte[16];
        new SecureRandom().nextBytes(iv);
        IvParameterSpec ivSpec = new IvParameterSpec(iv);
        
        // Create cipher
        Cipher cipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
        cipher.init(Cipher.ENCRYPT_MODE, key, ivSpec);
        
        // Encrypt
        byte[] encrypted = cipher.doFinal(plainText.getBytes("UTF-8"));
        
        // Combine IV and ciphertext
        byte[] combined = new byte[iv.length + encrypted.length];
        System.arraycopy(iv, 0, combined, 0, iv.length);
        System.arraycopy(encrypted, 0, combined, iv.length, encrypted.length);
        
        // Encode to base64 and add prefix
        return "$IV" + Base64.getEncoder().encodeToString(combined);
    }
}
```

### Node.js Example

```javascript
const crypto = require('crypto');

function encryptKey(plainText) {
    // From assets/Premium/stringMakerKey.txt
    const password = 'AraafRoyall@1211';
    
    // Generate AES key from password using SHA-256
    const key = crypto.createHash('sha256').update(password, 'utf-8').digest();
    
    // Generate random IV
    const iv = crypto.randomBytes(16);
    
    // Create cipher
    const cipher = crypto.createCipheriv('aes-256-cbc', key, iv);
    
    // Encrypt
    let encrypted = cipher.update(plainText, 'utf8');
    encrypted = Buffer.concat([encrypted, cipher.final()]);
    
    // Combine IV and ciphertext
    const combined = Buffer.concat([iv, encrypted]);
    
    // Encode to base64 and add prefix
    return '$IV' + combined.toString('base64');
}

// Usage
const encrypted = encryptKey('67d93aab');
console.log(encrypted);
```

## Key Format Examples

Here are some examples of plain text keys and their encrypted equivalents using `AraafRoyall@1211`:

| Plain Text Key | Encrypted Key (Example - varies due to random IV) |
|---------------|---------------------------------------------------|
| `67d93aab` | `$IVYScWFqqhrT6LDU6/8FR3WBt0Iwc5PwT8hRDhJi2BfTY=` |
| `R3CR700MP4R` | `$IVkL8pQ2xN7mA5vB9cF3dG6hJ0sK4tM1wE8rT2yU5iO=` |
| `TextView` | `$IVpZ3sR5tL8mA2nB6cD9fG1hJ4kM7oP0qW3xY6zE9vU=` |

**Note**: Each time you encrypt the same plain text, you'll get a different encrypted value because a random IV (Initialization Vector) is used. This is a security feature.

## Server Response Format

Once you have the encrypted key, use it in your server JSON response:

```json
{
    "id": "87386",
    "date": "27/06/2025",
    "status": "1",
    "key": "<YOUR_ENCRYPTED_KEY_HERE>",
    "comment": "Thanks For Trying Premium Version\nKeep Supporting the Project 👍",
    "mode": "Permanent Access",
    "uid": "80680986",
    "pid": "002Aa7r6FBDQxEyT4hPjrA=="
}
```

## Security Notes

1. **Random IV**: Each encryption generates a random IV, making the same plain text produce different ciphertexts each time. This is intentional and secure.

2. **Key Storage**: The plain text keys are stored in user files (e.g., `server/premium/users/002Aa7r6FBDQxEyT4hPjrA==`) and should be encrypted when sent to clients.

3. **Decryption**: The Android app automatically decrypts these keys using the same encryption key.

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'Crypto'"

**Solution**: Install pycryptodome:
```bash
pip3 install pycryptodome
```

### Issue: Different encrypted output each time

**This is normal**: Due to the random IV, each encryption produces a different result. The app can decrypt any of them correctly.

### Issue: Key doesn't work in the app

**Check**:
1. Make sure you're using the correct encryption key: `AraafRoyall@1211` (from stringMakerKey.txt)
2. Verify the `$IV` prefix is present
3. Ensure base64 encoding is correct

### Common Mistakes

1. **Wrong Key**: Using `Araaf@Royall$1211` instead of `AraafRoyall@1211` (no @ symbol between Araaf and Royall)
2. **Spaces**: The stringMakerKey has NO spaces, unlike ` Cleaner@Royall#6278 `
3. **Case Sensitivity**: The key is case-sensitive

## Additional Resources

- See `OPEN_SOURCE_README.md` for encryption key details
- Check `server/premium/users/` for example user files with encrypted keys
- Review `app/src/main/java/cleaner/Royall/Mainactivity.java` for decryption implementation

## Questions?

For more information or issues, please refer to the project documentation or contact the maintainers.
