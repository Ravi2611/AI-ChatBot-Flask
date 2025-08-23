import pandas as pd
import logging

logger = logging.getLogger("excel_parser")

def extract_text(file_path):
    """Extract text from Excel and return list of dicts with context info."""
    logger.info(f"[EXTRACTING EXCEL] {file_path}")
    text_data = []
    try:
        df = pd.read_excel(file_path)
        for i, row in df.iterrows():
            # Add column names for context
            text = ', '.join([f"{col}: {row[col]}" for col in df.columns])
            text_data.append({
                "text": text,
                "source_file": file_path,
                "row": i,
                "type": "table"
            })

        logger.info(f"✅ Extracted {len(text_data)} rows from Excel: {file_path}")
        return text_data

    except Exception as e:
        logger.exception(f"[ERROR] Failed to extract Excel {file_path}: {e}")
        return []
