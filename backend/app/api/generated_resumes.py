from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.generated_resume import GeneratedResumeResponse
from app.services.generated_resume_service import GeneratedResumeService


router = APIRouter(
    prefix="/generated-resumes",
    tags=["Generated Resumes"],
)


@router.get(
    "",
    response_model=list[GeneratedResumeResponse],
)
def get_generated_resumes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return GeneratedResumeService.get_all(
        db,
        user_id=current_user.id,
    )


@router.get(
    "/{generated_resume_id}",
    response_model=GeneratedResumeResponse,
)
def get_generated_resume(
    generated_resume_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    record = GeneratedResumeService.get_by_id(
        db,
        generated_resume_id=generated_resume_id,
        user_id=current_user.id,
    )

    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Generated resume not found.",
        )

    return record


@router.delete(
    "/{generated_resume_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_generated_resume(
    generated_resume_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    record = GeneratedResumeService.get_by_id(
        db,
        generated_resume_id=generated_resume_id,
        user_id=current_user.id,
    )

    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Generated resume not found.",
        )

    GeneratedResumeService.delete(
        db,
        record,
    )

    return