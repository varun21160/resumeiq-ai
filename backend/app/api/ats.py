from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.ai.ats_report_engine import ATSReportEngine
from app.core.security import get_current_user
from app.database.session import get_db
from app.models.resume import Resume
from app.models.user import User
from app.services.ats_service import ATSService


router = APIRouter(
    prefix="/ats",
    tags=["ATS Analysis"],
)


# ============================================================
# REQUEST SCHEMA
# ============================================================

class ATSAnalyzeRequest(BaseModel):
    resume_id: str = Field(
        ...,
        description="ID of the uploaded resume",
    )

    job_description: str = Field(
        ...,
        min_length=20,
        description="Target job description",
    )


# ============================================================
# ANALYZE RESUME
# ============================================================

@router.post("/analyze")
def analyze_resume(
    request: ATSAnalyzeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Analyze an uploaded resume against a target job description.

    The resume text is fetched from the database using resume_id.

    Requires:
        - Authenticated user
        - Valid resume_id
        - Resume must belong to the current user
        - Resume must have successfully extracted text
    """

    # --------------------------------------------------------
    # 1. Find resume belonging to current user
    # --------------------------------------------------------

    resume = (
        db.query(Resume)
        .filter(
            Resume.id == request.resume_id,
            Resume.user_id == current_user.id,
        )
        .first()
    )

    if resume is None:
        raise HTTPException(
            status_code=404,
            detail="Resume not found.",
        )

    # --------------------------------------------------------
    # 2. Make sure resume text was extracted
    # --------------------------------------------------------

    if not resume.extracted_text:
        raise HTTPException(
            status_code=400,
            detail=(
                "Resume text is not available. "
                "Please upload a readable PDF or DOCX resume."
            ),
        )

    # --------------------------------------------------------
    # 3. Make sure parsing was successful
    # --------------------------------------------------------

    if resume.parsing_status != "COMPLETED":
        raise HTTPException(
            status_code=400,
            detail=(
                f"Resume parsing is not completed. "
                f"Current status: {resume.parsing_status}"
            ),
        )

    # --------------------------------------------------------
    # 4. Generate ATS report
    # --------------------------------------------------------

    try:
        report = ATSReportEngine.generate(
            resume_text=resume.extracted_text,
            job_description=request.job_description,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"ATS analysis failed: {str(exc)}",
        ) from exc

    # --------------------------------------------------------
    # 5. Save ATS analysis
    # --------------------------------------------------------

    try:
        analysis = ATSService.create_analysis(
            db=db,
            user_id=current_user.id,
            resume_id=resume.id,
            job_description=request.job_description,
            report=report,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save ATS analysis: {str(exc)}",
        ) from exc

    # --------------------------------------------------------
    # 6. Return report
    # --------------------------------------------------------

    return {
        "id": analysis.id,
        "resume_id": analysis.resume_id,
        "overall_score": analysis.overall_score,
        "category_scores": analysis.category_scores,
        "analysis": analysis.analysis,
        "recommendations": analysis.recommendations,
        "created_at": analysis.created_at,
    }