"""Main file for iuys"""

import threading
from pyee import EventEmitter
from ocu import QueueWorker, VLMEngine, FileWatcher
from ocu.utils import logger, SingletonMeta


emitter = EventEmitter()


def run_watcher():
    """Main function to start file observer"""
    base_path = "/Users/limkuangtar/Desktop"
    watcher = FileWatcher(ee=emitter, input_path=base_path)
    watcher.observe()


class MainProgram(metaclass=SingletonMeta):
    """Main entrypoint for running the program"""

    in_progress = False

    def __init__(self) -> None:
        self.background_thread = threading.Thread(target=run_watcher, args=())
        self.background_thread.daemon = True
        self.background_thread.start()
        self.worker = QueueWorker(ee=emitter)
        self.vlm_engine = VLMEngine()

    def run(self):
        """Running loop for the program"""
        while True:
            if len(self.worker.task_list) == 0 or self.in_progress:
                continue

            logger.info(f"Received a new task: {self.worker.task_list[0]}")
            self.in_progress = True
            path = self.worker.task_list.pop()
            response = self.vlm_engine.query_on_image(
                prompt="Describe the image to me", image_path=path
            )
            logger.info(f"{self.vlm_engine.model_path} generated:\n{response}")
            self.in_progress = False


if __name__ == "__main__":
    try:
        MainProgram().run()
    except KeyboardInterrupt:
        logger.info("Keyboard interruption; Stopped")
