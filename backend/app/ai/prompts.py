def build_resume_review_prompt(resume_text: str) -> str:
    return f"""
You are an expert ATS reviewer and career coach.

Analyze the following resume.

Return your response in Markdown with the following sections:

## Overall Summary

## Strengths
- ...

## Weaknesses
- ...

## Suggestions
- ...

Resume:

{resume_text}
"""


def build_resume_tailor_prompt(
    resume_text: str,
    job_description: str,
) -> str:
    return f"""
You are an expert resume writer.

Optimize the resume for the following job description.

Keep the information truthful.
Do not invent experience.
Improve wording, keywords, and ATS compatibility.

Resume:

{resume_text}

Job Description:

{job_description}
"""


def build_cover_letter_prompt(
    resume_text: str,
    company: str,
    job_title: str,
    job_description: str,
) -> str:
    return f"""
Write a professional cover letter.

Company:
{company}

Job Title:
{job_title}

Job Description:
{job_description}

Candidate Resume:

{resume_text}
"""


def build_interview_prompt(
    resume_text: str,
    job_description: str,
) -> str:
    return f"""
Based on the resume and job description, generate:

- 10 Technical Interview Questions
- 5 HR Interview Questions

For every question, provide a short answer hint.

Resume:

{resume_text}

Job Description:

{job_description}
"""