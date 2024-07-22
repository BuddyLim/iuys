"""Main entry point for queue events"""

import time
from hashlib import sha256
from threading import Thread

from pyee import EventEmitter

from ocu.utils import SingletonMeta


class Program(Thread):
    def __init__(self, sleep=None):
        super().__init__()
        self._sleeps = [sleep]
        self.daemon = True

    def run(self):
        # print(f"{datetime.now()}: A")
        print("Start sleeping")
        self._sleep_all()
        # print(f"{datetime.now()}: B")
        print("Finished sleeping")

    def add_sleep(self, sleep):
        self._sleeps.append(sleep)

    def _sleep_all(self):
        while self._sleeps:
            sleep = self._sleeps.pop()
            print(f"taking a nap for {sleep}s")
            time.sleep(sleep)


class QueueWorker(metaclass=SingletonMeta):
    task = []
    task_dict: dict[str, Program] = {}
    event_emitter = None

    def __init__(self, ee: EventEmitter) -> None:
        self.event_emitter = ee
        self.event_emitter.add_listener("new_file", self.new_file)

    def new_file(self, path: str):
        print(f"New file received from {path}")

        hashed_path = sha256(path.encode()).hexdigest()
        if hashed_path not in self.task_dict:
            print("Setting task_dict ", hashed_path)
            task_in_completion = Program(sleep=7)
            self.task_dict.update({hashed_path: task_in_completion})
            task_in_completion.start()
        else:
            print("Adding sleep")
            self.task_dict[hashed_path].add_sleep(sleep=5)
            self.task.append(path)

    def on_error(self, message):
        print(message)
