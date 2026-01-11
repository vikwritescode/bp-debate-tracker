from utils import get_speaker
from utils import get_results
from utils import get_positions
from utils import get_speaks

import requests
import sqlite3
from datetime import datetime

def validate_date_format(date_string: str):
    """Validate YYYY-MM-DD format only"""
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return date_string
    except ValueError:
        raise ValueError("Invalid Date Format!")
        
def import_records(uid: str, tab_url: str, slug: str, speaker_url: str, date: str, con: sqlite3.Connection):
    validate_date_format(date)
    records = []
    try:
        speaker_rsp = requests.get(speaker_url)
        s = speaker_rsp.json()
    except Exception as e:
        raise RuntimeError("Could Not Fetch Speaker")
 
    r = get_results(tab_url, slug, s)[0]
    sp = get_speaks(tab_url, slug, s) 
    p = get_positions(tab_url, "_", r, s["team"])

    for round in r:
        if p.get(round["round"], "ABS") == "ABS":
            # skip "ABS rounds"
            continue
        # (userid, date, position, points, speaks)
        records.append((uid,
                        date,
                        p.get(round["round"], "ABS").upper(),
                        round["points"],
                        sp.get(round["round"], 0)))
    cur = con.cursor()
    try:
        cur.executemany("INSERT INTO debates (user_id, date, position, points, speaks) VALUES (?, ?, ?, ?, ?)", records)
        con.commit()
    except Exception as e:
        raise sqlite3.DatabaseError(e)
    return {"message": "records inserted succesfully"}