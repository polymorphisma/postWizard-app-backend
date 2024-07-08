# from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import File, UploadFile, Form
from fastapi.responses import JSONResponse
from typing import List
from app.utilities.utils import extract_extension, generate_uuid
from app.utilities.logger import logger
import os
import shutil

from app.Social_media_handler.sm_handler import Sm_handler

sm_handler_obj = Sm_handler()
ROOT_DIR = os.getcwd()
logger.info(ROOT_DIR)

image_director = os.path.join(ROOT_DIR, 'image')


class AiService:
    @staticmethod
    def upload(session: AsyncSession, images: List[UploadFile] = File(...), context: str = Form(...), socialMedia: str = Form(...)):
        if socialMedia == '':
            return JSONResponse({"success": False, "message": "Please choose one social media"})

        socialMedia = [x.lower() for x in socialMedia.split(",")]
        file_list = []

        for image in images:
            extension = extract_extension(image.filename)
            if extension not in ["png", "jpg", "jpeg"]:
                return JSONResponse({"success": False, "message": "File Extension Not valid."})
            uuid_val = generate_uuid()
            new_file_name = f"{uuid_val}.{extension}"
            save_file = os.path.join(image_director, new_file_name)

            try:
                with open(save_file, "wb") as buffer:
                    shutil.copyfileobj(image.file, buffer)
            except Exception as e:
                logger.info(e)
                return JSONResponse(content={"error": str(e)}, status_code=500)
            file_list.append(save_file)
        value = sm_handler_obj.entry_point(socialMedia, file_list, context)
        return JSONResponse(value, status_code=200)
