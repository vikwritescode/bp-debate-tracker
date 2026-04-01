"""
Simple Script to alter older SQL tables so that they have newer columns
"""

import sqlite3

conn = sqlite3.connect("debates.db")
cur = conn.cursor()

"""
"""
def column_exists(cur, table_name, column_name):
    cur.execute(f"PRAGMA table_info({table_name})")
    return any(row[1] == column_name for row in cur.fetchall())

# NEW MIGRATE
try:
    # create new table for tourns
    cur.execute("DROP TABLE IF EXISTS tournaments_new")
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS tournaments_new (
            tournament_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            user_id TEXT NOT NULL,
            date DATE NOT NULL,
            speaker_standing INTEGER NOT NULL default 0,
            team_standing INTEGER NOT NULL default 0,
            rooms INTEGER NOT NULL default 0,
            format TEXT NOT NULL CHECK(format IN ('BP', 'WSDC', 'AUS')) DEFAULT 'BP',
            partner TEXT,
            tab_url TEXT,
            speaker_url TEXT,
            slug TEXT
        );
        """
    )

    # create new table for debates
    cur.execute("DROP TABLE IF EXISTS debates_new")
    cur.execute(
        """
        CREATE TABLE debates_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            date DATE NOT NULL,
            position TEXT NOT NULL CHECK(position IN ('OG', 'OO', 'CG', 'CO', 'AFF', 'NEG', 'ABS')),
            sp_order INTEGER NOT NULL CHECK(sp_order >= 0 AND sp_order <= 3) DEFAULT 0,
            points INTEGER NOT NULL CHECK(points >= 0 AND points <= 3),
            speaks INTEGER NOT NULL,
            infoslide TEXT NOT NULL,
            motion TEXT NOT NULL,
            has_reply BIT NOT NULL DEFAULT 0,
            reply INTEGER NOT NULL DEFAULT 0,
            tournament_id INTEGER REFERENCES tournaments(tournament_id),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    )

    # copy all the tourns over
    cur.execute(
        """
        INSERT INTO tournaments_new (
            tournament_id, name, user_id, date, speaker_standing,
            team_standing, rooms, format, partner, tab_url, speaker_url, slug
        )
        SELECT
            tournament_id, name, user_id, date, speaker_standing,
            team_standing, rooms,
            COALESCE(format, 'BP'),
            partner, tab_url, speaker_url, slug
        FROM tournaments;
        """
    )

    # copy all the debates over
    cur.execute(
        f"""
        INSERT INTO debates_new (
            id, user_id, date, position, sp_order,
            points, speaks, infoslide, motion, has_reply, reply,
            tournament_id, created_at
        )
        SELECT
            id, user_id, date, position,
            {"sp_order" if column_exists(cur, "debates", "sp_order") else "0"},
            points, speaks, infoslide, motion,
            COALESCE(has_reply, 0),
            COALESCE(reply, 0),
            tournament_id, created_at
        FROM debates;
        """
    )

    # drop old table
    cur.execute("DROP TABLE debates;")
    cur.execute("DROP TABLE tournaments;")

    # rename new table to old name
    cur.execute("ALTER TABLE debates_new RENAME TO debates;")
    cur.execute("ALTER TABLE tournaments_new RENAME TO tournaments;")

    conn.commit()
finally:
    conn.close()
