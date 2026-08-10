from typing import Any, Dict, List

from pydantic import BaseModel, Field

from app.schemas.analyzer import AnalyzerResponse


class ATSReport(BaseModel):
    """
    Complete ATS analysis report.

    Deterministic analyzers provide numerical scores.
    Semantic analysis provides contextual AI insights.
    """

    overall_score: int = Field(
        ge=0,
        le=100,
    )

    category_scores: Dict[str, int]

    analysis: Dict[str, Any]

    recommendations: List[str] = Field(
        default_factory=list
    )