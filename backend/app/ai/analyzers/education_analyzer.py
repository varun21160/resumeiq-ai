import re
from typing import Optional

from app.ai.recommendation_builder import RecommendationBuilder
from app.schemas.analyzer import AnalyzerResponse


class EducationAnalyzer:
    """
    Analyzes education information present in a resume.

    Detects:
    - Degree
    - Branch / specialization
    - CGPA
    - Graduation year
    - Branch relevance to the job description
    """

    DEGREE_PATTERNS = [
        (
            r"\bb\.?\s*tech\b",
            "B.Tech",
        ),
        (
            r"\bbachelor\s+of\s+technology\b",
            "B.Tech",
        ),
        (
            r"\bb\.?\s*e\.?\b",
            "B.E",
        ),
        (
            r"\bbachelor\s+of\s+engineering\b",
            "B.E",
        ),
        (
            r"\bm\.?\s*tech\b",
            "M.Tech",
        ),
        (
            r"\bmaster\s+of\s+technology\b",
            "M.Tech",
        ),
        (
            r"\bm\.?\s*e\.?\b",
            "M.E",
        ),
        (
            r"\bb\.?\s*sc\b",
            "B.Sc",
        ),
        (
            r"\bbachelor\s+of\s+science\b",
            "B.Sc",
        ),
        (
            r"\bm\.?\s*sc\b",
            "M.Sc",
        ),
        (
            r"\bmaster\s+of\s+science\b",
            "M.Sc",
        ),
        (
            r"\bbca\b",
            "BCA",
        ),
        (
            r"\bbachelor\s+of\s+computer\s+applications\b",
            "BCA",
        ),
        (
            r"\bmca\b",
            "MCA",
        ),
        (
            r"\bmaster\s+of\s+computer\s+applications\b",
            "MCA",
        ),
        (
            r"\bph\.?\s*d\b",
            "PhD",
        ),
        (
            r"\bdoctor\s+of\s+philosophy\b",
            "PhD",
        ),
    ]

    BRANCH_PATTERNS = [
        (
            r"\bartificial\s+intelligence\s+and\s+machine\s+learning\b",
            "Artificial Intelligence and Machine Learning",
        ),
        (
            r"\bartificial\s+intelligence\s*&\s*machine\s+learning\b",
            "Artificial Intelligence and Machine Learning",
        ),
        (
            r"\bai\s*(?:and|&)\s*ml\b",
            "Artificial Intelligence and Machine Learning",
        ),
        (
            r"\baiml\b",
            "Artificial Intelligence and Machine Learning",
        ),
        (
            r"\bcomputer\s+science\s+and\s+engineering\b",
            "Computer Science and Engineering",
        ),
        (
            r"\bcomputer\s+science\b",
            "Computer Science",
        ),
        (
            r"\bcse\b",
            "Computer Science and Engineering",
        ),
        (
            r"\binformation\s+technology\b",
            "Information Technology",
        ),
        (
            r"\bdata\s+science\b",
            "Data Science",
        ),
        (
            r"\bmachine\s+learning\b",
            "Machine Learning",
        ),
        (
            r"\belectronics\s+and\s+communication\b",
            "Electronics and Communication Engineering",
        ),
        (
            r"\bece\b",
            "Electronics and Communication Engineering",
        ),
        (
            r"\bmechanical\s+engineering\b",
            "Mechanical Engineering",
        ),
        (
            r"\bcivil\s+engineering\b",
            "Civil Engineering",
        ),
    ]

    BRANCH_ALIASES = {
        "Artificial Intelligence and Machine Learning": [
            "artificial intelligence",
            "machine learning",
            "aiml",
            "ai/ml",
        ],
        "Computer Science and Engineering": [
            "computer science",
            "cse",
        ],
        "Computer Science": [
            "computer science",
            "cse",
        ],
        "Information Technology": [
            "information technology",
            "information tech",
            "it",
        ],
        "Data Science": [
            "data science",
            "data analytics",
        ],
        "Machine Learning": [
            "machine learning",
            "ml",
        ],
        "Electronics and Communication Engineering": [
            "electronics and communication",
            "electronics communication",
            "ece",
        ],
        "Mechanical Engineering": [
            "mechanical engineering",
            "mechanical",
        ],
        "Civil Engineering": [
            "civil engineering",
            "civil",
        ],
    }

    @classmethod
    def analyze(
        cls,
        resume_text: str,
        job_description: str,
    ) -> AnalyzerResponse:
        """
        Analyze education information against
        the target job description.
        """

        resume = resume_text.lower()
        jd = job_description.lower()

        degree = cls.extract_degree(
            resume
        )

        branch = cls.extract_branch(
            resume
        )

        cgpa = cls.extract_cgpa(
            resume
        )

        graduation_year = (
            cls.extract_graduation_year(
                resume
            )
        )

        branch_matches_jd = (
            cls.branch_matches_job(
                branch,
                jd,
            )
        )

        score = cls.calculate_score(
            degree=degree,
            branch=branch,
            cgpa=cgpa,
            branch_matches_jd=branch_matches_jd,
            graduation_year=graduation_year,
        )

        recommendations = (
            RecommendationBuilder
            .education_recommendations(
                degree=degree,
                branch=branch,
                cgpa=cgpa,
            )
        )

        # Graduation year is useful information,
        # so add a recommendation when it is missing.
        if graduation_year is None:
            recommendations.append(
                "Mention your graduation year or expected graduation year."
            )

        return AnalyzerResponse(
            score=score,
            details={
                "degree": degree,
                "branch": branch,
                "cgpa": cgpa,
                "graduation_year": graduation_year,
                "branch_matches_job": branch_matches_jd,
            },
            recommendations=sorted(
                set(recommendations)
            ),
        )

    @classmethod
    def extract_degree(
        cls,
        text: str,
    ) -> Optional[str]:
        """
        Extract the first recognized degree.
        """

        for pattern, degree in cls.DEGREE_PATTERNS:

            if re.search(
                pattern,
                text,
                re.IGNORECASE,
            ):
                return degree

        return None

    @classmethod
    def extract_branch(
        cls,
        text: str,
    ) -> Optional[str]:
        """
        Extract the first recognized branch/specialization.

        Longer and more specific patterns are checked
        before shorter patterns to avoid incorrect matches.
        """

        patterns = sorted(
            cls.BRANCH_PATTERNS,
            key=lambda item: len(item[0]),
            reverse=True,
        )

        for pattern, branch in patterns:

            if re.search(
                pattern,
                text,
                re.IGNORECASE,
            ):
                return branch

        return None

    @staticmethod
    def extract_cgpa(
        text: str,
    ) -> Optional[float]:
        """
        Extract CGPA from common resume formats.

        Supported examples:

        CGPA: 8.7
        CGPA - 8.7
        CGPA 8.7
        CGPA of 8.7
        8.7/10
        8.7 out of 10
        """

        patterns = [
            r"\bcgpa\s*(?:score)?\s*[:\-]?\s*(\d+(?:\.\d+)?)",
            r"\bcgpa\s+of\s+(\d+(?:\.\d+)?)",
            r"\b(\d+(?:\.\d+)?)\s*/\s*10\b",
            r"\b(\d+(?:\.\d+)?)\s+out\s+of\s+10\b",
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE,
            )

            if not match:
                continue

            try:
                value = float(
                    match.group(1)
                )
            except ValueError:
                continue

            if 0 <= value <= 10:
                return value

        return None

    @staticmethod
    def extract_graduation_year(
        text: str,
    ) -> Optional[int]:
        """
        Extract graduation or expected graduation year.

        Examples:

        Graduation Year: 2027
        Graduated: 2025
        Expected Graduation: 2027
        Passing Year: 2027
        """

        patterns = [
            (
                r"\bgraduation\s*year\s*[:\-]?\s*"
                r"(20\d{2})\b"
            ),
            (
                r"\bgraduated\s*(?:in|:|-)?\s*"
                r"(20\d{2})\b"
            ),
            (
                r"\bgraduation\s*[:\-]?\s*"
                r"(20\d{2})\b"
            ),
            (
                r"\bexpected\s+graduation"
                r"(?:\s+year)?\s*[:\-]?\s*"
                r"(20\d{2})\b"
            ),
            (
                r"\bexpected\s+to\s+graduate"
                r"(?:\s+in)?\s*[:\-]?\s*"
                r"(20\d{2})\b"
            ),
            (
                r"\bpassing\s+year\s*[:\-]?\s*"
                r"(20\d{2})\b"
            ),
            (
                r"\bpass(?:ing)?\s*out\s*year"
                r"\s*[:\-]?\s*(20\d{2})\b"
            ),
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE,
            )

            if match:
                return int(
                    match.group(1)
                )

        return None

    @classmethod
    def branch_matches_job(
        cls,
        branch: Optional[str],
        job_description: str,
    ) -> bool:
        """
        Determine whether the candidate's branch is
        relevant to the target job.

        Exact word boundaries are used so that short
        aliases such as 'IT' do not accidentally match
        unrelated words.
        """

        if not branch:
            return False

        aliases = cls.BRANCH_ALIASES.get(
            branch,
            [branch],
        )

        for alias in aliases:

            # Special handling for slash aliases.
            if "/" in alias:
                escaped_alias = re.escape(
                    alias
                )
            else:
                escaped_alias = re.escape(
                    alias
                )

            pattern = (
                rf"(?<!\w)"
                rf"{escaped_alias}"
                rf"(?!\w)"
            )

            if re.search(
                pattern,
                job_description,
                re.IGNORECASE,
            ):
                return True

        return False

    @staticmethod
    def calculate_score(
        degree: Optional[str],
        branch: Optional[str],
        cgpa: Optional[float],
        branch_matches_jd: bool,
        graduation_year: Optional[int],
    ) -> int:
        """
        Calculate education score.

        Maximum:
        - Degree: 30
        - Branch: 25
        - Branch relevance: 15
        - CGPA: 20
        - Graduation year: 10
        """

        score = 0

        # Degree
        if degree:
            score += 30

        # Branch/specialization
        if branch:
            score += 25

        # Relevance to target job
        if branch_matches_jd:
            score += 15

        # Academic performance
        if cgpa is not None:

            if cgpa >= 8.5:
                score += 20

            elif cgpa >= 7.5:
                score += 15

            elif cgpa >= 6.5:
                score += 10

            elif cgpa >= 5.5:
                score += 5

        # Graduation year
        if graduation_year is not None:
            score += 10

        return min(
            score,
            100,
        )