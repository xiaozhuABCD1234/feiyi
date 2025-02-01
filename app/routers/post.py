# app/routers/post.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List
import markdown
from bs4 import BeautifulSoup
from app.crud.post import CRUDPost
from app.schemas.post import PostCreate, PostRead, PostUpdate
from app.core.security import Security

router = APIRouter()


async def get_summary(content: str) -> str:
    html = markdown.markdown(content)
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator=" ")
    summary = text[:100].strip()
    if len(text) > 100:
        summary += "..."
    return summary


@router.post("/", response_model=PostRead)
async def create_post(post_data: PostCreate):
    content = post_data.content
    summary = await get_summary(content)
    return await CRUDPost.create_post(post_data, summary)


@router.get("/{post_id}", response_model=PostRead)
async def read_post(post_id: int):
    return await CRUDPost.read_post(post_id)


@router.get("/author/{author_id}", response_model=List[PostRead])
async def read_post_author(author_id: int):
    return await CRUDPost.read_post_by_author(author_id)


@router.put("/{post_id}", response_model=PostRead)
async def update_post(post_id: int, post_data: PostUpdate):
    content = post_data.summary
    post_data.summary = await get_summary(content)
    return await CRUDPost.update_post(post_id, post_data)


@router.delete("/{post_id}", status_code=204)
async def delete_post(post_id: int):
    return await CRUDPost.delete_post(post_id)


@router.get("/", response_model=list[PostRead])
async def read_post_all():
    return await CRUDPost.read_post_all()
