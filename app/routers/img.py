from fastapi import APIRouter, UploadFile, HTTPException, Response
import os
import cv2
import numpy as np
import aiofiles

from app.core.config import imgs_path

router = APIRouter()


imgs_path = imgs_path
img_profile_path = os.path.join(imgs_path, "profile")
os.makedirs(img_profile_path, exist_ok=True)



@router.post("/profile/{id}")
async def create_img_profile(id: int, file: UploadFile):
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
    # 获取后缀名
    file_extension = os.path.splitext(file.filename)[1].lower()
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    resized_image = cv2.resize(image, (200, 200), interpolation=cv2.INTER_AREA)

    if file.content_type != "image/gif":
        file_extension = ".jpg"  # 强制将扩展名改为 .jpg
        filename = f"{id}{file_extension}"  # 使用用户 ID 作为文件名
        save_path = os.path.join(img_profile_path, filename)  # 拼接保存路径
        cv2.imwrite(
            save_path, resized_image, [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        )  # 保存为 JPG，质量为 90
    else:
        # 如果是 GIF，保持原格式
        filename = f"{id}{file_extension}"  # 使用用户 ID 作为文件名
        save_path = os.path.join(img_profile_path, filename)  # 拼接保存路径
        cv2.imwrite(save_path, resized_image)  # 保存为原格式

    return {
        "message": "Image uploaded and resized successfully",
        "file_path": save_path,
    }


@router.get("/profile/{id}")
async def get_profile(id: int):
    jpg_path = os.path.join(img_profile_path, f"{id}.jpg")
    gif_path = os.path.join(img_profile_path, f"{id}.gif")
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
