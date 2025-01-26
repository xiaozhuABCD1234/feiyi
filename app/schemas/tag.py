# app/schemas/tag.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TagBase(BaseModel):
    name: str


class TagCreate(TagBase):
    posts: Optional[list[int]] = None
    pass


class TagRead(TagBase):
    id: int
    posts: Optional[list[int]] = None
    pass


class TagUpdate(TagBase):
    name: Optional[str] = None
    posts: Optional[list[int]] = None
    pass
