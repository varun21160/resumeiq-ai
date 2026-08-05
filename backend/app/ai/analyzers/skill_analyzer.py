from typing import Dict, List

from app.ai.keyword_extractor import KeywordExtractor
from app.ai.skill_scorer import SkillScorer
from backend.app.ai.skill_scorer import SkillScorer


class SkillAnalyzer:
    """
    Responsible for skill analysis only.
    """

    @staticmethod
    def analyze(
        resume_text: str,
        job_description: str,
    ) -> Dict:

        resume_skills = KeywordExtractor.extract(
            resume_text
        )

        jd_skills = KeywordExtractor.extract(
            job_description
        )

        score = SkillScorer.calculate(
            resume_skills,
            jd_skills,
        )

        extra_skills = sorted(
            list(
                set(resume_skills)
                - set(jd_skills)
            )
        )

        return {
            **score,
            "resume_skills": sorted(resume_skills),
            "job_description_skills": sorted(jd_skills),
            "extra_skills": extra_skills,
        }