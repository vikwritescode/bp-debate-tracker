import sqlite3

def get_all_debates(uid: str, db_conn: sqlite3.Connection):
    """
    Docstring for get_all_debates
    
    :param uid: The uid of the user making this request.
    :type uid: str
    
    :param database: The database connection
    :type database: sqlite3.Connection
    """
    cur = db_conn.cursor()
    cur.execute("SELECT * FROM debates WHERE user_id = ?", (uid,))
    x = cur.fetchall()
    print("d", x)
    return x
    
    