import argparse

def encrypt(plain_text, key, offset):
    encrypted_text = " ".join(str((ord(char) * key) - offset) for char in plain_text)
    return encrypted_text

def decrypt(encrypted_text, key, offset):
    decrypted_text = "".join(chr((int(num) + offset) // key) for num in encrypted_text.split())
    return decrypted_text

def main():
    parser = argparse.ArgumentParser(description="DualKey Encryption Tool")
    parser.add_argument("action", choices=["encrypt", "decrypt"], help="Encrypt or Decrypt a message")
    parser.add_argument("message", help="The message to encrypt or decrypt")
    parser.add_argument("key", type=int, help="4-digit encryption key")
    parser.add_argument("offset", type=int, help="Offset value")

    args = parser.parse_args()

    if args.action == "encrypt":
        print("Encrypted:", encrypt(args.message, args.key, args.offset))
    elif args.action == "decrypt":
        print("Decrypted:", decrypt(args.message, args.key, args.offset))

if __name__ == "__main__":
    main()
