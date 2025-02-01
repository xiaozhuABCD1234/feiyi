from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.crud.comment import CRUDComment
from app.models.models import User, Comment
from app.schemas.comment import CommentRead, CommentCreate, CommentUpdate


router = APIRouter()


@router.post(
    "/",
    response_model=CommentRead,
    status_code=status.HTTP_201_CREATED,
    summary="创建评论",
    description="创建一个新的评论。需要提供评论内容、关联的文章ID以及用户ID。",
)
async def create_comment(comment_data: CommentCreate):
    return await CRUDComment.create_comment(comment_data)


@router.get(
    "/{post_id}",
    response_model=List[CommentRead],
    summary="获取文章评论",
    description="根据文章ID获取该文章下的所有评论。支持分页查询。",
)
async def read_comment_by_post(post_id: int, skip: int = 0, limit: int = 10):
    return await CRUDComment.read_comment_by_post(post_id, skip, limit)


@router.put(
    "/{comment_id}",
    response_model=CommentRead,
    summary="更新评论",
    description="根据评论ID更新评论内容。需要提供新的评论内容。",
)
async def update_comment(comment_id: int, comment_data: CommentUpdate):
    return await CRUDComment.update_comment(comment_id, comment_data)


@router.delete(
    "/{comment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="删除评论",
    description="根据评论ID删除一条评论。",
)
async def delete_comment(comment_id: int):
    return await CRUDComment.delete_comment(comment_id)


@router.put(
    "/{comment_id}/like",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="点赞评论",
    description="根据评论ID和用户ID为某条评论点赞。",
)
async def like_comment(comment_id: int, user_id: int):
    return await CRUDComment.like_comment(comment_id, user_id)
