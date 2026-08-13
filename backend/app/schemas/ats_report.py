from typing import Any, Dict, List

from pydantic import BaseModel, Field


class ATSAnalyzeRequest(BaseModel):
    resume_text: str = Field(
        ...,
        min_length=50,
        description="Extracted resume text",
    )

    job_description: str = Field(
        ...,
        min_length=20,
        description="Target job description",
    )

    resume_id: str | None = Field(
        default=None,
        description="Optional resume ID associated with this analysis",
    )


class ATSReport(BaseModel):
    """
    Complete ATS analysis report.

    Deterministic analyzers provide numerical scores.
    """

    overall_score: int = Field(
        ge=0,
        le=100,
    )

    category_scores: Dict[str, int]

    analysis: Dict[str, Any]

    recommendations: List[str] = Field(
        default_factory=list,
    )


class ATSAnalysisResponse(ATSReport):
    """
    ATS report returned after saving the analysis.
    """

    id: str
    resume_id: str | None
    created_at: Any

    class Config:
        from_attributes = True