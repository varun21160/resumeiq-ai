from datetime import datetime
from typing import Any, Dict, List

from pydantic import BaseModel, Field


class GeneratedResumeCreate(BaseModel):
    job_description: str = Field(
        min_length=20,
    )


class GeneratedResumeResponse(BaseModel):
    id: str
    resume_id: str
    job_description: str
    ats_score: int
    generated_resume: Dict[str, Any]
    changes: List[str]
    created_at: datetime

    class Config:
        from_attributes = True