import sqlite3
from models import NotFoundError
def delete_tournament(tournament_id: str, uid: str, db: sqlite3.Connection):
    """
    Delete a tournament and all associated records
    
    :param tournament_id: tournament ID
    :type tournament_id: str
    :param uid: firebase user UID
    :type uid: str
    :param db: database connection
    :type db: sqlite3.Connection
    """
    try:
        cur = db.cursor()
        # check if this tournament even exists for the user
        cur.execute("""SELECT tournament_id
                    FROM tournaments
                    WHERE user_id = ? AND tournament_id = ? ;
                    """, (uid, tournament_id))
        recs = cur.fetchall()
        
        if len(recs) > 0:
            # if there are records to delete in the first place
            cur.execute("""
                        DELETE FROM debates
                        WHERE user_id = ? 
                        AND tournament_id = ? ;
                        """,
                        (uid, tournament_id))
            cur.execute("""
                        DELETE FROM tournaments
                        WHERE user_id = ?
                        AND tournament_id = ? ;
                        """,
                        (uid, tournament_id))
            db.commit()
            return {"message": "successfully deleted records"}
        # raise 404
        raise NotFoundError
    except sqlite3.DatabaseError as e:
        db.rollback()
        raise RuntimeError("Database Failed")
    except NotFoundError as e:
        raise
    except Exception as e:
        db.rollback()
        raise RuntimeError("Server Failed!")