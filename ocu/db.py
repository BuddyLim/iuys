"""Implementation of db connection for IUYS"""

import dbm
import dbm.gnu
from ocu.utils import SingletonMeta


class DBConnection(metaclass=SingletonMeta):
    """Main class for local key-value store institation"""

    store_path = "./iuys_store"
    db = None

    def __init__(self):
        self.db = dbm.open(self.store_path, "c")
