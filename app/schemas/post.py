from pydantic import BaseModel, field_validator
from typing import Optional, List
from datetime import datetime


class PostBase(BaseModel):
    title: str
    user_id: Optional[int] = None  # 使用 user_id 与模型定义一致


class PostCreate(PostBase):
    user_id: int  # 必须字段
    tags: Optional[List[str]] = None  # 新增 tags 字段，假设 tags 是字符串列表


class PostRead(PostBase):
    id: int
    created_at: datetime
    updated_at: datetime
    user_id: int  # 使用 user_id 与模型定义一致
    likes_count: int
    favorites_count: int
    tags: Optional[List[str]] = []  # 添加 tags 字段

    class Config:
        from_attributes = True

    @field_validator("tags", mode="before")
    def convert_tags(cls, v):
        if v is None:
            return []
        if isinstance(v, list):
            return v
        # 如果 v 是 ManyToManyRelation，提取标签名称
        return [tag.name for tag in v]


class PostUpdate(PostBase):
    title: Optional[str] = None
    updated_at: Optional[datetime] = None
    user_id: Optional[int] = None  # 如果允许更新 user_id，保留 Optional
    tags: Optional[List[str]] = None  # 新增 tags 字段，假设 tags 是字符串列表
