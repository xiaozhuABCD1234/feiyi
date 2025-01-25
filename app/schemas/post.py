# app/schemas/post.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PostBase(BaseModel):
    title: str
    user_id: Optional[int] = None  # 使用 user_id 与模型定义一致


class PostCreate(PostBase):
    user_id: int  # 必须字段


class PostRead(PostBase):
    id: int
    created_at: datetime
    updated_at: datetime
    user_id: int  # 使用 user_id 与模型定义一致


class PostUpdate(PostBase):
    title: Optional[str] = None
    updated_at: Optional[datetime] = None
    user_id: Optional[int] = None  # 如果允许更新 user_id，保留 Optional