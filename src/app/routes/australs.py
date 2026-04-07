from fastapi import APIRouter, Depends, HTTPException, status, Request
import sqlite3
from app.dependencies import get_current_user
from app.database import get_db
import service
from models import TournamentCreate, NotFoundError, TabAuthError, TabBrokenError, TournamentImportModel

router = APIRouter(prefix="/api/australs", tags=["australs"])

@router.post("/import")
def import_australs(tourn_data: TournamentImportModel, request: Request, user: dict = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db)):
    """
    Import an australs tournament from tab.
    
    :param tourn_data: Data needed to fetch the tournament records
    :type tourn_data: WSDCTournamentImportModel
    :param user: firebase user
    :type user: dict
    :param db: sqlite3 database connection
    :type db: sqlite3.Connection
    """
    try:
        return service.import_australs_records(
            uid=user["uid"],
            tab_url=tourn_data.url,
            slug=tourn_data.slug,
            speaker_url=tourn_data.speaker,
            date=tourn_data.date,
            con=db, 
            request=request)
    except TabAuthError as e:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, "tab auth")
    except TabBrokenError as e:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, "tab broken")
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))