from datetime import datetime
from typing import Any, Dict, List

from pydantic import BaseModel, Field


class ATSAnalysisResponse(BaseModel):
    """
    Response schema for a saved ATS analysis.
    """

    id: str

    user_id: str

    resume_id: str

    job_description: str

    overall_score: int = Field(
        ge=0,
        le=100,
    )

    category_scores: Dict[str, int]

    analysis: Dict[str, Any]

    recommendations: List[str]

    created_at: datetime

    class Config:
        from_attributes = True


class ATSAnalysisListResponse(BaseModel):
    """
    Response schema for ATS analysis history.
    """

    analyses: List[ATSAnalysisResponse]