# app/schemas/comment.py
from pydantic import BaseModel
from datetime import datetime


class CommentBase(BaseModel):
    text: str


class CommentCreate(CommentBase):
    user_id: int
    post_id: int


class CommentRead(CommentBase):
    id: int
    user_id: int
    post_id: int
    time: datetime
    likes_count: int


class CommentUpdate(BaseModel):
    text: str | None = None
