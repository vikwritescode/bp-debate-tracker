from utils import *
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from firebase_admin import credentials
import firebase_admin
from dotenv import load_dotenv
import os
import sqlite3
import service
from models import *
import joblib
from contextlib import asynccontextmanager
from app import get_db, create_tables, init_firebase, get_current_user
from app.routes import usertournaments, wsdc, australs, tab, debates

@asynccontextmanager
async def lifespan(app: FastAPI):
    # create tables if they don't exist
    create_tables()
    init_firebase()
    
    # load model
    global model, mlb, clf
    model = joblib.load("sentence_transformer.pkl")
    mlb = joblib.load("multilabel_binarizer.pkl")
    clf = joblib.load("classifier.pkl")

    app.state.model = model
    app.state.mlb = mlb
    app.state.clf = clf
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usertournaments.router)
app.include_router(wsdc.router)
app.include_router(australs.router)
app.include_router(tab.router)
app.include_router(debates.router)

@app.get("/api")
def root(user: dict = Depends(get_current_user)):
    """
    Returns a message. Message should appear if authenticated.
    
    :param user: user object
    :type user: dict
    """
    return {"message": "API is indeed running."}
   
if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)