from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.public import router as public_router
from app.routers.admin import router as admin_router

app = FastAPI(title="AUSC Confession System (MVP)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(public_router, prefix="/api")
app.include_router(admin_router, prefix="/api/admin")

@app.get("/")
def root():
    return {"ok": True, "service": "ausc-confession-system"}
