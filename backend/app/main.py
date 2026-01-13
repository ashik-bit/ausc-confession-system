from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.routers.public import router as public_router
from app.routers.admin import router as admin_router

app = FastAPI(title="AUSC Confession System (MVP)")

app.include_router(public_router, prefix="/api")
app.include_router(admin_router, prefix="/api/admin")

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.get("/", include_in_schema=False)
def homepage():
    return FileResponse(str(STATIC_DIR / "index.html"))

@app.get("/admin", include_in_schema=False)
def admin_page():
    return FileResponse(str(STATIC_DIR / "admin.html"))
