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
from ocu.utils import SingletonMeta, logger


class _Handler(FileSystemEventHandler, metaclass=SingletonMeta):
    """Event watching handler for file creation/modified events"""

    event_emitter = None

    def __init__(self, ee: EventEmitter) -> None:
        super().__init__()
        self.event_emitter = ee

    def on_any_event(self, event: FileSystemEvent):
        """Handle on create or modify file events"""
        if event.is_directory:
            return None

        elif event.event_type == EVENT_TYPE_MODIFIED:
            try:
                if os.path.isfile(event.src_path) is False:
                    return
                logger.info(f"Emitting message for {event.src_path}")
                self.event_emitter.emit("new_file", event.src_path)
            except ValueError as error:
                logger.error(f"{error} for {event.src_path}")


class FileWatcher(metaclass=SingletonMeta):
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
        self.observer = Observer()
        self.event_handler = _Handler(ee=ee)

    def observe(self):
        """Main func for running loop to watch for file changes"""
        try:
            logging.info("Start watching directory % s", self.path)
            self.observer.schedule(self.event_handler, self.path, recursive=False)
            self.observer.start()
            while True:
                time.sleep(4)
        except Exception as error:  # pylint: disable=W0718
            logging.error(error)
        finally:
            self.observer.stop()
            self.observer.join()
