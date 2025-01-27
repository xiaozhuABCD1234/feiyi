from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.crud.comment import CRUDComment
from app.models.models import User, Comment
from app.schemas.comment import CommentRead, CommentCreate, CommentUpdate


router = APIRouter()


@router.post("/", response_model=CommentRead, status_code=status.HTTP_201_CREATED)
async def create_comment(comment_data: CommentCreate):
    return await CRUDComment.create_comment(comment_data)


@router.get("/{post_id}", response_model=List[CommentRead])
async def read_comment_by_post(post_id: int, skip: int = 0, limit: int = 10):
    return await CRUDComment.read_comment_by_post(post_id, skip, limit)


@router.put("/{comment_id}", response_model=CommentRead)
async def update_comment(comment_id: int, comment_data: CommentUpdate):
    return await CRUDComment.update_comment(comment_id, comment_data)


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(comment_id: int):
    return await CRUDComment.delete_comment(comment_id)


@router.post("/{comment_id}/like", status_code=status.HTTP_204_NO_CONTENT)
async def like_comment(comment_id: int, user_id: int):
    return await CRUDComment.like_comment(comment_id, user_id)
