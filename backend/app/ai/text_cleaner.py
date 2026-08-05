import re

from app.ai.skill_aliases import SKILL_ALIASES


class TextCleaner:

    @staticmethod
    def clean(text: str) -> str:

        text = text.lower()

        # Replace aliases before removing punctuation
        for alias, canonical in SKILL_ALIASES.items():
            pattern = r"\b" + re.escape(alias) + r"\b"
            text = re.sub(pattern, canonical, text)

        text = re.sub(r"[^a-z0-9\s]", " ", text)

        text = re.sub(r"\s+", " ", text)

        return text.strip()