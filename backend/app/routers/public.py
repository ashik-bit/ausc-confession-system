from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from datetime import datetime
from pathlib import Path
import itertools
import re
import uuid

router = APIRouter()

# --- Local upload folder (MVP) ---
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# --- Confess number: 00001, 00002... ---
_counter = itertools.count(1)

def next_confess_num() -> str:
    return f"{next(_counter):05d}"

def safe_filename(name: str) -> str:
    name = name or "file"
    name = re.sub(r"[^a-zA-Z0-9._-]+", "_", name)
    return name[:120]

# In-memory submissions store (MVP)
SUBMISSIONS = []  # newest first


@router.post("/submit")
async def submit(
    fb_name: str = Form(...),
    confession: str = Form(...),
    caption: str = Form(""),
    from_text: str = Form("Anonymous"),
    to_text: str = Form("Anonymous"),
    image: UploadFile | None = File(None),
):
    fb_name = (fb_name or "").strip()
    confession = (confession or "").strip()
    caption = (caption or "").strip()
    from_text = (from_text or "").strip() or "Anonymous"
    to_text = (to_text or "").strip() or "Anonymous"

    if not fb_name:
        raise HTTPException(400, "Facebook name is required")
    if not confession:
        raise HTTPException(400, "Confession text is required")

    sub_id = str(uuid.uuid4())
    confess_num = next_confess_num()

    image_path = None
    if image is not None:
        fname = safe_filename(image.filename)
        out = UPLOAD_DIR / f"{confess_num}_{fname}"
        content = await image.read()
        out.write_bytes(content)
        image_path = str(out)

    # ✅ EXACT caption format user requested
    final_caption = (
        f"Confess Num: {confess_num}\n"
        f"From: {from_text}\n"
        f"To: {to_text}\n\n"
        f"{caption}".rstrip()
        + "\n"
    )

    item = {
        "id": sub_id,
        "confess_num": confess_num,
        "fb_name": fb_name,
        "from_text": from_text,
        "to_text": to_text,
        "confession": confession,
        "caption": caption,
        "final_caption": final_caption,
        "image_path": image_path,
        "created_at": datetime.utcnow().isoformat() + "Z",
    }
    SUBMISSIONS.insert(0, item)

    return {
        "ok": True,
        "message": "Submission received",
        "id": sub_id,
        "confess_num": confess_num,
        "final_caption": final_caption,
        "image_saved": bool(image_path),
        "warning": "আপনার Facebook নাম যেভাবে আছে ঠিক সেভাবেই লিখুন। ভুল নাম দিলে পোস্ট হবে না।",
    }


@router.get("/latest")
def latest():
    # For quick test
    return {"ok": True, "count": len(SUBMISSIONS), "items": SUBMISSIONS[:20]}
