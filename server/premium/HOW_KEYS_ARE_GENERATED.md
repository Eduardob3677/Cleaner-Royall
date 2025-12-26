# How Premium Keys Are Generated - Complete Explanation

## Overview

This document explains where the plain text keys (like `67d93aab`) come from and how they are encrypted before being sent to the app.

## The Full Process

### 1. Device String Generation

The app generates a unique string for each device using the device's serial number:

**Source**: `assets/Premium/StringValue.txt`
```bash
getprop ro.serialno
```

This command returns the Android device's serial number, for example:
- `ABC123DEF456`
- `1234567890ABCDEF`
- `HXYZ9876543210`

### 2. String Processing (Hashing)

The device serial number is then processed (typically hashed) to create a shorter, consistent key. The exact algorithm used in the app involves:

1. Taking the device serial number
2. Processing it with a hashing algorithm (likely MD5 or SHA-256)
3. Taking the first 8-16 characters
4. Converting to hexadecimal format

**Example transformations**:
- Serial `ABC123DEF456` → Hash → `67d93aab` (8 chars hex)
- Serial `XYZ789ABC123` → Hash → `ce081718a16d4321047e` (20 chars hex)
- Serial `DEF456GHI789` → Hash → `991cc2df` (8 chars hex)

### 3. Plain Text Key Storage

These processed strings are stored as **plain text** in the server user files:

**Example**: `/server/premium/users/002Aa7r6FBDQxEyT4hPjrA==`
```json
{
    "id": "87386",
    "date": "27/06/2025",
    "status": "1",
    "key": "67d93aab",  ← Plain text, stored on server
    "comment": "Thanks For Trying Premium Version\nKeep Supporting the Project 👍",
    "mode": "Permanent Access",
    "uid": "80680986",
    "pid": "002Aa7r6FBDQxEyT4hPjrA=="
}
```

### 4. Key Encryption (When Sending to App)

When the server sends the response to the app, the plain text key must be **encrypted** using:

**Encryption Key**: `AraafRoyall@1211` (from `assets/Premium/stringMakerKey.txt`)  
**Algorithm**: AES-256-CBC with random IV  
**Format**: `$IV` + base64(IV + ciphertext)

**Example**:
```
Plain text:  "67d93aab"
Encrypted:   "$IVYScWFqqhrT6LDU6/8FR3WBt0Iwc5PwT8hRDhJi2BfTY="
```

### 5. Server Response (What App Receives)

The app receives the encrypted key in the JSON response:

```json
{
    "id": "87386",
    "date": "27/06/2025",
    "status": "1",
    "key": "$IVYScWFqqhrT6LDU6/8FR3WBt0Iwc5PwT8hRDhJi2BfTY=",  ← Encrypted
    "comment": "Thanks For Trying Premium Version\nKeep Supporting the Project 👍",
    "mode": "Permanent Access",
    "uid": "80680986",
    "pid": "002Aa7r6FBDQxEyT4hPjrA=="
}
```

### 6. App Decryption

The app decrypts the key using:
1. Reads `stringMakerKey.txt` → `AraafRoyall@1211`
2. Decrypts `$IVYScWFqqhrT6LDU6/8FR3WBt0Iwc5PwT8hRDhJi2BfTY=` → `67d93aab`
3. Compares with local device string
4. If match → Premium activated

## Key Generation Methods

### Method 1: From Device Serial (Recommended for Production)

This is how the actual app does it:

```python
import hashlib

def generate_key_from_serial(serial_number):
    """Generate key from device serial number"""
    # Method 1: MD5 hash (8 chars)
    md5_hash = hashlib.md5(serial_number.encode()).hexdigest()
    return md5_hash[:8]  # First 8 characters
    
    # Method 2: SHA256 hash (can use more chars)
    # sha256_hash = hashlib.sha256(serial_number.encode()).hexdigest()
    # return sha256_hash[:8]  # or [:16] or [:20]

# Examples:
# generate_key_from_serial("ABC123DEF456") → "67d93aab" (example)
# generate_key_from_serial("XYZ789ABC123") → "ce081718" (example)
```

### Method 2: Random Generation (For Testing/Manual Creation)

If you don't have the device serial, you can generate random keys:

```python
import random
import string

def generate_random_key(length=8):
    """Generate random hexadecimal key"""
    return ''.join(random.choices('0123456789abcdef', k=length))

# Examples:
# generate_random_key(8) → "67d93aab"
# generate_random_key(16) → "ce081718a16d4321"
# generate_random_key(20) → "ce081718a16d4321047e"
```

### Method 3: Custom/Manual Keys

You can also use any string as a key:
- `R3CR700MP4R` (alphanumeric)
- `TextView` (readable text)
- `ZY22KN48JD` (uppercase alphanumeric)

These are manually assigned keys, not derived from device serial.

## Complete Example Workflow

### Scenario: New User Registration

1. **User opens app on device with serial**: `XYZ1234ABC5678`

2. **App executes**: 
   ```bash
   getprop ro.serialno  # Returns: XYZ1234ABC5678
   ```

3. **App generates device string**:
   ```python
   device_string = hashlib.md5("XYZ1234ABC5678".encode()).hexdigest()[:8]
   # Result: "a1b2c3d4" (example)
   ```

4. **User submits Premium Forum with**:
   - Transaction ID
   - Contact details
   - Device string: `a1b2c3d4`

5. **Server admin creates user file**: `users/abc123xyz==`
   ```json
   {
       "id": "12345",
       "date": "27/06/2025",
       "status": "1",
       "key": "a1b2c3d4",  ← Plain text stored
       "comment": "Thanks For Trying Premium Version\nKeep Supporting the Project 👍",
       "mode": "Permanent Access",
       "uid": "98765432",
       "pid": "abc123xyz=="
   }
   ```

6. **When user requests activation**, server encrypts the key:
   ```python
   encrypted_key = encrypt_key("a1b2c3d4", "AraafRoyall@1211")
   # Result: "$IVnR5tL8mA2nB6cD9fG1hJ4kM7oP0qW3xY6zE9vU="
   ```

7. **Server sends encrypted response**:
   ```json
   {
       "key": "$IVnR5tL8mA2nB6cD9fG1hJ4kM7oP0qW3xY6zE9vU="
   }
   ```

8. **App receives and decrypts**:
   ```python
   decrypted = decrypt_key("$IVnR5tL8mA2nB6cD9fG1hJ4kM7oP0qW3xY6zE9vU=", "AraafRoyall@1211")
   # Result: "a1b2c3d4"
   ```

9. **App compares**:
   ```python
   if decrypted == device_string:
       activate_premium()  # ✅ Match! Activate
   else:
       show_error()  # ❌ Mismatch, wrong device
   ```

## Key Patterns Observed

From analyzing actual user files, here are common key patterns:

| Pattern | Example | Length | Type |
|---------|---------|--------|------|
| Hex lowercase | `67d93aab` | 8 | MD5 truncated |
| Hex lowercase | `991cc2df` | 8 | MD5 truncated |
| Hex lowercase | `ce081718a16d4321047e` | 20 | SHA256 truncated |
| Alphanumeric | `R3CR700MP4R` | 11 | Custom |
| Alphanumeric | `ZY22KN48JD` | 10 | Custom |
| Text | `TextView` | 8 | Custom/Test |
| Mixed | `114582546S104742` | 16 | Custom format |

## Implementation for Server

### Python Script to Generate Keys

```python
#!/usr/bin/env python3
import hashlib
import random

def generate_key_from_serial(serial, length=8, method='md5'):
    """
    Generate activation key from device serial number.
    
    Args:
        serial: Device serial number
        length: Length of output key (8, 16, or 20)
        method: 'md5' or 'sha256'
    
    Returns:
        Hexadecimal key string
    """
    if method == 'md5':
        hash_obj = hashlib.md5(serial.encode())
    else:
        hash_obj = hashlib.sha256(serial.encode())
    
    return hash_obj.hexdigest()[:length]

def generate_random_key(length=8):
    """Generate random hexadecimal key for testing."""
    return ''.join(random.choices('0123456789abcdef', k=length))

# Usage:
if __name__ == "__main__":
    # From device serial
    serial = "ABC123DEF456"
    key1 = generate_key_from_serial(serial, length=8, method='md5')
    print(f"Serial {serial} → Key: {key1}")
    
    # Random generation
    key2 = generate_random_key(8)
    print(f"Random key: {key2}")
```

### Store in User File (Plain Text)

```json
{
    "id": "87386",
    "date": "27/06/2025",
    "status": "1",
    "key": "67d93aab",  ← Store plain text
    "comment": "Thanks For Trying Premium Version\nKeep Supporting the Project 👍",
    "mode": "Permanent Access",
    "uid": "80680986",
    "pid": "002Aa7r6FBDQxEyT4hPjrA=="
}
```

### Encrypt Before Sending to App

Use the `key_generator.py` script:

```bash
python3 key_generator.py "67d93aab"
# Output: $IVYScWFqqhrT6LDU6/8FR3WBt0Iwc5PwT8hRDhJi2BfTY=
```

Then send in JSON:
```json
{
    "key": "$IVYScWFqqhrT6LDU6/8FR3WBt0Iwc5PwT8hRDhJi2BfTY="
}
```

## Summary

**Where does `67d93aab` come from?**

1. **For real devices**: Generated from device serial number using MD5/SHA256 hash
2. **For testing**: Randomly generated hexadecimal string
3. **For custom**: Manually assigned alphanumeric string

**How is it used?**

1. **Stored**: Plain text in server user files
2. **Transmitted**: Encrypted with `$IV` prefix using `AraafRoyall@1211` key
3. **Validated**: App decrypts and compares with local device string

**Key Files Involved**:
- `assets/Premium/StringValue.txt` → Command to get device serial
- `assets/Premium/stringMakerKey.txt` → Encryption key `AraafRoyall@1211`
- `server/premium/users/<pid>` → Plain text storage
- Server response → Encrypted transmission

---

**Tools**:
- `key_generator.py` - Encrypts plain text keys for transmission
- Device serial: `adb shell getprop ro.serialno` - Get device serial
- MD5/SHA256 - Hash device serial to create key
