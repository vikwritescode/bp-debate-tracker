import sqlite3
from utils import get_data
from service import delete_tournament, import_records, import_australs_records, import_wsdc_records
from fastapi import Request
def refresh_tournament(tournament_id: int, uid: str, con: sqlite3.Connection, request: Request):
    """
    refreshes a tournament record by deleting the old one and reimporting it
    
    :param tournment_id: tournament ID
    :type tournment_id: int
    :param uid: user UID
    :type uid: str
    :param con: sqlite3 connection
    :type con: sqlite3.Connection
    :param request: request
    :type request: Request
    """
    cur = con.cursor()
    cur.execute("SELECT tab_url, slug, speaker_url, date, format FROM tournaments WHERE tournament_id = ? AND user_id = ?", (tournament_id, uid))
    res = cur.fetchone()
    if res is None:
        raise RuntimeError("tournament not found")
    tab_url, slug, speaker_url, date, format = res
    
    
    # delete old record
    print(f"attempting to delete tournament with id {tournament_id} for user {uid}")
    delete_tournament(tournament_id, uid, con)
    
    # import new record
    # use existing service to do this
    if format == "BP":
        import_records(uid, tab_url, slug, speaker_url, date, con, request)
    elif format == "AUS":
        import_australs_records(uid, tab_url, slug, speaker_url, date, con, request)
    elif format == "WSDC":
        import_wsdc_records(uid, tab_url, slug, speaker_url, date, con, request)
    return {"message": "tournament refreshed successfully"}