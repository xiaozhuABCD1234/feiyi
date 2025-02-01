# app/routers/auth.py
from fastapi import APIRouter, HTTPException, status, Depends
from app.models.models import User
from app.schemas.user import UserCreate, UserRead
from app.core.security import Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from app.crud.user import CRUDUser

router = APIRouter()

# 注册新用户
@router.post("/register", response_model=UserRead)
async def register(user: UserCreate):
    new_user = await CRUDUser.create_user(user)
    return UserRead.from_orm(new_user)

# 用户登录并获取 JWT 令牌
@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await Security.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=Security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = Security.create_access_token(
        data={"sub": user.name}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# 获取当前登录用户的信息
@router.get("/me", response_model=UserRead)
async def read_users_me(current_user: User = Depends(Security.get_current_user)):
    return current_user

