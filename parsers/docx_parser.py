from docx import Document
import logging

logger = logging.getLogger("docx_parser")

def extract_text(file_path):
    """Extract text from DOCX and return list of dicts with context info."""
    logger.info(f"[EXTRACTING DOCX] {file_path}")
    text_data = []
    try:
        doc = Document(file_path)
        for i, para in enumerate(doc.paragraphs):
            text = para.text.strip()
            if text:
                text_data.append({
                    "text": text,
                    "source_file": file_path,
                    "paragraph": i,
                    "type": "paragraph"
                })

        logger.info(f"✅ Extracted {len(text_data)} paragraphs from DOCX: {file_path}")
        return text_data

    except Exception as e:
        logger.exception(f"[ERROR] Failed to extract DOCX {file_path}: {e}")
        return []
