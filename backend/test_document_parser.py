from app.resume.document_parser import DocumentParser


FILE_PATH = r"F:\resume.pdf"

try:
    text = DocumentParser.extract_text(
        FILE_PATH
    )

    print("\n========== EXTRACTED RESUME ==========\n")
    print(text)

    print(
        "\n======================================"
    )

    print(
        f"\nCharacters extracted: {len(text)}"
    )

    print(
        f"Words extracted: {len(text.split())}"
    )

except Exception as exc:
    print(
        f"\nERROR: {exc}"
    )