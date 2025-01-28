# app/services/markdown.py
import aiofiles
import os
import markdown
from bs4 import BeautifulSoup
from fastapi import HTTPException
from app.core.config import markdowns_path


class MarkdownService:
    def __init__(self, post_id: int):
        self.post_id = post_id
        self.markdown_path = os.path.join(markdowns_path, f"{post_id}.md")

    async def create_markdown_file(self, content: str):
        try:
            async with aiofiles.open(
                self.markdown_path, mode="w", encoding="utf-8"
            ) as f:
                await f.write(content)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to create markdown file: {str(e)}"
            )

    async def read_markdown_file(self):
        try:
            async with aiofiles.open(
                self.markdown_path, mode="r", encoding="utf-8"
            ) as f:
                return await f.read()
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="Markdown file not found")
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to read markdown file: {str(e)}"
            )

    async def convert_markdown_to_html(self):
        content = await self.read_markdown_file()
        html = markdown.markdown(content)
        return str(html)

    async def extract_summary_from_markdown(self, summary_length: int = 100):
        html = await self.convert_markdown_to_html()
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(separator=" ")
        summary = text[:summary_length].strip()
        if len(text) > summary_length:
            summary += "..."
        return summary

    async def update_markdown_file(self, content: str):
        try:
            async with aiofiles.open(
                self.markdown_path, mode="w", encoding="utf-8"
            ) as f:
                await f.write(content)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to update markdown file: {str(e)}"
            )

    async def delete_markdown_file(self):
        try:
            if os.path.exists(self.markdown_path):
                os.remove(self.markdown_path)
            else:
                raise HTTPException(status_code=404, detail="Markdown file not found")
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to delete markdown file: {str(e)}"
            )
