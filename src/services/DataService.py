import os
import re
import random
import logging
import string
import aiofiles

from fastapi import UploadFile
from ..config import get_settings

settings = get_settings()


class DataService:
    def __init__(self):
        self.file_id = None

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

    def validate_file_type(self, file: UploadFile):
        if file.content_type not in settings.FILE_ALLOWED_TYPES:
            self.logger.warning("Fill type is not supported!")
            raise ValueError("File type is not supported!")

        if file.size > settings.FILE_MAX_SIZE * 1024 * 1024:
            self.logger.warning("Fill is larger than expected!")
            raise ValueError("File size is larger than allowed!")

        return True

    def preprocess_file_name(self, original_name: str):
        filename = original_name.lower()
        filename = filename.replace(" ", "_")
        filename = re.sub(r"[^a-z0-9_.]", "_", filename)
        return filename

    def generate_random_string(self, length=12):
        characters = string.ascii_letters + string.digits
        return "".join(random.choice(characters) for _ in range(length))

    def generate_file_path(self, course_name: str, original_name: str):
        preproccessed_file_name = self.preprocess_file_name(original_name=original_name)
        random_perfix = self.generate_random_string(length=12)
        new_file_name = random_perfix + "_" + preproccessed_file_name
        self.file_id = new_file_name
        path = os.path.join(settings.TEMP_DIR, course_name, new_file_name)

        while os.path.exists(path):
            random_perfix = self.generate_random_string(length=12)
            new_file_name = random_perfix + "_" + preproccessed_file_name
            self.file_id = new_file_name
            path = os.path.join(settings.TEMP_DIR, course_name, new_file_name)

        return path

    async def upload_file(self, file: UploadFile, course_name: str, original_name: str):
        file_path = self.generate_file_path(
            course_name=course_name,
            original_name=original_name,
        )
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        try:
            async with aiofiles.open(file=file_path, mode="wb") as f:
                while chunk := await file.read(settings.FILE_DEFAULT_CHUNK_SIZE):
                    await f.write(chunk)
            return True

        except Exception as e:
            self.logger.error(
                f"Error while uploading file {original_name} on {file_path}: {e}"
            )
            raise Exception(f"Upload failed: {e}") from e
