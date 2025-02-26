from typing import Optional, List
from pydantic import BaseModel


class SignalResponse(BaseModel):
    signal: str


class FileUploadResponse(BaseModel):
    signal: str
    file_id: str


class CollectionInfo(BaseModel):
    name: str
    count: int
    embeddings_dim: Optional[int] = None
    first_item_ID: Optional[str] = None
    first_item_metadatas: Optional[dict] = None
    first_item_document: Optional[str] = None


class BotDEBUGE(BaseModel):
    answer: str
    chat_history: List[dict]
    user_prompt: dict
