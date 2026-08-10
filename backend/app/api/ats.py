from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.ai.ats_report_engine import ATSReportEngine
from app.core.security import get_current_user
from app.models.user import User


router = APIRouter(
    prefix="/ats",
    tags=["ATS Analysis"],
)


class ATSAnalyzeRequest(BaseModel):
    resume_text: str = Field(
        ...,
        min_length=50,
        description="Extracted resume text",
    )

    job_description: str = Field(
        ...,
        min_length=20,
        description="Target job description",
    )


# ---------------------------------------------------------
# ATS ROUTER HEALTH CHECK
# ---------------------------------------------------------

@router.get("/health")
def ats_health():
    return {
        "status": "healthy",
        "service": "ATS Analysis",
    }


# ---------------------------------------------------------
# ATS ANALYSIS
# ---------------------------------------------------------

@router.post("/analyze")
def analyze_resume(
    request: ATSAnalyzeRequest,
    current_user: User = Depends(get_current_user),
):
    """
    Analyze a resume against a target job description.

    Requires an authenticated user.
    """

    try:
        report = ATSReportEngine.generate(
            resume_text=request.resume_text,
            job_description=request.job_description,
        )

        return report

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