# app/routers/tag.py
from fastapi import APIRouter, HTTPException
from typing import List
from app.crud.tag import CRUDTag
from app.crud.post import CRUDPost
from app.schemas.tag import TagCreate, TagRead, TagUpdate
from app.schemas.post import PostRead

router = APIRouter()


@router.get("/", response_model=List[TagRead])
async def read_tags():
    return await CRUDTag.read_tags()


@router.get("/{tag_id}", response_model=List[PostRead])
async def read_post_tag(tag_id: int):
    return await CRUDPost.read_post_by_tag(tag_id)
