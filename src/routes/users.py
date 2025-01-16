from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from src.db.users import User
from src.db.db import get_db
from src.models.user import UserCreate, UserResponse, Token
from src.core.config import settings
from src.utils.oauth2 import create_access_token, get_current_user, verify_token, create_refresh_token

# Constants
SECRET_KEY = settings.SECRET_KEY  # Replace with a secure key
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_EXPIRES

# Dependencies
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


# Helper functions
def password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    hashed_password = password_hash(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        full_name=user.full_name,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()  # `username` holds email in form data
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user.id})
    refresh_token = create_refresh_token(data={"sub": user.id})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer",
    }



@router.get("/me", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user



# Necessary endpoint for refresh token which could expire
@router.post("/refresh_token", response_model=Token)
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    try:
        payload = verify_token(refresh_token)
        id = payload.get("sub")

        db_user = db.query(User).filter(User.id == id).first()
        if db_user is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        new_access_token = create_access_token(data={"sub": id})
        return {"access_token": new_access_token, "token_type": "bearer", "refresh_token": refresh_token}
    except HTTPException:
        raise HTTPException(status_code=401, detail="Invalid refresh token")