# app/routers/user.py
from fastapi import APIRouter, Depends, HTTPException, status
from app.models.models import User
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.crud.user import CRUDUser


router = APIRouter()


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate):
    return await CRUDUser.create_user(user_data)


@router.get("/", response_model=list[UserRead])
async def get_all_users():
    return await CRUDUser.read_user_all()


@router.get("/{user_id}", response_model=UserRead)
async def get_user_by_id(user_id: int):
    return await CRUDUser.read_user_id(user_id)


@router.put("/{user_id}", response_model=UserRead)
async def update_user_by_id(user_id: int, user_data: UserUpdate):
    return await CRUDUser.update_user(user_id, user_data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_id(user_id: int):
    return await CRUDUser.delete_user(user_id)
