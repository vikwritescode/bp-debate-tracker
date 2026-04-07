from fastapi import APIRouter, Depends, HTTPException, status, Request
import sqlite3
from app.dependencies import get_current_user
from app.database import get_db
import service
from models import StartNotFoundError, TabAuthError, TabBrokenError, TournamentImportModel, NotFoundError

router = APIRouter(prefix="/api/tab", tags=["tab"])


@router.get("/tournaments")
def api_get_tab_tournaments(url: str, user: dict = Depends(get_current_user)):
    """
    get tournaments that exist on a tab
    
    :param url: Tab URL
    :type url: str
    :param user: firebase user
    :type user: dict
    """
    try:
        return service.get_tournaments(url)
    except TabAuthError as e:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, "tab auth")
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

@router.get("/speakers")
def api_get_names(url: str, slug: str, speaker: str, user: dict = Depends(get_current_user)):
    """
    Get list of speakers in a tournament that match a slug
    
    :param url: tab URL
    :type url: str
    :param slug: tournament slug
    :type slug: str
    :param speaker: speaker name (must be "in" their name on tab)
    :type speaker: str
    :param user: firebase user
    :type user: dict
    """
    try:
        return service.get_speaker(url, slug, speaker)
    except TabAuthError as e:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, "tab auth")
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/startdate")
def api_get_startdate(url: str, slug: str, user: dict = Depends(get_current_user)):
    """
    get start date for tournament
    
    :param url: tab URL
    :type url: str
    :param slug: tournament slug
    :type slug: str
    :param user: firebase user
    :type user: dict
    """
    try:
        return service.get_start_date(url, slug)
    except TabAuthError as e:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail="tab auth")
    except StartNotFoundError as e:
        raise HTTPException(status.HTTP_417_EXPECTATION_FAILED, detail="Could not find start time")

@router.post("/import")
def api_import_from_url(tourn_data: TournamentImportModel, request: Request, user: dict = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db)):
    """
    Docstring for api_import_from_url
    
    :param tourn_data: Data needed to fetch the tournament records
    :type tourn_data: TournamentImportModel
    :param user: firebase user
    :type user: dict
    :param db: sqlite3 connection
    :type db: sqlite3.Connection
    """
    try:
        return service.import_records(
            user["uid"],
            tourn_data.url,
            tourn_data.slug,
            tourn_data.speaker,
            tourn_data.date,
            db, 
            request)
    except TabAuthError as e:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, "tab auth")
    except TabBrokenError as e:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, "tab broken")
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("refresh/{tournament_id}")
def refresh_tournament(tournament_id: int, request: Request, user: dict = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db)):
    """
    Refresh a tournament's data from tab.

    :param tournament_id: tournament ID
    :type tournament_id: int
    :param request: request object
    :type request: Request
    :param user: firebase user
    :type user: dict
    :param db: sqlite3 database connection
    :type db: sqlite3.Connection
    """
    try:
        return service.refresh_tournament(tournament_id=tournament_id, uid=user["uid"], con=db, request=request)
    except TabAuthError as e:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, "tab auth")
    except TabBrokenError as e:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, "tab broken")
    except NotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "tournament not found")
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))