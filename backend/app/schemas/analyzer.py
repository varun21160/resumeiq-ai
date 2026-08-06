from typing import Any, Dict, List

from pydantic import BaseModel, Field


class AnalyzerResponse(BaseModel):
    """
    Standard response returned by every analyzer.
    """

    score: int = Field(..., ge=0, le=100)

    details: Dict[str, Any] = Field(default_factory=dict)

    recommendations: List[str] = Field(default_factory=list)