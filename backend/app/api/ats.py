from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.ats import ATSRequest, ATSResponse
from app.services.ats_service import ATSService

router = APIRouter(
    prefix="/ats",
    tags=["ATS"],
)


@router.post(
    "/analyze",
    response_model=ATSResponse,
)
def analyze_resume(
    request: ATSRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ATSService()

    result = service.analyze_resume(
        db=db,
        resume_id=request.resume_id,
        user_id=current_user.id,
        job_description=request.job_description,
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Resume not found.",
        )

    return result