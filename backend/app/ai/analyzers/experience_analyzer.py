import re
from typing import List

from app.ai.recommendation_builder import RecommendationBuilder
from app.schemas.analyzer import AnalyzerResponse


class ExperienceAnalyzer:
    """
    Analyzes professional and internship experience
    against a target job description.
    """

    ROLE_ALIASES = {
        "data analyst": [
            "data analyst",
            "data analytics",
            "data analytics intern",
            "data analyst intern",
            "analytics intern",
            "business data analyst",
        ],
        "business analyst": [
            "business analyst",
            "business analytics",
            "business analyst intern",
        ],
        "software engineer": [
            "software engineer",
            "software developer",
            "software engineering intern",
            "software developer intern",
        ],
        "backend developer": [
            "backend developer",
            "backend engineer",
            "backend development intern",
        ],
        "frontend developer": [
            "frontend developer",
            "frontend engineer",
            "frontend development intern",
        ],
        "full stack developer": [
            "full stack developer",
            "full stack engineer",
            "full-stack developer",
        ],
        "machine learning engineer": [
            "machine learning engineer",
            "machine learning intern",
            "ml engineer",
            "ml intern",
        ],
        "data scientist": [
            "data scientist",
            "data science intern",
            "data science",
        ],
        "python developer": [
            "python developer",
            "python developer intern",
        ],
        "ai engineer": [
            "ai engineer",
            "ai developer",
            "artificial intelligence engineer",
            "ai intern",
        ],
        "data engineer": [
            "data engineer",
            "data engineering intern",
        ],
        "cloud engineer": [
            "cloud engineer",
            "cloud engineering intern",
        ],
        "devops engineer": [
            "devops engineer",
            "devops intern",
        ],
        "business intelligence analyst": [
            "business intelligence analyst",
            "bi analyst",
            "business intelligence",
        ],
    }

    EXPERIENCE_SECTION_KEYWORDS = [
        "experience",
        "employment",
        "work experience",
        "professional experience",
        "career experience",
    ]

    INTERNSHIP_KEYWORDS = [
        "intern",
        "internship",
        "trainee",
        "apprentice",
    ]

    @classmethod
    def analyze(
        cls,
        resume_text: str,
        job_description: str,
    ) -> AnalyzerResponse:

        resume = resume_text.lower()
        jd = job_description.lower()

        years = cls.extract_years(resume)

        internship_count = cls.count_internships(resume)

        has_professional_experience = (
            cls.has_professional_experience(resume)
        )

        matched_roles = cls.find_matched_roles(
            resume,
            jd,
        )

        experience_type = cls.determine_experience_type(
            years=years,
            internship_count=internship_count,
            has_professional_experience=has_professional_experience,
        )

        score = cls.calculate_score(
            years=years,
            internship_count=internship_count,
            matched_roles=len(matched_roles),
            has_professional_experience=has_professional_experience,
        )

        recommendations = []

        if years == 0 and internship_count == 0:
            recommendations.append(
                "Clearly mention internship or professional experience if applicable."
            )

        if internship_count > 0:
            recommendations.append(
                "Highlight internship responsibilities, technologies used, and measurable outcomes."
            )

        if not matched_roles:
            recommendations.append(
                "Use job titles and experience descriptions that closely match the target position."
            )

        return AnalyzerResponse(
            score=score,
            details={
                "years_of_experience": years,
                "internship_count": internship_count,
                "has_professional_experience": has_professional_experience,
                "experience_type": experience_type,
                "matched_roles": matched_roles,
            },
            recommendations=sorted(set(recommendations)),
        )

    @classmethod
    def find_matched_roles(
        cls,
        resume: str,
        job_description: str,
    ) -> List[str]:
        """
        Match a target role using related role titles and aliases.

        Example:
        Data Analytics Intern
        ->
        Data Analyst
        """

        matched_roles = []

        for canonical_role, aliases in cls.ROLE_ALIASES.items():

            resume_has_role = any(
                cls.contains_phrase(resume, alias)
                for alias in aliases
            )

            jd_has_role = any(
                cls.contains_phrase(job_description, alias)
                for alias in aliases
            )

            if resume_has_role and jd_has_role:
                matched_roles.append(canonical_role)

        return sorted(set(matched_roles))

    @staticmethod
    def contains_phrase(
        text: str,
        phrase: str,
    ) -> bool:

        pattern = rf"\b{re.escape(phrase.lower())}\b"

        return bool(
            re.search(
                pattern,
                text.lower(),
                re.IGNORECASE,
            )
        )

    @classmethod
    def extract_years(
        cls,
        text: str,
    ) -> int:
        """
        Extract explicit experience durations.

        Examples:
        2 years
        3+ years
        5 yrs
        1 year of experience
        """

        matches = re.findall(
            r"(\d+)\s*(?:\+)?\s*(?:years?|yrs?)"
            r"(?:\s+of\s+(?:professional\s+)?experience)?",
            text,
            re.IGNORECASE,
        )

        if not matches:
            return 0

        return max(
            int(value)
            for value in matches
        )

    @classmethod
    def count_internships(
        cls,
        text: str,
    ) -> int:

        count = 0

        for keyword in cls.INTERNSHIP_KEYWORDS:

            matches = re.findall(
                rf"\b{re.escape(keyword)}\b",
                text,
                re.IGNORECASE,
            )

            count += len(matches)

        return count

    @classmethod
    def has_professional_experience(
        cls,
        text: str,
    ) -> bool:

        for keyword in cls.EXPERIENCE_SECTION_KEYWORDS:

            if cls.contains_phrase(text, keyword):
                return True

        return False

    @staticmethod
    def determine_experience_type(
        years: int,
        internship_count: int,
        has_professional_experience: bool,
    ) -> str:

        if years > 0:
            return "professional"

        if internship_count > 0:
            return "internship"

        if has_professional_experience:
            return "experience_section_present"

        return "fresher"

    @staticmethod
    def calculate_score(
        years: int,
        internship_count: int,
        matched_roles: int,
        has_professional_experience: bool,
    ) -> int:

        score = 0

        # Full-time/professional experience
        if years > 0:
            score += min(years * 15, 60)

        # Internship experience
        elif internship_count > 0:
            score += min(internship_count * 15, 30)

        # Experience section exists
        elif has_professional_experience:
            score += 10

        # Relevant role alignment
        score += min(matched_roles * 20, 40)

        return min(score, 100)