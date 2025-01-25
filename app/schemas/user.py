# app/schemas/user.py
from sqlmodel import Field, SQLModel, Relationship
from pydantic import BaseModel, EmailStr
from typing import List, Optional


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    name: Optional[str] = None
    password: Optional[str] = None
    email: Optional[EmailStr] = None

    class Config:
        orm_mode = True
