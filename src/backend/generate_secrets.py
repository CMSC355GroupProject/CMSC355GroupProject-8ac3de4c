import secrets

# Generate a 64-character hexadecimal string
secret_key = secrets.token_hex(32)
print(secret_key)