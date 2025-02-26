import os
import shutil
from datetime import datetime
import chromadb

from ..VictorsInterface import VectorsInterface
from ..VictorsEnums import ChromaDistanceEnums
from ...schemas import RetrievedDocument
from ...config import get_settings

import logging

settings = get_settings()


class ChromaProvider(VectorsInterface):
    def __init__(
        self,
        vdb_path: str = "./chroma_db",
        distance: str = ChromaDistanceEnums.COSINE.value,
    ):
        self.client = None
        self.vdb_path = vdb_path
        self.distance = distance
        self.logger = self.__logger__()

    def __logger__(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def connect(self):
        self.client = chromadb.PersistentClient(path=self.vdb_path)

    def disconnect(self):
        NotImplementedError

    def is_collection_exists(self, collection_name):
        collection_names = self.client.list_collections()
        if collection_name in collection_names:
            return True
        return False

    def list_all_collections(self):
        return self.client.list_collections()

    def get_collection_info(self, collection_name):
        if not self.is_collection_exists(collection_name):
            self.logger.warning(f"{collection_name} is not exists!")

        collection = self.client.get_collection(collection_name)
        count = collection.count()
        if not count:
            return {"name": collection_name, "count": 0}
        return {
            "name": collection_name,
            "count": collection.count(),
            "embeddings_dim": collection.peek(limit=1)["embeddings"][0].shape[0],
            "first_item_ID": collection.peek(limit=1)["ids"][0],
            "first_item_metadatas": collection.peek(limit=1)["metadatas"][0],
            "first_item_document": collection.peek(limit=1)["documents"][0],
        }

    def delete_collection(self, collection_name):
        if not self.is_collection_exists(collection_name):
            self.logger.warning(f"{collection_name} is not exists!")

        try:
            self.client.delete_collection(name=collection_name)
            temp_path = os.path.join(settings.TEMP_DIR, collection_name)
            if os.path.exists(temp_path):
                shutil.rmtree(temp_path)
        except Exception as e:
            self.logger.error(f"Error while deleting {collection_name} | {e}")
            raise

    def create_collection(
        self, collection_name, embedding_function=None, do_reset=False
    ):
        if do_reset:
            self.delete_collection(collection_name)
        try:
            self.client.create_collection(
                name=collection_name,
                embedding_function=embedding_function,
                metadata={
                    "created": str(datetime.now()),
                    "hnsw:space": self.distance,
                },
            )
        except Exception as e:
            self.logger.error(f"Error while creating {collection_name} | {e}")
            raise

    def insert_documents(
        self, collection_name, documents, embeddings=None, metadatas=None
    ):
        if not self.is_collection_exists(collection_name):
            self.logger.warning(f"{collection_name} is not exists!")

        collection = self.client.get_collection(collection_name)
        ids = [
            f"id{i+1}"
            for i in range(collection.count(), collection.count() + len(documents))
        ]
        if not metadatas:
            metadatas = [None] * len(documents)
            try:
                if embeddings:
                    collection.add(
                        documents=documents,
                        embeddings=embeddings,
                        metadatas=metadatas,
                        ids=ids,
                    )
                else:
                    collection.add(
                        documents=documents,
                        metadatas=metadatas,
                        ids=ids,
                    )
            except Exception as e:
                self.logger.error(f"Error while inserion | {e}")
                raise

    def search_by_victors(self, collection_name, victors, limit=5):
        if not self.is_collection_exists(collection_name):
            self.logger.warning(f"{collection_name} is not exists!")

        collection = self.client.get_collection(collection_name)
        try:
            results = collection.query(
                query_embeddings=victors,
                n_results=limit,
            )
            return [
                RetrievedDocument(
                    **{
                        "document": results["documents"][0][i],
                        "distance": results["distances"][0][i],
                    }
                )
                for i in range(limit)
            ]
        except Exception as e:
            self.logger.error(f"Error while search on {collection_name} | {e}")
            raise

    def search_by_texts(self, collection_name, text, limit=5):
        raise NotImplementedError
