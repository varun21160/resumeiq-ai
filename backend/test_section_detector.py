from pprint import pprint

from app.resume.document_parser import DocumentParser
from app.resume.section_detector import SectionDetector


FILE_PATH = r"F:\resume.pdf"


try:
    resume_text = DocumentParser.extract_text(
        FILE_PATH
    )

    sections = SectionDetector.detect(
        resume_text
    )

    print("\n========== DETECTED SECTIONS ==========\n")

    for section_name, content in sections.items():
        print(f"\n--- {section_name.upper()} ---")
        print(content[:1000])

    print(
        "\n======================================="
    )

    print(
        "\nSections detected:",
        list(sections.keys()),
    )

except Exception as exc:
    print(
        f"\nERROR: {exc}"
    )