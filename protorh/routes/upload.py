from fastapi import APIRouter, HTTPException, status, File, UploadFile
from fastapi.responses import JSONResponse, FileResponse
from lib.auth import get_user
from utils.helper import find_file_by_name
import shutil
import os


router = APIRouter(
    tags=['upload']
)


# define path to pic
path = os.path.relpath("./assets/picture/profiles")


# Endpoint : /api/picture/user/{id}
# Type : POST
# upload a picture
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

    filename = find_file_by_name(token, path)

    if not filename:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "type": "picture_error",
                "error": "This user does not have picture"
            }
        )

    return FileResponse(filename)


# Endpoint : /api/upload/picture/user/{id}
# Type : POST
# upload a picture
@router.post("/upload/picture/user/{id}")
async def upload_pic(id, image: UploadFile = File()):
    if not image:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file provided"
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
    # check file type
    if not image.content_type in ["image/jpeg", "image/png", "image/gif"]:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "type": "image_type",
                "error": "Image type is not: gif, png or jpg"
            }
        )

    # check if dir exist
    if not os.path.exists(path):
        os.makedirs(path)
    # save file with token as filename
    try:
        with open(f"{path}/{user['token']}.{image.filename.split('.')[-1]}", "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
    except shutil.Error as err:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "type": "upload_error",
                "error": err
            }
        )

    return {"message": "file uploaded"}
