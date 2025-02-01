# app/crud/like_favorite.py
from fastapi import HTTPException
from typing import List
from app.models.models import User, Post
from app.schemas.post import PostRead


async def get_liked_posts_by_user(user_id: int) -> List[PostRead]:
    try:
        # 查询用户及其点赞的帖子
        user = await User.get(id=user_id).prefetch_related("liked_posts")
    except User.DoesNotExist:
        # 如果用户不存在，抛出 404 错误
        raise HTTPException(status_code=404, detail="User not found")

    # 将帖子对象序列化为 PostRead 模型
    liked_posts = [PostRead.from_orm(post) for post in user.liked_posts]
    return liked_posts