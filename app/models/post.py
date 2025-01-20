# app/models/post.py
from __future__ import annotations
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime, timezone
from .user import User, UserRead  # 导入 User 模型


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
    author: User = Relationship(back_populates="posts")


class PostRead(PostBase):
    id: int = Field(description="文章ID")
    author_id: int = Field(description="作者ID")
    author: UserRead = Field(description="帖子作者")


class PostCreate(SQLModel):
    title: str = Field(description="帖子标题")
    content: str = Field(description="帖子内容")
    author_id: int = Field(description="作者ID")


class PostUpdate(SQLModel):
    title: str | None = None
    content: str | None = None
