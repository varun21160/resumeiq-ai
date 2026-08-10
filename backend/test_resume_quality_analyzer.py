from pprint import pprint

from app.resume.document_parser import DocumentParser
from app.ai.analyzers.resume_quality_analyzer import (
    ResumeQualityAnalyzer,
)


FILE_PATH = r"F:\resume.pdf"


try:
    resume_text = DocumentParser.extract_text(
        FILE_PATH
    )

    result = ResumeQualityAnalyzer.analyze(
        resume_text=resume_text,
        job_description="",
    )

    print("\n========== RESUME QUALITY ==========\n")

    pprint(
        result.model_dump()
    )

    print(
        "\n===================================="
    )

except Exception as exc:
    print(
        f"\nERROR: {exc}"
    )