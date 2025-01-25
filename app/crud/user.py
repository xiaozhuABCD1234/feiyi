# app/crud/user.py
from fastapi import HTTPException
from sqlmodel import Session, select
from typing import List, Optional
from pydantic import EmailStr

from app.models.models import User
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.core.security import Security


# 检查用户名是否重复
async def _check_user_name_is_existing(name: str) -> Optional[User]:
    user = await User.get_or_none(name=name)
    if not user:
        return None
    raise HTTPException(status_code=400, detail="Username already exists")


# 检查邮箱是否重复
async def _check_user_email_is_existing(email: EmailStr) -> Optional[User]:
    user = await User.get_or_none(email=email)
    if not user:
        return None
    raise HTTPException(status_code=400, detail="Email already exists")


async def create_user(user_data: UserCreate) -> User:
    await _check_user_email_is_existing(user_data.email)
    await _check_user_name_is_existing(user_data.name)
    user_data.password = Security.get_password_hash(user_data.password)
    new_user = await User.create(
        name=user_data.name, email=user_data.email, password=user_data.password
    )
    return new_user


async def read_user_all() -> List[UserRead]:
    users = await User.all()
    return [UserRead.model_validate(dict(user)) for user in users]


async def read_user_id(user_id: int) -> UserRead:
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserRead.model_validate(user.model_dump())


async def update_user(user_id: int, user_data: UserUpdate) -> User:
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await _check_user_email_is_existing(user_data.email)
    await _check_user_name_is_existing(user_data.name)
    if user_data.password:
        user_data.password = Security.get_password_hash(user_data.password)
    await user.update_from_dict(user_data.dict(exclude_unset=True))
    await user.save()
    return user


async def read_user_id(user_id: int) -> UserRead:
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserRead.model_validate(user)


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


async def delete_user(user_id: int) -> None:
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await user.delete()


class CRUDUser:
    @staticmethod
    async def create_user(user_data: UserCreate) -> User:
        return await create_user(user_data)

    @staticmethod
    async def read_user_all() -> List[UserRead]:
        return await read_user_all()

    @staticmethod
    async def read_user_id(user_id: int) -> UserRead:
        return await read_user_id(user_id)

    @staticmethod
    async def update_user(user_id: int, user_data: UserUpdate) -> User:
        return await update_user(user_id, user_data)

    @staticmethod
    async def delete_user(user_id: int) -> None:
        return await delete_user(user_id)
