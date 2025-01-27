# app/crud/tag.py
from fastapi import HTTPException
from tortoise.query_utils import Prefetch
from app.models.models import Tag, Post
from app.schemas.tag import TagCreate, TagRead, TagUpdate
from app.schemas.post import PostRead


class CRUDTag:
    """封装标签操作的 CRUD 类"""

    @staticmethod
    async def read_tags() -> list[TagRead]:
        """读取所有标签"""
        tags = await Tag.all().prefetch_related("posts")
        return [TagRead.model_validate(tag) for tag in tags]
