import os
from stellar_sdk import Keypair as StellarKeypair, Keypair
from solana.account import Account as SolanaAccount
from cryptography.fernet import Fernet

def encrypt_private_key(private_key, passphrase):
    cipher_suite = Fernet(passphrase)
    encrypted_private_key = cipher_suite.encrypt(private_key.encode())
    return encrypted_private_key

def decrypt_private_key(encrypted_private_key, passphrase):
    cipher_suite = Fernet(passphrase)
    decrypted_private_key = cipher_suite.decrypt(encrypted_private_key)
    return decrypted_private_key.decode()

def check_keys(private_key, chain):
    try:
        if chain == "stellar":
            Keypair.from_secret(private_key)
        elif chain == "solana":
            SolanaAccount(private_key)
    except Exception as e:
        print(f"ERROR: Invalid {chain} private key:", e)
        return False
    return True

def generate_or_load_keys(name):
    directory = f"~/hero/cfg/keys/"
    os.makedirs(os.path.expanduser(directory), exist_ok=True)
    stellar_file_path = os.path.expanduser(f"{directory}/stellar_{name}/private_key.enc")
    solana_file_path = os.path.expanduser(f"{directory}/solana_{name}/private_key.enc")

    # Check if keys already exist
    if os.path.isfile(stellar_file_path) and os.path.isfile(solana_file_path):
        with open(stellar_file_path, 'rb') as file:
            encrypted_stellar_private_key = file.read()
        with open(solana_file_path, 'rb') as file:
            encrypted_solana_private_key = file.read()

        return decrypt_private_key(encrypted_stellar_private_key, os.getenv("SECRET")), decrypt_private_key(encrypted_solana_private_key, os.getenv("SECRET"))

    # Generate new keys
    else:
        # Generate Stellar keypair
        stellar_keypair = StellarKeypair.random()

        # Generate Solana keypair
        solana_keypair = SolanaAccount()

        # Encrypt private keys
        encrypted_stellar_private_key = encrypt_private_key(stellar_keypair.secret, os.getenv("SECRET").encode())
        encrypted_solana_private_key = encrypt_private_key(solana_keypair.secret_key(), os.getenv("SECRET").encode())

        # Save encrypted private keys
        with open(stellar_file_path, 'wb') as file:
            file.write(encrypted_stellar_private_key)
        with open(solana_file_path, 'wb') as file:
            file.write(encrypted_solana_private_key)

        return stellar_keypair.secret, solana_keypair.secret_key()

def main():
    # Get name from user input
    name = input("Enter name: ")

    # Generate or load keys
    stellar_private_key, solana_private_key = generate_or_load_keys(name)

    # Check if keys work
    if not check_keys(stellar_private_key, "stellar") or not check_keys(solana_private_key, "solana"):
        print("ERROR: Key validation failed.")
        return

    print("Keys generated and validated successfully.")

if __name__ == "__main__":
    main()
