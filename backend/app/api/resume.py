import os
from pathlib import Path
from uuid import uuid4
from app.utils.resume_parser import ResumeParser

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.resume import Resume
from app.models.user import User
from app.repositories.resume_repository import ResumeRepository
from app.schemas.resume import ResumeResponse
from app.core.security import get_current_user

router = APIRouter(prefix="/resumes", tags=["Resumes"])

UPLOAD_DIR = Path("uploads/resumes")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".docx"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


@router.post(
    "/upload",
    response_model=ResumeResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    extension = os.path.splitext(file.filename)[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are allowed.",
        )

    contents = await file.read()

    stored_filename = f"{uuid4()}{extension}"
    file_path = UPLOAD_DIR / stored_filename

    with open(file_path, "wb") as f:
        f.write(contents)

    try:
        extracted_text = ResumeParser.extract_text(str(file_path))
        parsing_status = "COMPLETED"
    except Exception:
        extracted_text = None
        parsing_status = "FAILED"

    resume = Resume(
    user_id=current_user.id,
    original_filename=file.filename,
    stored_filename=stored_filename,
    file_path=str(file_path),
    file_size=len(contents),
    file_type=extension.replace(".", "").upper(),
    extracted_text=extracted_text,
    parsing_status=parsing_status,
)

    repository = ResumeRepository()
    return repository.create(db, resume)