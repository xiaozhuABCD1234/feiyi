# app/crud/user.py
from fastapi import HTTPException
from sqlmodel import Session, select
from typing import List, Optional

from app.models.models import User
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.core.security import Security
from app.database.db import SessionDep


async def create_user(user_data: UserCreate, db: SessionDep):
    # 检查用户名是否重复
    existing_user = db.exec(select(User).where(User.name == user_data.name)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    # 检查邮箱是否重复
    existing_email = db.exec(select(User).where(User.email == user_data.email)).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")

    user_data.password = Security.get_password_hash(user_data.password)
    new_user = User.model_validate(user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def read_user_all(
    db: SessionDep, skip: Optional[int] = 0, limit: Optional[int] = 100
):
    users = db.exec(select(User).offset(skip).limit(limit)).all()
    return users


async def read_user_id(user_id: int, db: SessionDep) -> UserRead:
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user_read = UserRead(id=user.id, name=user.name, email=user.email)
    return user_read


async def update_user(user_id: int, user_data: UserUpdate, db: SessionDep):
    user_db = db.get(User, user_id)
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    # 检查用户名是否重复
    existing_user = db.exec(select(User).where(User.name == user_data.name)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    # 检查邮箱是否重复
    existing_email = db.exec(select(User).where(User.email == user_data.email)).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")

    if user_data.password:
        user_data.password = Security.get_password_hash(user_data.password)
    user_data_dict = user_data.model_dump(exclude_unset=True)
    user_db.sqlmodel_update(user_data_dict)
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db


async def delete_user(user_id: int, db: SessionDep):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return


class CRUDUser:
    create_user = create_user
    read_user_all = read_user_all
    read_user_id = read_user_id
    update_user = update_user
    delete_user = delete_user
