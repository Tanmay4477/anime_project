from fastapi import Security, HTTPException
import jwt
from passlib.context import CryptContext
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from datetime import datetime, timedelta, timezone

security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
secret = "this_is_a_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRY_MINUTES = 30

def get_password_hash(password):
        return pwd_context.hash(password)
    
def verify_password(plain_password, hash_password):
        return pwd_context.verify(plain_password, hash_password)
    
def encode_token(jwt_id):
        payload = {
            'id': jwt_id,
            'iat': datetime.now(timezone.utc),
            'exp': datetime.now(timezone.utc) + timedelta(days=10, minutes=15)      
        }
        encoded_jwt = jwt.encode(payload, secret, algorithm=ALGORITHM)
        return encoded_jwt
    
def decode_token(token):
    try:
        payload = jwt.decode(token, secret, algorithms=ALGORITHM)
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
        
def auth_wrapper(auth: HTTPAuthorizationCredentials = Security(security)):
    return decode_token(auth.credentials) 
#  credentials come from the library as it removes bearer which is the first part and the second part is the token

