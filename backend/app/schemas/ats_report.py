from typing import Dict, List

from pydantic import BaseModel

from app.schemas.analyzer import AnalyzerResponse


class ATSReport(BaseModel):
    overall_score: int

    category_scores: Dict[str, int]

    analysis: Dict[str, AnalyzerResponse]

    recommendations: List[str]