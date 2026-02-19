"""
Simple Script to alter older SQL tables so that they have newer columns
"""
import sqlite3
conn = sqlite3.connect("debates.db")
cur = conn.cursor()

try:
    cur.execute("ALTER TABLE tournaments ADD COLUMN speaker_standing INTEGER NOT NULL DEFAULT 0")
    cur.execute("ALTER TABLE tournaments ADD COLUMN team_standing INTEGER NOT NULL DEFAULT 0")
    cur.execute("ALTER TABLE tournaments ADD COLUMN rooms INTEGER NOT NULL DEFAULT 0")
    
    conn.commit()

except sqlite3.OperationalError as e:
    conn.rollback()
    if "duplicate column name" in str(e):
        print("Columns already exist, skipping migration")
    
    else:
        raise
    
finally:
    conn.close()
