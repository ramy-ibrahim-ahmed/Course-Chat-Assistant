from .providers import ChromaProvider
from .VictorsEnums import VectorsEnums


class VictorsFactory:
    def __init__(self, path, distance_method):
        self.path = path
        self.distance_method = distance_method

    def create(self, provider: str):
        if provider == VectorsEnums.CHROMA.value:
            vdb = ChromaProvider(
                vdb_path=self.path,
                distance=self.distance_method,
            )
            return vdb
        return None
