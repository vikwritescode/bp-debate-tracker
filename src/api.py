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
    position TEXT NOT NULL CHECK(position IN ('OG', 'OO', 'CG', 'CO', 'ABS')),
    points INTEGER NOT NULL CHECK(points >= 0 AND points <= 3),
    speaks INTEGER NOT NULL,
    infoslide TEXT NOT NULL,
    motion TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
            """)

cur.execute("""
CREATE TABLE IF NOT EXISTS categories (
    debate_id INTEGER NOT NULL,
    category TEXT NOT NULL CHECK(category IN (
        'Economics',
        'International Relations',
        'Africa',
        'Art',
        'Asia',
        'Children',
        'Cities',
        'Criminal Justice',
        'Culture',
        'Feminism',
        'Latin America',
        'Law',
        'LGBTQ+',
        'Media',
        'Medical',
        'Middle East',
        'Military',
        'Minority Communities',
        'Philosophy',
        'Politics',
        'Religion',
        'Romance/Sexuality',
        'Science/Technology',
        'Social Justice',
        'Sports'
    )),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

con.commit()
con.close()
# TODO: use a faster approach

def get_db():
    """
    function to pass database connections to the service layer,
    closing even if errors occur
    """
    conn = sqlite3.connect('debates.db')
    try:
        yield conn
    finally:
        conn.close() 

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
    """
    Returns a message. Message should appear if authenticated.
    
    :param user: user object
    :type user: dict
    """
    return {"message": "API is indeed running."}

@app.get("/api/get")
def api_get(user: dict = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db)):
    """
    Docstring for api_get
    
    :param user: user dictionary (firebase)
    :type user: dict
    :param db: sqlite database connection
    :type db: sqlite3.Connection
    """
    try:
        f = service.get_all_debates(user["uid"], db)
        return {"debates": f}
    except RuntimeError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=str(e))

@app.post("/api/add")
def api_post(debate: DebateCreate, user: dict = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db)):
    """
    Add another debate to the database.
    
    :param debate: Data for the table
    :type debate: DebateCreate
    :param user: the user object
    :type user: dict
    :param db: sqlite3 database connection
    :type db: sqlite3.Connection
    """
    try:
        attempt = service.insert_debate(debate, user["uid"], db)
        return {"id": attempt, "message": "Successfully inserted record"}
    except RuntimeError as e:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, e)
    
@app.get("/api/tournaments")
def api_get_tournaments(url: str, user: dict = Depends(get_current_user)):
    """
    get tournaments that exist on a tab
    
    :param url: Tab URL
    :type url: str
    :param user: firebase user
    :type user: dict
    """
    try:
        return service.get_tournaments(url)
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

@app.get("/api/speakers")
def api_get_names(url: str, slug: str, speaker: str, user: dict = Depends(get_current_user)):
    """
    Get list of speakers in a tournament that match a slug
    
    :param url: tab URL
    :type url: str
    :param slug: tournament slug
    :type slug: str
    :param speaker: speaker name (must be "in" their name on tab)
    :type speaker: str
    :param user: firebase user
    :type user: dict
    """
    try:
        return service.get_speaker(url, slug, speaker)
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.post("/api/import")
def api_import_from_url(tourn_data: TournamentImportModel, user: dict = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db)):
    """
    Docstring for api_import_from_url
    
    :param tourn_data: Data needed to fetch the tournament records
    :type tourn_data: TournamentImportModel
    :param user: firebase user
    :type user: dict
    :param db: sqlite3 connection
    :type db: sqlite3.Connection
    """
    try:
        return service.import_records(user["uid"], tourn_data.url, tourn_data.slug, tourn_data.speaker, tourn_data.date, db)
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@app.delete("/api/delete/{debate_id}")
def api_delete_debate(debate_id: int, user: dict = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db)):
    """
    Delete debate index {debate_id} if it exists and is owned by user
    
    :param debate_id: The debate to delete
    :type debate_id: int
    :param user: firebase user
    :type user: dict
    :param db: sqlite3 database object
    :type db: sqlite3.Connection
    """
    try:
        return service.delete_record(user["uid"], debate_id, db)
    except RuntimeError as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except NotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User Record Not Found")
        
    
if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)