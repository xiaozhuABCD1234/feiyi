# app/routers/tag.py
from fastapi import APIRouter, HTTPException
from typing import List
from app.crud.tag import CRUDTag
from app.schemas.tag import TagCreate, TagRead, TagUpdate

router = APIRouter()


@router.get("/", response_model=List[TagRead])
async def read_tags():
    return await CRUDTag.read_tags()
