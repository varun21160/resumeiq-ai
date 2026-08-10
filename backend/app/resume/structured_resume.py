from typing import Dict, List, Optional

from app.resume.section_detector import SectionDetector


class StructuredResumeExtractor:
    """
    Converts detected resume sections into a normalized
    structured representation.
    """

    SECTION_KEYS = [
        "header",
        "summary",
        "skills",
        "experience",
        "internships",
        "projects",
        "education",
        "certifications",
        "achievements",
        "publications",
        "volunteering",
        "leadership",
        "extracurricular",
    ]

    @classmethod
    def extract(
        cls,
        resume_text: str,
    ) -> Dict[str, object]:
        """
        Extract a structured representation of the resume.
        """

        if not resume_text or not resume_text.strip():
            raise ValueError(
                "Resume text cannot be empty."
            )

        sections = SectionDetector.detect(
            resume_text
        )

        structured = {}

        for key in cls.SECTION_KEYS:
            structured[key] = sections.get(
                key,
                "",
            )

        structured["full_text"] = resume_text.strip()

        structured["detected_sections"] = [
            key
            for key in cls.SECTION_KEYS
            if structured[key]
        ]

        return structured

    @staticmethod
    def get_section(
        structured_resume: Dict[str, object],
        section: str,
    ) -> str:
        """
        Safely retrieve a specific resume section.
        """

        value = structured_resume.get(
            section,
            "",
        )

        if not isinstance(value, str):
            return ""

        return value.strip()