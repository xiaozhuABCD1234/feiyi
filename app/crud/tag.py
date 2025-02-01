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

    @staticmethod
    async def update_tag(tag_data: TagUpdate, tag_id: int) -> TagRead:
        tag = await Tag.get_or_none(id=tag_id)
        if not tag:
            raise HTTPException(status_code=404, detail="Tag not found")
        update_data = tag_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(tag, key, value)

        await tag.save()
        return TagRead.model_validate(tag)

    @staticmethod
    async def delete_tag(tag_id: int) -> None:
        """删除标签"""
        tag = await Tag.get_or_none(id=tag_id)
        if not tag:
            raise HTTPException(status_code=404, detail="标签未找到")
        await tag.delete()
