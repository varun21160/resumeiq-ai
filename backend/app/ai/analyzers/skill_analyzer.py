from app.ai.keyword_extractor import KeywordExtractor
from app.ai.recommendation_builder import RecommendationBuilder
from app.ai.skill_scorer import SkillScorer
from app.schemas.analyzer import AnalyzerResponse


class SkillAnalyzer:
    """
    Responsible for analyzing resume skills against a job description.
    """

    @staticmethod
    def analyze(
        resume_text: str,
        job_description: str,
    ) -> AnalyzerResponse:

        # Extract skills
        resume_skills = KeywordExtractor.extract(resume_text)
        jd_skills = KeywordExtractor.extract(job_description)

        # Calculate skill score
        result = SkillScorer.calculate(
            resume_skills,
            jd_skills,
        )

        # Skills not required by the job description
        extra_skills = sorted(
            list(set(resume_skills) - set(jd_skills))
        )

        recommendations = RecommendationBuilder.skill_recommendations(
            missing_skills=result["missing_skills"],
            extra_skills=extra_skills,
        )

        return AnalyzerResponse(
            score=result["score"],
            details={
                "matched_skills": result["matched_skills"],
                "missing_skills": result["missing_skills"],
                "extra_skills": extra_skills,
                "resume_skills": sorted(resume_skills),
                "job_description_skills": sorted(jd_skills),
            },
            recommendations=recommendations,
        )