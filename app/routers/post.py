# app/routers/post.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
import markdown
from bs4 import BeautifulSoup
from app.crud.post import CRUDPost
from app.schemas.post import PostCreate, PostRead, PostUpdate
from app.core.security import Security

router = APIRouter()


async def get_summary(content: str) -> str:
    """
    从文章内容生成摘要。
    - 将 Markdown 转换为 HTML。
    - 从 HTML 中提取纯文本。
    - 将文本截取至 100 个字符。
    """
    html = markdown.markdown(content)
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator=" ")
    summary = text[:100].strip()
    if len(text) > 100:
        summary += "..."
    return summary


@router.post(
    "/",
    response_model=PostRead,
    status_code=status.HTTP_201_CREATED,
    summary="创建文章",
    description="根据提供的内容、标题和作者 ID 创建一篇新文章。摘要将自动从内容中生成。",
)
async def create_post(post_data: PostCreate):
    content = post_data.content
    summary = await get_summary(content)
    return await CRUDPost.create_post(post_data, summary)


@router.get(
    "/{post_id}",
    response_model=PostRead,
    summary="获取文章",
    description="根据文章的唯一 ID 获取单篇文章。",
)
async def read_post(post_id: int):
    return await CRUDPost.read_post(post_id)


@router.get(
    "/author/{author_id}",
    response_model=List[PostRead],
    summary="获取作者的文章",
    description="根据作者 ID 获取该作者撰写的所有文章。",
)
async def read_post_author(author_id: int):
    return await CRUDPost.read_post_by_author(author_id)


@router.put(
    "/{post_id}",
    response_model=PostRead,
    summary="更新文章",
    description="根据文章 ID 更新现有文章。摘要将根据更新后的内容自动重新生成。",
)
async def update_post(post_id: int, post_data: PostUpdate):
    content = post_data.content
    post_data.summary = await get_summary(content)
    return await CRUDPost.update_post(post_id, post_data)


@router.delete(
    "/{post_id}",
    status_code=204,
    summary="删除文章",
    description="根据文章 ID 删除一篇文章。此操作不可逆。",
)
async def delete_post(post_id: int):
    return await CRUDPost.delete_post(post_id)


@router.get(
    "/",
    response_model=List[PostRead],
    summary="获取所有文章",
    description="获取所有文章的列表，按创建时间排序。",
)
async def read_post_all():
    return await CRUDPost.read_post_all()
