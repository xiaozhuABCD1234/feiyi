from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from tortoise import Tortoise
from app.core.config import TORTOISE_ORM
from app.routers import user, auth, post, tag, comment

app = FastAPI()

app.include_router(user.router, prefix="/users", tags=["user"])
app.include_router(auth.router, prefix="/user/auth", tags=["auth"])
app.include_router(post.router, prefix="/posts", tags=["post"])
app.include_router(tag.router, prefix="/tags", tags=["tag"])
app.include_router(comment.router, prefix="/comments", tags=["comment"])

Tortoise._init_timezone(use_tz=True, timezone="Asia/Shanghai")
register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,  # 自动生成表结构，仅在开发环境中使用
    add_exception_handlers=True,
)
