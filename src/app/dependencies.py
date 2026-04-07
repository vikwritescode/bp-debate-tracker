import os
import firebase_admin
from firebase_admin import credentials
from dotenv import load_dotenv

from .auth import get_current_user

def init_firebase():
    load_dotenv()
    if not firebase_admin._apps:
        cred = credentials.Certificate(os.getenv("SERVICE_ACCT_KEY"))
        firebase_admin.initialize_app(cred)