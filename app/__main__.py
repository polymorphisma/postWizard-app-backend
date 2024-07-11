from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import uvicorn
from app.run_migration import run_migration

from app.routers.api_router import api_router

app = FastAPI(title="So Fast Project", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="template")

# Run migrations before starting the app
run_migration()


@app.get("/")
async def index(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("home.html", context=context)

app.include_router(api_router)

# make https redirect work
if __name__ == "__main__":
    uvicorn.run(
        "app.__main__:app",  # Changed from "__main__:app" to "app.__main__:app"
        loop="asyncio",
        host="0.0.0.0",
        port=8080,
        # reload=True,
        workers=5,
        env_file="../.env",
    )
