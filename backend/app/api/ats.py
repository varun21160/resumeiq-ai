from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.ai.ats_report_engine import ATSReportEngine
from app.database.session import get_db
from app.models.user import User
from app.core.security import get_current_user


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


@router.post("/analyze")
def analyze_resume(
    request: ATSAnalyzeRequest,
    current_user: User = Depends(get_current_user),
):
    try:
        report = ATSReportEngine.generate(
            resume_text=request.resume_text,
            job_description=request.job_description,
        )

        return report

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"ATS analysis failed: {str(exc)}",
        )