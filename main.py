"""Main file for iuys"""

import threading
import gc
from pyee import EventEmitter
from ocu import QueueWorker, FileWatcher, VLMEngine
from ocu.utils import logger, SingletonMeta

# from mlx_lm import load, generate
from model import Bert, load_model


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
        # self.vlm_engine = VLMEngine()

    def run(self):
        """Running loop for the program"""
        while True:
            if len(self.worker.task_list) == 0 or self.in_progress:
                continue

            vlm_engine = VLMEngine()

            logger.info(f"Received a new task: {self.worker.task_list[0]}")

            self.in_progress = True
            path = self.worker.task_list.pop()
            response = vlm_engine.query_on_image(
                prompt="Describe the contents of the image in a short and concise manner",
                image_path=path,
            )

            logger.info(f"{vlm_engine.model_path} generated:\n{response}")
            del vlm_engine
            self.in_progress = False
            gc.collect()


if __name__ == "__main__":
    try:
        # MainProgram().run()

        model, tokenizer = load_model(
            "sentence-transformers/all-MiniLM-L6-v2", "./model/all-MiniLM-L6-v2.npz"
        )
    except KeyboardInterrupt:
        logger.info("Keyboard interruption; Stopped")
