from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request, File, UploadFile, Form
from fastapi.security import HTTPBasic
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import shutil
from dotenv import load_dotenv
from utils import extract_extension, generate_uuid
import os
from typing import List

from sm_handler import Sm_handler

sm_handler_obj = Sm_handler()

load_dotenv()

app = FastAPI()
security = HTTPBasic()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

image_director = "uploaded_image"


@app.get("/")
async def index(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("home.html", context=context)


@app.post("/upload")
async def upload_image(images: List[UploadFile] = File(...), context: str = Form(...), socialMedia: str = Form(...)):
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
            return JSONResponse(content={"error": str(e)}, status_code=500)
        file_list.append(save_file)
    value = sm_handler_obj.entry_point(socialMedia, file_list, context)
    print(value)
    return JSONResponse(value, status_code=200)


@app.get("/test")
async def test_function(request: Request):
    return JSONResponse({"success": True, "message": "A.M.A is working"})
