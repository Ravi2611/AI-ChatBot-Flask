import PyPDF2
import logging

logger = logging.getLogger("pdf_parser")

def extract_text(file_path):
    """Extract text from PDF and return list of dicts with context info."""
    logger.info(f"[EXTRACTING PDF] {file_path}")
    text_data = []
    try:
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                if text:
                    # Split into paragraphs for better chunking
                    for j, para in enumerate(text.split('\n\n')):
                        para = para.strip()
                        if para:
                            text_data.append({
                                "text": para,
                                "source_file": file_path,
                                "page": i,
                                "paragraph": j,
                                "type": "pdf"
                            })

        logger.info(f"✅ Extracted {len(text_data)} chunks from PDF: {file_path}")
        return text_data

    except Exception as e:
        logger.exception(f"[ERROR] Failed to extract PDF {file_path}: {e}")
        return []
