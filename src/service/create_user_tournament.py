import sqlite3
from models import TournamentCreate
def create_user_tournament(tournament: TournamentCreate, uid: str, db: sqlite3.Connection):
    """
    Insert a single tournament record into the SQL table
    
    :param tournament: The details of the record
    :type debate: TournamentCreate
    :param uid: The UID of the user
    :type uid: str
    :param db: The Database Connection
    :type db: sqlite3.Connection
    """
    try:
        cur = db.cursor()
        cur.execute("INSERT INTO tournaments (user_id, date, name) VALUES (?, ?, ?)",
        (uid, tournament.date, tournament.name))
        db.commit()
        return cur.lastrowid
    except sqlite3.DatabaseError as e:
        raise RuntimeError("Database Error")