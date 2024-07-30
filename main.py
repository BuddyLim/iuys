"""Main file for iuys"""

import threading
import gc
from pyee import EventEmitter
from ocu.worker import QueueWorker
from ocu.watcher import FileWatcher
from ocu.vlm import VLMEngine
from ocu.utils import logger, SingletonMeta
from ocu.v_store import VectorDBConnection
from ocu.kv_store import KVConnection

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
        try:
            self.background_thread = threading.Thread(target=run_watcher, args=())
            self.background_thread.daemon = True
            self.background_thread.start()
            self.worker = QueueWorker(ee=emitter)
            self.kv_connection = KVConnection()
            self.v_connection = VectorDBConnection()

        except Exception as error:  # pylint: disable=broad-except
            logger.error(error)
            raise

    def run(self):
        """Running loop for the program"""
        while True:
            if len(self.worker.task_list) == 0 or self.in_progress:
                continue

            logger.info(f"Received a new task: {self.worker.task_list[0]}")
            self.in_progress = True

            path = self.worker.task_list.pop()
            response = self.get_vlm_response(path=path)
            self.store_response(text=response, path=path)

            self.in_progress = False

    def get_vlm_response(self, path: str) -> str:
        # Need to refactor this into it's own handlerclass
        """Query the vlm for its inference on image"""
        vlm_engine = VLMEngine()

        response = vlm_engine.query_on_image(
            prompt="Describe the contents of the image in precise but short details",
            image_path=path,
        )

        logger.info(f"{vlm_engine.model_path} generated:\n{response}")
        del vlm_engine
        gc.collect()
        return response

    def store_response(self, text: str, path: str):
        """Stores the response into the vector db"""

        self.v_connection.store_text(text, path)
        self.kv_connection.store_kv(path, text)
        logger.info(f"Stored entry of: {path}")
        gc.collect()


if __name__ == "__main__":
    try:
        MainProgram().run()
    except KeyboardInterrupt:
        logger.info("Keyboard interruption; Stopped")
