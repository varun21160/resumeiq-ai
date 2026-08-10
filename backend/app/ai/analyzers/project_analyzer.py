import re
from typing import List

from app.schemas.analyzer import AnalyzerResponse


class ProjectAnalyzer:
    """
    Analyzes project information present in a resume.

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
        "summary",
        "profile",
        "objective",

        "skills",
        "technical skills",
        "core skills",
        "technical competencies",

        "experience",
        "work experience",
        "professional experience",
        "employment history",
        "work history",

        "internship",
        "internships",
        "internship experience",

        "education",
        "academic background",
        "educational background",
        "academic qualifications",

        "certifications",
        "certificates",
        "licenses & certifications",
        "licenses and certifications",

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
        "volunteer work",

        "leadership",
        "leadership experience",

        "extracurricular",
        "extracurricular activities",
        "activities",
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
        "hadoop",
        "kafka",
        "streamlit",
        "git",
        "github",
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
        "integrated",
        "optimized",
        "improved",
        "reduced",
        "increased",
        "achieved",
        "processed",
    ]

    METRIC_KEYWORDS = [
        "accuracy",
        "performance",
        "efficiency",
        "time",
        "records",
        "users",
        "customers",
        "transactions",
        "revenue",
        "cost",
        "churn",
        "mrr",
        "arr",
        "kpi",
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

        matched_technologies = cls.find_matched_technologies(
            project_section,
            jd_lower,
        )

        github = cls.has_github(
            resume_lower
        )

        portfolio = cls.has_portfolio(
            resume_lower
        )

        measurable_results = cls.detect_measurable_results(
            project_section
        )

        action_keywords = cls.count_action_keywords(
            project_section
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
                "Add measurable project outcomes such as accuracy, "
                "performance improvement, time saved, or business impact."
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

    # ============================================================
    # PROJECT SECTION EXTRACTION
    # ============================================================

    @classmethod
    def extract_project_section(
        cls,
        text: str,
    ) -> str:
        """
        Extract only the project section.

        Stops when another recognized resume section begins.
        """

        if not text or not text.strip():
            return ""

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

            if normalized in cls.PROJECT_SECTION_HEADERS:
                start_index = index + 1
                break

        # If no Projects heading exists, use the full text.
        if start_index is None:
            return text.strip()

        project_lines = []

        for line in lines[start_index:]:

            normalized = cls.normalize_heading(line)

            if normalized in cls.SECTION_HEADERS:
                break

            project_lines.append(line)

        return "\n".join(project_lines).strip()

    @staticmethod
    def normalize_heading(
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

    # ============================================================
    # PROJECT COUNTING
    # ============================================================

    @classmethod
    def count_projects(
        cls,
        project_section: str,
    ) -> int:
        """
        Count actual project titles.

        The analyzer assumes a project entry generally looks like:

            Project Title
            Description...
            Description...
            GitHub...

        Description lines, URLs, metrics and technology
        metadata are excluded from project titles.
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

            if not cls.is_project_title(line):
                continue

            # A valid project title should have project-related
            # content immediately following it.
            following_lines = lines[
                index + 1:index + 4
            ]

            if not following_lines:
                continue

            content_count = sum(
                1
                for next_line in following_lines
                if cls.is_project_content(next_line)
            )

            if content_count >= 1:
                project_count += 1

        return min(project_count, 10)

    @classmethod
    def is_project_title(
        cls,
        line: str,
    ) -> bool:
        """
        Determine whether a line is likely to be a project title.
        """

        cleaned = cls.clean_bullet_prefix(line)

        if not cleaned:
            return False

        if cls.is_url(cleaned):
            return False

        if cls.is_technology_line(cleaned):
            return False

        if cls.is_description_line(cleaned):
            return False

        if cls.is_metric_line(cleaned):
            return False

        # Do not treat standalone technology names as titles.
        if cls.is_single_technology(cleaned):
            return False

        words = cleaned.split()

        # Project titles generally have 1-10 words.
        if len(words) < 1 or len(words) > 10:
            return False

        # A sentence ending in punctuation is more likely
        # to be a description than a project title.
        if cleaned.endswith(
            (".", "!", "?")
        ):
            return False

        # Very long lowercase sentences are usually descriptions.
        if len(words) >= 6 and cleaned[0].islower():
            return False

        return True

    @classmethod
    def is_project_content(
        cls,
        line: str,
    ) -> bool:

        if cls.is_url(line):
            return True

        if cls.is_description_line(line):
            return True

        if cls.is_metric_line(line):
            return True

        technology_count = sum(
            1
            for technology in cls.TECH_KEYWORDS
            if cls.contains_phrase(
                line,
                technology,
            )
        )

        if technology_count >= 1:
            return True

        return False

    # ============================================================
    # DESCRIPTION DETECTION
    # ============================================================

    @classmethod
    def is_description_line(
        cls,
        line: str,
    ) -> bool:

        cleaned = cls.clean_bullet_prefix(line)
        lowered = cleaned.lower()

        for keyword in cls.ACTION_KEYWORDS:

            if re.search(
                rf"\b{re.escape(keyword)}\b",
                lowered,
            ):
                return True

        prefixes = (
            "using ",
            "with ",
            "responsible for ",
            "worked on ",
            "this project ",
            "implemented ",
            "developed ",
            "built ",
            "created ",
            "designed ",
            "deployed ",
            "analyzed ",
            "automated ",
            "engineered ",
            "optimized ",
        )

        if lowered.startswith(prefixes):
            return True

        # Sentences longer than 15 words are generally descriptions.
        if len(cleaned.split()) > 15:
            return True

        return False

    @classmethod
    def is_metric_line(
        cls,
        line: str,
    ) -> bool:

        lowered = line.lower()

        if re.search(
            r"\b\d+(?:\.\d+)?\s*%",
            lowered,
        ):
            return True

        for keyword in cls.METRIC_KEYWORDS:

            if re.search(
                rf"\b{re.escape(keyword)}\b",
                lowered,
            ):
                if re.search(
                    r"\d",
                    lowered,
                ):
                    return True

        return False

    # ============================================================
    # TECHNOLOGY DETECTION
    # ============================================================

    @classmethod
    def is_technology_line(
        cls,
        line: str,
    ) -> bool:

        lowered = line.lower().strip()

        prefixes = (
            "technologies:",
            "technology:",
            "tech stack:",
            "tech:",
            "tools:",
            "tools used:",
            "technologies used:",
            "built with:",
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
    def is_single_technology(
        cls,
        line: str,
    ) -> bool:

        normalized = line.lower().strip()

        for technology in cls.TECH_KEYWORDS:

            if normalized == technology.lower():
                return True

        return False

    # ============================================================
    # TECHNOLOGY MATCHING
    # ============================================================

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

    # ============================================================
    # LINKS
    # ============================================================

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
                r"(portfolio|vercel|netlify|live\s+demo)",
                text,
                re.IGNORECASE,
            )
        )

    # ============================================================
    # MEASURABLE RESULTS
    # ============================================================

    @staticmethod
    def detect_measurable_results(
        text: str,
    ) -> bool:
        """
        Detect measurable project outcomes.

        Examples:

        92% accuracy
        improved performance by 20%
        reduced reporting time by 40%
        processed 10,000 records
        """

        patterns = [
            r"\b\d+(?:\.\d+)?\s*%",

            (
                r"\b\d+(?:,\d{3})*\+?\s*"
                r"(?:users|records|rows|transactions|customers)\b"
            ),

            (
                r"\b(?:improved|increased|reduced|decreased|"
                r"achieved|reached|maintained|processed)\b"
                r".{0,80}"
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

    # ============================================================
    # ACTION VERBS
    # ============================================================

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

    # ============================================================
    # BULLET / TEXT HELPERS
    # ============================================================

    @staticmethod
    def clean_bullet_prefix(
        line: str,
    ) -> str:

        return re.sub(
            r"^[\-\*\u2022\u25CF\d\.\)\s]+",
            "",
            line,
        ).strip()

    # ============================================================
    # SCORING
    # ============================================================

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

        # --------------------------------------------------------
        # Project quantity
        # --------------------------------------------------------
        score += min(
            project_count * 10,
            30,
        )

        # --------------------------------------------------------
        # Technology relevance
        # --------------------------------------------------------
        score += min(
            matched_technologies * 8,
            30,
        )

        # --------------------------------------------------------
        # Public evidence
        # --------------------------------------------------------
        if github:
            score += 10

        if portfolio:
            score += 10

        # --------------------------------------------------------
        # Measurable impact
        # --------------------------------------------------------
        if measurable_results:
            score += 15

        # --------------------------------------------------------
        # Action-oriented language
        # --------------------------------------------------------
        if action_keywords >= 2:
            score += 5

        return min(
            score,
            100,
        )