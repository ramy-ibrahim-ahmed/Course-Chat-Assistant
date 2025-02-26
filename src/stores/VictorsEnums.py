from enum import Enum


class VectorsEnums(Enum):
    CHROMA = "CHROMA"


class ChromaDistanceEnums(Enum):
    COSINE = "cosine"
    L2 = "l2"
    IP = "ip"
