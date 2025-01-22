import argparse
import os

# ANSI escape codes for color
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'

def encrypt(plain_text, key, offset):
    if len(plain_text) > 300:
        return "Error: Input text is too long. Limit to 300 characters."
    try:
        encrypted_text = " ".join(str((ord(char) * key) - offset) for char in plain_text)
        return encrypted_text
    except Exception as e:
        return f"Error during encryption: {e}"

def decrypt(encrypted_text, key, offset):
    decrypted_text = ""
    try:
        encrypted_numbers = encrypted_text.strip().split()
        for number in encrypted_numbers:
            ascii_value = (int(number) + offset) // key
            decrypted_text += chr(ascii_value)
    except Exception as e:
        return f"Error during decryption: {e}"
    return decrypted_text

def encrypt_file(file_path, key, offset):
    try:
        with open(file_path, 'r') as file:
            plain_text = file.read().strip()
            encrypted_text = encrypt(plain_text, key, offset)
            with open('encrypted.txt', 'w') as enc_file:
                enc_file.write(encrypted_text)
            return f"{GREEN}Encrypted content saved to encrypted.txt{RESET}"
    except FileNotFoundError:
        return f"{RED}Error: File not found.{RESET}"

def decrypt_file(file_path, key, offset):
    try:
        with open(file_path, 'r') as file:
            encrypted_text = file.read().strip()
            decrypted_text = decrypt(encrypted_text, key, offset)
            with open('decrypted.txt', 'w') as dec_file:
                dec_file.write(decrypted_text)
            return f"{GREEN}Decrypted content saved to decrypted.txt{RESET}"
    except FileNotFoundError:
        return f"{RED}Error: File not found.{RESET}"

if __name__ == "__main__":
    print(f"{GREEN}\
    DDDDD   U   U   AAAAA   L       K   K   EEEEE   Y   Y\n\
    D    D  U   U  A     A  L       K  K    E        Y Y\n\
    D    D  U   U  AAAAAAA  L       KKK     EEEE      Y\n\
    D    D  U   U  A     A  L       K  K    E         Y\n\
    DDDDD   UUUUU  A     A  LLLLL   K   K   EEEEE     Y{RESET}\n")
    print(f"{YELLOW}Seedphrase Encryption/Decryption Tool{RESET}\n")

    parser = argparse.ArgumentParser(description="DualKey Encryption Tool")
    parser.add_argument("-a", "--action", choices=["encrypt", "decrypt"], help="Action to perform")
    parser.add_argument("-m", "--message", help="Text to encrypt/decrypt")
    parser.add_argument("-f", "--file", help="Path to file to encrypt/decrypt")
    parser.add_argument("-k", "--key", type=int, help="Encryption key (4-digit number)")
    parser.add_argument("-o", "--offset", type=int, help="Offset value (4 to 6 digits)")

    args = parser.parse_args()

    if args.action and args.key and args.offset:
        if args.file:
            if args.action == "encrypt":
                print(encrypt_file(args.file, args.key, args.offset))
            elif args.action == "decrypt":
                print(decrypt_file(args.file, args.key, args.offset))
        elif args.message:
            if args.action == "encrypt":
                print(f"{GREEN}Encrypted Text: {RESET}{encrypt(args.message, args.key, args.offset)}")
            elif args.action == "decrypt":
                print(f"{GREEN}Decrypted Text: {RESET}{decrypt(args.message, args.key, args.offset)}")
        else:
            print(f"{RED}Error: Please provide a message or file path.{RESET}")
    else:
        while True:
            try:
                key = int(input(f"{YELLOW}Enter encryption key (4-digit number): {RESET}"))
                if key < 1000 or key > 9999:
                    print(f"{RED}Error: Encryption key must be a 4-digit number.{RESET}")
                    continue
                offset = int(input(f"{YELLOW}Enter offset value (4 to 6 digit number): {RESET}"))
                if offset < 1000 or offset > 999999:
                    print(f"{RED}Error: Offset must be between 4 to 6 digits.{RESET}")
                    continue
                break
            except ValueError:
                print(f"{RED}Error: Please enter valid numbers.{RESET}")

        while True:
            action = input(f"{YELLOW}Do you want to (E)ncrypt, (D)ecrypt, or (Q)uit? {RESET}").strip().upper()
            if action == 'Q':
                print(f"{RED}Exiting program. Goodbye!{RESET}")
                break
            elif action == 'E':
                plain_text = input(f"{YELLOW}Enter text to encrypt (max 300 characters): {RESET}")
                encrypted_text = encrypt(plain_text, key, offset)
                print(f"{GREEN}Encrypted Text: {RESET}{encrypted_text}")
            elif action == 'D':
                encrypted_text = input(f"{YELLOW}Enter the encrypted text to decrypt: {RESET}")
                decrypted_text = decrypt(encrypted_text, key, offset)
                print(f"{GREEN}Decrypted Text: {RESET}{decrypted_text}")
            else:
                print(f"{RED}Invalid option. Please enter 'E' for encrypt, 'D' for decrypt, or 'Q' to quit.{RESET}")
