from typing import List

from app.ai.fuzzy_matcher import FuzzyMatcher
from app.ai.skill_weights import SKILL_WEIGHTS


class ATSScorer:

    @staticmethod
    def calculate(
        resume_skills: List[str],
        jd_skills: List[str],
    ):

        matched = []
        missing = []

        total_weight = 0
        matched_weight = 0

        for jd_skill in jd_skills:

            weight = SKILL_WEIGHTS.get(jd_skill, 5)
            total_weight += weight

            found = False

            for resume_skill in resume_skills:

                if (
                    resume_skill == jd_skill
                    or FuzzyMatcher.is_match(
                        resume_skill,
                        jd_skill,
                    )
                ):
                    matched.append(jd_skill)
                    matched_weight += weight
                    found = True
                    break

            if not found:
                missing.append(jd_skill)

        score = (
            round((matched_weight / total_weight) * 100)
            if total_weight > 0
            else 0
        )

        return {
            "ats_score": score,
            "matched_skills": sorted(set(matched)),
            "missing_skills": sorted(set(missing)),
        }