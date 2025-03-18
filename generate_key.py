from cryptography.fernet import Fernet

# Generate a new encryption key
key = Fernet.generate_key()

# Save the key to a file (DO NOT SHARE THIS KEY)
with open("encryption.key", "wb") as key_file:
    key_file.write(key)

print("✅ Encryption key generated and saved as 'encryption.key'. Keep it secure!")
