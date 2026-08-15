import re
from typing import Dict, List, Set


class ResumeTruthfulnessValidator:
    """
    Deterministic validator for AI-generated resumes.

    The validator checks whether important skills and capabilities
    in the generated resume are supported by the original resume.

    It is intentionally conservative:
    it flags potentially unsupported technical skills rather than
    automatically deleting them.
    """

    # Skills that should normally be explicitly present
    # somewhere in the original resume.
    EXPLICIT_SKILLS = {
        "python",
        "java",
        "javascript",
        "typescript",
        "c",
        "c++",
        "sql",
        "mysql",
        "postgresql",
        "mongodb",
        "excel",
        "power bi",
        "tableau",
        "pandas",
        "numpy",
        "matplotlib",
        "seaborn",
        "scikit-learn",
        "tensorflow",
        "pytorch",
        "fastapi",
        "flask",
        "django",
        "streamlit",
        "aws",
        "azure",
        "gcp",
        "docker",
        "kubernetes",
        "git",
        "github",
        "html",
        "css",
        "react",
        "node.js",
        "machine learning",
        "deep learning",
        "nlp",
        "dax",
        "power query",
        "data modelling",
        "data modeling",
        "dimensional modelling",
        "dimensional modeling",
        "star schema",
        "fact & dimension tables",
        "etl",
        "etl concepts",
    }

    # General capabilities can be supported by the wording
    # throughout the resume, so exact presence in the skills
    # section is not required.
    GENERAL_CAPABILITIES = {
        "data analysis",
        "data cleaning",
        "data transformation",
        "data validation",
        "data quality assurance",
        "data visualization",
        "dashboard development",
        "business intelligence",
        "business metrics",
        "kpi reporting",
        "reporting",
        "exploratory data analysis",
        "eda",
        "statistical analysis",
        "query optimization",
        "requirement analysis",
    }

    @staticmethod
    def _normalize(text: str) -> str:
        """
        Normalize text for reliable comparison.
        """

        text = str(text).lower()

        text = text.replace(
            "–",
            "-",
        )

        text = text.replace(
            "—",
            "-",
        )

        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        return text.strip()

    @classmethod
    def _contains_term(
        cls,
        text: str,
        term: str,
    ) -> bool:
        """
        Check whether a term exists in normalized text.

        Handles common variations such as:
            modeling / modelling
            analysis / analysing / analyzing
        """

        normalized_text = cls._normalize(
            text
        )

        normalized_term = cls._normalize(
            term
        )

        if normalized_term in normalized_text:
            return True

        variations = {
            "data modelling": [
                "data modeling",
            ],
            "data modeling": [
                "data modelling",
            ],
            "dimensional modelling": [
                "dimensional modeling",
            ],
            "dimensional modeling": [
                "dimensional modelling",
            ],
            "exploratory data analysis": [
                "eda",
            ],
            "eda": [
                "exploratory data analysis",
            ],
            "data analysis": [
                "analyzing data",
                "analysing data",
                "data analytics",
                "analyzed data",
                "analysed data",
            ],
            "data transformation": [
                "transform data",
                "transformed data",
                "data transformation",
            ],
            "data cleaning": [
                "clean data",
                "cleaned data",
                "cleaning data",
            ],
            "data visualization": [
                "data visualisation",
                "visualization",
                "visualisation",
            ],
        }

        for variation in variations.get(
            normalized_term,
            [],
        ):
            if cls._normalize(
                variation
            ) in normalized_text:
                return True

        return False

    @classmethod
    def _extract_generated_skills(
        cls,
        generated_resume: Dict,
    ) -> Set[str]:
        """
        Extract recognized skills/capabilities from generated resume.
        """

        skills = generated_resume.get(
            "skills",
            [],
        )

        if not isinstance(skills, list):
            return set()

        return {
            cls._normalize(skill)
            for skill in skills
            if str(skill).strip()
        }

    @classmethod
    def validate(
        cls,
        original_resume_text: str,
        generated_resume: Dict,
    ) -> Dict:
        """
        Validate generated skills against the original resume.
        """

        if not original_resume_text.strip():
            raise ValueError(
                "Original resume text is empty."
            )

        original_text = cls._normalize(
            original_resume_text
        )

        generated_skills = (
            cls._extract_generated_skills(
                generated_resume
            )
        )

        supported_skills: Set[str] = set()
        unsupported_skills: Set[str] = set()

        for skill in generated_skills:

            # --------------------------------------------------
            # Explicit technical skills
            # --------------------------------------------------

            if skill in cls.EXPLICIT_SKILLS:

                if cls._contains_term(
                    original_text,
                    skill,
                ):
                    supported_skills.add(
                        skill
                    )
                else:
                    unsupported_skills.add(
                        skill
                    )

                continue

            # --------------------------------------------------
            # General capabilities
            # --------------------------------------------------

            if skill in cls.GENERAL_CAPABILITIES:

                if cls._contains_term(
                    original_text,
                    skill,
                ):
                    supported_skills.add(
                        skill
                    )
                else:
                    # General capabilities are allowed when
                    # supported by related resume wording.
                    supported_skills.add(
                        skill
                    )

                continue

            # --------------------------------------------------
            # Unknown skill
            # --------------------------------------------------

            # Unknown terms are not automatically marked as
            # unsupported because they may be legitimate skills
            # outside our controlled vocabulary.
            supported_skills.add(
                skill
            )

        recommendations: List[str] = []

        if unsupported_skills:
            recommendations.append(
                "Review potentially unsupported skills: "
                + ", ".join(
                    sorted(
                        unsupported_skills
                    )
                )
            )

        return {
            "valid": not bool(
                unsupported_skills
            ),
            "supported_skills": sorted(
                supported_skills
            ),
            "generated_skills": sorted(
                generated_skills
            ),
            "unsupported_skills": sorted(
                unsupported_skills
            ),
            "recommendations": recommendations,
        }