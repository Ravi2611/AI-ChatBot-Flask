import os
import logging
from config import WATCH_FOLDER
from parsers import csv_parser, excel_parser, pdf_parser, docx_parser

logger = logging.getLogger("file_handler")
processed_files = set()

def process_file(file_path, embedding_index):
    """Process a single file and add its text to Postgres."""
    ext = os.path.splitext(file_path)[1].lower()
    text_data = []

    try:
        if ext == ".csv":
            text_data = csv_parser.extract_text(file_path)
        elif ext in [".xlsx", ".xls"]:
            text_data = excel_parser.extract_text(file_path)
        elif ext == ".pdf":
            text_data = pdf_parser.extract_text(file_path)
        elif ext == ".docx":
            text_data = docx_parser.extract_text(file_path)
        else:
            logger.warning(f"Unsupported file type: {file_path}")
            return False

        if text_data:
            added_count = 0
            skipped_count = 0

            for item in text_data:
                try:
                    embedding_index.add_texts([item], file_name=os.path.basename(file_path))
                    added_count += 1
                except Exception as e:
                    logger.warning(f"⚠️ Skipping duplicate or error for text: {item.get('text', '')[:50]}... ({e})")
                    skipped_count += 1

            logger.info(f"✅ Metadata added from {file_path} → Added: {added_count}, Skipped: {skipped_count}")
            return True
        else:
            logger.warning(f"No text extracted from {file_path}, skipping.")
            return False

    except Exception as e:
        logger.exception(f"Error processing file {file_path}: {e}")
        return False

def handle_new_file(file_path, embedding_index):
    """Handle a newly added file (skip hidden/system files)."""
    if os.path.basename(file_path).startswith('.'):
        logger.debug(f"Ignoring hidden/system file: {file_path}")
        return "skipped"

    if os.path.isfile(file_path) and file_path not in processed_files:
        logger.info(f"[PROCESSING NEW FILE] {file_path}")
        processed_files.add(file_path)
        success = process_file(file_path, embedding_index)
        return "processed" if success else "failed"
    else:
        logger.debug(f"File already processed or invalid: {file_path}")
        return "skipped"

def process_existing_files(embedding_index):
    """Process all files already present in the folder."""
    os.makedirs(WATCH_FOLDER, exist_ok=True)
    logger.info(f"Scanning existing files in folder: {WATCH_FOLDER}")

    processed, skipped, failed = 0, 0, 0
    for filename in os.listdir(WATCH_FOLDER):
        file_path = os.path.join(WATCH_FOLDER, filename)
        if os.path.isfile(file_path):
            result = handle_new_file(file_path, embedding_index)
            if result == "processed":
                processed += 1
            elif result == "skipped":
                skipped += 1
            elif result == "failed":
                failed += 1

    logger.info(f"📊 File processing summary → Processed: {processed}, Skipped: {skipped}, Failed: {failed}")


