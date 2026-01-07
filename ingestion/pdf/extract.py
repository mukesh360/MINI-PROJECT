import pdfplumber


def extract_text_from_pdf(file_path: str):
    pages_text = []

    with pdfplumber.open(file_path) as pdf:
        for page_no, page in enumerate(pdf.pages):
            text = page.extract_text()

            if text and text.strip():
                pages_text.append({
                    "page": page_no + 1,
                    "text": text.strip()
                })

    return pages_text
