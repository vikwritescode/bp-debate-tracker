from fastapi import APIRouter, Depends, HTTPException, status
import sqlite3
from app.dependencies import get_current_user
from app.database import get_db
import service
from models import TournamentCreate, NotFoundError

router = APIRouter(prefix="/api/usertournaments", tags=["tournaments"])

@router.get("/")
def api_get_tournaments(user: dict = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db)):
    """
    Gets all tournament records associated with a user.
    
    :param user: firebase user
    :type user: dict
    :param db: sqlite3 database connection
    :type db: sqlite3.Connection
    """
    try:
        return service.get_user_tournaments(user["uid"], db)
    except Exception as e:
        raise
    
@router.post("/create")
def api_create_tournaments(tourn: TournamentCreate, user: dict = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db)):
    """
    Gets all tournament records associated with a user.
    :param tourn: tournament to create
    :type tourn: TournamentCreate
    :param user: firebase user
    :type user: dict
    :param db: sqlite3 database connection
    :type db: sqlite3.Connection
    """
    try:
        attempt = service.create_user_tournament(tourn, user["uid"], db)
        return {"id": attempt, "message": "Successfully inserted record"}
    except RuntimeError as e:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, e)
    
@router.delete("/delete/{tournament_id}")
def api_delete_tournament(tournament_id: int, user: dict = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db)):
    """
    Delete a tournament and all associated records with this tournament.
    
    :param tournament_id: tournament ID
    :type tournament_id: int
    :param user: firebase user
    :type user: dict
    :param db: sqlite3 database
    :type db: sqlite3.Connection
    """
    try:
        return service.delete_tournament(tournament_id, user["uid"], db)
    except NotFoundError:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)