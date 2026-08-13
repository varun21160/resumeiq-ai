from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.ats_analysis import (
    ATSAnalysisListResponse,
    ATSAnalysisResponse,
)
from app.services.ats_analysis_service import ATSAnalysisService


router = APIRouter(
    prefix="/analyses",
    tags=["ATS Analysis History"],
)


@router.get(
    "",
    response_model=ATSAnalysisListResponse,
)
def get_analysis_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get all ATS analyses belonging to the current user.
    """

    analyses = ATSAnalysisService.get_analyses(
        db=db,
        user_id=current_user.id,
    )

    return {
        "analyses": [
            ATSAnalysisService.to_response(
                analysis
            )
            for analysis in analyses
        ]
    }


@router.get(
    "/{analysis_id}",
    response_model=ATSAnalysisResponse,
)
def get_analysis(
    analysis_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get one ATS analysis belonging to the current user.
    """

    analysis = ATSAnalysisService.get_analysis(
        db=db,
        analysis_id=analysis_id,
        user_id=current_user.id,
    )

    if analysis is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ATS analysis not found.",
        )

    return ATSAnalysisService.to_response(
        analysis
    )


@router.delete(
    "/{analysis_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_analysis(
    analysis_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete one ATS analysis belonging to the current user.
    """

    analysis = ATSAnalysisService.get_analysis(
        db=db,
        analysis_id=analysis_id,
        user_id=current_user.id,
    )

    if analysis is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ATS analysis not found.",
        )

    ATSAnalysisService.delete_analysis(
        db=db,
        analysis=analysis,
    )

    return