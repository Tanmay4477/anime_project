from fastapi import APIRouter, Depends
from controllers.user import create_user_response, give_token
# from utils.wraper import ResponseWraper, UserSchema
from sqlmodel import Session
from db.config import get_session
from fastapi import HTTPException
from schemas.register import Register


USER_ROUTES = APIRouter()

@USER_ROUTES.post("/register")
def register_user(user: Register, session: Session = Depends(get_session)):
    try:
        print("dcbsdkj")
        response = create_user_response(user, session)
        return response
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail="Catch Error found")


@USER_ROUTES.post("/login")
def login_user_route(user: Register, session: Session = Depends(get_session)):
    try:
        value = give_token(user, session)
        return value
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail="Catch Error found")