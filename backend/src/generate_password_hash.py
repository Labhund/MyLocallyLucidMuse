# Create this script: backend/src/generate_password_hash.py
from .auth import pwd_manager as pwd

if __name__ == "__main__":
    username = input("Enter username: ")
    plain_password = input("Enter password: ")
    
    hashed = pwd.hash_password(plain_password)
    print(f"\nHashed password for user {username} is:\n{hashed}")
