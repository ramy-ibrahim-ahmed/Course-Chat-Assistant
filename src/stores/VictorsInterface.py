from abc import ABC, abstractmethod
from typing import List, Dict, Optional

from ..schemas.VictorsSchemas import RetrievedDocument

class VectorsInterface(ABC):
    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def disconnect(self) -> None:
        pass

    @abstractmethod
    def list_all_collections(self) -> List[str]:
        pass

    @abstractmethod
    def is_collection_exists(self, collection_name: str) -> bool:
        pass

    @abstractmethod
    def get_collection_info(self, collection_name: str) -> Dict:
        pass

    @abstractmethod
    def delete_collection(self, collection_name: str) -> None:
        pass

    @abstractmethod
    def create_collection(
        self,
        collection_name: str,
        embedding_model: Optional[int] = None,
        do_reset: Optional[bool] = False,
    ) -> bool:
        pass

    @abstractmethod
    def insert_documents(
        self,
        collection_name: str,
        documents: List[str],
        embeddings: Optional[List[List[float]]] = None,
        metadata: Optional[List[dict]] = None,
    ) -> bool:
        pass

    @abstractmethod
    def search_by_texts(
        self,
        collection_name: str,
        text: List[str],
        limit: Optional[int] = 5,
    ) -> str:
        pass

    @abstractmethod
    def search_by_victors(
        self,
        collection_name: str,
        victor: List[List[float]],
        limit: Optional[int] = 5,
    ) -> str:
        pass
