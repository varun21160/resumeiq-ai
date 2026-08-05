from sqlalchemy.orm import Session

from app.ai.ats_engine import ATSEngine
from app.repositories.resume_repository import ResumeRepository


class ATSService:

    def __init__(self):
        self.repository = ResumeRepository()

    def analyze_resume(
        self,
        db: Session,
        resume_id: str,
        user_id: str,
        job_description: str,
    ):
        resume = self.repository.get_by_id(
            db,
            resume_id,
            user_id,
        )

        if resume is None:
            return None

        return ATSEngine.analyze(
            resume.extracted_text or "",
            job_description,
        )