# app/schemas/user.py
from pydantic import BaseModel, EmailStr
from typing import Optional


# 用户注册时的请求模型
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


# 用户更新时的请求模型
class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


# 用户读取时的响应模型
class UserRead(BaseModel):
    id: int
    name: str
    email: EmailStr


class UserLogin(BaseModel):
    email: EmailStr
    password: str
