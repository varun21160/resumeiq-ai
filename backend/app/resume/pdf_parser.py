from pathlib import Path

from pypdf import PdfReader


class PDFParser:
    """
    Extracts text from PDF resume files.
    """

    @staticmethod
    def extract(file_path: str) -> str:
        """
        Extract text from all pages of a PDF.

        Raises:
            FileNotFoundError:
                If the file does not exist.

            ValueError:
                If the PDF cannot be read or contains no text.
        """

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Resume file not found: {file_path}"
            )

        if path.suffix.lower() != ".pdf":
            raise ValueError(
                "PDFParser only supports PDF files."
            )

        try:
            reader = PdfReader(str(path))
        except Exception as exc:
            raise ValueError(
                "Unable to read the PDF resume."
            ) from exc

        pages = []

        for page in reader.pages:
            try:
                text = page.extract_text() or ""
            except Exception:
                text = ""

            if text.strip():
                pages.append(text)

        extracted_text = "\n".join(pages).strip()

        if not extracted_text:
            raise ValueError(
                "No readable text was found in the PDF. "
                "The resume may be image-based or scanned."
            )

        return extracted_text