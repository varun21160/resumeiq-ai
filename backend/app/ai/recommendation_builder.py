from typing import List


class RecommendationBuilder:
    """
    Builds recommendations for different analyzers.
    """

    @staticmethod
    def skill_recommendations(
        missing_skills: List[str],
        extra_skills: List[str],
    ) -> List[str]:

        recommendations = []

        if missing_skills:
            recommendations.append(
                f"Add the following missing skills: {', '.join(missing_skills)}."
            )

        if extra_skills:
            recommendations.append(
                "Highlight projects or experience demonstrating your additional skills."
            )

        return recommendations

    @staticmethod
    def experience_recommendations(
        years: int,
        matched_roles: List[str],
    ) -> List[str]:

        recommendations = []

        if years == 0:
            recommendations.append(
                "Clearly mention internships or professional experience."
            )

        if not matched_roles:
            recommendations.append(
                "Use job titles that closely match the target position."
            )

        return recommendations

    @staticmethod
    def project_recommendations(
        project_count: int,
        github: bool,
        portfolio: bool,
    ) -> List[str]:

        recommendations = []

        if project_count < 2:
            recommendations.append(
                "Include at least two strong technical projects."
            )

        if not github:
            recommendations.append(
                "Add GitHub repository links to showcase your work."
            )

        if not portfolio:
            recommendations.append(
                "Include a portfolio or live demo link."
            )

        return recommendations

    @staticmethod
    def education_recommendations(
        degree: str | None,
        branch: str | None,
        cgpa: float | None,
    ) -> List[str]:

        recommendations = []

        if not degree:
            recommendations.append(
                "Mention your highest degree."
            )

        if not branch:
            recommendations.append(
                "Include your specialization or branch."
            )

        if cgpa is None:
            recommendations.append(
                "Mention your CGPA if it strengthens your profile."
            )

        elif cgpa < 7:
            recommendations.append(
                "Highlight projects, certifications, and technical skills to offset a lower CGPA."
            )

        return recommendations
    
    @staticmethod
    def certification_recommendations(
        certification_count: int,
        relevant_count: int,
    ) -> List[str]:

        recommendations = []

        if certification_count == 0:
            recommendations.append(
                "Add relevant industry certifications to strengthen your profile."
            )

        elif certification_count < 3:
            recommendations.append(
                "Consider earning more certifications related to your target role."
            )

        if relevant_count == 0 and certification_count > 0:
            recommendations.append(
                "Add certifications that align more closely with the job description."
            )

        return recommendations