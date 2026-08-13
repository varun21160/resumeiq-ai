from pathlib import Path
import tempfile

from app.resume.document_parser import DocumentParser


def expect_error(
    name,
    expected_exception,
    function,
):
    try:
        function()

    except expected_exception as exc:
        print(
            f"✅ {name}: "
            f"{type(exc).__name__} - {exc}"
        )
        return

    except Exception as exc:
        print(
            f"❌ {name}: "
            f"Wrong exception {type(exc).__name__}"
        )
        return

    print(
        f"❌ {name}: "
        f"No exception was raised"
    )


def test_missing_file():

    expect_error(
        "Missing file",
        FileNotFoundError,
        lambda: DocumentParser.extract_text(
            "does_not_exist.pdf"
        ),
    )


def test_unsupported_file():

    with tempfile.NamedTemporaryFile(
        suffix=".txt",
        delete=False,
    ) as temp:

        temp_path = temp.name

    try:

        expect_error(
            "Unsupported file",
            ValueError,
            lambda: DocumentParser.extract_text(
                temp_path
            ),
        )

    finally:

        Path(temp_path).unlink(
            missing_ok=True
        )


def test_empty_pdf():

    with tempfile.NamedTemporaryFile(
        suffix=".pdf",
        delete=False,
    ) as temp:

        temp_path = temp.name

    try:

        expect_error(
            "Empty PDF",
            ValueError,
            lambda: DocumentParser.extract_text(
                temp_path
            ),
        )

    finally:

        Path(temp_path).unlink(
            missing_ok=True
        )


def test_empty_docx():

    with tempfile.NamedTemporaryFile(
        suffix=".docx",
        delete=False,
    ) as temp:

        temp_path = temp.name

    try:

        expect_error(
            "Empty DOCX",
            ValueError,
            lambda: DocumentParser.extract_text(
                temp_path
            ),
        )

    finally:

        Path(temp_path).unlink(
            missing_ok=True
        )


if __name__ == "__main__":

    print()
    print(
        "========== DOCUMENT VALIDATION TESTS =========="
    )

    test_missing_file()
    test_unsupported_file()
    test_empty_pdf()
    test_empty_docx()

    print(
        "==============================================="
    )

    print(
        "\nValidation tests completed."
    )