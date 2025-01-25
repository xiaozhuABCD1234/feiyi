# app/models/models.py
from sqlmodel import Field, SQLModel, Relationship
from pydantic import EmailStr
from typing import List, Optional
from datetime import datetime, timedelta, timezone


def get_utcnow():
    return datetime.now(timezone.utc)


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, description="用户ID")
    name: str = Field(index=True, unique=True, description="用户名")
    email: EmailStr = Field(index=True, unique=True, description="用户邮箱")
    password: str = Field(description="哈希加密后的密码")
    posts: List["Post"] = Relationship(back_populates="author")


class Post(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, description="文章ID")
    title: str = Field(index=True, description="文章标题")
    created_at: datetime = Field(default=get_utcnow(), description="创建时间")
    updated_at: datetime = Field(default=get_utcnow(), description="更新时间")
    author_id: int = Field(index=True, foreign_key="user.id", description="作者ID")
    author: Optional[User] = Relationship(back_populates="posts")
