"""Main entrypoint for filewatching"""

import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import (
    FileSystemEventHandler,
    FileSystemEvent,
    EVENT_TYPE_CREATED,
    EVENT_TYPE_MODIFIED,
)


class Handler(FileSystemEventHandler):
    """File watching handler for file creation/modified events"""

    @staticmethod
    def on_create_or_modify(event: FileSystemEvent):
        """Handle on create or modify file events"""
        if event.is_directory:
            return None

        elif event.event_type == EVENT_TYPE_CREATED:
            # Event is created, you can process it now
            print(f"Watchdog received created event - {event.src_path}")
        elif event.event_type == EVENT_TYPE_MODIFIED:
            print(f"Watchdog received modified event - {event.src_path}")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    logging.info("start watching directory % s", path)
    event_handler = Handler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(5)
    finally:
        observer.stop()
        observer.join()
