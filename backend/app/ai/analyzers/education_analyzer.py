import re

from app.ai.recommendation_builder import RecommendationBuilder
from app.schemas.analyzer import AnalyzerResponse


class EducationAnalyzer:
    """
    Analyze the education section of a resume.
    """

    DEGREE_KEYWORDS = [
        "b.tech",
        "btech",
        "b.e",
        "be",
        "m.tech",
        "mtech",
        "m.e",
        "me",
        "b.sc",
        "bsc",
        "m.sc",
        "msc",
        "bca",
        "mca",
        "phd",
    ]

    BRANCH_KEYWORDS = [
        "computer science",
        "cse",
        "information technology",
        "it",
        "artificial intelligence",
        "artificial intelligence and machine learning",
        "aiml",
        "machine learning",
        "data science",
        "electronics",
        "ece",
        "mechanical",
        "civil",
    ]

    @classmethod
    def analyze(
        cls,
        resume_text: str,
        job_description: str,
    ) -> AnalyzerResponse:

        resume = resume_text.lower()
        jd = job_description.lower()

        degree = cls.extract_degree(resume)

        branch = cls.extract_branch(resume)

        cgpa = cls.extract_cgpa(resume)

        graduation_year = cls.extract_graduation_year(resume)

        score = cls.calculate_score(
            degree,
            branch,
            cgpa,
            jd,
        )

        recommendations = RecommendationBuilder.education_recommendations(
            degree=degree,
            branch=branch,
            cgpa=cgpa,
        )

        return AnalyzerResponse(
            score=score,
            details={
                "degree": degree,
                "branch": branch,
                "cgpa": cgpa,
                "graduation_year": graduation_year,
            },
            recommendations=recommendations,
        )

    @classmethod
    def extract_degree(cls, text):

        for degree in cls.DEGREE_KEYWORDS:
            if degree in text:
                return degree.upper()

        return None

    @classmethod
    def extract_branch(cls, text):

        for branch in cls.BRANCH_KEYWORDS:
            if branch in text:
                return branch.title()

        return None

    @staticmethod
    def extract_cgpa(text):

        match = re.search(r"(\d\.\d{1,2})\s*(?:cgpa)?", text)

        if match:
            return float(match.group(1))

        return None

    @staticmethod
    def extract_graduation_year(text):

        years = re.findall(r"20\d{2}", text)

        if years:
            return max(years)

        return None

    @staticmethod
    def calculate_score(
        degree,
        branch,
        cgpa,
        jd,
    ):

        score = 0

        if degree:
            score += 35

        if branch:
            score += 25

            if branch.lower() in jd:
                score += 10

        if cgpa:

            if cgpa >= 8.5:
                score += 30

            elif cgpa >= 7.5:
                score += 20

            elif cgpa >= 6.5:
                score += 10

        return min(score, 100)