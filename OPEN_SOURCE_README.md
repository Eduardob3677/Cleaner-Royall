# Cleaner Royall - Open Source Version

## Important Notice

This application is now **fully open source and free**. All premium features, subscriptions, and trial limitations have been removed.

## Changes Made for Open Source Release

### 1. Encryption Removed
- All encrypted content has been decrypted and stored in plaintext
- Encryption/decryption methods in `Mainactivity.java` have been disabled
- Server configuration files are now in readable format

### 2. Premium Features Removed
- No subscription or payment required
- No trial periods or limitations
- All features available to everyone
- Premium validation code disabled

### 3. Server Files Decrypted
- All `.enc` files have been decrypted
- JSON configuration files with encrypted fields now contain plaintext
- Shell scripts fully decrypted

## Encryption Keys Used (For Reference Only)

The following keys were used to decrypt the content. They are no longer needed as all content is now in plaintext:

| Key | Algorithm | Previous Usage |
|-----|-----------|----------------|
| `Royalls` | AES-256-ECB | Files without $IV prefix |
| ` Cleaner@Royall#6278 ` | AES-256-CBC | Content prefixed with $IV |
| `Araaf@Royall$1211` | AES-256-CBC | Premium activator scripts |

All keys used SHA-256 key derivation with PKCS5 padding.

## Code Changes

### Disabled Encryption Methods
The following methods in `Mainactivity.java` have been disabled:
- `generateKey()` - Returns null
- `_DecryptedStringKey()` - Returns string as-is without decryption
- `_LibEncryptedDecrypted()` - Empty method

### Premium/Subscription Code
- `PremiumForumActivity.java` - Marked as deprecated
- All premium checks should be bypassed
- Trial reset features converted to informational messages

## Building the App

This is now a standard Android project with no special encryption requirements. Simply:

1. Open in Android Studio
2. Build and run
3. No API keys or premium features to configure

## License

This project is now open source. Please check the LICENSE file for details.

## Contributing

Contributions are welcome! Since the app is now open source, feel free to:
- Report issues
- Submit pull requests
- Suggest improvements
- Help with documentation

## Credits

Original Author: Araaf Royall

---

**Note**: This open source version removes all monetization, encryption, and premium features. The app is provided as-is for educational and practical use.
