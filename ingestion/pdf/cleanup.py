import re
import unicodedata


def normalize_text(text: str) -> str:
    # Unicode normalization
    text = unicodedata.normalize("NFKC", text)

    # Remove dot leaders (......)
    text = re.sub(r"\.{3,}", " ", text)

    # Replace multiple newlines with max two
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Replace multiple spaces/tabs with single space
    text = re.sub(r"[ \t]+", " ", text)

    # Remove non-printable characters (except newline)
    text = re.sub(r"[^\x20-\x7E\n]", "", text)

    # Strip leading/trailing whitespace
    text = text.strip()

    return text
