from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from src.core.config import settings
from src.db.db import get_db
from src.db.users import User
from src.models.user import TokenData

oauth2_schema = OAuth2PasswordBearer(tokenUrl="users/login")

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = int(settings.ACCESS_EXPIRES)
REFRESH_TOKEN_EXPIRE_DAYS = int(settings.REFRESH_EXPIRES)


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)



def create_access_token(data: dict) -> str:
    """
    Generate an access token with an expiration time.
    """
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict) -> str:
    """
    Generate a refresh token with an expiration time.
    """
    expire = datetime.now() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)



def verify_token(token: str) -> dict:
    """
    Verify the token and return the payload.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    

def verify_access_token(token: str, credentials_exception: HTTPException = credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("sub")
        if not id:
            raise credentials_exception
        token_data = TokenData(id=str(id))
    except JWTError:
        raise credentials_exception
    return token_data



def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)) -> User:
    token_data = verify_access_token(token)
    user_id = token_data.id
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user