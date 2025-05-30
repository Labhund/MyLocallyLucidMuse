from typing import Optional, Dict
import bcrypt
import secrets
import os

# Function to generate salt (this should be done once at the beginning)
def _generate_salt() -> bytes:
    return bcrypt.gensalt()

class PasswordManager:
    def __init__(self):
        self.salt = None
    
    def init(self) -> bool:
        if not hasattr(self, 'initialized') or not self.initialized:
            # Only generate salt once
            try:
                self.salt = _generate_salt()
                return True
            except Exception as e:
                print(f"Error initializing password manager: {e}")
                return False
        return True

    def hash_password(self, password: str) -> bytes:
        if not self.salt:
            raise ValueError("Password manager not initialized")
        
        # Convert salt to tuple format expected by bcrypt
        salt_tuple = (self.salt,)
        return bcrypt.hashpw(password.encode('utf-8'), self.salt).decode()

    def verify_password(self, password: str, hashed: bytes) -> bool:
        if not self.salt:
            raise ValueError("Password manager not initialized")
        
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
        except:
            return False

# Create instance
password_manager = PasswordManager()

# Initialize password manager (call this once at startup)
if os.getenv("ENV") != "production":
    # Only initialize salt in development environments for security reasons
    password_manager.init()
