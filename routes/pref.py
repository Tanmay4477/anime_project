from fastapi import APIRouter, Depends
from schemas.pref import Genres
from sqlmodel import Session
from db.config import get_session
from fastapi import HTTPException
from controllers.pref import *
from utils.auth import auth_wrapper

PREF_ROUTES = APIRouter()

@PREF_ROUTES.post("/preferences")
async def set_preferences_route(genres: Genres, session: Session = Depends(get_session), payload = Depends(auth_wrapper)):
    try:
        response = await set_preferences(genres, session, payload)
        return response
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail="Catch Error found")
    
