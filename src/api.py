from utils import *
import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from firebase_admin import credentials, auth
import firebase_admin
from dotenv import load_dotenv
import os

from auth import get_current_user

load_dotenv()
if not firebase_admin._apps:
    cred = credentials.Certificate(os.getenv("SERVICE_ACCT_KEY"))
    firebase_admin.initialize_app(cred)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root(user: dict = Depends(get_current_user)):
    return {"message": "API is indeed running."}

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)