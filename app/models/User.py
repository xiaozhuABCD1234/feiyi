# app/models/User.py
from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    UserName: str = Field(index=True, unique=True)
    password: str
    UserEmail: EmailStr = Field(index=True, unique=True)


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class UserCreate(UserBase):
    pass


class UserUpdate(SQLModel):
    UserName: str | None = None
    password: str | None = None
    UserEmail: EmailStr | None = None

