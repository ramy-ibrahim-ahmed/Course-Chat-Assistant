from pydantic import BaseModel


class RetrievedDocument(BaseModel):
    document: str
    distance: float
