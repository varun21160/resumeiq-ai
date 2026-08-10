import json
from typing import Any, Dict

from app.ai.gemini_client import gemini_client
from app.ai.semantic_validator import SemanticValidator


class SemanticAnalyzer:
    """
    Uses Gemini to perform semantic analysis between
    a resume and a job description.

    This layer does NOT calculate the main ATS score.

    It identifies:
    - Strong matches
    - Partial matches
    - Missing requirements
    - Critical missing requirements
    - Preferred missing requirements
    - Experience relevance
    - Project relevance
    - Education relevance
    - Key strengths
    - Key gaps
    - JD-specific recommendations
    """

    @staticmethod
    def analyze(
        resume_text: str,
        job_description: str,
    ) -> Dict[str, Any]:
        """
        Analyze the semantic relationship between a resume
        and a job description.
        """

        if not resume_text or not resume_text.strip():
            raise ValueError(
                "Resume text cannot be empty."
            )

        if not job_description or not job_description.strip():
            raise ValueError(
                "Job description cannot be empty."
            )

        prompt = f"""
You are an expert ATS and recruitment analysis engine.

Analyze the following resume against the given job description.

Your goal is to determine how well the candidate's actual
experience, skills, projects, education, and qualifications
align with the job requirements.

IMPORTANT RULES:

1. Do not invent information that is not present in the resume.

2. Do not assume that a keyword match means the candidate has
   meaningful experience with that skill.

3. Distinguish between:
   - exact matches
   - semantically related matches
   - partial matches
   - missing requirements
   - critical missing requirements
   - preferred missing requirements

4. Identify requirements that appear critical to the job.

5. A requirement should be classified as CRITICAL only when the
   job description clearly presents it as:
   - mandatory
   - required
   - essential
   - a core responsibility
   - a must-have qualification

6. Requirements described using terms such as:
   - preferred
   - preferred qualification
   - nice to have
   - plus
   - bonus
   - desirable
   - good to have

   must NOT be classified as critical missing requirements.
   Put them under preferred_missing_requirements instead.

7. General soft skills such as communication, teamwork,
   leadership, adaptability, and problem-solving should NOT
   automatically be classified as critical missing requirements.

8. A soft skill should only be classified as critical when the
   job description explicitly makes it a mandatory qualification
   or essential responsibility.

9. Do not infer that a missing skill is critical merely because
   it appears somewhere in the job description.

10. Evaluate whether the candidate's experience is relevant
    to the target role.

11. Evaluate whether the candidate's projects are relevant
    to the target role.

12. Evaluate whether the candidate's education is relevant
    to the target role.

13. Base every conclusion only on evidence available in the
    resume and job description.

14. Do not invent companies, responsibilities, technologies,
    achievements, certifications, metrics, or experience.

15. Do not calculate the final ATS score.

16. Return ONLY valid JSON.

17. Do not wrap the JSON in markdown code fences.

JOB DESCRIPTION:
----------------
{job_description}

RESUME:
----------------
{resume_text}

Return JSON using exactly this structure:

{{
    "strong_matches": [
        "..."
    ],
    "partial_matches": [
        "..."
    ],
    "missing_requirements": [
        "..."
    ],
    "critical_missing_requirements": [
        "..."
    ],
    "preferred_missing_requirements": [
        "..."
    ],
    "experience_relevance": {{
        "level": "high | medium | low",
        "explanation": "..."
    }},
    "project_relevance": {{
        "level": "high | medium | low",
        "explanation": "..."
    }},
    "education_relevance": {{
        "level": "high | medium | low",
        "explanation": "..."
    }},
    "key_strengths": [
        "..."
    ],
    "key_gaps": [
        "..."
    ],
    "recommendations": [
        "..."
    ]
}}
"""

        response = gemini_client.generate(
            prompt
        )

        parsed_response = SemanticAnalyzer._parse_response(
            response
        )

        return SemanticValidator.validate(
            parsed_response
        )

    @staticmethod
    def _parse_response(
        response: str,
    ) -> Dict[str, Any]:
        """
        Safely parse Gemini's JSON response.
        """

        if not response:
            raise ValueError(
                "Gemini returned an empty response."
            )

        cleaned = response.strip()

        # Remove markdown code fences if Gemini
        # unexpectedly returns them.
        if cleaned.startswith("```"):
            lines = cleaned.splitlines()

            # Remove opening fence
            if lines:
                lines = lines[1:]

            # Remove closing fence
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]

            cleaned = "\n".join(lines).strip()

        try:
            result = json.loads(cleaned)

        except json.JSONDecodeError as exc:
            raise ValueError(
                "Gemini returned an invalid JSON response."
            ) from exc

        if not isinstance(result, dict):
            raise ValueError(
                "Gemini response must be a JSON object."
            )

        return result