import sqlite3

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
        cur.execute("SELECT * FROM debates WHERE user_id = ?", (uid,))
        x = cur.fetchall()
        return x
    except sqlite3.Error as e:
        raise RuntimeError("Database Issue")
    
    