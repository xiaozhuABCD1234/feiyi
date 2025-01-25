# # app/routers/post.py
# from fastapi import APIRouter, Depends, HTTPException, status
# from app.models.models import Post
# from app.schemas.post import PostCreate, PostRead, PostUpdate
# from app.crud.post import CRUDPost
# from app.database.db import SessionDep

# router = APIRouter()


# @router.post("/", response_model=PostCreate, status_code=status.HTTP_201_CREATED)
# async def create_post(post_data: PostCreate, db: SessionDep):
#     return await CRUDPost.create_post(post_data, db)


# @router.get("/", response_model=list[PostRead])
# async def get_all_posts(db: SessionDep, skip: int = 0, limit: int = 100):
#     return await CRUDPost.read_post_all(db, skip, limit)


# @router.get("/{post_id}", response_model=PostRead)
# async def get_post_by_id(post_id: int, db: SessionDep):
#     return await CRUDPost.read_post_id(post_id, db)


# @router.put("/{post_id}", response_model=PostUpdate)
# async def update_post_by_id(post_id: int, post_data: PostUpdate, db: SessionDep):
#     return await CRUDPost.update_post(post_id, post_data, db)


# @router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_post_by_id(post_id: int, db: SessionDep):
#     return await CRUDPost.delete_post(post_id, db)
