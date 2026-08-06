import re

from app.ai.recommendation_builder import RecommendationBuilder
from app.schemas.analyzer import AnalyzerResponse


class ExperienceAnalyzer:
    """
    Analyze the experience section of a resume.
    """

    ROLE_KEYWORDS = [
        "data analyst",
        "business analyst",
        "software engineer",
        "backend developer",
        "frontend developer",
        "full stack developer",
        "machine learning engineer",
        "data scientist",
        "python developer",
        "ai engineer",
    ]

    @classmethod
    def analyze(
        cls,
        resume_text: str,
        job_description: str,
    ) -> AnalyzerResponse:

        resume = resume_text.lower()
        jd = job_description.lower()

        matched_roles = []

        for role in cls.ROLE_KEYWORDS:
            if role in resume and role in jd:
                matched_roles.append(role)

        years = cls.extract_years(resume)

        score = cls.calculate_score(
            years,
            len(matched_roles),
        )

        recommendations = RecommendationBuilder.experience_recommendations(
            years=years,
            matched_roles=matched_roles,
        )

        return AnalyzerResponse(
            score=score,
            details={
                "years_of_experience": years,
                "matched_roles": matched_roles,
            },
            recommendations=recommendations,
        )

    @staticmethod
    def extract_years(text: str) -> int:
        """
        Extract years like:
        2 years
        3+ years
        5 yrs
        """

        matches = re.findall(
            r"(\d+)\s*(?:\+)?\s*(?:years?|yrs?)",
            text,
        )

        if not matches:
            return 0

        return max(int(x) for x in matches)

    @staticmethod
    def calculate_score(
        years: int,
        matched_roles: int,
    ) -> int:

        score = 0

        score += min(years * 15, 60)

        score += min(matched_roles * 20, 40)

        return min(score, 100)