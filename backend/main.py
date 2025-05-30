from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello from the MyLocallyLucidMuse Backend!"}

@app.get("/test")
async def test_endpoint():
    return {"message": "This is a test endpoint!"}