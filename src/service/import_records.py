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
    """
    creates debate records based on a speaker at a tournament
    
    :param uid: user UID
    :type uid: str
    :param tab_url: tab URL
    :type tab_url: str
    :param slug: tournament slug
    :type slug: str
    :param speaker_url: speaker URL
    :type speaker_url: str
    :param date: date of tournament in yyyy-mm-dd form
    :type date: str
    :param con: sqlite3 connection
    :type con: sqlite3.Connection
    """
    validate_date_format(date)
    records = []
    try:
        speaker_rsp = requests.get(speaker_url)
        s = speaker_rsp.json()
        r = get_results(tab_url, slug, s)[0]
        sp = get_speaks(tab_url, slug, s) 
        p = get_positions(tab_url, "_", r, s["team"])
    except Exception as e:
        raise RuntimeError("error fetching participant data")
    try:
        for round in r:
            if p.get(round["round"], "ABS") == "ABS":
                # skip "ABS rounds"
                continue
            records.append((uid, 
                            date,
                            p.get(round["round"], "ABS").upper(),
                            round["points"],
                            sp.get(round["round"], 0)))
    except Exception as e:
        raise RuntimeError("error processing participant data")
    cur = con.cursor()
    try:
        cur.executemany("INSERT INTO debates (user_id, date, position, points, speaks) VALUES (?, ?, ?, ?, ?)", records)
        con.commit()
    except Exception as e:
        raise sqlite3.DatabaseError("error writing to DB")
    return {"message": "records inserted succesfully"}