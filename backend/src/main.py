from typing import Optional, Dict
import jwt
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasicCredentials, BasicAuthSecurityError
import os
from .auth import hash_password as pwd_hash
from .auth import password_manager as pwd_manager



# Create FastAPI app instance
app = FastAPI()

# Add CORS middleware for React frontend access
origins = ["*"]  # This will be replaced with just your domain later
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello from the MyLocallyLucidMuse Backend!"}

@app.get("/test")
async def test_endpoint():
    return {"message": "This is a test endpoint!"}

SECRET_KEY = os.getenv("JWT_SECRET_KEY") or "fallback_secret_key" # THIS IS NOT SECURE, DO NOT USE IN PRODUCTION

@app.api_rote("/secure-endpoint", methods=["GET"])
async def secure_endpoint(credentials: HTTPBasicCredentials = Depends(BasicAuthSecurityError)):
    if not credentials or not credentials.username or not credentials.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    # Here you would typically verify the username and password against your user database
    # For demonstration, we will just hash the password and return it
    hashed_password = pwd_manager.hash_password(credentials.password)
    
    return {"message": "Secure endpoint accessed", "hashed_password": hashed_password}

def get_current_username(credentials: HTTPBasicCredentials) -> Optional[str]:
    if pwd_manager.verify_password(credentials.username, "your_password_here"):
        # Assuming you have a way to verify the username and password
        # For demonstration, we will just return the username
        return credentials.username
    return None