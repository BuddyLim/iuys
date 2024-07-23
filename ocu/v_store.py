"""Main file for lancedb connection"""

import lancedb


class VectorConnection:
    """Main class to handle lancedb connection"""

    def __init__(self) -> None:
        uri = "../store/iuys_kv_store"
        db = lancedb.connect(uri)
