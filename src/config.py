from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    EMBED_MODEL_NAME: str
    GENERATION_MODEL_NAME: str
    VDB_PATH: str
    DEFAULT_LANGUAGE: str = "en"
    FILE_ALLOWED_TYPES: list
    FILE_MAX_SIZE: int
    FILE_DEFAULT_CHUNK_SIZE: int
    TEMP_DIR: str

    class Config:
        env_file = r".env"


def get_settings():
    return Settings()
