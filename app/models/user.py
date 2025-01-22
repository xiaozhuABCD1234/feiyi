# app/models/user.py
from sqlmodel import Field, SQLModel
from pydantic import EmailStr


class UserBase(SQLModel):
    name: str = Field(index=True, unique=True, description="用户名")
    email: EmailStr = Field(index=True, unique=True, description="用户邮箱")


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True, description="用户ID")
    password: str = Field(description="哈系加密后的密码")


class UserCreate(UserBase):
    password: str = Field(description="用户密码")


class UserRead(UserBase):
    id: int = Field(description="用户ID")


class UserUpdate(SQLModel):
    name: str | None = None
    password: str | None = None
    email: EmailStr | None = None
