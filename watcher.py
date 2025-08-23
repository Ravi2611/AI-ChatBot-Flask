import os
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from config import WATCH_FOLDER
from file_handler import handle_new_file

logger = logging.getLogger("watcher")

class FileWatcherHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            logger.info(f"📂 New file detected: {event.src_path}")
            try:
                handle_new_file(event.src_path)
            except Exception as e:
                logger.error(f"❌ Error handling file {event.src_path}: {e}")

def start_watcher():
    os.makedirs(WATCH_FOLDER, exist_ok=True)
    event_handler = FileWatcherHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_FOLDER, recursive=False)
    observer.start()

    logger.info(f"👀 Watching folder: {WATCH_FOLDER}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("🛑 Stopping file watcher...")
        observer.stop()
    except Exception as e:
        logger.error(f"⚠️ Watcher crashed: {e}")
        observer.stop()
    observer.join()
    logger.info("✅ File watcher stopped cleanly.")
