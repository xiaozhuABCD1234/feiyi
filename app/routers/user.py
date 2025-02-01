from fastapi import APIRouter, Depends, HTTPException, status
from app.models.models import User
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.crud.user import CRUDUser
from app.core.security import Security

router = APIRouter()


@router.post(
    "/",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="注册新用户",
    description="接收用户的基本信息，创建一个新的用户记录，并返回用户详情。",
)
async def register_user(user_data: UserCreate):
    return await CRUDUser.create_user(user_data)


@router.get(
    "/",
    response_model=list[UserRead],
    summary="获取所有用户",
    description="返回系统中所有用户的列表，包括用户的基本信息。",
)
async def get_all_users():
    return await CRUDUser.read_user_all()


@router.get(
    "/{user_id}",
    response_model=UserRead,
    summary="根据用户ID获取用户详情",
    description="通过指定的用户ID，返回该用户的具体信息。",
)
async def get_user_by_id(user_id: int):
    return await CRUDUser.read_user_id(user_id)


@router.put(
    "/{user_id}",
    response_model=UserRead,
    summary="根据用户ID更新用户信息",
    description="需要验证当前用户是否有权限更新指定用户的信息。",
)
async def update_user_by_id(
    user_id: int,
    user_data: UserUpdate,
    current_user: User = Depends(Security.get_current_user),
):
    await Security.check_user_permissions(current_user, user_id)
    return await CRUDUser.update_user(user_id, user_data)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="根据用户ID删除用户",
    description="需要验证当前用户是否有权限删除指定用户。",
)
async def delete_user_by_id(
    user_id: int,
    current_user: User = Depends(Security.get_current_user),
):
    await Security.check_user_permissions(current_user, user_id)
    return await CRUDUser.delete_user(user_id)
