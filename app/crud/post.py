# app/crud/post.py
from fastapi import HTTPException, status
from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime, timedelta, timezone
from app.models.models import Post
from app.schemas.post import PostCreate, PostRead, PostUpdate
from app.database.db import SessionDep


async def create_post(post_data: PostCreate, db: SessionDep):
    new_post = Post.model_validate(post_data)
    new_post.created_at = datetime.now(timezone.utc)
    new_post.updated_at = datetime.now(timezone.utc)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


async def read_post_user_id(user_id: int, db: SessionDep) -> List[PostRead]:
    posts = db.exec(select(Post).where(Post.author_id == user_id)).all()
    if not posts:
        raise HTTPException(status_code=404, detail="Posts not found")
    return posts


async def read_post_all(
    db: SessionDep, skip: Optional[int] = 0, limit: Optional[int] = 100
):
    posts = db.exec(select(Post).offset(skip).limit(limit)).all()
    return posts


async def read_post_id(post_id: int, db: SessionDep) -> PostRead:
    post = db.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


async def update_post(post_id: int, post_data: PostUpdate, db: SessionDep):
    post_db = db.get(Post, post_id)
    if not post_db:
        raise HTTPException(status_code=404, detail="Post not found")
    post_data_dict = post_data.model_dump(exclude_unset=True)
    for key, value in post_data_dict.items():
        setattr(post_db, key, value)
    db.commit()
    db.refresh(post_db)
    return post_db


async def delete_post(post_id: int, db: SessionDep):
    post = db.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return None


class CRUDPost:
    create_post = create_post
    read_post_user_id = read_post_user_id
    read_post_all = read_post_all
    read_post_id = read_post_id
    update_post = update_post
    delete_post = delete_post
