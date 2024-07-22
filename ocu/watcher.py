"""Main entrypoint for filewatching"""

import time
import logging
import os
from pyee import EventEmitter
from watchdog.observers import Observer
from watchdog.events import (
    FileSystemEventHandler,
    FileSystemEvent,
    EVENT_TYPE_MODIFIED,
)


class _Handler(FileSystemEventHandler):
    """Event watching handler for file creation/modified events"""

    event_emitter = None

    def __init__(self, ee: EventEmitter) -> None:
        super().__init__()
        self.event_emitter = ee

    def on_any_event(self, event: FileSystemEvent):
        """Handle on create or modify file events"""
        if event.is_directory:
            return None

        # # elif event.event_type == EVENT_TYPE_CREATED:
        # #     # Event is created, you can process it now
        # #     print(f"Watchdog received created event - {event.src_path}")

        elif event.event_type == EVENT_TYPE_MODIFIED:
            try:
                if os.path.isfile(event.src_path) is False:
                    return
                print("Emitting message..")
                resp = self.event_emitter.emit("new_file", event.src_path)
                print(resp)
            except ValueError:
                pass
            # print(f"Watchdog received modified event - {event.src_path}")


class FileWatcher:
    """Main implementation for file watching for local I/O ops"""

    observer = None
    path = "."

    def __init__(self, ee: EventEmitter, input_path=".") -> None:
        if len(input_path) > 1:
            self.path = input_path

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        logging.info("start watching directory % s", self.path)
        self.observer = Observer()
        self.event_handler = _Handler(ee=ee)

    def observe(self):
        self.observer.schedule(self.event_handler, self.path, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        finally:
            self.observer.stop()
            self.observer.join()
