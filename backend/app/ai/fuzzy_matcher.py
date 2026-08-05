from rapidfuzz import fuzz


class FuzzyMatcher:

    MATCH_THRESHOLD = 85

    @staticmethod
    def is_match(skill1: str, skill2: str) -> bool:
        """
        Returns True if two skills are similar enough.
        """
        similarity = fuzz.ratio(
            skill1.lower(),
            skill2.lower(),
        )

        return similarity >= FuzzyMatcher.MATCH_THRESHOLD