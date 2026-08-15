import os
from pathlib import Path
from uuid import uuid4

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status,
)
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.database.session import get_db
from app.models.resume import Resume
from app.models.user import User
from app.schemas.resume import (
    ResumeResponse,
    ResumeListResponse,
)
from app.ai.validators.resume_truthfulness_validator import (
    ResumeTruthfulnessValidator,
)
from app.schemas.resume_generation import (
    ResumeGenerationRequest,
    ResumeGenerationResponse,
    GeneratedResume,
)
from app.services.resume_service import ResumeService
from app.services.resume_generator import ResumeGenerator
from app.resume.document_parser import DocumentParser
from app.services.generated_resume_service import (
    GeneratedResumeService,
)

router = APIRouter(
    prefix="/resumes",
    tags=["Resumes"],
)


# ============================================================
# Configuration
# ============================================================

UPLOAD_DIR = Path("uploads/resumes")

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
}

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


# ============================================================
# Helper Functions
# ============================================================

def get_file_extension(
    filename: str | None,
) -> str:
    """
    Return the lowercase file extension.
    """

    if not filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Resume filename is required.",
        )

    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Only PDF and DOCX files are allowed."
            ),
        )

    return extension


def validate_file_size(
    contents: bytes,
) -> None:
    """
    Validate uploaded file size.
    """

    if not contents:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded resume file is empty.",
        )

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds the 5 MB limit.",
        )


# ============================================================
# Upload Resume
# ============================================================

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
    """
    Upload and parse a resume.

    Supported formats:
        - PDF
        - DOCX

    Processing flow:

        Upload
            ↓
        Validate extension
            ↓
        Validate size
            ↓
        Save file
            ↓
        DocumentParser
            ↓
        TextCleaner
            ↓
        Store resume
            ↓
        Return resume information
    """

    # --------------------------------------------------------
    # Validate filename and extension
    # --------------------------------------------------------

    extension = get_file_extension(
        file.filename
    )

    # --------------------------------------------------------
    # Read uploaded file
    # --------------------------------------------------------

    try:

        contents = await file.read()

    except Exception as exc:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to read the uploaded resume.",
        ) from exc

    # --------------------------------------------------------
    # Validate file size
    # --------------------------------------------------------

    validate_file_size(
        contents
    )

    # --------------------------------------------------------
    # Generate unique stored filename
    # --------------------------------------------------------

    stored_filename = (
        f"{uuid4()}{extension}"
    )

    file_path = (
        UPLOAD_DIR / stored_filename
    )

    # --------------------------------------------------------
    # Save uploaded file
    # --------------------------------------------------------

    try:

        with open(
            file_path,
            "wb",
        ) as output_file:

            output_file.write(
                contents
            )

    except Exception as exc:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to save the uploaded resume.",
        ) from exc

    # --------------------------------------------------------
    # Extract resume text
    # --------------------------------------------------------

    try:

        extracted_text = (
            DocumentParser.extract_text(
                str(file_path)
            )
        )

    except FileNotFoundError as exc:

        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Uploaded resume file could not be found.",
        ) from exc

    except ValueError as exc:

        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    except Exception as exc:

        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(
                "An unexpected error occurred while "
                "processing the resume."
            ),
        ) from exc

    # --------------------------------------------------------
    # Validate extracted text
    # --------------------------------------------------------

    if not extracted_text.strip():

        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "No readable text could be extracted "
                "from the resume."
            ),
        )

    # --------------------------------------------------------
    # Create Resume database object
    # --------------------------------------------------------

    resume = Resume(
        user_id=current_user.id,
        original_filename=file.filename,
        stored_filename=stored_filename,
        file_path=str(file_path),
        file_size=len(contents),
        file_type=extension.replace(
            ".",
            "",
        ).upper(),
        extracted_text=extracted_text,
        parsing_status="COMPLETED",
    )

    # --------------------------------------------------------
    # Save through service
    # --------------------------------------------------------

    service = ResumeService()

    try:

        return service.create_resume(
            db,
            resume,
        )

    except Exception as exc:

        # If database storage fails, don't leave
        # an orphaned file on disk.

        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to save resume information.",
        ) from exc


# ============================================================
# Get All User Resumes
# ============================================================

@router.get(
    "",
    response_model=ResumeListResponse,
)
def get_resumes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Return all resumes belonging to the current user.
    """

    service = ResumeService()

    resumes = service.get_resumes(
        db,
        current_user.id,
    )

    return {
        "resumes": resumes,
    }


# ============================================================
# Get Single Resume
# ============================================================

@router.get(
    "/{resume_id}",
    response_model=ResumeResponse,
)
def get_resume(
    resume_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Return a single resume belonging to the current user.
    """

    service = ResumeService()

    resume = service.get_resume(
        db,
        resume_id,
        current_user.id,
    )

    if resume is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found.",
        )

    return resume


@router.post(
    "/{resume_id}/generate",
    response_model=ResumeGenerationResponse,
    status_code=status.HTTP_200_OK,
)
def generate_resume(
    resume_id: str,
    request: ResumeGenerationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ResumeService()

    resume = service.get_resume(
        db,
        resume_id,
        current_user.id,
    )

    if resume is None:
        raise HTTPException(
            status_code=404,
            detail="Resume not found.",
        )

    if not resume.extracted_text:
        raise HTTPException(
            status_code=400,
            detail=(
                "Resume does not contain extracted text. "
                "Please upload a readable PDF or DOCX resume."
            ),
        )

    try:
        # --------------------------------------------------
        # 1. Generate tailored resume using Gemini
        # --------------------------------------------------

        generated_data = ResumeGenerator.generate(
            resume_text=resume.extracted_text,
            job_description=request.job_description,
        )

        changes = generated_data.pop(
            "changes",
            [],
        )

        # --------------------------------------------------
        # 2. Validate generated resume against original
        # --------------------------------------------------

        validation = ResumeTruthfulnessValidator.validate(
            original_resume_text=resume.extracted_text,
            generated_resume=generated_data,
        )

        # --------------------------------------------------
        # 3. Convert generated resume into schema
        # --------------------------------------------------

        generated_resume = GeneratedResume.model_validate(
            generated_data
        )

        # --------------------------------------------------
        # 4. Convert generated resume to plain text
        # --------------------------------------------------

        generated_resume_text = ResumeGenerator.to_text(
            generated_resume.model_dump()
        )

        # --------------------------------------------------
        # 5. Run existing ATS engine
        # --------------------------------------------------

        from app.ai.ats_report_engine import ATSReportEngine

        ats_report = ATSReportEngine.generate(
            resume_text=generated_resume_text,
            job_description=request.job_description,
        )
        generated_record = GeneratedResumeService.create(
    db,
    user_id=current_user.id,
    resume_id=resume.id,
    job_description=request.job_description,
    ats_score=ats_report.overall_score,
    generated_resume=generated_resume.model_dump(),
    changes=changes,
)

        # --------------------------------------------------
        # 6. Add validation information to changes
        # --------------------------------------------------

        if validation["unsupported_skills"]:
            changes.append(
                "Potentially unsupported skills detected: "
                + ", ".join(
                    validation["unsupported_skills"]
                )
            )

        # --------------------------------------------------
        # 7. Return final generation response
        # --------------------------------------------------

        return {
    "id": generated_record.id,
    "resume_id": resume.id,
    "ats_score": ats_report.overall_score,
    "generated_resume": generated_resume,
    "changes": changes,
}

    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Resume generation failed: {exc}",
        ) from exc
# ============================================================
# Delete Resume
# ============================================================

@router.delete(
    "/{resume_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_resume(
    resume_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete a resume and its stored file.
    """

    service = ResumeService()

    resume = service.get_resume(
        db,
        resume_id,
        current_user.id,
    )

    if resume is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found.",
        )

    # --------------------------------------------------------
    # Delete physical file
    # --------------------------------------------------------

    if resume.file_path:

        file_path = Path(
            resume.file_path
        )

        if file_path.exists():

            try:
                file_path.unlink()

            except OSError as exc:

                raise HTTPException(
                    status_code=500,
                    detail=(
                        "Unable to delete the stored "
                        "resume file."
                    ),
                ) from exc

    # --------------------------------------------------------
    # Delete database record
    # --------------------------------------------------------

    service.delete_resume(
        db,
        resume,
    )

    return None
