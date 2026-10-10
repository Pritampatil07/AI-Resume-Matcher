import pytest

from backend.parser import (
    extract_resume_text,
    ResumeParsingError,
)


def test_rejects_empty_file():
    with pytest.raises(ResumeParsingError):
        extract_resume_text("resume.pdf", b"")


def test_rejects_unsupported_file():
    with pytest.raises(ResumeParsingError):
        extract_resume_text(
            "resume.txt",
            b"This is a sample resume text."
        )


def test_rejects_oversized_file():
    with pytest.raises(ResumeParsingError):
        extract_resume_text(
            "resume.pdf",
            b"x" * (5 * 1024 * 1024 + 1)
        )
