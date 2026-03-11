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
    
    # create NEW table for debates with new columns
    cur.execute("""
    CREATE TABLE IF NOT EXISTS debates_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    date DATE NOT NULL,
    position TEXT NOT NULL CHECK(position IN ('OG', 'OO', 'CG', 'CO', 'AFF', 'NEG', 'ABS')),
    has_reply BIT NOT NULL DEFAULT 0,
    reply NUMERIC NOT NULL DEFAULT 0,
    points INTEGER NOT NULL CHECK(points >= 0 AND points <= 3),
    speaks NUMERIC NOT NULL,
    infoslide TEXT NOT NULL,
    motion TEXT NOT NULL,
    tournament_id INTEGER REFERENCES Tournaments(tournament_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
            """)
    
    # no position, speaks, has_reply, reply in old table
    # insert all old records into new table
    cur.execute("""
                INSERT INTO debates_new 
                    (id, user_id, date,
                    position, points, speaks,
                    infoslide, motion, created_at,
                    tournament_id)
                    
                    SELECT id, user_id, date,
                    position, points, speaks,
                    infoslide, motion, created_at,
                    tournament_id FROM debates;
                """)
    
    # rename old table and new table
    cur.execute("DROP TABLE IF EXISTS debates_old")
    cur.execute("ALTER TABLE debates RENAME TO debates_old")
    cur.execute("ALTER TABLE debates_new RENAME TO debates")
    conn.commit()

except sqlite3.OperationalError as e:
    conn.rollback()
    if "duplicate column name" in str(e):
        print("Columns already exist, skipping migration (c)")
    
    else:
        raise

# add format column to tournaments
try:
    cur.execute("ALTER TABLE tournaments ADD COLUMN format TEXT NOT NULL CHECK(format IN ('BP', 'WSDC', 'AUS')) DEFAULT 'BP'")
    conn.commit()

except sqlite3.OperationalError as e:
    conn.rollback()
    if "duplicate column name" in str(e):
        print("Columns already exist, skipping migration (d)")
    
    else:
        raise

finally:
    conn.close()
