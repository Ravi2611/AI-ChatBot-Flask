import pandas as pd
import logging

logger = logging.getLogger("csv_parser")

def extract_text(file_path):
    """Extract text from CSV and return list of dicts with context info."""
    logger.info(f"[EXTRACTING CSV] {file_path}")
    try:
        df = pd.read_csv(file_path)
        text_data = []

        for i, row in df.iterrows():
            # Include column names for context
            text = ', '.join([f"{col}: {row[col]}" for col in df.columns])
            text_data.append({
                "text": text,
                "source_file": file_path,
                "row": i,
                "type": "table"
            })

        logger.info(f"✅ Extracted {len(text_data)} rows from CSV: {file_path}")
        return text_data

    except Exception as e:
        logger.exception(f"[ERROR] Failed to extract CSV {file_path}: {e}")
        return []
