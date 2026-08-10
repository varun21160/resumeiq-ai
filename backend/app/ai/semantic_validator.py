from typing import Any, Dict, List

class SemanticValidator:
    """
    Validates and normalizes the structured response returned
    by the semantic analyzer.

    This layer protects the application from malformed or
    inconsistent Gemini responses.
    """

    REQUIRED_LIST_FIELDS = [
    "strong_matches",
    "partial_matches",
    "missing_requirements",
    "critical_missing_requirements",
    "preferred_missing_requirements",
    "key_strengths",
    "key_gaps",
    "recommendations",
]

    VALID_RELEVANCE_LEVELS = {
        "high",
        "medium",
        "low",
    }

    @classmethod
    def validate(
        cls,
        result: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Validate and normalize semantic analysis output.
        """

        if not isinstance(result, dict):
            raise ValueError(
                "Semantic analysis result must be a dictionary."
            )

        validated = {}

        # --------------------------------------------------
        # Validate list-based fields
        # --------------------------------------------------

        for field in cls.REQUIRED_LIST_FIELDS:
            validated[field] = cls._clean_list(
                result.get(field, [])
            )

        # --------------------------------------------------
        # Validate relevance sections
        # --------------------------------------------------

        validated["experience_relevance"] = (
            cls._clean_relevance(
                result.get("experience_relevance")
            )
        )

        validated["project_relevance"] = (
            cls._clean_relevance(
                result.get("project_relevance")
            )
        )

        validated["education_relevance"] = (
            cls._clean_relevance(
                result.get("education_relevance")
            )
        )

        # --------------------------------------------------
        # Remove duplicate items
        # --------------------------------------------------

        for field in cls.REQUIRED_LIST_FIELDS:
            validated[field] = cls._unique(
                validated[field]
            )

        # --------------------------------------------------
        # Prevent contradictory classifications
        #
        # A requirement classified as critical missing
        # should also exist in missing requirements.
        # --------------------------------------------------

        validated["missing_requirements"] = (
            cls._ensure_parent_requirements(
                validated["missing_requirements"],
                validated["critical_missing_requirements"],
            )
        )

        # --------------------------------------------------
        # Remove critical requirements from strong matches
        # if Gemini accidentally classified the same item
        # in both categories.
        # --------------------------------------------------

        critical = {
            cls._normalize_text(item)
            for item in validated[
                "critical_missing_requirements"
            ]
        }

        validated["strong_matches"] = [
            item
            for item in validated["strong_matches"]
            if cls._normalize_text(item)
            not in critical
        ]

        return validated

    @staticmethod
    def _clean_list(
        value: Any,
    ) -> List[str]:
        """
        Convert a response field into a clean list of strings.
        """

        if value is None:
            return []

        if isinstance(value, str):
            value = [value]

        if not isinstance(value, list):
            return []

        cleaned = []

        for item in value:
            if not isinstance(item, str):
                continue

            item = item.strip()

            if item:
                cleaned.append(item)

        return cleaned

    @staticmethod
    def _unique(
        values: List[str],
    ) -> List[str]:
        """
        Remove duplicate strings while preserving order.
        """

        seen = set()
        result = []

        for value in values:
            key = value.casefold()

            if key in seen:
                continue

            seen.add(key)
            result.append(value)

        return result

    @classmethod
    def _clean_relevance(
        cls,
        value: Any,
    ) -> Dict[str, str]:
        """
        Validate a relevance object.

        Expected:

        {
            "level": "high",
            "explanation": "..."
        }
        """

        if not isinstance(value, dict):
            return {
                "level": "low",
                "explanation": "",
            }

        level = str(
            value.get("level", "low")
        ).strip().lower()

        if level not in cls.VALID_RELEVANCE_LEVELS:
            level = "low"

        explanation = value.get(
            "explanation",
            "",
        )

        if not isinstance(explanation, str):
            explanation = str(explanation)

        return {
            "level": level,
            "explanation": explanation.strip(),
        }

    @staticmethod
    def _normalize_text(
        value: str,
    ) -> str:
        """
        Normalize text for comparison.
        """

        return " ".join(
            value.casefold().split()
        )

    @classmethod
    def _ensure_parent_requirements(
        cls,
        missing: List[str],
        critical_missing: List[str],
    ) -> List[str]:
        """
        Ensure every critical missing requirement is also
        represented in missing_requirements.
        """

        result = list(missing)

        existing = {
            cls._normalize_text(item)
            for item in result
        }

        for item in critical_missing:
            normalized = cls._normalize_text(item)

            if normalized not in existing:
                result.append(item)
                existing.add(normalized)

        return result