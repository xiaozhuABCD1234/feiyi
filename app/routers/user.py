# app/routers/user.py
from fastapi import APIRouter, Depends, HTTPException, status
from app.models.models import User
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.crud.user import CRUDUser
from app.database.db import SessionDep

router = APIRouter()


@router.post("/", response_model=UserCreate, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate, db: SessionDep):
    return await CRUDUser.create_user(user_data, db)


@router.get("/", response_model=list[UserRead])
async def get_all_users(db: SessionDep, skip: int = 0, limit: int = 100):
    return await CRUDUser.read_user_all(db, skip, limit)


@router.get("/{user_id}", response_model=UserRead)
async def get_user_by_id(user_id: int, db: SessionDep):
    return await CRUDUser.read_user_id(user_id, db)


@router.put("/{user_id}", response_model=UserUpdate)
async def update_user_by_id(user_id: int, user_data: UserUpdate, db: SessionDep):
    return await CRUDUser.update_user(user_id, user_data, db)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_id(user_id: int, db: SessionDep):
    return await CRUDUser.delete_user(user_id, db)
