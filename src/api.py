from utils import *
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware

from firebase_admin import credentials, auth
import firebase_admin
from dotenv import load_dotenv
import os
import sqlite3

from auth import get_current_user
import service

from models import *
import joblib

from contextlib import asynccontextmanager


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

# attempt to add this column, should allow migration from older values
try:
    cur.execute("ALTER TABLE debates ADD COLUMN tournament_id INTEGER REFERENCES Tournaments(tournament_id);")
except sqlite3.OperationalError as e:
    if "duplicate column name: tournament_id" not in str(e):
        raise

cur.execute("""
CREATE TABLE IF NOT EXISTS categories (
    debate_id INTEGER NOT NULL,
    user_id TEXT NOT NULL,
    category TEXT NOT NULL CHECK(category IN (
        'Africa',
        'Animal Rights',
        'Art',
        'Artificial Intelligence',
        'Asia',
        'Australia',
        'Charity',
        'Children',
        'Cities',
        'Climate Change',
        'Colonialism',
        'Criminal Justice',
        'Culture',
        'Cybersecurity',
        'Democracy',
        'Development',
        'Disability Rights',
        'Drugs',
        'Economics',
        'Education/Academia',
        'Elderly/Aging',
        'Energy',
        'Environment',
        'Ethics',
        'Europe',
        'Feminism',
        'Healthcare',
        'Historical Memory',
        'Housing',
        'Human Rights',
        'Immigration',
        'Indigenous People',
        'International Relations',
        'Labor',
        'Latin America',
        'Law',
        'LGBTQ+',
        'Media',
        'Medical',
        'Mental Health',
        'Middle East',
        'Military',
        'Minority Communities',
        'Nationalism',
        'Philosophy',
        'Police',
        'Policy',
        'Politics',
        'Privacy',
        'Private Property',
        'Refugees/Asylum',
        'Religion',
        'Romance/Sex',
        'Romance/Sexuality',
        'Science/Technology',
        'Social Justice',
        'Social Policy',
        'Sports',
        'Terrorism',
        'Trade'
    )),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS tournaments (
    tournament_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    user_id TEXT NOT NULL,
    date DATE NOT NULL,
    speaker_standing INTEGER NOT NULL default 0,
    team_standing INTEGER NOT NULL default 0,
    rooms INTEGER NOT NULL default 0
);
""")

con.commit()
con.close()

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

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: load model
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

# global variables for the trained model being loaded in
model = None
mlb = None
clf = None

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
    except TabAuthError as e:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, "tab auth")
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
    except TabAuthError as e:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, "tab auth")
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/api/startdate")
def api_get_startdate(url: str, slug: str, user: dict = Depends(get_current_user)):
    """
    get start date for tournament
    
    :param url: tab URL
    :type url: str
    :param slug: tournament slug
    :type slug: str
    :param user: firebase user
    :type user: dict
    """
    try:
        return service.get_start_date(url, slug)
    except TabAuthError as e:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail="tab auth")
    except StartNotFoundError as e:
        raise HTTPException(status.HTTP_417_EXPECTATION_FAILED, detail="Could not find start time")

@app.post("/api/import")
def api_import_from_url(tourn_data: TournamentImportModel, request: Request, user: dict = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db)):
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
        return service.import_records(
            user["uid"],
            tourn_data.url,
            tourn_data.slug,
            tourn_data.speaker,
            tourn_data.date,
            db, 
            request)
    except TabAuthError as e:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, "tab auth")
    except TabBrokenError as e:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, "tab broken")
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/api/usertournaments")
def api_get_tournaments(user: dict = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db)):
    """
    Gets all tournament records associated with a user.
    
    :param user: firebase user
    :type user: dict
    :param db: sqlite3 database connection
    :type db: sqlite3.Connection
    """
    try:
        return service.get_user_tournaments(user["uid"], db)
    except Exception as e:
        raise
    
@app.post("/api/usertournaments/create")
def api_create_tournaments(tourn: TournamentCreate, user: dict = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db)):
    """
    Gets all tournament records associated with a user.
    :param tourn: tournament to create
    :type tourn: TournamentCreate
    :param user: firebase user
    :type user: dict
    :param db: sqlite3 database connection
    :type db: sqlite3.Connection
    """
    try:
        attempt = service.create_user_tournament(tourn, user["uid"], db)
        return {"id": attempt, "message": "Successfully inserted record"}
    except RuntimeError as e:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, e)
  
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

@app.delete("/api/usertournaments/delete/{tournament_id}")
def api_delete_tournament(tournament_id: int, user: dict = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db)):
    """
    Delete a tournament and all associated records with this tournament.
    
    :param tournament_id: tournament ID
    :type tournament_id: int
    :param user: firebase user
    :type user: dict
    :param db: sqlite3 database
    :type db: sqlite3.Connection
    """
    try:
        return service.delete_tournament(tournament_id, user["uid"], db)
    except NotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    
if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)