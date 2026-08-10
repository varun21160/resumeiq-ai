from typing import Dict


class OverallATSScorer:
    """
    Calculates the final ATS score from analyzer category scores.

    All weights add up to exactly 100.

    Current scoring model:

        Skills          35%
        Experience      20%
        Projects        15%
        Education       10%
        Certifications   5%
        Resume Quality  15%

    Total             100%
    """

    WEIGHTS = {
        "skills": 35,
        "experience": 20,
        "projects": 15,
        "education": 10,
        "certifications": 5,
        "resume_quality": 15,
    }

    @classmethod
    def calculate(
        cls,
        scores: Dict[str, float],
    ) -> int:
        """
        Calculate the weighted overall ATS score.

        Example:

        {
            "skills": 81,
            "experience": 70,
            "projects": 100,
            "education": 100,
            "certifications": 70,
            "resume_quality": 88,
        }

        Returns:
            Integer score between 0 and 100.
        """

        total = 0.0

        for category, weight in cls.WEIGHTS.items():

            score = scores.get(
                category,
                0,
            )

            # Keep every category within a valid range.
            score = max(
                0,
                min(
                    float(score),
                    100,
                ),
            )

            total += (
                score * weight / 100
            )

        return round(
            max(
                0,
                min(
                    total,
                    100,
                ),
            )
        )