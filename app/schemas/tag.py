from pydantic import BaseModel, field_validator, Field
from typing import List, Optional
from datetime import datetime


class TagRead(BaseModel):
    id: int
    name: str
    posts: Optional[List[int]] = None

    class Config:
        from_attributes = True  # 支持从 ORM 对象加载数据

    @field_validator("posts", mode="before")
    def convert_posts(cls, v):
        if v is None:
            return []
        if isinstance(v, list):
            return v
        # 如果 v 是 ManyToManyRelation，提取帖子 ID
        return [post.name for post in v]

class TagBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="标签名称")


class TagCreate(TagBase):
    posts: Optional[List[int]] = Field(None, description="与标签关联的帖子 ID 列表")


class TagUpdate(BaseModel):
    name: Optional[str] = Field(
        None, min_length=1, max_length=50, description="标签名称"
    )
    posts: Optional[List[int]] = Field(None, description="与标签关联的帖子 ID 列表")
