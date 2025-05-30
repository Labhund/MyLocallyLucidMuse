from typing import Optional
from fastapi import FastAPI, Request, HTTPException, status, Depends # Modified import
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import os
import ollama
from dotenv import load_dotenv # Add this import

load_dotenv()

app = FastAPI()

# Create an environment variable for your JWT secret (e.g., in .env file)
JWT_SECRET = os.getenv("JWT_SECRET_KEY")
if not JWT_SECRET:
    raise RuntimeError("JWT secret not configured")

@app.middleware("http")
async def verify_token(request: Request, call_next):
    credentials = request.cookies.get("access_token")
    # Initialize request.state.user to None or a default unauthenticated user object
    request.state.user = None 
    if credentials and credentials.startswith("Bearer "):
        token = credentials.split(" ")[1]
        
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"]) # Specify algorithms
            # Store user info for context
            request.state.user = {
                "sub": payload["sub"],
                "name": payload.get("name"),
                "email": payload.get("email")
            }
        except jwt.ExpiredSignatureError:
            # Handle expired token specifically if needed
            pass # Or raise HTTPException
        except jwt.InvalidTokenError:
            # Handle other invalid token errors
            pass # Or raise HTTPException
        except Exception as e:
            # Log other unexpected errors during token decoding
            print(f"Error decoding token: {e}")
            pass
            
    response = await call_next(request)
    return response

# Placeholder for get_current_user. You'll need to implement this properly.
def get_current_user(request: Request) -> Optional[dict]:
    return getattr(request.state, "user", None)

# Add this to your existing endpoints (backend/main.py routes):

@app.get("/api/v1/user/me", tags=["User"])
async def read_user(current_user: Optional[dict] = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return {"user": current_user}

@app.post("/api/v1/ollama/chat", tags=["Ollama"])
async def ollama_chat(request: Request):
    body = await request.json()
    model = body.get("model", "llama2") # Default to llama2 if no model is specified
    messages = body.get("messages")

    if not messages:
        raise HTTPException(status_code=400, detail="No messages provided")

    try:
        response = ollama.chat(
            model=model,
            messages=messages
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/ollama/models", tags=["Ollama"])
async def list_ollama_models():
    try:
        models = ollama.list()
        return models
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# For frontend debugging
@app.get("/test-auth")
async def test_auth():
    return "Test auth endpoint"
