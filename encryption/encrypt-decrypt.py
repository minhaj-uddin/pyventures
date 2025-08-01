import argparse
from pathlib import Path
from cryptography.fernet import Fernet


def generate_key(key_file: Path) -> None:
    """Generate and save a Fernet encryption key."""
    key = Fernet.generate_key()
    key_file.write_bytes(key)
    print(f"Key saved to {key_file}")


def load_key(key_file: Path) -> bytes:
    """Load a Fernet key from file."""
    return key_file.read_bytes()


def encrypt_file(input_file: Path, output_file: Path, key: bytes) -> None:
    """Encrypt a file using Fernet symmetric encryption."""
    fernet = Fernet(key)
    plaintext = input_file.read_bytes()
    ciphertext = fernet.encrypt(plaintext)
    output_file.write_bytes(ciphertext)
    print(f"Encrypted file saved to {output_file}")


def decrypt_file(input_file: Path, output_file: Path, key: bytes) -> None:
    """Decrypt a file using Fernet symmetric encryption."""
    fernet = Fernet(key)
    ciphertext = input_file.read_bytes()
    plaintext = fernet.decrypt(ciphertext)
    output_file.write_bytes(plaintext)
    print(f"Decrypted file saved to {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Encrypt or decrypt text files.")
    parser.add_argument(
        "mode", choices=["encrypt", "decrypt", "genkey"], help="Operation mode.")
    parser.add_argument("--key", type=Path, required=True,
                        help="Path to key file.")
    parser.add_argument("--infile", type=Path, help="Input file path.")
    parser.add_argument("--outfile", type=Path, help="Output file path.")

    args = parser.parse_args()

    if args.mode == "genkey":
        generate_key(args.key)
    elif args.mode in ("encrypt", "decrypt"):
        if not args.infile or not args.outfile:
            parser.error(
                "Encrypt/decrypt mode requires --infile and --outfile.")
        key = load_key(args.key)
        if args.mode == "encrypt":
            encrypt_file(args.infile, args.outfile, key)
        else:
            decrypt_file(args.infile, args.outfile, key)

# Generate a key:
# python encrypt-decrypt.py genkey --key secret.key

# Encrypt a file:
# python encrypt-decrypt.py encrypt --key secret.key --infile message.txt --outfile message.enc

# Decrypt a file:
# python encrypt-decrypt.py decrypt --key secret.key --infile message.enc --outfile decrypted.txt


if __name__ == "__main__":
    main()
