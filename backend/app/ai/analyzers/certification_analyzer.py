from app.ai.recommendation_builder import RecommendationBuilder
from app.schemas.analyzer import AnalyzerResponse


class CertificationAnalyzer:
    """
    Analyze certifications in a resume.
    """

    CERTIFICATION_KEYWORDS = [
        "aws",
        "microsoft",
        "azure",
        "google",
        "oracle",
        "cisco",
        "ibm",
        "coursera",
        "udemy",
        "nptel",
        "edx",
        "linkedin learning",
        "hackerrank",
        "meta",
        "databricks",
        "snowflake",
        "power bi",
        "tableau",
    ]

    @classmethod
    def analyze(
        cls,
        resume_text: str,
        job_description: str,
    ) -> AnalyzerResponse:

        resume = resume_text.lower()
        jd = job_description.lower()

        found_certifications = sorted([
            cert
            for cert in cls.CERTIFICATION_KEYWORDS
            if cert in resume
        ])

        relevant_certifications = sorted([
            cert
            for cert in found_certifications
            if cert in jd
        ])

        score = cls.calculate_score(
            len(found_certifications),
            len(relevant_certifications),
        )

        recommendations = RecommendationBuilder.certification_recommendations(
            certification_count=len(found_certifications),
            relevant_count=len(relevant_certifications),
        )

        return AnalyzerResponse(
            score=score,
            details={
                "certification_count": len(found_certifications),
                "certifications": found_certifications,
                "relevant_certifications": relevant_certifications,
            },
            recommendations=recommendations,
        )

    @staticmethod
    def calculate_score(
        total: int,
        relevant: int,
    ) -> int:

        score = 0

        score += min(total * 10, 50)

        score += min(relevant * 10, 50)

        return min(score, 100)