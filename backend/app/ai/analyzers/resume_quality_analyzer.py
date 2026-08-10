import re
from typing import Dict, List

from app.resume.section_detector import SectionDetector
from app.schemas.analyzer import AnalyzerResponse


class ResumeQualityAnalyzer:
    """
    Evaluates the structural and ATS-friendly quality of a resume.

    SectionDetector is used as the single source of truth for
    identifying resume sections.
    """

    ACTION_VERBS = {
        "analyzed",
        "built",
        "created",
        "developed",
        "designed",
        "implemented",
        "improved",
        "automated",
        "optimized",
        "engineered",
        "deployed",
        "integrated",
        "led",
        "managed",
        "delivered",
        "generated",
        "performed",
        "configured",
        "tested",
        "evaluated",
        "processed",
        "transformed",
        "visualized",
        "develop",
        "create",
        "build",
        "design",
        "implement",
        "improve",
        "automate",
        "optimize",
        "engineer",
        "deploy",
        "integrate",
        "manage",
        "deliver",
        "generate",
        "perform",
        "configure",
        "test",
        "evaluate",
        "process",
        "transform",
        "visualize",
    }

    METRIC_PATTERNS = [
        r"\b\d+(?:\.\d+)?\s*%",
        r"\b\d+(?:\.\d+)?\s*(?:percent|percentage)\b",
        r"\b\d+(?:\.\d+)?\s*(?:k|m|b)\b",
        (
            r"\b\d+(?:\.\d+)?\+?\s*"
            r"(?:users|customers|records|rows|employees|"
            r"projects|reports|datasets)\b"
        ),
        (
            r"\b(?:reduced|increased|improved|saved|generated|"
            r"processed|achieved)\b.{0,80}"
            r"\b\d+(?:\.\d+)?\b"
        ),
    ]

    CONTACT_PATTERNS = {
        "email": (
            r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b"
        ),
        "phone": (
            r"(?:\+?\d{1,3}[\s.-]?)?"
            r"(?:\d[\s.-]?){8,14}\d"
        ),
        "linkedin": (
            r"linkedin\.com/in/"
        ),
        "github": (
            r"github\.com/"
        ),
    }

    @classmethod
    def analyze(
        cls,
        resume_text: str,
        job_description: str = "",
    ) -> AnalyzerResponse:
        """
        Analyze resume quality.
        """

        if not resume_text or not resume_text.strip():
            raise ValueError(
                "Resume text cannot be empty."
            )

        text = resume_text.strip()
        lower_text = text.lower()

        # -----------------------------------------
        # Detect sections using SectionDetector
        # -----------------------------------------

        detected_sections = SectionDetector.detect(
            text
        )

        section_presence = (
            cls.build_section_presence(
                detected_sections
            )
        )

        # -----------------------------------------
        # Analyze resume content
        # -----------------------------------------

        contact_information = (
            cls.analyze_contact_information(
                text
            )
        )

        bullet_count = cls.count_bullets(
            text
        )

        action_verb_count = (
            cls.count_action_verbs(
                lower_text
            )
        )

        measurable_result_count = (
            cls.count_measurable_results(
                text
            )
        )

        word_count = len(
            re.findall(
                r"\b[\w+#./-]+\b",
                text,
            )
        )

        # -----------------------------------------
        # Calculate score
        # -----------------------------------------

        score = cls.calculate_score(
            sections=section_presence,
            contact=contact_information,
            bullet_count=bullet_count,
            action_verb_count=action_verb_count,
            measurable_result_count=(
                measurable_result_count
            ),
            word_count=word_count,
        )

        # -----------------------------------------
        # Recommendations
        # -----------------------------------------

        recommendations = (
            cls.generate_recommendations(
                sections=section_presence,
                contact=contact_information,
                bullet_count=bullet_count,
                action_verb_count=action_verb_count,
                measurable_result_count=(
                    measurable_result_count
                ),
                word_count=word_count,
            )
        )

        return AnalyzerResponse(
            score=score,
            details={
                "word_count": word_count,
                "section_presence": section_presence,
                "contact_information": contact_information,
                "bullet_count": bullet_count,
                "action_verb_count": action_verb_count,
                "measurable_result_count": (
                    measurable_result_count
                ),
            },
            recommendations=recommendations,
        )

    @staticmethod
    def build_section_presence(
        detected_sections: Dict[str, str],
    ) -> Dict[str, bool]:
        """
        Convert SectionDetector's section-content dictionary
        into boolean section presence values.
        """

        known_sections = [
            "header",
            "summary",
            "skills",
            "experience",
            "internships",
            "projects",
            "education",
            "certifications",
            "achievements",
            "publications",
            "volunteering",
            "leadership",
            "extracurricular",
        ]

        return {
            section: bool(
                detected_sections.get(
                    section,
                    ""
                ).strip()
            )
            if isinstance(
                detected_sections.get(
                    section,
                    ""
                ),
                str,
            )
            else bool(
                detected_sections.get(
                    section,
                    ""
                )
            )
            for section in known_sections
        }

    @classmethod
    def analyze_contact_information(
        cls,
        text: str,
    ) -> Dict[str, bool]:
        """
        Detect common resume contact information.
        """

        return {
            "email": bool(
                re.search(
                    cls.CONTACT_PATTERNS["email"],
                    text,
                    re.IGNORECASE,
                )
            ),
            "phone": bool(
                re.search(
                    cls.CONTACT_PATTERNS["phone"],
                    text,
                )
            ),
            "linkedin": bool(
                re.search(
                    cls.CONTACT_PATTERNS["linkedin"],
                    text,
                    re.IGNORECASE,
                )
            ),
            "github": bool(
                re.search(
                    cls.CONTACT_PATTERNS["github"],
                    text,
                    re.IGNORECASE,
                )
            ),
        }

    @staticmethod
    def count_bullets(
        text: str,
    ) -> int:
        """
        Count common resume bullet formats.
        """

        count = 0

        for line in text.splitlines():
            stripped = line.strip()

            if re.match(
                r"^(?:[-•●▪◦*])\s+",
                stripped,
            ):
                count += 1

        return count

    @classmethod
    def count_action_verbs(
        cls,
        text: str,
    ) -> int:
        """
        Count action verbs used in the resume.
        """

        words = re.findall(
            r"\b[a-zA-Z]+\b",
            text.lower(),
        )

        return sum(
            1
            for word in words
            if word in cls.ACTION_VERBS
        )

    @classmethod
    def count_measurable_results(
        cls,
        text: str,
    ) -> int:
        """
        Detect measurable achievements and outcomes.
        """

        count = 0

        for pattern in cls.METRIC_PATTERNS:
            count += len(
                re.findall(
                    pattern,
                    text,
                    flags=(
                        re.IGNORECASE
                        | re.DOTALL
                    ),
                )
            )

        return count

    @staticmethod
    def calculate_score(
        sections: Dict[str, bool],
        contact: Dict[str, bool],
        bullet_count: int,
        action_verb_count: int,
        measurable_result_count: int,
        word_count: int,
    ) -> int:
        """
        Calculate deterministic resume-quality score.
        """

        score = 0

        # -----------------------------------------
        # Required sections: 30 points
        # -----------------------------------------

        if sections.get(
            "skills",
            False,
        ):
            score += 10

        if (
            sections.get(
                "experience",
                False,
            )
            or sections.get(
                "internships",
                False,
            )
        ):
            score += 10

        if sections.get(
            "education",
            False,
        ):
            score += 10

        # -----------------------------------------
        # Optional sections: 15 points
        # -----------------------------------------

        if sections.get(
            "summary",
            False,
        ):
            score += 5

        if sections.get(
            "projects",
            False,
        ):
            score += 5

        if sections.get(
            "certifications",
            False,
        ):
            score += 5

        # -----------------------------------------
        # Contact information: 20 points
        # -----------------------------------------

        if contact.get(
            "email",
            False,
        ):
            score += 7

        if contact.get(
            "phone",
            False,
        ):
            score += 5

        if contact.get(
            "linkedin",
            False,
        ):
            score += 4

        if contact.get(
            "github",
            False,
        ):
            score += 4

        # -----------------------------------------
        # Bullet points: 10 points
        # -----------------------------------------

        if bullet_count >= 5:
            score += 10

        elif bullet_count >= 3:
            score += 7

        elif bullet_count >= 1:
            score += 4

        # -----------------------------------------
        # Action verbs: 10 points
        # -----------------------------------------

        if action_verb_count >= 8:
            score += 10

        elif action_verb_count >= 5:
            score += 7

        elif action_verb_count >= 2:
            score += 4

        # -----------------------------------------
        # Measurable results: 10 points
        # -----------------------------------------

        if measurable_result_count >= 5:
            score += 10

        elif measurable_result_count >= 3:
            score += 7

        elif measurable_result_count >= 1:
            score += 4

        # -----------------------------------------
        # Resume length: 5 points
        # -----------------------------------------

        if 250 <= word_count <= 1200:
            score += 5

        elif 150 <= word_count <= 1500:
            score += 3

        return min(
            score,
            100,
        )

    @staticmethod
    def generate_recommendations(
        sections: Dict[str, bool],
        contact: Dict[str, bool],
        bullet_count: int,
        action_verb_count: int,
        measurable_result_count: int,
        word_count: int,
    ) -> List[str]:
        """
        Generate actionable resume-quality recommendations.
        """

        recommendations = []

        if not sections.get(
            "skills",
            False,
        ):
            recommendations.append(
                "Add a clearly labeled Skills section."
            )

        if not (
            sections.get(
                "experience",
                False,
            )
            or sections.get(
                "internships",
                False,
            )
        ):
            recommendations.append(
                "Add a clearly labeled Experience "
                "or Internships section."
            )

        if not sections.get(
            "education",
            False,
        ):
            recommendations.append(
                "Add a clearly labeled Education section."
            )

        if not sections.get(
            "summary",
            False,
        ):
            recommendations.append(
                "Consider adding a concise professional "
                "summary tailored to the target role."
            )

        if not sections.get(
            "projects",
            False,
        ):
            recommendations.append(
                "Add relevant technical or academic projects."
            )

        if not sections.get(
            "certifications",
            False,
        ):
            recommendations.append(
                "Add relevant certifications if they "
                "strengthen your application."
            )

        if not contact.get(
            "email",
            False,
        ):
            recommendations.append(
                "Add a professional email address."
            )

        if not contact.get(
            "phone",
            False,
        ):
            recommendations.append(
                "Add a reachable phone number."
            )

        if not contact.get(
            "linkedin",
            False,
        ):
            recommendations.append(
                "Add a LinkedIn profile URL."
            )

        if bullet_count < 3:
            recommendations.append(
                "Use concise bullet points for experience "
                "and project descriptions."
            )

        if action_verb_count < 5:
            recommendations.append(
                "Start experience and project bullets with "
                "strong action verbs."
            )

        if measurable_result_count == 0:
            recommendations.append(
                "Add measurable outcomes such as percentages, "
                "performance improvements, time saved, records "
                "processed, or business impact."
            )

        if word_count < 150:
            recommendations.append(
                "The resume appears too short. Add relevant "
                "evidence of skills, experience, projects, "
                "and achievements."
            )

        elif word_count > 1500:
            recommendations.append(
                "The resume may be too lengthy. Remove redundant "
                "content and prioritize information relevant "
                "to the target role."
            )

        return recommendations