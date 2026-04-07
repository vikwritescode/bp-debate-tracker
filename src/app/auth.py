from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth
import os
import firebase_admin
from firebase_admin import credentials
from dotenv import load_dotenv

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    try:
        id_token = credentials.credentials
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Failed to Authenticate: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

def init_firebase():
    load_dotenv()
    if not firebase_admin._apps:
        cred = credentials.Certificate(os.getenv("SERVICE_ACCT_KEY"))
        firebase_admin.initialize_app(cred)