"""Main file for lancedb connection"""

import lancedb
from lancedb.embeddings import get_registry
from lancedb.pydantic import LanceModel, Vector
from lancedb.table import Table
from lancedb import DBConnection
from uuid import uuid4
from typing import List

from ocu.utils import logger

model = get_registry().get("sentence-transformers").create()
IMAGE_TABLE = "images"


class ImageModel(LanceModel):
    """Model for OCU images"""

    vector: Vector(model.ndims()) = model.VectorField()
    text: str = model.SourceField()
    path: str
    uid: str


class VectorDBConnection:
    """Main class to handle lancedb connection"""

    vector_embedder = None

    db: DBConnection = None
    uri: str = "./store/iuys_v_store"
    table: Table = None

    def __init__(self, uri: str = ".") -> None:
        if len(uri) > 1:
            self.uri = uri
        self.db = lancedb.connect(self.uri)

        self.table = self.db.create_table(  # pylint:disable=E1123
            name=IMAGE_TABLE,
            schema=ImageModel,
            exist_ok=True,
        )

    def store_text(self, text: str, path: str):
        """Converts text into embeddings and store it into IMAGE_TABLE"""

        uid = str(uuid4())
        self.table.add(data=[{"text": text, "path": path, "uid": uid}])
        logger.info(f"Added new entry to {IMAGE_TABLE} - {uid} - {path}")

    def get_text(self, text: str) -> List[ImageModel]:
        """Queries from IMAGE_TABLE and return results"""

        query_result = self.table.search(text).to_list()
        return query_result
