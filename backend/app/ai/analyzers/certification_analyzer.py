import re
from typing import List

from app.schemas.analyzer import AnalyzerResponse


class CertificationAnalyzer:
    """
    Deterministic certification analyzer.

    Detects:
    - Certification section
    - Individual certification entries
    - Certification providers
    - Relevant certifications based on JD
    """

    CERTIFICATION_HEADERS = {
        "certifications",
        "certification",
        "certificates",
        "certificate",
        "licenses & certifications",
        "licenses and certifications",
        "professional certifications",
        "certificates and training",
    }

    SECTION_HEADERS = {
        "education",
        "experience",
        "work experience",
        "professional experience",
        "employment",
        "employment history",
        "internship",
        "internships",
        "internship experience",
        "projects",
        "project experience",
        "academic projects",
        "technical projects",
        "skills",
        "technical skills",
        "achievements",
        "accomplishments",
        "awards",
        "honors",
        "honours",
        "publications",
        "research publications",
        "papers",
        "volunteering",
        "volunteer experience",
        "leadership",
        "leadership experience",
        "extracurricular",
        "extracurricular activities",
        "activities",
        "summary",
        "objective",
        "contact",
        "contact information",
        "references",
    }

    CERTIFICATION_PROVIDERS = [
        "nptel",
        "hackerrank",
        "coursera",
        "udemy",
        "simplilearn",
        "cisco",
        "infosys springboard",
        "tata",
        "tata group",
        "forage",
        "google",
        "microsoft",
        "aws",
        "amazon web services",
        "ibm",
        "oracle",
        "meta",
        "linkedin learning",
        "hp life",
        "accenture",
        "deloitte",
        "pwc",
        "ey",
        "kpmg",
    ]

    RELEVANCE_KEYWORDS = [
        "data",
        "analytics",
        "data analytics",
        "data science",
        "python",
        "sql",
        "power bi",
        "tableau",
        "excel",
        "machine learning",
        "artificial intelligence",
        "ai",
        "generative ai",
        "genai",
        "statistics",
        "business intelligence",
        "business analytics",
        "cloud",
        "aws",
        "azure",
        "gcp",
        "database",
        "programming",
        "software",
    ]

    @classmethod
    def analyze(
        cls,
        resume_text: str,
        job_description: str,
    ) -> AnalyzerResponse:

        resume_text = resume_text or ""
        job_description = job_description or ""

        certification_section = cls.extract_certification_section(
            resume_text
        )

        certifications = cls.extract_certifications(
            certification_section
        )

        # Fallback only when the section itself is not usable.
        if not certifications:
            certifications = cls.extract_certifications_from_text(
                resume_text
            )

        relevant_certifications = cls.find_relevant_certifications(
            certifications,
            job_description,
        )

        certification_count = len(certifications)

        score = cls.calculate_score(
            certification_count=certification_count,
            relevant_count=len(relevant_certifications),
        )

        recommendations = []

        if certification_count == 0:
            recommendations.append(
                "Add relevant certifications if they strengthen your application."
            )

        elif not relevant_certifications:
            recommendations.append(
                "Add certifications that align more closely with the job description."
            )

        elif certification_count < 2:
            recommendations.append(
                "Consider earning more certifications related to your target role."
            )

        return AnalyzerResponse(
            score=score,
            details={
                "certification_count": certification_count,
                "certifications": certifications,
                "relevant_certifications": relevant_certifications,
            },
            recommendations=sorted(set(recommendations)),
        )

    # ============================================================
    # SECTION EXTRACTION
    # ============================================================

    @classmethod
    def extract_certification_section(
        cls,
        text: str,
    ) -> str:

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        if not lines:
            return ""

        start_index = None

        for index, line in enumerate(lines):

            normalized = cls.normalize_heading(line)

            if normalized in cls.CERTIFICATION_HEADERS:
                start_index = index + 1
                break

        if start_index is None:
            return ""

        section_lines = []

        for line in lines[start_index:]:

            normalized = cls.normalize_heading(line)

            if normalized in cls.SECTION_HEADERS:
                break

            section_lines.append(line)

        return "\n".join(section_lines).strip()

    # ============================================================
    # CERTIFICATION EXTRACTION
    # ============================================================

    @classmethod
    def extract_certifications(
        cls,
        section_text: str,
    ) -> List[str]:

        if not section_text.strip():
            return []

        certifications = []

        lines = [
            line.strip()
            for line in section_text.splitlines()
            if line.strip()
        ]

        for line in lines:

            cleaned = re.sub(
                r"^[\-\*\u2022\d\.\)\s]+",
                "",
                line,
            ).strip()

            if not cleaned:
                continue

            # Ignore obvious date lines.
            if re.fullmatch(
                r"(19|20)\d{2}"
                r"(?:\s*[-–—]\s*"
                r"(?:(19|20)\d{2}|present))?",
                cleaned,
                re.IGNORECASE,
            ):
                continue

            # Ignore URLs.
            if re.search(
                r"https?://|www\.|github\.com|linkedin\.com",
                cleaned,
                re.IGNORECASE,
            ):
                continue

            # Ignore contact information accidentally placed
            # inside the certification section.
            if cls.is_contact_line(cleaned):
                continue

            # Ignore obvious non-certification headings.
            if cls.normalize_heading(cleaned) in cls.SECTION_HEADERS:
                continue

            # A certification entry must look like a certification.
            if cls.looks_like_certification(cleaned):
                certifications.append(
                    cls.normalize_certification(cleaned)
                )

        return cls.unique_preserve_order(certifications)

    # ============================================================
    # FALLBACK EXTRACTION
    # ============================================================

    @classmethod
    def extract_certifications_from_text(
        cls,
        text: str,
    ) -> List[str]:

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        certifications = []

        for line in lines:

            cleaned = re.sub(
                r"^[\-\*\u2022\d\.\)\s]+",
                "",
                line,
            ).strip()

            if not cleaned:
                continue

            if cls.is_contact_line(cleaned):
                continue

            if cls.looks_like_certification(cleaned):
                certifications.append(
                    cls.normalize_certification(cleaned)
                )

        return cls.unique_preserve_order(certifications)

    # ============================================================
    # CERTIFICATION VALIDATION
    # ============================================================

    @classmethod
    def looks_like_certification(
        cls,
        line: str,
    ) -> bool:

        lowered = line.lower()

        provider_found = any(
            provider in lowered
            for provider in cls.CERTIFICATION_PROVIDERS
        )

        certification_word_found = any(
            keyword in lowered
            for keyword in [
                "certification",
                "certificate",
                "certified",
                "course",
                "job simulation",
                "virtual experience",
                "professional certificate",
            ]
        )

        # Known provider + reasonable title.
        if provider_found and len(line.split()) >= 2:
            return True

        # Generic certification title.
        if certification_word_found:
            return True

        return False

    # ============================================================
    # CONTACT FILTER
    # ============================================================

    @staticmethod
    def is_contact_line(
        line: str,
    ) -> bool:

        lowered = line.lower().strip()

        # Email
        if re.search(
            r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
            line,
            re.IGNORECASE,
        ):
            return True

        # Phone numbers
        if re.search(
            r"(?:\+?\d[\d\s().-]{8,}\d)",
            line,
        ):
            return True

        # Contact headings
        if lowered in {
            "contact",
            "contact information",
            "phone",
            "email",
            "mobile",
            "linkedin",
            "github",
        }:
            return True

        return False

    # ============================================================
    # NORMALIZATION
    # ============================================================

    @staticmethod
    def normalize_heading(
        text: str,
    ) -> str:

        text = text.strip().lower()

        text = re.sub(
            r"^[\-\*\u2022\d\.\)\s]+",
            "",
            text,
        )

        text = re.sub(
            r"[:|]+$",
            "",
            text,
        )

        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        return text.strip()

    @staticmethod
    def normalize_certification(
        text: str,
    ) -> str:

        text = re.sub(
            r"^[\-\*\u2022]+",
            "",
            text,
        ).strip()

        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        return text

    # ============================================================
    # RELEVANCE
    # ============================================================

    @classmethod
    def find_relevant_certifications(
        cls,
        certifications: List[str],
        job_description: str,
    ) -> List[str]:

        if not certifications:
            return []

        jd_lower = job_description.lower()

        jd_keywords = [
            keyword
            for keyword in cls.RELEVANCE_KEYWORDS
            if keyword in jd_lower
        ]

        relevant = []

        for certification in certifications:

            cert_lower = certification.lower()

            provider_match = any(
                provider in cert_lower
                and provider in jd_lower
                for provider in cls.CERTIFICATION_PROVIDERS
            )

            keyword_match = any(
                keyword in cert_lower
                for keyword in jd_keywords
            )

            strong_match = (
                (
                    "nptel" in cert_lower
                    and (
                        "python" in cert_lower
                        or "data" in cert_lower
                    )
                )
                or (
                    "hackerrank" in cert_lower
                    and "sql" in cert_lower
                )
                or (
                    "tata" in cert_lower
                    and (
                        "data" in cert_lower
                        or "genai" in cert_lower
                        or "analytics" in cert_lower
                    )
                )
                or (
                    "cisco" in cert_lower
                    and (
                        "data" in cert_lower
                        or "ai" in cert_lower
                    )
                )
                or (
                    "power bi" in cert_lower
                    and "power bi" in jd_lower
                )
            )

            if (
                provider_match
                or keyword_match
                or strong_match
            ):
                relevant.append(certification)

        return cls.unique_preserve_order(relevant)

    # ============================================================
    # SCORE
    # ============================================================

    @staticmethod
    def calculate_score(
        certification_count: int,
        relevant_count: int,
    ) -> int:

        if certification_count == 0:
            return 0

        quantity_score = min(
            certification_count * 15,
            45,
        )

        relevance_score = min(
            relevant_count * 15,
            55,
        )

        return min(
            quantity_score + relevance_score,
            100,
        )

    # ============================================================
    # UTILITY
    # ============================================================

    @staticmethod
    def unique_preserve_order(
        items: List[str],
    ) -> List[str]:

        seen = set()
        result = []

        for item in items:

            key = item.lower().strip()

            if key not in seen:
                seen.add(key)
                result.append(item)

        return result