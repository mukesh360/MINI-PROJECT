from unittest import mock
from ingestion.pdf.extract import extract_text_from_pdf


def test_extract_text_from_pdf_mocked():
    fake_page = mock.Mock()
    fake_page.extract_text.return_value = "Sample text"

    fake_pdf = mock.Mock()
    fake_pdf.pages = [fake_page]

    with mock.patch("pdfplumber.open", return_value=fake_pdf):
        results = extract_text_from_pdf("dummy.pdf")

    assert len(results) == 1
    assert results[0]["page"] == 1
    assert results[0]["text"] == "Sample text"


