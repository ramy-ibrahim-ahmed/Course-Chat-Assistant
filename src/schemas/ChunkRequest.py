from pydantic import BaseModel
from typing import Optional


class ChunkRequest(BaseModel):
    file_name: str = None
    chunk_size: Optional[int] = 100
    chunk_overlap: Optional[int] = 20
