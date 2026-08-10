from pprint import pprint

from app.resume.document_parser import DocumentParser
from app.resume.structured_resume import StructuredResumeExtractor


FILE_PATH = r"F:\resume.pdf"


try:
    resume_text = DocumentParser.extract_text(
        FILE_PATH
    )

    structured = StructuredResumeExtractor.extract(
        resume_text
    )

    print("\n========== STRUCTURED RESUME ==========\n")

    pprint(structured)

    print(
        "\n======================================="
    )

    print(
        "\nDetected sections:"
    )

    for section in structured["detected_sections"]:
        print(
            f"  ✓ {section}"
        )

except Exception as exc:
    print(
        f"\nERROR: {exc}"
    )