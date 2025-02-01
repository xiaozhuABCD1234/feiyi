# app/crud/user.py
from fastapi import HTTPException
from sqlmodel import Session, select
from typing import List, Optional
from pydantic import EmailStr

from app.models.models import User
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.core.security import Security


async def _check_user_name_is_existing(name: str) -> None:
    user = await User.get_or_none(name=name)
    if user:
        raise HTTPException(status_code=400, detail="Username already exists")


async def _check_user_email_is_existing(email: EmailStr) -> None:
    user = await User.get_or_none(email=email)
    if user:
        raise HTTPException(status_code=400, detail="Email already exists")


class CRUDUser:
    @staticmethod
    async def create_user(user_data: UserCreate) -> User:
        await _check_user_email_is_existing(user_data.email)
        await _check_user_name_is_existing(user_data.name)
        user_data.password = Security.get_password_hash(user_data.password)
        new_user = await User.create(
            name=user_data.name, email=user_data.email, password=user_data.password
        )
        if new_user.id == 1:
            new_user.permissions = "admin"
        await new_user.save()
        return new_user

    @staticmethod
    async def update_user(user_id: int, user_data: UserUpdate) -> User:
        user = await User.get_or_none(id=user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        await _check_user_email_is_existing(user_data.email)
        await _check_user_name_is_existing(user_data.name)
        if user_data.password:
            user_data.password = Security.get_password_hash(user_data.password)
        update_data = user_data.model_dump(exclude_unset=True)
        await user.update_from_dict(update_data)
        await user.save()
        return user

    @staticmethod
    async def read_user_all() -> List[UserRead]:
        users = await User.all()
        return [UserRead.model_validate(dict(user)) for user in users]

    @staticmethod
    async def read_user_id(user_id: int) -> UserRead:
        user = await User.get_or_none(id=user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserRead.model_validate(user)

    @staticmethod
    async def update_user(user_id: int, user_data: UserUpdate) -> User:
        user = await User.get_or_none(id=user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        await _check_user_email_is_existing(user_data.email)
        await _check_user_name_is_existing(user_data.name)
        if user_data.password:
            user_data.password = Security.get_password_hash(user_data.password)
        await user.update_from_dict(user_data.model_dump(exclude_unset=True))
        await user.save()
        return user

    @staticmethod
    async def delete_user(user_id: int) -> None:
        user = await User.get_or_none(id=user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        await user.delete()
