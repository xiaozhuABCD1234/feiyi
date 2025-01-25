# app/crud/post.py
from fastapi import HTTPException
from tortoise.query_utils import Prefetch
from app.models.models import Post, User
from app.schemas.post import PostCreate, PostRead, PostUpdate


async def _check_user_id_is_existing(user_id: int) -> User:
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def create_post(post_data: PostCreate) -> PostRead:
    await _check_user_id_is_existing(post_data.user_id)
    post = Post(title=post_data.title, user_id=post_data.user_id)
    await post.save()
    return post


async def read_post(post_id: int) -> PostRead:
    post = await Post.get_or_none(id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


async def read_post_by_author(author_id: int) -> list[PostRead]:
    await _check_user_id_is_existing(author_id)
    posts = await Post.filter(user_id=author_id)  # 修改为 user_id
    return [PostRead.model_validate(post) for post in posts]


async def update_post(post_id: int, post_data: PostUpdate) -> PostRead:
    post = await Post.get_or_none(id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    await post.update_from_dict(post_data.model_dump(exclude_unset=True))
    await post.save()
    return post


async def delete_post(post_id: int) -> None:
    post = await Post.get_or_none(id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    await post.delete()


class CRUDPost:
    @staticmethod
    async def create_post(post_data: PostCreate) -> PostRead:
        return await create_post(post_data)

    @staticmethod
    async def read_post_id(post_id: int) -> PostRead:
        return await read_post(post_id)

    @staticmethod
    async def read_post_author(author_id: int) -> list[PostRead]:
        return await read_post_by_author(author_id)

    @staticmethod
    async def update_post(post_id: int, post_data: PostUpdate) -> PostRead:
        return await update_post(post_id, post_data)

    @staticmethod
    async def delete_post(post_id: int) -> None:
        return await delete_post(post_id)
