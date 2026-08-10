from typing import Dict


class OverallATSScorer:
    """
    Calculates the final ATS score from individual category scores.

    All weights are normalized to a total of 100.
    """

    WEIGHTS = {
        "skills": 35,
        "experience": 25,
        "projects": 15,
        "education": 10,
        "certifications": 5,
        "structure": 5,
        "achievements": 3,
        "formatting": 2,
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
                "skills": 90,
                "experience": 70,
                "projects": 80,
                "education": 90,
                "certifications": 60
            }

        Missing categories contribute 0.
        """

        weighted_score = 0.0
        total_weight = sum(cls.WEIGHTS.values())

        if total_weight == 0:
            return 0

        for category, weight in cls.WEIGHTS.items():
            score = scores.get(category, 0)

            # Protect against invalid values.
            score = max(0.0, min(float(score), 100.0))

            weighted_score += score * weight

        final_score = weighted_score / total_weight

        return round(
            max(0.0, min(final_score, 100.0))
        )