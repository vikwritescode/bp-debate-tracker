from utils import *
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def root():
    return {"message": "API is indeed running."}

@app.get("/api/speaker")
def get_speaker()