from fastapi import APIRouter, Depends
from schemas.query import SearchRequest
from sqlmodel import Session
from db.config import get_session
from fastapi import HTTPException
from controllers.anime import *
from utils.auth import auth_wrapper

ANIME_ROUTES = APIRouter()

@ANIME_ROUTES.post("/search")
async def search_route(search: SearchRequest):
    try:
        response = await search_controller(search)
        return response
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail="Catch Error found")
    
@ANIME_ROUTES.post("/recommendations")
def get_recommendation_route(session: Session = Depends(get_session), payload = Depends(auth_wrapper)):
    try:
        print("fvndfvj")
        response = get_recommendation(session, payload)
        return response
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail="Catch Error found")


