import sqlite3
import json

def get_user_tournaments(uid: str, db_conn: sqlite3.Connection) -> list:
    """
    Get all tournaments associated with a user
    
    :param uid: firebase uid
    :type uid: str
    :param db_conn: sqlite3 database connection
    :type db_conn: sqlite3.Connection
    :return: list of debates associated with user
    :rtype: list
    """
    try:
        cur = db_conn.cursor()
        cur.execute("""
                SELECT tournament_id, name, date, speaker_standing, team_standing, rooms from tournaments
                WHERE user_id = ?
                    """, (uid,))
        x = cur.fetchall()
        r = [
            {"id": i[0],
             "name": i[1],
             "date": i[2],
             "speaker_standing": i[3],
             "team_standing": i[4],
             "rooms": i[5]
             }
            for i in x]
        return r
    except sqlite3.Error as e:
        raise RuntimeError("Database Issue")