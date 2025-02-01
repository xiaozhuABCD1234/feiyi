# app/schemas/user.py
from sqlmodel import Field, SQLModel, Relationship
from pydantic import BaseModel, EmailStr
from typing import List, Optional


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserRead(BaseModel):
    id: int
    name: str
    email: str
    permissions: str

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    name: Optional[str] = None
    password: Optional[str] = None
    email: Optional[EmailStr] = None
    permissions: str | None = None

    class Config:
        from_attributes = True
