import json
import re
from typing import Any, Dict

from app.ai.gemini_client import gemini_client


class ResumeGenerator:
    """
    Generates a truth-preserving, ATS-optimized resume
    from an existing resume and a target job description.

    Important:
    The AI must NOT invent:
        - companies
        - job titles
        - degrees
        - certifications
        - projects
        - technologies
        - achievements
        - metrics
    """

    @staticmethod
    def _extract_json(text: str) -> Dict[str, Any]:
        """
        Extract JSON from Gemini response.

        Handles:
            1. Pure JSON
            2. ```json ... ```
            3. Extra text surrounding JSON
        """

        if not text:
            raise ValueError(
                "AI returned an empty response."
            )

        cleaned = text.strip()

        # Remove markdown code fences.
        cleaned = re.sub(
            r"^```json\s*",
            "",
            cleaned,
            flags=re.IGNORECASE,
        )

        cleaned = re.sub(
            r"^```\s*",
            "",
            cleaned,
        )

        cleaned = re.sub(
            r"\s*```$",
            "",
            cleaned,
        )

        cleaned = cleaned.strip()

        # First attempt: complete response is JSON.
        try:
            result = json.loads(cleaned)

            if not isinstance(result, dict):
                raise ValueError(
                    "AI response JSON must be an object."
                )

            return result

        except json.JSONDecodeError:
            pass

        # Second attempt: locate the JSON object.
        start = cleaned.find("{")
        end = cleaned.rfind("}")

        if start == -1 or end == -1 or end <= start:
            raise ValueError(
                "AI response did not contain valid JSON."
            )

        json_text = cleaned[start:end + 1]

        try:
            result = json.loads(json_text)
        except json.JSONDecodeError as exc:
            raise ValueError(
                "AI returned malformed JSON."
            ) from exc

        if not isinstance(result, dict):
            raise ValueError(
                "AI response JSON must be an object."
            )

        return result

    @staticmethod
    def _build_prompt(
        resume_text: str,
        job_description: str,
    ) -> str:

        return f"""
You are an expert ATS resume optimization system.

Your task is to create a tailored resume using:

1. The candidate's EXISTING resume
2. The TARGET job description

IMPORTANT TRUTHFULNESS RULE:

You MUST NOT invent or fabricate information.

Do NOT create:
- fake companies
- fake job titles
- fake employment
- fake degrees
- fake certifications
- fake projects
- fake technologies
- fake achievements
- fake numbers
- fake percentages
- fake metrics
- fake dates

You may:
- rewrite existing information
- improve wording
- improve grammar
- reorder information
- emphasize skills already present
- emphasize projects already present
- make existing achievements more ATS-friendly
- use terminology from the job description ONLY when the candidate's resume genuinely supports it
- combine existing information without changing its meaning

If information does not exist in the resume, do NOT create it.

TARGET JOB DESCRIPTION:
-----------------------
{job_description}
-----------------------

BASE RESUME:
------------
{resume_text}
------------

Generate a professional ATS-optimized resume.

Return ONLY valid JSON.

The JSON must have exactly this structure:

{{
  "name": "candidate name",
  "email": "candidate email",
  "phone": "candidate phone",
  "location": "candidate location",
  "summary": "tailored professional summary",
  "skills": [
    "skill 1",
    "skill 2"
  ],
  "experience": [
    {{
      "company": "existing company",
      "role": "existing role",
      "duration": "existing duration",
      "bullets": [
        "rewritten truthful bullet",
        "rewritten truthful bullet"
      ]
    }}
  ],
  "projects": [
    {{
      "name": "existing project",
      "description": "truthful project description",
      "technologies": [
        "technology"
      ],
      "bullets": [
        "truthful project bullet"
      ]
    }}
  ],
  "education": [
    {{
      "degree": "existing degree",
      "institution": "existing institution",
      "duration": "existing duration"
    }}
  ],
  "certifications": [
    "existing certification"
  ],
  "links": [
    "existing portfolio/GitHub/LinkedIn link"
  ],
  "changes": [
    "brief description of meaningful tailoring change"
  ]
}}

Do not include markdown.
Do not include explanations outside JSON.
"""
    @staticmethod
    def to_text(
        generated_resume: dict,
    ) -> str:
        """
        Convert the structured generated resume into plain text
        so the existing ATS engine can analyze it.
        """

        sections = []

        name = generated_resume.get("name", "")
        email = generated_resume.get("email", "")
        phone = generated_resume.get("phone", "")
        location = generated_resume.get("location", "")

        contact = " | ".join(
            value
            for value in [
                name,
                email,
                phone,
                location,
            ]
            if value
        )

        if contact:
            sections.append(contact)

        summary = generated_resume.get(
            "summary",
            "",
        )

        if summary:
            sections.append(
                f"SUMMARY\n{summary}"
            )

        skills = generated_resume.get(
            "skills",
            [],
        )

        if skills:
            sections.append(
                "SKILLS\n"
                + ", ".join(skills)
            )

        experience = generated_resume.get(
            "experience",
            [],
        )

        if experience:
            experience_lines = [
                "EXPERIENCE"
            ]

            for item in experience:
                company = item.get(
                    "company",
                    "",
                )

                role = item.get(
                    "role",
                    "",
                )

                duration = item.get(
                    "duration",
                    "",
                )

                header = " | ".join(
                    value
                    for value in [
                        role,
                        company,
                        duration,
                    ]
                    if value
                )

                if header:
                    experience_lines.append(
                        header
                    )

                for bullet in item.get(
                    "bullets",
                    [],
                ):
                    experience_lines.append(
                        f"- {bullet}"
                    )

            sections.append(
                "\n".join(experience_lines)
            )

        projects = generated_resume.get(
            "projects",
            [],
        )

        if projects:
            project_lines = [
                "PROJECTS"
            ]

            for project in projects:
                name = project.get(
                    "name",
                    "",
                )

                if name:
                    project_lines.append(
                        name
                    )

                description = project.get(
                    "description",
                    "",
                )

                if description:
                    project_lines.append(
                        description
                    )

                technologies = project.get(
                    "technologies",
                    [],
                )

                if technologies:
                    project_lines.append(
                        "Technologies: "
                        + ", ".join(
                            technologies
                        )
                    )

                for bullet in project.get(
                    "bullets",
                    [],
                ):
                    project_lines.append(
                        f"- {bullet}"
                    )

            sections.append(
                "\n".join(project_lines)
            )

        education = generated_resume.get(
            "education",
            [],
        )

        if education:
            education_lines = [
                "EDUCATION"
            ]

            for item in education:
                degree = item.get(
                    "degree",
                    "",
                )

                institution = item.get(
                    "institution",
                    "",
                )

                duration = item.get(
                    "duration",
                    "",
                )

                line = " | ".join(
                    value
                    for value in [
                        degree,
                        institution,
                        duration,
                    ]
                    if value
                )

                if line:
                    education_lines.append(
                        line
                    )

            sections.append(
                "\n".join(education_lines)
            )

        certifications = generated_resume.get(
            "certifications",
            [],
        )

        if certifications:
            sections.append(
                "CERTIFICATIONS\n"
                + "\n".join(
                    f"- {certification}"
                    for certification in certifications
                )
            )

        links = generated_resume.get(
            "links",
            [],
        )

        if links:
            sections.append(
                "LINKS\n"
                + "\n".join(links)
            )

        return "\n\n".join(
            sections
        ).strip()

    @classmethod
    def generate(
        cls,
        resume_text: str,
        job_description: str,
    ) -> Dict[str, Any]:

        if not resume_text.strip():
            raise ValueError(
                "Resume text is empty."
            )

        if not job_description.strip():
            raise ValueError(
                "Job description is empty."
            )

        prompt = cls._build_prompt(
            resume_text=resume_text,
            job_description=job_description,
        )

        try:
            response = gemini_client.generate(
                prompt
            )
        except Exception as exc:
            raise RuntimeError(
                f"AI resume generation failed: {exc}"
            ) from exc

        result = cls._extract_json(
            response
        )

        # Remove changes from the generated resume object
        # and return them separately.
        changes = result.pop(
            "changes",
            [],
        )

        if not isinstance(changes, list):
            changes = []

        result["changes"] = [
            str(change)
            for change in changes
        ]

        return result