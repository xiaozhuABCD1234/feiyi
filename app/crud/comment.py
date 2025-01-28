# app/crud/comment.py
from fastapi import HTTPException
from tortoise.query_utils import Prefetch
from app.models.models import Post, User, Comment
from app.schemas.comment import CommentRead, CommentCreate, CommentUpdate
from tortoise.transactions import in_transaction


async def check_liked(comment_id: int, user_id) -> bool:
    comment = await Comment.get_or_none(id=comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return await comment.liked_by.filter(id=user_id).exists()


async def create_comment(comment_data: CommentCreate):
    comment = Comment(
        text=comment_data.text,
        post_id=comment_data.post_id,
        user_id=comment_data.user_id,
        likes_count=0,
    )
    await comment.save()
    comment_dict = comment.__dict__
    return CommentRead.model_validate(comment_dict)


async def read_comment_by_post(post_id: int, skip: int = 0, limit: int = 10):
    # 查询某个帖子的评论（支持分页）
    comments = await Comment.filter(post_id=post_id).offset(skip).limit(limit).all()
    if not comments:
        raise HTTPException(status_code=404, detail="No comments found for this post")
    return [CommentRead.model_validate(comment.__dict__) for comment in comments]


async def update_comment(comment_id: int, comment_data: CommentUpdate):
    # 更新评论
    comment = await Comment.get_or_none(id=comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    # 更新字段
    if comment_data.text is not None:
        comment.text = comment_data.text

    await comment.save()  # 保存更新
    return CommentRead.model_validate(comment.__dict__)


async def delete_comment(comment_id: int):
    # 删除评论
    comment = await Comment.get_or_none(id=comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    await comment.delete()
    return {"message": "Comment deleted successfully"}


async def like_comment(comment_id: int, user_id: int):
    async with in_transaction():
        comment = await Comment.get_or_none(id=comment_id)
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")

        user = await User.get_or_none(id=user_id)  # 查询 User 实例
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        has_liked = await check_liked(comment_id, user_id)
        if has_liked:
            # 取消点赞
            comment.likes_count -= 1
            await comment.liked_by.remove(user)  # 传递 User 实例
        else:
            # 点赞
            comment.likes_count += 1
            await comment.liked_by.add(user)  # 传递 User 实例

        await comment.save()
        return comment.likes_count


class CRUDComment:
    create_comment = create_comment
    read_comment_by_post = read_comment_by_post
    update_comment = update_comment
    delete_comment = delete_comment
    like_comment = like_comment
