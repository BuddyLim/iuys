"""Implementation of db connection for IUYS"""

import dbm
from ocu.utils import SingletonMeta


class KVConnection(metaclass=SingletonMeta):
    """Main class for local key-value store institation"""

    store_path = "../store/iuys_kv_store"
    db = None

    def __init__(self, path: str = ""):
        if len(path) > 1:
            self.store_path = path

        self.db = dbm.open(self.store_path, "c")

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.db.close()
