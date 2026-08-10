import re
from typing import List

from app.schemas.analyzer import AnalyzerResponse


class ProjectAnalyzer:
    """
    Analyzes projects in a resume.

    Detects:
    - Project section
    - Individual project entries
    - Relevant technologies
    - GitHub links
    - Portfolio/live-demo links
    - Measurable outcomes
    - Action-oriented descriptions
    """

    PROJECT_SECTION_HEADERS = [
        "projects",
        "project experience",
        "academic projects",
        "technical projects",
        "personal projects",
        "selected projects",
        "key projects",
    ]

    SECTION_HEADERS = {
        "education",
        "experience",
        "work experience",
        "professional experience",
        "skills",
        "technical skills",
        "certifications",
        "certificates",
        "achievements",
        "summary",
        "objective",
        "internships",
        "employment",
    }

    TECH_KEYWORDS = [
        "python",
        "sql",
        "power bi",
        "tableau",
        "excel",
        "fastapi",
        "django",
        "flask",
        "docker",
        "aws",
        "azure",
        "gcp",
        "react",
        "javascript",
        "typescript",
        "pandas",
        "numpy",
        "tensorflow",
        "pytorch",
        "scikit-learn",
        "machine learning",
        "deep learning",
        "postgresql",
        "mysql",
        "mongodb",
        "spark",
        "pyspark",
        "databricks",
    ]

    ACTION_KEYWORDS = [
        "developed",
        "built",
        "implemented",
        "created",
        "designed",
        "engineered",
        "deployed",
        "automated",
        "analyzed",
        "developing",
        "building",
    ]

    @classmethod
    def analyze(
        cls,
        resume_text: str,
        job_description: str,
    ) -> AnalyzerResponse:

        project_section = cls.extract_project_section(
            resume_text
        )

        resume_lower = resume_text.lower()
        jd_lower = job_description.lower()

        project_count = cls.count_projects(
            project_section
        )

        matched_technologies = (
            cls.find_matched_technologies(
                project_section,
                jd_lower,
            )
        )

        github = cls.has_github(
            resume_lower
        )

        portfolio = cls.has_portfolio(
            resume_lower
        )

        measurable_results = (
            cls.detect_measurable_results(
                project_section
            )
        )

        action_keywords = (
            cls.count_action_keywords(
                project_section
            )
        )

        score = cls.calculate_score(
            project_count=project_count,
            matched_technologies=len(
                matched_technologies
            ),
            github=github,
            portfolio=portfolio,
            measurable_results=measurable_results,
            action_keywords=action_keywords,
        )

        recommendations = []

        if project_count == 0:
            recommendations.append(
                "Add relevant technical or academic projects."
            )

        elif project_count < 2:
            recommendations.append(
                "Include at least two strong projects relevant to your target role."
            )

        if not matched_technologies:
            recommendations.append(
                "Mention the technologies and tools used in your projects."
            )

        if not measurable_results:
            recommendations.append(
                "Add measurable project outcomes such as accuracy, performance improvement, time saved, or business impact."
            )

        if not github:
            recommendations.append(
                "Add GitHub repository links to showcase your work."
            )

        if not portfolio:
            recommendations.append(
                "Include a portfolio or live demo link when available."
            )

        return AnalyzerResponse(
            score=score,
            details={
                "project_count": project_count,
                "matched_technologies": matched_technologies,
                "github": github,
                "portfolio": portfolio,
                "measurable_results": measurable_results,
                "action_keywords": action_keywords,
            },
            recommendations=sorted(
                set(recommendations)
            ),
        )

    @classmethod
    def extract_project_section(
        cls,
        text: str,
    ) -> str:
        """
        Extract the project section while preserving
        the original line structure.
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

            normalized = line.lower().strip(
                " :-"
            )

            if normalized in cls.PROJECT_SECTION_HEADERS:
                start_index = index + 1
                break

        if start_index is None:
            return text

        project_lines = []

        for line in lines[start_index:]:

            normalized = line.lower().strip(
                " :-"
            )

            if normalized in cls.SECTION_HEADERS:
                break

            project_lines.append(line)

        return "\n".join(project_lines)

    @classmethod
    def count_projects(
        cls,
        project_section: str,
    ) -> int:
        """
        Count actual project entries.

        A project is identified by a title-like line
        followed by project-related content.

        Description lines, URLs, and technology
        metadata are not counted as projects.
        """

        if not project_section.strip():
            return 0

        lines = [
            line.strip()
            for line in project_section.splitlines()
            if line.strip()
        ]

        if not lines:
            return 0

        project_count = 0

        for index, line in enumerate(lines):

            cleaned = re.sub(
                r"^[\-\*\u2022\d\.\)\s]+",
                "",
                line,
            ).strip()

            if not cleaned:
                continue

            # Ignore URLs.
            if cls.is_url(cleaned):
                continue

            # Ignore description/action lines.
            if cls.is_description_line(cleaned):
                continue

            # Ignore technology metadata.
            if cls.is_technology_line(cleaned):
                continue

            words = cleaned.split()

            # Project title should normally be 2-10 words.
            if len(words) < 2 or len(words) > 10:
                continue

            # Look ahead for project-related content.
            following_lines = lines[
                index + 1:index + 3
            ]

            has_project_content = any(
                cls.is_project_content(next_line)
                for next_line in following_lines
            )

            if has_project_content:
                project_count += 1

        return min(project_count, 10)

    @staticmethod
    def is_url(
        text: str,
    ) -> bool:

        return bool(
            re.search(
                r"(https?://|www\.|github\.com)",
                text,
                re.IGNORECASE,
            )
        )

    @classmethod
    def is_technology_line(
        cls,
        line: str,
    ) -> bool:
        """
        Detect lines that are primarily technology/tool lists.
        """

        lowered = line.lower().strip()

        prefixes = (
            "technologies:",
            "technology:",
            "tech stack:",
            "tech:",
            "tools:",
            "tools used:",
            "technologies used:",
        )

        if lowered.startswith(prefixes):
            return True

        found = 0

        for technology in cls.TECH_KEYWORDS:

            if cls.contains_phrase(
                lowered,
                technology,
            ):
                found += 1

        words = len(line.split())

        if words > 0 and found >= 2:
            if found >= words / 2:
                return True

        return False

    @classmethod
    def is_project_content(
        cls,
        line: str,
    ) -> bool:
        """
        Determine whether a line looks like content
        belonging to a project.
        """

        lowered = line.lower()

        if cls.is_description_line(line):
            return True

        if cls.is_url(line):
            return True

        if cls.detect_measurable_results(line):
            return True

        technology_count = sum(
            1
            for technology in cls.TECH_KEYWORDS
            if cls.contains_phrase(
                lowered,
                technology,
            )
        )

        return technology_count >= 1

    @classmethod
    def is_project_title(
        cls,
        line: str,
    ) -> bool:
        """
        Determine whether a line looks like a
        project title.
        """

        if cls.is_description_line(line):
            return False

        if cls.is_url(line):
            return False

        if cls.is_technology_line(line):
            return False

        words = line.split()

        if len(words) < 2:
            return False

        if len(words) > 10:
            return False

        return True

    @classmethod
    def is_description_line(
        cls,
        line: str,
    ) -> bool:

        lowered = line.lower()

        # Action-oriented descriptions.
        for keyword in cls.ACTION_KEYWORDS:

            if re.search(
                rf"\b{re.escape(keyword)}\b",
                lowered,
            ):
                return True

        # Common description prefixes.
        if lowered.startswith(
            (
                "using ",
                "with ",
                "responsible for ",
                "worked on ",
                "developed ",
                "built ",
                "created ",
                "implemented ",
                "designed ",
                "deployed ",
                "analyzed ",
                "this project ",
            )
        ):
            return True

        # Long sentences are usually descriptions.
        if len(line.split()) > 20:
            return True

        return False

    @classmethod
    def find_matched_technologies(
        cls,
        project_text: str,
        job_description: str,
    ) -> List[str]:

        matched = []

        for technology in cls.TECH_KEYWORDS:

            project_match = cls.contains_phrase(
                project_text,
                technology,
            )

            jd_match = cls.contains_phrase(
                job_description,
                technology,
            )

            if project_match and jd_match:
                matched.append(technology)

        return sorted(
            set(matched)
        )

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

    @staticmethod
    def has_github(
        text: str,
    ) -> bool:

        return bool(
            re.search(
                r"github\.com",
                text,
                re.IGNORECASE,
            )
        )

    @staticmethod
    def has_portfolio(
        text: str,
    ) -> bool:

        return bool(
            re.search(
                r"(portfolio|vercel|netlify|live demo)",
                text,
                re.IGNORECASE,
            )
        )

    @staticmethod
    def detect_measurable_results(
        text: str,
    ) -> bool:
        """
        Detect measurable project outcomes.

        Examples:
        92% accuracy
        reduced time by 30%
        processed 10,000 records
        improved performance by 20%
        """

        patterns = [
            r"\b\d+(?:\.\d+)?\s*%",
            (
                r"\b\d+(?:,\d{3})*\+?\s*"
                r"(?:users|records|rows|transactions|customers)\b"
            ),
            (
                r"\b(?:improved|increased|reduced|decreased|"
                r"achieved|reached|maintained)\b"
                r".{0,60}"
                r"\b\d+(?:\.\d+)?"
            ),
        ]

        return any(
            re.search(
                pattern,
                text,
                re.IGNORECASE,
            )
            for pattern in patterns
        )

    @classmethod
    def count_action_keywords(
        cls,
        text: str,
    ) -> int:

        count = 0

        for keyword in cls.ACTION_KEYWORDS:

            count += len(
                re.findall(
                    rf"\b{re.escape(keyword)}\b",
                    text,
                    re.IGNORECASE,
                )
            )

        return count

    @staticmethod
    def calculate_score(
        project_count: int,
        matched_technologies: int,
        github: bool,
        portfolio: bool,
        measurable_results: bool,
        action_keywords: int,
    ) -> int:

        score = 0

        # Project quantity
        score += min(
            project_count * 15,
            30,
        )

        # Technology relevance
        score += min(
            matched_technologies * 8,
            30,
        )

        # Public evidence
        if github:
            score += 10

        if portfolio:
            score += 10

        # Measurable impact
        if measurable_results:
            score += 15

        # Strong project language
        if action_keywords >= 2:
            score += 5

        return min(
            score,
            100,
        )