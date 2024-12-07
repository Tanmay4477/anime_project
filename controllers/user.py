from sqlmodel import Session, select
# from utils.wraper import ResponseWraper, UserSchema, LoginUserSchema
# from utils.status_code import Http, Message
from models.user import User
# from utils.auth import auth_wrapper, get_password_hash, verify_password, encode_token, decode_token
from fastapi import HTTPException
from schemas.register import Register
from utils.auth import get_password_hash, verify_password, encode_token
from schemas.response import ResponseWraper

def create_user_response(user: Register, session: Session):
    try:
        result = select(User).where(User.username == user.username)
        statement = session.exec(result).first()

        if statement:
            raise HTTPException(status_code=400, detail="Already exist")
        hashed_password = get_password_hash(user.password)
        
        db_user = User(username=user.username, password=hashed_password, genres=[])
        db_user.password = hashed_password
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        print(db_user, "svcdhv")
        return ResponseWraper(status=200, message="Signup Successful", data="SUCCESS")
    except HTTPException as http_err:
        raise http_err
    except Exception as error:
        print(error)
        raise HTTPException(status_code=500, detail="Catch Error found")
    

def give_token(user: Register, session: Session):
    try:
        statement = select(User).where(User.username == user.username)
        result = session.exec(statement).first()
        if not result:
            raise HTTPException(status_code=403, detail="User not exist")
        verify_pass = verify_password(user.password, result.password)
        if not verify_pass:
            raise HTTPException(status_code=400, detail="Username or password is incorrect")
        token = encode_token(result.id)
        return ResponseWraper(status=200, message="LOGIN SUCCESSFUL", data=token)
    except HTTPException as http_err:
        raise http_err
    except Exception as error:
        raise HTTPException(status_code=500, detail="Catch Error found")
