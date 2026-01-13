from fastapi import FastAPI
from routers.public import router as public_router
from routers.admin import router as admin_router

app = FastAPI(title="AUSC Confession System")

app.include_router(public_router, prefix="/api")
app.include_router(admin_router, prefix="/api/admin")

@app.get("/")
def root():
    return {"status": "ok"}
