from pathlib import Path

from app.services.resume_extractor import ResumeExtractor


FILE_PATH = Path(
 r"F:\resume.pdf"
)


try:
    text = ResumeExtractor.extract(FILE_PATH)

    print()
    print("=" * 60)
    print("RESUME EXTRACTION SUCCESS")
    print("=" * 60)

    print(text)

    print("=" * 60)
    print(f"Characters extracted: {len(text)}")
    print(f"Words extracted: {len(text.split())}")
    print("=" * 60)

except Exception as exc:
    print()
    print("=" * 60)
    print("EXTRACTION FAILED")
    print("=" * 60)
    print(exc)
    print("=" * 60)