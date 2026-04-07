from fastapi import APIRouter, Depends, HTTPException, status, Request
import sqlite3
from app.dependencies import get_current_user
from app.database import get_db
import service
from models import DebateCreate, NotFoundError

router = APIRouter(prefix="/api/debates", tags=["debates"])

@router.get("/get")
def api_get(user: dict = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db)):
    """
    Docstring for api_get
    
    :param user: user dictionary (firebase)
    :type user: dict
    :param db: sqlite database connection
    :type db: sqlite3.Connection
    """
    try:
        f = service.get_all_debates(user["uid"], db)
        return {"debates": f}
    except RuntimeError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=str(e))

@router.post("/add")
def api_post(debate: DebateCreate, user: dict = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db)):
    """
    Add another debate to the database.
    
    :param debate: Data for the table
    :type debate: DebateCreate
    :param user: the user object
    :type user: dict
    :param db: sqlite3 database connection
    :type db: sqlite3.Connection
    """
    try:
        attempt = service.insert_debate(debate, user["uid"], db)
        return {"id": attempt, "message": "Successfully inserted record"}
    except RuntimeError as e:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, e)
    
  
@router.delete("/delete/{debate_id}")
def api_delete_debate(debate_id: int, user: dict = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db)):
    """
    Delete debate index {debate_id} if it exists and is owned by user
    
    :param debate_id: The debate to delete
    :type debate_id: int
    :param user: firebase user
    :type user: dict
    :param db: sqlite3 database object
    :type db: sqlite3.Connection, request: Request = None
    """
    try:
        return service.delete_record(user["uid"], debate_id, db)
    except RuntimeError as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except NotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User Record Not Found")