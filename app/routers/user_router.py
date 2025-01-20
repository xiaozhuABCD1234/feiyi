# app/routers/user_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List, Optional
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta

from app.models.user import User, UserCreate, UserUpdate
from app.database.db import get_session

# 配置密钥和算法
SECRET_KEY = "b0e76c3bbd67925c313d8c71fb0cddb20fe5aa2dcefd4902b2906ac31761bdae"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 初始化密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 初始化 OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# JWT 生成和验证函数
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str, db: Session):
    # 验证用户名和密码
    user = db.exec(select(User).where(User.name == username)).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.exec(select(User).where(User.name == username)).first()
    if user is None:
        raise credentials_exception
    return user


user = APIRouter()


@user.post("/", response_model=User)
async def create_user(user_data: UserCreate, db: Session = Depends(get_session)):
    # 检查用户名是否重复
    existing_user = db.exec(select(User).where(User.name == user_data.name)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    # 检查邮箱是否重复
    existing_email = db.exec(select(User).where(User.email == user_data.email)).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")

    user_data.password = get_password_hash(user_data.password)
    new_user = User.model_validate(user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@user.get("/", response_model=List[User])
async def read_user_all(
    skip: Optional[int] = 0,
    limit: Optional[int] = 100,
    db: Session = Depends(get_session),
):
    users = db.exec(select(User).offset(skip).limit(limit)).all()
    return users


@user.get("/{user_id}", response_model=User)
async def read_user_id(user_id: int, db: Session = Depends(get_session)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user.patch("/{user_id}", response_model=User)
async def update_user(
    user_id: int, user_data: UserUpdate, db: Session = Depends(get_session)
):
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
        user_data.password = get_password_hash(user_data.password)
    user_data_dict = user_data.model_dump(exclude_unset=True)
    user_db.sqlmodel_update(user_data_dict)
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db


@user.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int, db: Session = Depends(get_session)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return


# 用户登录
@user.post("/token", response_model=dict)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.name}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# 获取当前登录用户
@user.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
