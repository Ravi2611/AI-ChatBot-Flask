import os
import time
import logging
from config import WATCH_FOLDER, SCHEDULE_INTERVAL
from file_handler import handle_new_file

logger = logging.getLogger("scheduler")

def scan_folder():
    os.makedirs(WATCH_FOLDER, exist_ok=True)
    processed, skipped, failed = 0, 0, 0

    for filename in os.listdir(WATCH_FOLDER):
        if filename.startswith("."):  # Skip hidden/system files
            skipped += 1
            continue

        file_path = os.path.join(WATCH_FOLDER, filename)
        if os.path.isdir(file_path):  # Skip directories
            skipped += 1
            continue

        try:
            handle_new_file(file_path)
            processed += 1
        except Exception as e:
            logger.error(f"❌ Failed to process {file_path}: {e}")
            failed += 1

    logger.info(f"[SCHEDULER] Processed {processed} files, skipped {skipped}, failed {failed}")

def start_scheduler():
    logger.info(f"⏰ Scheduler started — scanning {WATCH_FOLDER} every {SCHEDULE_INTERVAL} seconds")
    try:
        while True:
            scan_folder()
            time.sleep(SCHEDULE_INTERVAL)
    except KeyboardInterrupt:
        logger.info("🛑 Scheduler stopped by user.")
    except Exception as e:
        logger.error(f"⚠️ Scheduler crashed: {e}")
