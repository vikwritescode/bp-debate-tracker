from utils import *
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from firebase_admin import credentials, auth
import firebase_admin
from dotenv import load_dotenv
import os
import sqlite3

from auth import get_current_user
import service

from models import *


con = sqlite3.connect("debates.db")
cur = con.cursor()

# create us a table for debates if not already there
cur.execute("""
CREATE TABLE IF NOT EXISTS debates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    date DATE NOT NULL,
    position TEXT NOT NULL CHECK(position IN ('OG', 'OO', 'CG', 'CO')),
    points INTEGER NOT NULL CHECK(points >= 0 AND points <= 3),
    speaks INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
            """)
con.commit()
con.close()
# TODO: use a faster approach

def get_db():
    conn = sqlite3.connect('debates.db')
    try:
        yield conn
    finally:
        conn.close()  # Always close, even if errors happen

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

@app.get("/api")
def root(user: dict = Depends(get_current_user)):
    return {"message": "API is indeed running."}

@app.get("/api/get")
def api_get(user: dict = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db)):
    f = service.get_all_debates(user["uid"], db)
    return {"debates": f}

@app.post("/api/add")
def api_post(debate: DebateCreate, user: dict = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db)):
    try:
        attempt = service.insert_debate(debate, user["uid"], db)
        return {"id": attempt, "message": "Successfully inserted record"}
    except sqlite3.Error as e:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Database Error")
    
@app.get("/api/tournaments")
def api_get_tournaments(url: str, user: dict = Depends(get_current_user)):
    try:
        return service.get_tournaments(url)
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Server Error")

@app.get("/api/speakers")
def api_get_names(url: str, slug: str, speaker: str, user: dict = Depends(get_current_user)):
    try:
        return service.get_speaker(url, slug, speaker)
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Skill Issue") 

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)