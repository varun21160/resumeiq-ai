from app.ai.keyword_extractor import KeywordExtractor
from app.ai.skill_scorer import SkillScorer

class ATSEngine:

    @staticmethod
    def analyze(
        resume_text: str,
        job_description: str,
    ):
        """
        Complete ATS analysis pipeline.
        """

        resume_skills = KeywordExtractor.extract(resume_text)

        jd_skills = KeywordExtractor.extract(job_description)

        result = SkillScorer.calculate(
            resume_skills,
            jd_skills,
        )

        result["resume_skills"] = resume_skills
        result["job_description_skills"] = jd_skills

        return result