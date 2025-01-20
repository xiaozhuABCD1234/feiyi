# app/models/User.py
from pydantic import EmailStr
from sqlmodel import Field, SQLModel, Relationship
from typing import List
from datetime import datetime, timezone


class UserBase(SQLModel):
    name: str = Field(index=True, unique=True, description="用户名")
    email: EmailStr = Field(index=True, unique=True, description="用户邮箱")


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True, description="用户ID")
    password: str = Field(description="哈系加密后的密码")
    posts: List["Post"] = Relationship(
        back_populates="author", description="用户创建的页面列表"
    )


class UserCreate(UserBase):
    password: str = Field(description="用户密码")


class UserRead(UserBase):
    id: int = Field(description="用户ID")


class UserUpdate(UserBase):
    name: str | None = None
    password: str | None = None
    email: EmailStr | None = None


class PostBase(SQLModel):
    title: str = Field(index=True, description="帖子标题")
    content: str = Field(description="帖子内容")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), description="创建时间"
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), description="更新时间"
    )


class Post(PostBase, table=True):
    id: int | None = Field(index=True, primary_key=True, description="文章ID")
    author_id: int = Field(foreign_key="user.id", description="作者ID")
    author: User = Relationship(back_populates="posts", description="帖子作者")


class PostRead(PostBase):
    id: int = Field(description="文章ID")
    author_id: int = Field(description="作者ID")
    author: User = Field(description="帖子作者")


class PostCreate(PostBase):
    id: int | None = Field(description="文章ID")
    author_id: int = Field(description="作者ID")
    author: UserRead = Field(description="帖子作者")


class PostUpdate(PostBase):
    title: str | None = None
    content: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
