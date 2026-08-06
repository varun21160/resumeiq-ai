from app.ai.recommendation_builder import RecommendationBuilder
from app.schemas.analyzer import AnalyzerResponse


class ProjectAnalyzer:
    """
    Analyze projects in a resume.
    """

    PROJECT_KEYWORDS = [
        "project",
        "developed",
        "built",
        "implemented",
        "created",
        "designed",
    ]

    TECH_KEYWORDS = [
        "python",
        "sql",
        "power bi",
        "tableau",
        "excel",
        "fastapi",
        "django",
        "flask",
        "docker",
        "aws",
        "azure",
        "gcp",
        "react",
        "javascript",
        "pandas",
        "numpy",
        "tensorflow",
        "pytorch",
        "machine learning",
    ]

    @classmethod
    def analyze(
        cls,
        resume_text: str,
        job_description: str,
    ) -> AnalyzerResponse:

        resume = resume_text.lower()
        jd = job_description.lower()

        project_count = sum(
            resume.count(keyword)
            for keyword in cls.PROJECT_KEYWORDS
        )

        matched_tech = sorted(
            [
                tech
                for tech in cls.TECH_KEYWORDS
                if tech in resume and tech in jd
            ]
        )

        has_github = (
            "github.com" in resume
            or "github" in resume
        )

        has_portfolio = (
            "portfolio" in resume
            or "vercel" in resume
            or "netlify" in resume
        )

        score = cls.calculate_score(
            project_count,
            len(matched_tech),
            has_github,
            has_portfolio,
        )

        recommendations = RecommendationBuilder.project_recommendations(
            project_count=project_count,
            github=has_github,
            portfolio=has_portfolio,
        )

        return AnalyzerResponse(
            score=score,
            details={
                "project_count": project_count,
                "matched_technologies": matched_tech,
                "github": has_github,
                "portfolio": has_portfolio,
            },
            recommendations=recommendations,
        )

    @staticmethod
    def calculate_score(
        projects: int,
        tech: int,
        github: bool,
        portfolio: bool,
    ) -> int:

        score = 0

        score += min(projects * 20, 40)

        score += min(tech * 8, 40)

        if github:
            score += 10

        if portfolio:
            score += 10

        return min(score, 100)