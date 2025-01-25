# app/routers/post.py
from fastapi import APIRouter, Depends, HTTPException
from app.crud.post import CRUDPost
from app.schemas.post import PostCreate, PostRead, PostUpdate

router = APIRouter()


@router.post("/posts/", response_model=PostRead)
async def create_post(post_data: PostCreate):
    return await CRUDPost.create_post(post_data)


@router.get("/posts/{post_id}", response_model=PostRead)
async def read_post(post_id: int):
    return await CRUDPost.read_post(post_id)


@router.get("/posts/author/{author_id}", response_model=list[PostRead])
async def read_post_author(author_id: int):
    return await CRUDPost.read_post_author(author_id)


@router.put("/posts/{post_id}", response_model=PostRead)
async def update_post(post_id: int, post_data: PostUpdate):
    return await CRUDPost.update_post(post_id, post_data)


@router.delete("/posts/{post_id}", status_code=204)
async def delete_post(post_id: int):
    return await CRUDPost.delete_post(post_id)
