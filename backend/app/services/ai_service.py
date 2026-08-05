from app.ai.gemini_client import gemini_client
from app.ai.prompts import (
    build_cover_letter_prompt,
    build_interview_prompt,
    build_resume_review_prompt,
    build_resume_tailor_prompt,
)


class AIService:
    """
    Business logic for AI-powered features.
    """

    @staticmethod
    def review_resume(resume_text: str) -> str:
        prompt = build_resume_review_prompt(resume_text)
        return gemini_client.generate(prompt)

    @staticmethod
    def tailor_resume(
        resume_text: str,
        job_description: str,
    ) -> str:
        prompt = build_resume_tailor_prompt(
            resume_text,
            job_description,
        )
        return gemini_client.generate(prompt)

    @staticmethod
    def generate_cover_letter(
        resume_text: str,
        company: str,
        job_title: str,
        job_description: str,
    ) -> str:
        prompt = build_cover_letter_prompt(
            resume_text,
            company,
            job_title,
            job_description,
        )
        return gemini_client.generate(prompt)

    @staticmethod
    def generate_interview_questions(
        resume_text: str,
        job_description: str,
    ) -> str:
        prompt = build_interview_prompt(
            resume_text,
            job_description,
        )
        return gemini_client.generate(prompt)