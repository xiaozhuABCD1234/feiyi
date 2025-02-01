from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from tortoise import Tortoise
from app.core.config import TORTOISE_ORM
from app.routers import user, auth, post, tag, comment, img
from app.middlewares.permissions import get_user_permissions_middleware

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def user_permissions_middleware(request: Request, call_next):
    await get_user_permissions_middleware(request)
    response = await call_next(request)
    return response


app.include_router(user.router, prefix="/users", tags=["user"])
app.include_router(auth.router, prefix="/user/auth", tags=["auth"])
app.include_router(post.router, prefix="/posts", tags=["post"])
app.include_router(tag.router, prefix="/tags", tags=["tag"])
app.include_router(comment.router, prefix="/comments", tags=["comment"])
app.include_router(img.router, prefix="/imgs", tags=["img"])

Tortoise._init_timezone(use_tz=True, timezone="Asia/Shanghai")
register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,  # 自动生成表结构，仅在开发环境中使用
    add_exception_handlers=True,
)


@app.get("/")
async def helloworld():
    return
