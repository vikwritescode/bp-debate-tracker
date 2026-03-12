
import sqlite3

from fastapi import Request
from utils.get_wsdc_data import get_wsdc_data
from utils import correct_url

def import_wsdc_records(
    user_uid: str,
    tourn_url: str,
    tourn_slug: str,
    speaker_url: str,
    speaker_date,
    db: sqlite3.Connection,
    request: Request,
):
    """
    Import a WSDC tournament from tab.
    :param tourn_url: URL of the tournament on tab
    :type tourn_url: str
    :param tourn_slug: Slug of the tournament (e.g. "wsdc-2024")
    :type tourn_slug: str
    :param speaker_url: URL of the speaker page on tab
    :type speaker_url: str
    :param db: sqlite3 database object
    :type db: sqlite3.Connection
    :param user_uid: UID of the user performing the import
    :type user_uid: str
    """
    data = get_wsdc_data(correct_url(tourn_url), tourn_slug, speaker_url)
    return data