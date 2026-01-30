import sqlite3
import json

def get_all_debates(uid: str, db_conn: sqlite3.Connection) -> list:
    """
    Get all debates associated with a user
    
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
                SELECT d.id, d.user_id, t.date, d.position, d.points, d.speaks, d.infoslide, d.motion, json_group_array(c.category) AS categories, t.name AS tournament_name
                FROM debates d
                LEFT JOIN categories c ON d.id = c.debate_id
                LEFT JOIN tournaments t on t.tournament_id = d.tournament_id
                WHERE d.user_id = ?
                GROUP BY d.id
                ORDER BY d.date DESC, d.id;
                    """, (uid,))
        x = cur.fetchall()
        r = [
            {"id": i[0],
             "uid": i[1],
             "date": i[2],
             "position": i[3],
             "points": i[4],
             "speaks": i[5],
             "infoslide": i[6],
             "motion": i[7],
             "categories": json.loads(i[8]),
             "tournament": i[9]
        } for i in x]
        return r
    except sqlite3.Error as e:
        raise RuntimeError("Database Issue")
    
    