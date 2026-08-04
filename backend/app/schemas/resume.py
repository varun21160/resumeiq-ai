from datetime import datetime
from pydantic import BaseModel
from typing import List


class ResumeResponse(BaseModel):
    id: str
    original_filename: str
    file_type: str
    file_size: int
    version: int
    parsing_status: str
    created_at: datetime

    class Config:
        from_attributes = True

class ResumeListResponse(BaseModel):
    resumes: List[ResumeResponse]