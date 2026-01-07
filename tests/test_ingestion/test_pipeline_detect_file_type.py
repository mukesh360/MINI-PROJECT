import os
import pytest
from unittest import mock

from ingestion.pipeline import detect_file_type


# ---------- Helpers ----------

def mock_exists(path):
    return True


# ---------- Tests ----------

def test_file_not_exists():
    with mock.patch("os.path.exists", return_value=False):
        assert detect_file_type("missing.file") == "unsupported"


def test_detect_pdf():
    with mock.patch("os.path.exists", mock_exists), \
         mock.patch("magic.from_file", return_value="application/pdf"):
        assert detect_file_type("sample.pdf") == "pdf"


def test_detect_csv_text_csv():
    with mock.patch("os.path.exists", mock_exists), \
         mock.patch("magic.from_file", return_value="text/csv"):
        assert detect_file_type("data.csv") == "csv"


def test_detect_csv_excel_mime():
    with mock.patch("os.path.exists", mock_exists), \
         mock.patch("magic.from_file", return_value="application/vnd.ms-excel"):
        assert detect_file_type("data.xls") == "csv"


def test_detect_text_file():
    with mock.patch("os.path.exists", mock_exists), \
         mock.patch("magic.from_file", return_value="text/plain"):
        assert detect_file_type("notes.txt") == "txt"


def test_detect_unknown_binary():
    with mock.patch("os.path.exists", mock_exists), \
         mock.patch("magic.from_file", return_value="application/octet-stream"):
        assert detect_file_type("binary.bin") == "unsupported"
