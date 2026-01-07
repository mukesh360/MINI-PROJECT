import os
import magic


def detect_file_type(file_path: str) -> str:
    """
    Detect file type using MIME sniffing instead of extension.
    """
    if not os.path.exists(file_path):
        return "unsupported"

    mime = magic.from_file(file_path, mime=True)

    if mime == "application/pdf":
        return "pdf"
    elif mime in ("text/csv", "application/csv", "application/vnd.ms-excel"):
        return "csv"
    elif mime.startswith("text/"):
        return "txt"
    else:
        return "unsupported"


'''
import os

def detect_file_type(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return "pdf"
    elif ext == ".csv":
        return "csv"
    elif ext == ".txt":
        return "txt"
    else:
        return "unsupported"

'''