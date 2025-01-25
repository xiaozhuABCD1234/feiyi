# app/core/security.py
from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from typing import Optional
from sqlmodel import Session, select
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import User
from app.database.db import SessionDep
from app.core.config import settings


class Security:
    # 密码加密工具
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    # JWT 配置
    SECRET_KEY = settings.SECRET_KEY  # openssl rand -hex 32
    ALGORITHM = settings.ALGORITHM
    ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

    @staticmethod
    def get_password_hash(password: str) -> str:
        return Security.pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return Security.pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    # 创建 JWT 令牌
    def create_access_token(
        data: dict, expires_delta: Optional[timedelta] = None
    ) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=Security.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, Security.SECRET_KEY, algorithm=Security.ALGORITHM
        )
        return encoded_jwt

    @staticmethod
    # 解码 JWT 令牌
    def decode_token(token: str) -> Optional[dict]:
        try:
            payload = jwt.decode(
                token, Security.SECRET_KEY, algorithms=[Security.ALGORITHM]
            )
            return payload
        except JWTError:
            return None

    @staticmethod
    # 验证用户
    def authenticate_user(
        db: SessionDep, username: str, password: str
    ) -> Optional[User]:
        user = db.exec(select(User).where(User.name == username)).first()
        if not user:
            return None
        if not Security.verify_password(password, user.password):
            return None
        return user

    @staticmethod
    # 从 JWT 令牌中获取当前用户
    async def get_current_user(
        db: SessionDep,
        token: str = Depends(OAuth2PasswordBearer(tokenUrl="token")),
    ):
        payload = Security.decode_token(token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
        username = payload.get("sub")
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
        user = db.exec(select(User).where(User.name == username)).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
            )
        return user
