import secrets

# Generate a secure random hexadecimal token of 165 bytes (330 characters)
secret_key = secrets.token_hex(16)

print("Your Flask secret key is:")
print(secret_key)
