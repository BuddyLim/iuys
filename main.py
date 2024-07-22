import threading
from pyee import EventEmitter
from ocu import QueueWorker
from ocu import VLMEngine
from ocu import FileWatcher

emitter = EventEmitter()


def run_watcher():
    base_path = "/Users/limkuangtar/Desktop"
    watcher = FileWatcher(ee=emitter, input_path=base_path)
    watcher.observe()


if __name__ == "__main__":
    try:
        background_thread = threading.Thread(target=run_watcher, args=())
        background_thread.daemon = True
        background_thread.start()
        worker = QueueWorker(ee=emitter)
        vlm_engine = VLMEngine()

        IN_PROGRESS = False

        while True:
            if len(worker.task) == 0 or IN_PROGRESS:
                continue
            print(worker.task)
            print("Main thread received new task")
            IN_PROGRESS = True
            path = worker.task.pop()
            response = vlm_engine.query_on_image(
                prompt="Describe the image to me", image_path=path
            )
            print(response)
            IN_PROGRESS = False

    except KeyboardInterrupt:
        print("Stopped")
