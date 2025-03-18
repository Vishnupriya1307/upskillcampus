from cryptography.fernet import Fernet

# Function to load the encryption key
def load_key():
    with open("secret.key", "rb") as key_file:
        return key_file.read().strip()  # Ensures no extra spaces/newlines

# Load the key
ENCRYPTION_KEY = load_key()

# Initialize Fernet cipher
cipher = Fernet(ENCRYPTION_KEY)
