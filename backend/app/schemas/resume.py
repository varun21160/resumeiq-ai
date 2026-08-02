from datetime import datetime
from pydantic import BaseModel


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