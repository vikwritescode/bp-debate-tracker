"""
Simple Script to alter older SQL tables so that they have newer columns
"""
import sqlite3
conn = sqlite3.connect("debates.db")
cur = conn.cursor()


# UPGRADE TO TRACK SIZE AND RANKING
try:
    cur.execute("ALTER TABLE tournaments ADD COLUMN speaker_standing INTEGER NOT NULL DEFAULT 0")
    cur.execute("ALTER TABLE tournaments ADD COLUMN team_standing INTEGER NOT NULL DEFAULT 0")
    cur.execute("ALTER TABLE tournaments ADD COLUMN rooms INTEGER NOT NULL DEFAULT 0")
    
    conn.commit()

except sqlite3.OperationalError as e:
    conn.rollback()
    if "duplicate column name" in str(e):
        print("Columns already exist, skipping migration (a)")
    
    else:
        conn.close()
        raise

    
# UPGRADE DATABASE TO TRACK PARTNER, NAME, URL, SLUG
try:
    cur.execute("ALTER TABLE tournaments ADD COLUMN partner TEXT")
    cur.execute("ALTER TABLE tournaments ADD COLUMN speaker_url TEXT")
    cur.execute("ALTER TABLE tournaments ADD COLUMN tab_url TEXT")
    cur.execute("ALTER TABLE tournaments ADD COLUMN slug TEXT")
    
    conn.commit()

except sqlite3.OperationalError as e:
    conn.rollback()
    if "duplicate column name" in str(e):
        print("Columns already exist, skipping migration (b)")
    
    else:
        raise

# add format column to tournaments
try:
    cur.execute("ALTER TABLE tournaments ADD COLUMN format TEXT NOT NULL CHECK(format IN ('BP', 'WSDC', 'AUS')) DEFAULT 'BP'")
    cur.execute("ALTER TABLE tournaments ADD COLUMN substantive BIT NOT NULL DEFAULT 1")
    conn.commit()

except sqlite3.OperationalError as e:
    conn.rollback()
    if "duplicate column name" in str(e):
        print("Columns already exist, skipping migration (c)")
    
    else:
        raise
    

finally:
    conn.close()
