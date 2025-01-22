# app/schemas/user.py
from pydantic import BaseModel, EmailStr
from typing import Optional


# 用户注册时的请求模型
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "name": "JohnDoe",
                "email": "johndoe@example.com",
                "password": "password123",
            }
        }


# 用户更新时的请求模型
class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "JohnDoe",
                "email": "johndoe@example.com",
                "password": "newpassword",
            }
        }


# 用户读取时的响应模型
class UserRead(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True  # 允许 Pydantic 模型与 SQLAlchemy 模型交互
        schema_extra = {
            "example": {
                "id": 1, 
                "name": "JohnDoe",
                "email": "johndoe@example.com"
            }
        }
