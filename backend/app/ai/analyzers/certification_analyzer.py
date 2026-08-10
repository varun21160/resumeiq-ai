from typing import List

from app.ai.recommendation_builder import RecommendationBuilder
from app.schemas.analyzer import AnalyzerResponse


class CertificationAnalyzer:
    """
    Analyze certifications in a resume.

    Detects:
    - Certification providers
    - Certification-related keywords
    - Relevant certifications based on the job description
    - Certification recommendations
    """

    CERTIFICATION_KEYWORDS = [
        "aws certified",
        "aws certification",
        "microsoft certified",
        "microsoft certification",
        "azure certification",
        "azure certified",
        "google cloud certification",
        "google certified",
        "oracle certification",
        "oracle certified",
        "cisco certification",
        "cisco certified",
        "ibm certification",
        "ibm certified",
        "coursera",
        "udemy",
        "nptel",
        "edx",
        "linkedin learning",
        "hackerrank",
        "meta certification",
        "meta certified",
        "databricks certification",
        "databricks certified",
        "snowflake certification",
        "snowflake certified",
        "power bi certification",
        "power bi certified",
        "tableau certification",
        "tableau certified",
    ]

    CERTIFICATION_SECTION_HEADERS = [
        "certifications",
        "certification",
        "certificates",
        "certificate",
        "professional certifications",
        "professional certificates",
        "licenses & certifications",
        "licenses and certifications",
    ]

    SECTION_HEADERS = {
        "education",
        "experience",
        "work experience",
        "professional experience",
        "projects",
        "skills",
        "technical skills",
        "achievements",
        "summary",
        "objective",
        "internships",
        "employment",
    }

    CERTIFICATION_PHRASES = [
        "certified",
        "certification",
        "certificate",
        "certification course",
        "professional certificate",
        "course completion",
    ]

    @classmethod
    def analyze(
        cls,
        resume_text: str,
        job_description: str,
    ) -> AnalyzerResponse:
        """
        Analyze certifications in the resume against
        the target job description.
        """

        certification_section = (
            cls.extract_certification_section(
                resume_text
            )
        )

        resume_lower = resume_text.lower()
        jd_lower = job_description.lower()

        found_certifications = (
            cls.extract_certifications(
                certification_section,
                resume_lower,
            )
        )

        relevant_certifications = (
            cls.find_relevant_certifications(
                found_certifications,
                jd_lower,
            )
        )

        score = cls.calculate_score(
            total=len(found_certifications),
            relevant=len(
                relevant_certifications
            ),
        )

        recommendations = (
            RecommendationBuilder
            .certification_recommendations(
                certification_count=len(
                    found_certifications
                ),
                relevant_count=len(
                    relevant_certifications
                ),
            )
        )

        return AnalyzerResponse(
            score=score,
            details={
                "certification_count": len(
                    found_certifications
                ),
                "certifications": found_certifications,
                "relevant_certifications": (
                    relevant_certifications
                ),
            },
            recommendations=recommendations,
        )

    @classmethod
    def extract_certification_section(
        cls,
        text: str,
    ) -> str:
        """
        Extract the certification section while
        preserving line structure.

        If no certification section exists,
        the complete resume is returned so that
        inline certifications can still be detected.
        """

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        if not lines:
            return ""

        start_index = None

        for index, line in enumerate(lines):

            normalized = (
                line.lower()
                .strip(" :-")
            )

            if normalized in (
                cls.CERTIFICATION_SECTION_HEADERS
            ):
                start_index = index + 1
                break

        if start_index is None:
            return text

        certification_lines = []

        for line in lines[start_index:]:

            normalized = (
                line.lower()
                .strip(" :-")
            )

            if normalized in cls.SECTION_HEADERS:
                break

            certification_lines.append(line)

        return "\n".join(
            certification_lines
        )

    @classmethod
    def extract_certifications(
        cls,
        certification_section: str,
        complete_resume: str,
    ) -> List[str]:
        """
        Extract certification names.

        Section-based detection is preferred because it
        reduces false positives from skills and projects.
        """

        found = []

        # First inspect the certification section.
        for certification in cls.CERTIFICATION_KEYWORDS:

            if cls.contains_phrase(
                certification_section,
                certification,
            ):
                found.append(certification)

        # If no certification section was detected,
        # inspect the complete resume for explicit
        # certification language.
        if not found:

            for certification in (
                cls.CERTIFICATION_KEYWORDS
            ):

                if cls.contains_phrase(
                    complete_resume,
                    certification,
                ):
                    found.append(certification)

        return sorted(
            set(found)
        )

    @classmethod
    def find_relevant_certifications(
        cls,
        certifications: List[str],
        job_description: str,
    ) -> List[str]:
        """
        Determine which detected certifications are
        relevant to the target job.

        A certification is considered relevant when
        its important keywords appear in the JD.
        """

        relevant = []

        for certification in certifications:

            if cls.contains_phrase(
                job_description,
                certification,
            ):
                relevant.append(
                    certification
                )
                continue

            # Handle provider/tool relationships.
            provider_keywords = (
                cls.get_related_keywords(
                    certification
                )
            )

            if any(
                cls.contains_phrase(
                    job_description,
                    keyword,
                )
                for keyword in provider_keywords
            ):
                relevant.append(
                    certification
                )

        return sorted(
            set(relevant)
        )

    @staticmethod
    def get_related_keywords(
        certification: str,
    ) -> List[str]:
        """
        Map certifications to related technologies
        so relevance is not dependent on an exact
        phrase match.
        """

        mappings = {
            "aws certified": [
                "aws",
                "amazon web services",
                "cloud",
            ],
            "aws certification": [
                "aws",
                "amazon web services",
                "cloud",
            ],
            "azure certification": [
                "azure",
                "microsoft azure",
                "cloud",
            ],
            "azure certified": [
                "azure",
                "microsoft azure",
                "cloud",
            ],
            "google cloud certification": [
                "google cloud",
                "gcp",
                "cloud",
            ],
            "google certified": [
                "google cloud",
                "gcp",
            ],
            "power bi certification": [
                "power bi",
                "business intelligence",
                "bi",
            ],
            "power bi certified": [
                "power bi",
                "business intelligence",
                "bi",
            ],
            "tableau certification": [
                "tableau",
                "data visualization",
                "visualization",
            ],
            "tableau certified": [
                "tableau",
                "data visualization",
                "visualization",
            ],
            "databricks certification": [
                "databricks",
                "spark",
                "pyspark",
            ],
            "databricks certified": [
                "databricks",
                "spark",
                "pyspark",
            ],
            "snowflake certification": [
                "snowflake",
                "data warehouse",
            ],
            "snowflake certified": [
                "snowflake",
                "data warehouse",
            ],
            "cisco certification": [
                "cisco",
                "networking",
                "ccna",
            ],
            "cisco certified": [
                "cisco",
                "networking",
                "ccna",
            ],
        }

        return mappings.get(
            certification,
            [certification],
        )

    @staticmethod
    def contains_phrase(
        text: str,
        phrase: str,
    ) -> bool:
        """
        Safely check whether a phrase exists
        in the supplied text.
        """

        text = text.lower()
        phrase = phrase.lower()

        return phrase in text

    @classmethod
    def calculate_score(
        cls,
        total: int,
        relevant: int,
    ) -> int:
        """
        Calculate certification score.

        Relevant certifications receive more weight
        than simply having many certifications.

        Maximum:
        - 30 points for certification coverage
        - 70 points for relevant certifications
        """

        if total == 0:
            return 0

        # Base certification coverage.
        coverage_score = min(
            total * 10,
            30,
        )

        # Relevance is more important.
        relevance_score = min(
            relevant * 20,
            70,
        )

        return min(
            coverage_score + relevance_score,
            100,
        )