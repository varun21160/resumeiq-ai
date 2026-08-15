from typing import List

from sqlalchemy.orm import Session

from app.models.generated_resume import GeneratedResume


class GeneratedResumeService:
    """
    Database operations for generated resumes.
    """

    @staticmethod
    def create(
        db: Session,
        *,
        user_id: str,
        resume_id: str,
        job_description: str,
        ats_score: int,
        generated_resume: dict,
        changes: List[str],
    ) -> GeneratedResume:

        record = GeneratedResume(
            user_id=user_id,
            resume_id=resume_id,
            job_description=job_description,
            ats_score=ats_score,
            generated_resume=generated_resume,
            changes=changes,
        )

        db.add(record)
        db.commit()
        db.refresh(record)

        return record

    @staticmethod
    def get_by_id(
        db: Session,
        *,
        generated_resume_id: str,
        user_id: str,
    ) -> GeneratedResume | None:

        return (
            db.query(GeneratedResume)
            .filter(
                GeneratedResume.id == generated_resume_id,
                GeneratedResume.user_id == user_id,
            )
            .first()
        )

    @staticmethod
    def get_all(
        db: Session,
        *,
        user_id: str,
    ) -> list[GeneratedResume]:

        return (
            db.query(GeneratedResume)
            .filter(
                GeneratedResume.user_id == user_id,
            )
            .order_by(
                GeneratedResume.created_at.desc()
            )
            .all()
        )

    @staticmethod
    def delete(
        db: Session,
        record: GeneratedResume,
    ) -> None:

        db.delete(record)
        db.commit()