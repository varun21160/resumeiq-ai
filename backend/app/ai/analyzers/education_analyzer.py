import re
from typing import Optional

from app.schemas.analyzer import AnalyzerResponse


class EducationAnalyzer:
    """
    Analyzes education information from a resume.

    Detects:
    - Degree
    - Academic branch / specialization
    - CGPA / GPA
    - Graduation year
    - Education section presence
    - Whether the degree/branch matches the job description
    """

    DEGREE_PATTERNS = [
        ("B.Tech", r"\bb\.?\s*tech\b|\bbachelor\s+of\s+technology\b"),
        ("B.E", r"\bb\.?\s*e\.?\b|\bbachelor\s+of\s+engineering\b"),
        ("B.Sc", r"\bb\.?\s*sc\.?\b|\bbachelor\s+of\s+science\b"),
        ("BCA", r"\bbca\b|\bbachelor\s+of\s+computer\s+applications\b"),
        ("M.Tech", r"\bm\.?\s*tech\b|\bmaster\s+of\s+technology\b"),
        ("M.E", r"\bm\.?\s*e\.?\b|\bmaster\s+of\s+engineering\b"),
        ("M.Sc", r"\bm\.?\s*sc\.?\b|\bmaster\s+of\s+science\b"),
        ("MCA", r"\bmca\b|\bmaster\s+of\s+computer\s+applications\b"),
        ("MBA", r"\bmba\b|\bmaster\s+of\s+business\s+administration\b"),
        ("Ph.D", r"\bph\.?\s*d\.?\b|\bdoctor\s+of\s+philosophy\b"),
    ]

    BRANCH_KEYWORDS = [
        "computer science",
        "computer science and engineering",
        "artificial intelligence",
        "artificial intelligence and machine learning",
        "machine learning",
        "data science",
        "data analytics",
        "information technology",
        "information science",
        "electronics and communication",
        "electrical engineering",
        "mechanical engineering",
        "civil engineering",
        "software engineering",
        "cyber security",
        "cybersecurity",
    ]

    EDUCATION_HEADERS = [
        "education",
        "academic background",
        "educational background",
        "academic qualifications",
        "qualifications",
    ]

    @classmethod
    def analyze(
        cls,
        resume_text: str,
        job_description: str,
    ) -> AnalyzerResponse:

        resume_text = resume_text or ""
        job_description = job_description or ""

        education_text = cls.extract_education_section(
            resume_text
        )

        search_text = education_text or resume_text

        degree = cls.detect_degree(search_text)
        branch = cls.detect_branch(search_text)
        cgpa = cls.detect_cgpa(search_text)
        graduation_year = cls.detect_graduation_year(
            search_text
        )

        branch_matches_job = cls.branch_matches_job(
            branch,
            job_description,
        )

        score = cls.calculate_score(
            degree=degree,
            branch=branch,
            cgpa=cgpa,
            graduation_year=graduation_year,
            branch_matches_job=branch_matches_job,
        )

        recommendations = []

        if not degree:
            recommendations.append(
                "Mention your degree clearly, such as B.Tech, B.E., B.Sc., or equivalent."
            )

        if not branch:
            recommendations.append(
                "Mention your academic specialization or branch."
            )

        if cgpa is None:
            recommendations.append(
                "Mention your CGPA or GPA if it strengthens your application."
            )

        if graduation_year is None:
            recommendations.append(
                "Mention your graduation year or expected graduation year."
            )

        if (
            branch
            and job_description.strip()
            and not branch_matches_job
        ):
            recommendations.append(
                "Highlight coursework or academic projects relevant to the target role."
            )

        return AnalyzerResponse(
            score=score,
            details={
                "degree": degree,
                "branch": branch,
                "cgpa": cgpa,
                "graduation_year": graduation_year,
                "branch_matches_job": branch_matches_job,
            },
            recommendations=sorted(
                set(recommendations)
            ),
        )

    @classmethod
    def extract_education_section(
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

        start_index: Optional[int] = None

        for index, line in enumerate(lines):
            normalized = cls.normalize(line)

            if normalized in cls.EDUCATION_HEADERS:
                start_index = index + 1
                break

        if start_index is None:
            return ""

        stop_headers = {
            "skills",
            "technical skills",
            "projects",
            "experience",
            "work experience",
            "professional experience",
            "internship",
            "internships",
            "certifications",
            "certificates",
            "achievements",
            "publications",
            "volunteering",
            "leadership",
            "extracurricular",
            "extracurricular activities",
        }

        section_lines = []

        for line in lines[start_index:]:
            normalized = cls.normalize(line)

            if normalized in stop_headers:
                break

            section_lines.append(line)

        return "\n".join(section_lines).strip()

    @classmethod
    def detect_degree(
        cls,
        text: str,
    ) -> Optional[str]:

        for degree_name, pattern in cls.DEGREE_PATTERNS:
            if re.search(
                pattern,
                text,
                re.IGNORECASE,
            ):
                return degree_name

        return None

    @classmethod
    def detect_branch(
        cls,
        text: str,
    ) -> Optional[str]:

        lowered = text.lower()

        # Check longer phrases first.
        keywords = sorted(
            cls.BRANCH_KEYWORDS,
            key=len,
            reverse=True,
        )

        for branch in keywords:
            if re.search(
                rf"\b{re.escape(branch)}\b",
                lowered,
                re.IGNORECASE,
            ):
                return branch.title()

        return None

    @staticmethod
    def detect_cgpa(
        text: str,
    ) -> Optional[float]:

        patterns = [
            r"\bCGPA\s*[:\-]?\s*(\d+(?:\.\d+)?)",
            r"\bGPA\s*[:\-]?\s*(\d+(?:\.\d+)?)",
            r"\b(\d+(?:\.\d+)?)\s*/\s*10\b",
        ]

        for pattern in patterns:
            match = re.search(
                pattern,
                text,
                re.IGNORECASE,
            )

            if match:
                try:
                    value = float(match.group(1))

                    if 0 <= value <= 10:
                        return value

                except ValueError:
                    pass

        return None

    @staticmethod
    def detect_graduation_year(
        text: str,
    ) -> Optional[int]:

        # Handles:
        # 2023-2027
        # 2023 – 2027
        # 2023 - Present
        # Expected Graduation: 2027
        # Graduation Year: 2027
        # 2027

        explicit_patterns = [
            r"(?:graduation|graduating|expected\s+graduation)"
            r"(?:\s+year)?\s*[:\-]?\s*(20\d{2})",

            r"(?:expected|class\s+of)\s+(20\d{2})",
        ]

        for pattern in explicit_patterns:
            match = re.search(
                pattern,
                text,
                re.IGNORECASE,
            )

            if match:
                return int(match.group(1))

        # Academic range such as 2023-2027.
        range_patterns = [
            r"\b(20\d{2})\s*[-–—]\s*(20\d{2})\b",
            r"\b(20\d{2})\s+to\s+(20\d{2})\b",
        ]

        for pattern in range_patterns:
            match = re.search(
                pattern,
                text,
                re.IGNORECASE,
            )

            if match:
                start_year = int(match.group(1))
                end_year = int(match.group(2))

                if end_year >= start_year:
                    return end_year

        return None

    @classmethod
    def branch_matches_job(
        cls,
        branch: Optional[str],
        job_description: str,
    ) -> bool:

        if not branch:
            return False

        if not job_description.strip():
            return True

        branch_lower = branch.lower()
        jd_lower = job_description.lower()

        # Direct match.
        if branch_lower in jd_lower:
            return True

        # Related academic terms.
        related_groups = [
            {
                "artificial intelligence",
                "machine learning",
                "data science",
                "data analytics",
                "computer science",
            },
            {
                "computer science",
                "computer science and engineering",
                "information technology",
                "information science",
            },
            {
                "electronics and communication",
                "electrical engineering",
            },
        ]

        for group in related_groups:

            branch_matches_group = any(
                term in branch_lower
                for term in group
            )

            jd_matches_group = any(
                term in jd_lower
                for term in group
            )

            if branch_matches_group and jd_matches_group:
                return True

        return False

    @staticmethod
    def calculate_score(
        degree: Optional[str],
        branch: Optional[str],
        cgpa: Optional[float],
        graduation_year: Optional[int],
        branch_matches_job: bool,
    ) -> int:

        score = 0

        # Degree
        if degree:
            score += 35

        # Branch / specialization
        if branch:
            score += 20

        # Relevant branch
        if branch_matches_job:
            score += 15

        # CGPA
        if cgpa is not None:
            score += 15

        # Graduation year
        if graduation_year is not None:
            score += 15

        return min(score, 100)

    @staticmethod
    def normalize(
        text: str,
    ) -> str:

        text = text.lower().strip()

        text = re.sub(
            r"[:\-|]+$",
            "",
            text,
        )

        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        return text.strip()