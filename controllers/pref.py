from sqlmodel import Session, select
# from utils.wraper import ResponseWraper, UserSchema, LoginUserSchema
# from utils.status_code import Http, Message
from models.user import User
# from utils.auth import auth_wrapper, get_password_hash, verify_password, encode_token, decode_token
from schemas.response import ResponseWraper
from fastapi import HTTPException
from schemas.pref import Genres

async def set_preferences(genres: Genres, session: Session, payload) -> ResponseWraper:
    try:
        id = payload['id']
        user = session.exec(select(User).where(User.id == id)).first()
        if not user:
            raise HTTPException(status_code=400, detail="User not found")
        user.genres = genres.genres
        session.add(user)
        session.commit()
        session.refresh(user)
        return ResponseWraper(status=200, message="Preference updated successfully", data="SUCCESS")
    except HTTPException as http_err:
        raise http_err
    except Exception as error:
        print(error)
        raise HTTPException(status_code=500, detail="Catch Error found")