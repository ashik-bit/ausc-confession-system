from fastapi import APIRouter, HTTPException, Header

from app.config import ADMIN_PASSWORD, ADMIN_ACCESS_KEY
from app.routers.public import SUBMISSIONS

router = APIRouter()

def require_admin(x_admin_auth: str | None) -> str:
    """
    Header: X-ADMIN-AUTH: password:<pass>
    OR      X-ADMIN-AUTH: key:<access_key>
    """
    if not x_admin_auth:
        raise HTTPException(status_code=401, detail="Missing X-ADMIN-AUTH header")

    if x_admin_auth.startswith("password:"):
        pw = x_admin_auth.removeprefix("password:").strip()
        if pw and pw == ADMIN_PASSWORD:
            return "password"
        raise HTTPException(status_code=401, detail="Invalid admin password")

    if x_admin_auth.startswith("key:"):
        k = x_admin_auth.removeprefix("key:").strip()
        if k and k == ADMIN_ACCESS_KEY:
            return "access_key"
        raise HTTPException(status_code=401, detail="Invalid access key")

    raise HTTPException(status_code=401, detail="Invalid auth format")


@router.get("/submissions")
def admin_submissions(
    x_admin_auth: str | None = Header(default=None, alias="X-ADMIN-AUTH")
):
    method = require_admin(x_admin_auth)
    return {
        "ok": True,
        "auth_method": method,
        "count": len(SUBMISSIONS),
        "items": SUBMISSIONS
    }

