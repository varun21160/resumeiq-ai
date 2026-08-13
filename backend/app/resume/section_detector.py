import re
from typing import Dict, List


class SectionDetector:
    """
    Detects common resume sections from cleaned resume text.

    The detector is intentionally rule-based so that section
    boundaries remain predictable and explainable.
    """

    SECTION_ALIASES = {
        "summary": [
            "summary",
            "professional summary",
            "profile",
            "career summary",
            "objective",
            "career objective",
        ],
        "contact": [
            "contact",
            "contact information",
            "contact details",
        ],
        "skills": [
            "skills",
            "technical skills",
            "core skills",
            "technical competencies",
            "skills & technologies",
            "skills and technologies",
        ],
        "experience": [
            "experience",
            "work experience",
            "professional experience",
            "employment history",
            "work history",
        ],
        "internships": [
            "internship",
            "internships",
            "internship experience",
        ],
        "projects": [
            "projects",
            "academic projects",
            "technical projects",
            "personal projects",
            "key projects",
        ],
        "education": [
            "education",
            "academic background",
            "educational background",
            "academic qualifications",
        ],
        "certifications": [
            "certifications",
            "certificates",
            "licenses & certifications",
            "licenses and certifications",
        ],
        "achievements": [
            "achievements",
            "accomplishments",
            "awards",
            "honors",
            "honours",
        ],
        "publications": [
            "publications",
            "research publications",
            "papers",
        ],
        "volunteering": [
            "volunteering",
            "volunteer experience",
            "volunteer work",
        ],
        "leadership": [
            "leadership",
            "leadership experience",
        ],
        "extracurricular": [
            "extracurricular",
            "extracurricular activities",
            "activities",
        ],
    }

    @classmethod
    def detect(
        cls,
        text: str,
    ) -> Dict[str, str]:
        """
        Detect resume sections and return their extracted content.

        Example:

        {
            "skills": "...",
            "experience": "...",
            "projects": "...",
            "education": "..."
        }
        """

        if not text or not text.strip():
            return {}

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        section_positions = []

        for index, line in enumerate(lines):
            section = cls._identify_section(line)

            if section:
                section_positions.append(
                    (index, section)
                )

        if not section_positions:
            return {
                "full_text": text.strip()
            }

        sections: Dict[str, str] = {}

        # Text before the first recognized heading.
        first_position = section_positions[0][0]

        if first_position > 0:
            header_text = "\n".join(
                lines[:first_position]
            ).strip()

            if header_text:
                sections["header"] = header_text

        # Extract each section until the next heading.
        for position, (start_index, section_name) in enumerate(
            section_positions
        ):
            next_index = (
                section_positions[position + 1][0]
                if position + 1 < len(section_positions)
                else len(lines)
            )

            content = "\n".join(
                lines[start_index + 1:next_index]
            ).strip()

            if not content:
                continue

            # If a section appears more than once, merge it.
            if section_name in sections:
                sections[section_name] = (
                    sections[section_name]
                    + "\n"
                    + content
                ).strip()
            else:
                sections[section_name] = content

        return sections

    @classmethod
    def _identify_section(
        cls,
        line: str,
    ) -> str | None:
        """
        Identify whether a single line is a section heading.
        """

        normalized = cls._normalize_heading(line)

        if not normalized:
            return None

        for section_name, aliases in cls.SECTION_ALIASES.items():
            for alias in aliases:
                if normalized == cls._normalize_heading(alias):
                    return section_name

        return None

    @staticmethod
    def _normalize_heading(
        text: str,
    ) -> str:
        """
        Normalize a potential section heading.
        """

        text = text.lower().strip()

        # Remove common heading punctuation.
        text = re.sub(
            r"[:\-|]+$",
            "",
            text,
        )

        # Collapse whitespace.
        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        return text.strip()