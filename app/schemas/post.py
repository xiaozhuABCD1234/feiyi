# app/schemas/post.py
from pydantic import BaseModel
from typing import Optional, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from .user import UserRead


class PostBase(BaseModel):
    title: str


class PostCreate(PostBase):
    author_id: int


class PostRead(PostBase):
    id: int
    created_at: datetime
    updated_at: datetime
    author_id: int

    class Config:
        orm_mode = True


class PostUpdate(PostBase):
    title: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
