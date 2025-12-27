# Premium Key Generation - Quick Start

## TL;DR - How to Generate Keys

### Step 1: Choose or Generate Plain Text Key

**Option A: From device serial** (recommended):
```bash
adb shell getprop ro.serialno
# Example output: ABC123DEF456
```

Then hash it:
```python
import hashlib
plain_key = hashlib.md5("ABC123DEF456".encode()).hexdigest()[:8]
# Result: 67d93aab (example)
```

**Option B: Use any custom string**:
```
R5CW82XYYDL
67d93aab
TextView
```

### Step 2: Encrypt the Key

```bash
cd server/premium
python3 key_generator.py "R5CW82XYYDL"
```

Output:
```
Encrypted Key: $IV8ZvyHWpSbA6dLX6KUtOcGFPHs5qKEH+Fny1Yw23kTcE=
```

### Step 3: Use in Server Response

**Store plain text in user file** (`server/premium/users/<pid>`):
```json
{
    "id": "87386",
    "date": "27/06/2025",
    "status": "1",
    "key": "R5CW82XYYDL",
    "comment": "Thanks For Trying Premium Version\nKeep Supporting the Project 👍",
    "mode": "Permanent Access",
    "uid": "80680986",
    "pid": "002Aa7r6FBDQxEyT4hPjrA=="
}
```

**Send encrypted in API response**:
```json
{
    "id": "87386",
    "date": "27/06/2025",
    "status": "1",
    "key": "$IV8ZvyHWpSbA6dLX6KUtOcGFPHs5qKEH+Fny1Yw23kTcE=",
    "comment": "Thanks For Trying Premium Version\nKeep Supporting the Project 👍",
    "mode": "Permanent Access",
    "uid": "80680986",
    "pid": "002Aa7r6FBDQxEyT4hPjrA=="
}
```

## Installation

```bash
pip3 install pycryptodome
```

## Examples

### Example 1: Simple hex key
```bash
python3 key_generator.py "67d93aab"
# Output: $IVYScWFqqhrT6LDU6/8FR3WBt0Iwc5PwT8hRDhJi2BfTY=
```

### Example 2: Alphanumeric key
```bash
python3 key_generator.py "R5CW82XYYDL"
# Output: $IV8ZvyHWpSbA6dLX6KUtOcGFPHs5qKEH+Fny1Yw23kTcE=
```

### Example 3: Text key
```bash
python3 key_generator.py "TextView"
# Output: $IVpZ3sR5tL8mA2nB6cD9fG1hJ4kM7oP0qW3xY6zE9vU=
```

## Technical Details

**Encryption Key**: `AraafRoyall@1211` (from APK smali analysis)  
**Algorithm**: AES-256-CBC  
**Key Derivation**: SHA-256  
**Format**: `$IV` + base64(IV + ciphertext)

## Documentation

- **KEY_GENERATION_GUIDE.md** - Complete encryption guide with code examples
- **HOW_KEYS_ARE_GENERATED.md** - Explains where plain text keys come from
- **key_generator.py** - Python script to encrypt keys

## Quick Test

```bash
# Generate a test key
python3 key_generator.py "test123"

# Expected output format:
# Encrypted Key: $IV<base64_string>
```

## Notes

- Each encryption produces a **different output** due to random IV (this is normal and secure)
- Store **plain text** keys in user files
- Send **encrypted** keys to the app
- The app decrypts using the same key: `AraafRoyall@1211`

---

**Based on**: Smali analysis of https://github.com/Eduardob3677/Cleaner_Royall.git  
**Encryption Key Source**: `assets/Premium/stringMakerKey.txt`
