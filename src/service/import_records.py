from utils import get_data

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
        tab_data = get_data(tab_url, slug, speaker_url)
        for round in tab_data:
            records.append((uid, 
                            date,
                            round["position"].upper(),
                            round["points"],
                            round["speaks"]))
    except Exception as e:
        raise RuntimeError("error fetching participant data")
    cur = con.cursor()
    try:
        cur.executemany("INSERT INTO debates (user_id, date, position, points, speaks) VALUES (?, ?, ?, ?, ?)", records)
        con.commit()
    except Exception as e:
        raise sqlite3.DatabaseError("error writing to DB")
    return {"message": "records inserted succesfully"}