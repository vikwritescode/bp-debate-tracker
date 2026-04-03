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
                    SELECT
                    t.tournament_id,
                    t.name,
                    t.date,
                    t.speaker_standing,
                    t.team_standing,
                    t.rooms,
                    t.partner,
                    t.format,
                    t.tab_url,
                    COALESCE(SUM(d.points), 0) AS total_points,
                    COALESCE(AVG(d.speaks), 0) AS avg_speaks
                    FROM tournaments t
                    LEFT JOIN debates d ON d.tournament_id = t.tournament_id
                    WHERE t.user_id = ?
                    GROUP BY
                      t.tournament_id, t.name, t.date, t.speaker_standing,
                      t.team_standing, t.rooms, t.partner;
                    """, (uid,))
        x = cur.fetchall()
        r = [
            {"id": i[0],
             "name": i[1],
             "date": i[2],
             "speaker_standing": i[3],
             "team_standing": i[4],
             "rooms": i[5],
             "partner": i[6],
             "format": i[7],
             "tab_url": i[8],
             "total_points": i[9],
             "avg_speaks": i[10]
             }
            for i in x]
        return r
    except sqlite3.Error as e:
        raise RuntimeError("Database Issue")