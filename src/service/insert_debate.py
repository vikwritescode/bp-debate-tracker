import sqlite3
from models import DebateCreate
def insert_debate(debate: DebateCreate, uid: str, db: sqlite3.Connection):
    """
    Insert a single debate result into the SQL table
    
    :param debate: The details of the record
    :type debate: DebateCreate
    :param uid: The UID of the user
    :type uid: str
    :param db: The Database Connection
    :type db: sqlite3.Connection
    """
    try:
        cur = db.cursor()
        cur.execute("INSERT INTO debates (user_id, date, position, points, speaks, infoslide, motion) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (uid, debate.date, debate.position, debate.points, debate.speaks, debate.infoslide, debate.motion))
        db.commit()
        return cur.lastrowid
    except sqlite3.DatabaseError as e:
        raise RuntimeError("Database Error")
    
    