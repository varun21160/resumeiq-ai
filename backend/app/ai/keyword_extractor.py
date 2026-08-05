import re

from app.ai.skill_dictionary import TECHNICAL_SKILLS
from app.ai.text_cleaner import TextCleaner


class KeywordExtractor:

    @staticmethod
    def extract(text: str):
        """
        Extract skills using whole-word matching.
        """

        cleaned_text = TextCleaner.clean(text)

        found_skills = []

        for skill in TECHNICAL_SKILLS:
            pattern = r"\b" + re.escape(skill) + r"\b"

            if re.search(pattern, cleaned_text):
                found_skills.append(skill)

        return sorted(set(found_skills))