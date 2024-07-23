"""Main entry point for queue events"""

import time
from hashlib import sha256
from threading import Thread
from typing import List

from pyee import EventEmitter

from ocu.utils import SingletonMeta, logger


class QueueThread(Thread):
    """Thread handler to delay new entry of tasks for `QueueWorker.tasks`"""

    def __init__(self, task: str, sleep=None):
        super().__init__()
        self._sleeps = [sleep]
        self.daemon = True
        self.task = task

    def run(self):
        logger.info(f"Start sleeping for task: {self.task}")
        self._sleep_all()
        logger.info(f"Finished sleeping for task: {self.task}")
        return

    def add_sleep(self, sleep):
        """Allows the thread to add more delay to the execution"""
        self._sleeps.append(sleep)

    def _sleep_all(self):
        while self._sleeps:
            sleep = self._sleeps.pop()
            logger.info(f"Taking more sleep for task: {self.task} of {sleep}s")
            time.sleep(sleep)


class QueueWorker(metaclass=SingletonMeta):
    """Main entry point for receiving new file creation events"""

    task_list: List[str] = []
    task_dict: dict[str, QueueThread] = {}
    event_emitter = None
    _sleep_duration = 5

    def __init__(self, ee: EventEmitter) -> None:
        self.event_emitter = ee
        self.event_emitter.add_listener("new_file", self.new_file)
        self.event_emitter.add_listener("error", self.on_error)

    def new_file(self, path: str):
        """
        Handles new file creation from watchdog.
        Because of how sometimes files are created, for example, screenshots,
        we need to first, hash the string path to create an unique ID and
        find a way to delay the new entry into `self.task` as the I/O operation
        may have not been completed yet
        """
        logger.info(f"New event received from {path}")
        hashed_path = sha256(path.encode()).hexdigest()

        if hashed_path not in self.task_dict:
            logger.info(f"New file from {path}")
            logger.info(f"Setting task_dict: {hashed_path}")

            task_in_completion = QueueThread(
                sleep=self._sleep_duration, task=hashed_path
            )
            self.task_dict.update({hashed_path: task_in_completion})
            task_in_completion.start()
            return

        logger.info(f"Existing file but new event from {path}")
        logger.info(f"Adding sleep for: {hashed_path}")

        self.task_dict[hashed_path].add_sleep(sleep=self._sleep_duration)
        self.task_list.append(path)
        del self.task_dict[hashed_path]

    def on_error(self, message):
        """Handles when event emitter has error"""
        logger.error(message)
