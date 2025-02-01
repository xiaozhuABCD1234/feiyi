from fastapi import APIRouter, UploadFile, HTTPException, Response
import os
import cv2
import numpy as np
import aiofiles
from typing import List

from app.core.config import imgs_path

router = APIRouter()

img_profile_path = os.path.join(imgs_path, "profile")
os.makedirs(img_profile_path, exist_ok=True)

img_post_path = os.path.join(imgs_path, "post")
os.makedirs(img_post_path, exist_ok=True)


@router.post("/profile/{user_id}")
async def create_img_profile(user_id: int, file: UploadFile):
    if file.content_type not in [
        "image/jpeg",
        "image/png",
        "image/gif",
        "image/bmp",
        "image/tiff",
        "image/webp",
    ]:
        raise HTTPException(
            status_code=400, detail="Invalid file type. Only images are allowed."
        )
    os.makedirs(img_profile_path, exist_ok=True)
    # 获取后缀名
    file_extension = os.path.splitext(file.filename)[1].lower()
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    resized_image = cv2.resize(image, (200, 200), interpolation=cv2.INTER_AREA)

    if file.content_type != "image/gif":
        file_extension = ".jpg"  # 强制将扩展名改为 .jpg
        filename = f"{user_id}{file_extension}"  # 使用用户 ID 作为文件名
        save_path = os.path.join(img_profile_path, filename)  # 拼接保存路径
        cv2.imwrite(
            save_path, resized_image, [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        )  # 保存为 JPG，质量为 90
    else:
        # 如果是 GIF，保持原格式
        filename = f"{user_id}{file_extension}"  # 使用用户 ID 作为文件名
        save_path = os.path.join(img_profile_path, filename)  # 拼接保存路径
        cv2.imwrite(save_path, resized_image)  # 保存为原格式

    return {
        "message": "Image uploaded and resized successfully",
        "file_path": save_path,
    }


@router.get("/profile/{user_id}")
async def get_profile(user_id: int):
    jpg_path = os.path.join(img_profile_path, f"{user_id}.jpg")
    gif_path = os.path.join(img_profile_path, f"{user_id}.gif")
    if os.path.exists(jpg_path):
        async with aiofiles.open(jpg_path, mode="rb") as f:
            content = await f.read()
        return Response(content=content, media_type="image/jpeg")
    elif os.path.exists(gif_path):
        async with aiofiles.open(gif_path, mode="rb") as f:
            content = await f.read()
        return Response(content=content, media_type="image/gif")
    else:
        raise HTTPException(status_code=404, detail="Profile image not found")


@router.post("/post/{post_id}")
async def create_img_post(post_id: int, files: List[UploadFile]):
    saved_files = []

    count = 1
    for file in files:
        if file.content_type not in [
            "image/jpeg",
            "image/png",
            "image/gif",
            "image/bmp",
            "image/tiff",
            "image/webp",
        ]:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type for {file.filename}. Only images are allowed.",
            )
        os.makedirs(img_profile_path, exist_ok=True)
        file_extension = os.path.splitext(file.filename)[1].lower()
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if file.content_type != "image/gif":
            file_extension = ".jpg"  # 强制将扩展名改为 .jpg
            filename = f"{post_id}-{count}{file_extension}"
            save_path = os.path.join(img_post_path, filename)  # 拼接保存路径
            cv2.imwrite(
                save_path, image, [int(cv2.IMWRITE_JPEG_QUALITY), 90]
            )  # 保存为 JPG，质量为 90
        else:
            # 如果是 GIF，保持原格式
            filename = f"{post_id}-{count}{file_extension}"
            save_path = os.path.join(img_post_path, filename)  # 拼接保存路径
            cv2.imwrite(save_path, image)  # 保存为原格式
        count += 1
        # 记录成功上传的文件信息
        saved_files.append(
            {
                "filename": filename,
                "file_path": save_path,
                "message": "Image uploaded and resized successfully",
            }
        )
    return {
        "message": "All images uploaded successfully",
        "saved_files": saved_files,
    }


@router.get("/post/{post_id}/{img_id}")
async def get_post_img(post_id, img_id: int):
    jpg_path = os.path.join(img_post_path, f"{post_id}-{img_id}.jpg")
    gif_path = os.path.join(img_post_path, f"{post_id}-{img_id}.gif")
    if os.path.exists(jpg_path):
        async with aiofiles.open(jpg_path, mode="rb") as f:
            content = await f.read()
        return Response(content=content, media_type="image/jpeg")
    elif os.path.exists(gif_path):
        async with aiofiles.open(gif_path, mode="rb") as f:
            content = await f.read()
        return Response(content=content, media_type="image/gif")
    else:
        raise HTTPException(status_code=404, detail="Post image not found")
