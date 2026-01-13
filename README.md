# AUSC Confession System (MVP)

Public users can submit confession + caption + optional image.
Admin can view submissions using password or access key.

## Project Structure
- backend/  -> FastAPI API
- frontend/ -> Static HTML pages

## Run Locally (Backend)
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
