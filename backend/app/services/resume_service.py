from sqlalchemy.orm import Session

from app.models.resume import Resume
from app.repositories.resume_repository import ResumeRepository


class ResumeService:

    def __init__(self):
        self.repository = ResumeRepository()

    def create_resume(self, db: Session, resume: Resume):
        return self.repository.create(db, resume)

    def get_resumes(self, db: Session, user_id: str):
        return self.repository.get_all_by_user(db, user_id)

    def get_resume(self, db: Session, resume_id: str, user_id: str):
        return self.repository.get_by_id(
            db,
            resume_id,
            user_id,
        )

    def delete_resume(self, db: Session, resume: Resume):
        self.repository.delete(db, resume)