from typing import Dict


class OverallATSScorer:
    """
    Combines analyzer scores into a final ATS score.
    """

    WEIGHTS = {
        "skills": 40,
        "experience": 25,
        "projects": 15,
        "education": 10,
        "structure": 5,
        "achievements": 5,
        "formatting": 5,
        "certifications":10,
    }

    @classmethod
    def calculate(cls, scores: Dict[str, float]) -> int:
        """
        scores example:
        {
            "skills": 90,
            "experience": 70,
            ...
        }
        """

        total = 0

        for category, weight in cls.WEIGHTS.items():
            total += scores.get(category, 0) * weight

        return round(total / 100)