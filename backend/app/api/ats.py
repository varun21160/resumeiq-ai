from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.ai.ats_report_engine import ATSReportEngine
from app.core.security import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.services.ats_analysis_service import ATSAnalysisService
from app.services.resume_service import ResumeService


router = APIRouter(
    prefix="/ats",
    tags=["ATS Analysis"],
)


class ATSAnalyzeRequest(BaseModel):
    """
    Request body for ATS analysis.

    The resume text is retrieved from the uploaded resume
    stored in the database.
    """

    resume_id: str = Field(
        ...,
        min_length=1,
        description="ID of the uploaded resume",
    )

    job_description: str = Field(
        ...,
        min_length=20,
        description="Target job description",
    )


@router.post("/analyze")
def analyze_resume(
    request: ATSAnalyzeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Analyze a stored resume against a job description.

    Flow:

        resume_id
            ↓
        Find user's resume
            ↓
        Get extracted_text
            ↓
        Run ATS analyzers
            ↓
        Save ATS analysis
            ↓
        Update resume ATS score
            ↓
        Return report
    """

    try:
        # ---------------------------------------------------------
        # 1. Find the resume belonging to the current user
        # ---------------------------------------------------------

        resume_service = ResumeService()

        resume = resume_service.get_resume(
            db=db,
            resume_id=request.resume_id,
            user_id=current_user.id,
        )

        if resume is None:
            raise HTTPException(
                status_code=404,
                detail="Resume not found.",
            )

        # ---------------------------------------------------------
        # 2. Make sure resume extraction succeeded
        # ---------------------------------------------------------

        if not resume.extracted_text:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Resume text is not available. "
                    "Please upload a readable PDF or DOCX resume."
                ),
            )

        # ---------------------------------------------------------
        # 3. Generate ATS report
        # ---------------------------------------------------------

        report = ATSReportEngine.generate(
            resume_text=resume.extracted_text,
            job_description=request.job_description,
        )

        # ---------------------------------------------------------
        # 4. Convert Pydantic report to dictionary
        # ---------------------------------------------------------

        if hasattr(report, "model_dump"):
            report_data = report.model_dump()

        elif hasattr(report, "dict"):
            report_data = report.dict()

        else:
            report_data = dict(report)

        # ---------------------------------------------------------
        # 5. Save ATS analysis
        # ---------------------------------------------------------

        saved_analysis = ATSAnalysisService.create_analysis(
            db=db,
            user_id=current_user.id,
            resume_id=resume.id,
            job_description=request.job_description,
            report=report_data,
        )

        # ---------------------------------------------------------
        # 6. Update resume's latest ATS score
        # ---------------------------------------------------------

        resume.ats_score = report_data["overall_score"]

        db.add(resume)
        db.commit()
        db.refresh(resume)

        # ---------------------------------------------------------
        # 7. Return final response
        # ---------------------------------------------------------

        return {
            "analysis_id": saved_analysis.id,
            **report_data,
        }

    except HTTPException:
        raise

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"ATS analysis failed: {str(exc)}",
        ) from exc