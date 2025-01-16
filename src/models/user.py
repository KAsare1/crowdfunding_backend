from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Optional



class UserBase(BaseModel):
    username: str = Field(..., max_length=50)
    email: EmailStr
    full_name: Optional[str] = None



class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserResponse(UserBase):
    id: str
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str



class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    id: str 
