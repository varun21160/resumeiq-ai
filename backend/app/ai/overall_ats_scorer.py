from typing import Dict


class OverallATSScorer:
    """
    Calculates the final ATS score from analyzer category scores.

    Scoring weights:

        Skills           35%
        Experience      20%
        Projects        15%
        Education       10%
        Certifications   5%
        Resume Quality  15%

        Total           100%
    """

    WEIGHTS = {
        "skills": 35,
        "experience": 20,
        "projects": 15,
        "education": 10,
        "certifications": 5,
        "resume_quality": 15,
    }

    REQUIRED_CATEGORIES = tuple(WEIGHTS.keys())

    @classmethod
    def _validate_weights(cls) -> None:
        """
        Ensure scoring weights are correctly configured.
        """

        total_weight = sum(cls.WEIGHTS.values())

        if total_weight != 100:
            raise ValueError(
                f"ATS scoring weights must total 100. "
                f"Current total: {total_weight}"
            )

    @classmethod
    def _normalize_score(cls, score) -> float:
        """
        Convert a category score to a valid value between 0 and 100.
        """

        try:
            score = float(score)
        except (TypeError, ValueError):
            return 0.0

        return max(
            0.0,
            min(score, 100.0),
        )

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
                "certifications": 90,
                "resume_quality": 88,
            }

        Returns:
            Integer score between 0 and 100.
        """

        if not isinstance(scores, dict):
            raise ValueError(
                "ATS scores must be provided as a dictionary."
            )

        cls._validate_weights()

        total = 0.0

        for category, weight in cls.WEIGHTS.items():

            # Missing categories are treated as zero.
            raw_score = scores.get(
                category,
                0,
            )

            score = cls._normalize_score(
                raw_score
            )

            weighted_score = (
                score * weight / 100
            )

            total += weighted_score

        # Keep the final result within ATS score limits.
        total = max(
            0.0,
            min(total, 100.0),
        )

        return int(
            round(total)
        )