from fastapi import APIRouter, HTTPException, status, File, UploadFile
from fastapi.responses import JSONResponse, FileResponse
from lib.auth import get_user
from utils.helper import find_file_by_name
import os
from PIL import Image


router = APIRouter(
    tags=['upload']
)


# define path to pic
path = os.path.relpath("./assets/picture/profiles")


# Endpoint : /api/picture/user/{id}
# Type : POST
# JWT required : False
# get user's picture
@router.get("/picture/user/{id}")
async def get_pic(id):
    user = await get_user(id=id)

    if not user:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "type": "user_error",
                "error": "User not found"
            }
        )

    token = user["token"]

    file_path, file_ext = find_file_by_name(token, path)

    if not file_path:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "type": "picture_error",
                "error": "This user does not have picture"
            }
        )

    return FileResponse(file_path, filename="image." + file_ext)


# Endpoint : /api/upload/picture/user/{id}
# Type : POST
# JWT required : False
# upload a picture and assign to user
@router.post("/upload/picture/user/{id}")
async def upload_pic(id, image: UploadFile = File()):
    if not image:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No image provided"
        )

    # check user
    user = await get_user(id=id)
    if not user:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "type": "user_error",
                "error": "User not found"
            }
        )

    # load image
    image_load = Image.open(image.file, mode="r")

    # get image size in string format: 123x123
    image_size = 'x'.join(map(str, image_load.size))

    # get image format
    image_format = image_load.format

    # check image size
    if image_load.size > (800, 800):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "type": "image_size",
                "error": f"Image size must not exceed 800x800 (current: {image_size})"
            }
        )

    # check image format
    if not image_format in ["PNG", "JPEG", "GIF"]:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "type": "image_type",
                "error": "Image type is not: gif, png or jpg"
            }
        )

    # check if dir exist
    if not os.path.exists(path):
        os.makedirs(path)

    # save file with token as filename
    image_load.save(f"{path}/{user['token']}.{image.filename.split('.')[-1]}")

    return {"message": "picture uploaded"}
