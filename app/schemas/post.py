from pydantic import BaseModel, field_validator
from typing import Optional, List
from datetime import datetime
from tortoise.queryset import QuerySet
from tortoise.fields import ManyToManyRelation

class PostBase(BaseModel):
    title: str
    user_id: Optional[int] = None  # 使用 user_id 与模型定义一致


class PostCreate(PostBase):
    user_id: int  # 必须字段
    content: str
    tags: Optional[List[str]] = None  # 新增 tags 字段，假设 tags 是字符串列表


class PostReadBase(PostBase):
    id: int
    created_at: datetime
    updated_at: datetime
    user_id: int
    likes_count: int
    favorites_count: int
    tags: Optional[List[str]] = []

    class Config:
        from_attributes = True

    @field_validator("tags", mode="before")
    def convert_tags(cls, v):
        if v is None:
            return []
        if isinstance(v, list):
            return v
        # 如果 v 是 ManyToManyRelation，提取帖子 ID
        return [tag.name for tag in v]

class PostRead(PostReadBase):
    summary: str = ""


class PostReadComplete(PostReadBase):
    content: str


class PostUpdate(PostBase):
    title: Optional[str] = None
    summary: str | None = None
    updated_at: Optional[datetime] = None
    user_id: Optional[int] = None  # 如果允许更新 user_id，保留 Optional
    tags: Optional[List[str]] = None  # 新增 tags 字段，假设 tags 是字符串列表
