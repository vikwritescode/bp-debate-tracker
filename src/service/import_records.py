from utils import get_data
from ai import classify
from fastapi import Request
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
        
def import_records(uid: str, tab_url: str, slug: str, speaker_url: str, date: str, con: sqlite3.Connection, request: Request):
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
    :param request: request
    :type request: Request
    """
    validate_date_format(date)
    records = []
    try:
        tab_data = get_data(tab_url, slug, speaker_url)
        cur = con.cursor()
        for round in tab_data:
            rcd = (uid, 
                            date,
                            round["position"].upper(),
                            round["points"],
                            round["speaks"],
                            round["info_slide"],
                            round["motion"])
            print(f"FOR {round["motion"]}")
            try:
                cats = classify(round["info_slide"], round["motion"], request)
            except Exception as e:
                print("whoops", str(e))
            print(cats)
            cur.execute("INSERT INTO debates (user_id, date, position, points, speaks, infoslide, motion) VALUES (?, ?, ?, ?, ?, ?, ?)", rcd)
            p_key = cur.lastrowid
            if p_key is None:
                raise RuntimeError("did not insert record")
            tuples = [(p_key, uid, c) for c in cats]
            cur.executemany("INSERT INTO categories (debate_id, user_id, category) VALUES (?, ?, ?)", tuples)
    except Exception as e:
        raise RuntimeError("error fetching participant data")
    try:
        # cur.executemany("INSERT INTO debates (user_id, date, position, points, speaks, infoslide, motion) VALUES (?, ?, ?, ?, ?, ?, ?)", records)
        con.commit()
    except Exception as e:
        raise sqlite3.DatabaseError("error writing to DB")
    return {"message": "records inserted succesfully"}