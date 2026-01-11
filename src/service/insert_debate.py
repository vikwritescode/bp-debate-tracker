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
    cur = db.cursor()
    cur.execute("INSERT INTO debates (user_id, date, position, points, speaks) VALUES (?, ?, ?, ?, ?)",
        (uid, debate.date, debate.position, debate.points, debate.speaks))
    db.commit()
    return cur.lastrowid
    