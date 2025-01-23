from __future__ import annotations
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from datetime import datetime, timezone
from pydantic import HttpUrl
# from app.models.user import User, UserRead


class PostBase(SQLModel):
    title: str = Field(description="帖子标题")
    content: str = Field(description="帖子内容")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), description="创建时间"
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), description="更新时间"
    )

    # 外键关联用户
    user_id: int = Field(foreign_key="user.id", description="作者ID")


class Post(PostBase, table=True):
    id: int | None = Field(default=None, primary_key=True, description="帖子ID")

    # # 关联用户
    # author: User = Relationship(back_populates="posts")


class PostCreate(PostBase):
    pass


class PostRead(PostBase):
    id: int = Field(description="帖子ID")
    # author: "UserRead"


class PostUpdate(SQLModel):
    title: str | None = None
    content: str | None = None
    updated_at: datetime | None = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
