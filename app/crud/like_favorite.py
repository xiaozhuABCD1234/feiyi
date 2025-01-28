# # app/crud/like_favorite.py
# from fastapi import HTTPException
# from typing import List
# from app.models.models import User, Post
# from app.schemas.post import PostRead

# async def get_user_likes_lsit(user_id: int) -> List[PostRead]:
#     user = await User.get_or_none(id=user_id)
#     if not user:
        