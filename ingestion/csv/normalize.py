import pandas as pd


def extract_text_from_csv(file_path: str):
    records = []

    try:
        # Attempt standard CSV parsing
        df = pd.read_csv(file_path)

    except pd.errors.ParserError:
        # Fallback: tolerate bad lines
        df = pd.read_csv(
            file_path,
            sep=None,
            engine="python",
            on_bad_lines="skip"
        )

    for idx, row in df.iterrows():
        text = " ".join(str(value) for value in row if pd.notna(value))

        records.append({
            "row": idx + 1,
            "text": text
        })

    return records
