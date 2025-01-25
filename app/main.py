from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from app.routers import user, auth, post

app = FastAPI()

app.include_router(user.router, prefix="/users", tags=["user"])
app.include_router(auth.router, prefix="/user/auth", tags=["auth"])
# app.include_router(post.router, prefix="/posts", tags=["post"])


register_tortoise(
    app,
    config={
        "connections": {"default": "sqlite://app/data/database.db"},
        "apps": {
            "models": {
                "models": ["app.models.models"],
                "default_connection": "default",
            },
        },
        "timezone": "Asia/Shanghai",
    },
    generate_schemas=True,  # 自动生成表结构，仅在开发环境中使用
    add_exception_handlers=True,
)
