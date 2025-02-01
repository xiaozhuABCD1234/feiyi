# app/crud/post.py
from fastapi import HTTPException
from tortoise.query_utils import Prefetch
from app.models.models import Post, User, Tag
from app.schemas.post import PostCreate, PostRead, PostUpdate


async def _check_user_id_is_existing(user_id: int) -> User:
    # 检查用户是否存在，如果不存在则抛出 404 错误
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


class CRUDPost:
    @staticmethod
    async def get_likes_count(post_id) -> int:
        post = await Post.get(id=post_id).prefetch_related("likes")
        return await post.likes.all().count()

    @staticmethod
    async def get_favorites_count(post_id) -> int:
        post = await Post.get(id=post_id).prefetch_related("favorites")
        return await post.favorites.all().count()

    @staticmethod
    async def create_post(post_data: PostCreate, summary: str) -> PostRead:
        """创建帖子，如果标题重复则自动添加数字编号"""
        title = post_data.title
        count = 0
        while await Post.get_or_none(title=title):
            count += 1
            title = f"{post_data.title} ({count})"
        post_data.title = title

        post = Post(
            title=post_data.title,
            user_id=post_data.user_id,
            likes_conut=0,
            favorites_count=0,
            summary=summary,
        )
        await post.save()

        # 处理 tags
        if post_data.tags is not None:
            tags = []
            for tag_name in post_data.tags:
                tag, _ = await Tag.get_or_create(name=tag_name)
                tags.append(tag)

            # 添加 tags 到帖子
            await post.tags.add(*tags)

        # 预加载 tags 以便在 PostRead 中使用
        await post.fetch_related("tags")

        return PostRead.model_validate(post)

    @staticmethod
    async def read_post(post_id: int) -> PostRead:
        # 根据帖子 ID 读取帖子
        post = await Post.get_or_none(id=post_id).prefetch_related("tags")
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        return PostRead.model_validate(post)  # 使用 model_validate 替代 dict(post)

    @staticmethod
    async def read_post_by_author(author_id: int) -> list[PostRead]:
        # 根据作者 ID 读取帖子列表
        await _check_user_id_is_existing(author_id)
        posts = await Post.filter(user_id=author_id).prefetch_related("tags")
        return [
            PostRead.model_validate(post) for post in posts
        ]  # 使用 model_validate 替代 dict(post)

    @staticmethod
    async def update_post(post_id: int, post_data: PostUpdate) -> PostRead:
        # 更新帖子内容
        post = await Post.get_or_none(id=post_id).prefetch_related(
            "tags"
        )  # 预加载 tags
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        # 更新普通字段
        update_data = post_data.model_dump(exclude_unset=True, exclude={"tags"})
        await post.update_from_dict(update_data)
        await post.save()

        # 更新 tags
        if post_data.tags is not None:
            tags = []
            for tag_name in post_data.tags:
                tag, _ = await Tag.get_or_create(name=tag_name)
                tags.append(tag)

            # 清除旧的 tags 并添加新的 tags
            await post.tags.clear()
            await post.tags.add(*tags)

        # 预加载 tags 以便在 PostRead 中使用
        await post.fetch_related("tags")
        post.tags = [tag.name for tag in post.tags]
        return PostRead.model_validate(post)

    @staticmethod
    async def delete_post(post_id: int) -> None:
        # 根据帖子 ID 删除帖子
        post = await Post.get_or_none(id=post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        await post.delete()

    @staticmethod
    async def read_post_all() -> list[PostRead]:
        # 读取所有帖子
        posts = await Post.all().prefetch_related("tags")
        return [
            PostRead.model_validate(post) for post in posts
        ]  # 使用 model_validate 替代 dict(post)

    @staticmethod
    async def read_post_by_tag(tag_id: int) -> list[PostRead]:
        # 根据标签 ID 读取帖子列表
        tag = await Tag.get_or_none(id=tag_id)
        if not tag:
            raise HTTPException(status_code=404, detail="Tag not found")
        posts = await tag.posts.all().prefetch_related("tags")
        return [PostRead.model_validate(post) for post in posts]

    @staticmethod
    async def like_post(post_id: int, user_id: int) -> int:
        # 点赞帖子
        post = await Post.get_or_none(id=post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        user = await User.get_or_none(id=user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if await post.likes.filter(id=user_id).exists():
            post.likes_count -= 1
            post.likes.remove(user)
        else:
            post.likes_count += 1
            post.likes.add(user)
        await post.save()
        return post.likes_count

    @staticmethod
    async def favorite_post(post_id: int, user_id: int) -> int:
        # 收藏帖子
        post = await Post.get_or_none(id=post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        user = await User.get_or_none(id=user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if await post.favorites.filter(id=user_id).exists():
            post.favorites_count -= 1
            post.favorites.remove(user)
        else:
            post.favorites_count += 1
            post.favorites.add(user)
        await post.save()
        return post.favorites_count
