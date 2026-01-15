import sqlite3
from models import NotFoundError

def delete_record(uid: str, debate_id: int, db: sqlite3.Connection) -> dict:
    """
    Delete record if owned by UID
    
    :param uid: Description
    :type uid: str
    :param debate_id: Debate ID (primary key)
    :type debate_id: int
    :param db: sqlite3 database connection
    :type db: sqlite3.Connection
    :return: Success Message
    :rtype: dict
    """
    try:
        cur = db.cursor()
        cur.execute("SELECT 1 from debates WHERE user_id=? AND id=?", (uid, debate_id))
        recs = cur.fetchall()
        if len(recs) == 0:
            raise NotFoundError("Record Not Found")
        cur.execute("DELETE FROM debates WHERE user_id=? and id=?", (uid, debate_id))
        cur.execute("DELETE FROM categories where id=?", (debate_id))
        db.commit()
        return {"message": "record deleted successfully"}
    except NotFoundError as e:
        raise
    except Exception as e:
        raise RuntimeError("Server Error")