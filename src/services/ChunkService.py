import os

from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from ..config import get_settings

settings = get_settings()


class ChunkService:

    def __init__(self, course_name):
        self.course_name = course_name
        self.project_path = os.path.join(settings.TEMP_DIR, course_name)
        self.file_path = None

    def get_file_extention(self, file_name: str):
        return os.path.splitext(file_name)[-1]

    def get_file_loader(self, file_name: str):
        file_ext = self.get_file_extention(file_name=file_name)
        self.file_path = os.path.join(self.project_path, file_name)

        if not os.path.exists(self.file_path):
            return None
        if file_ext == ".txt":
            return TextLoader(file_path=self.file_path, encoding="utf-8")
        if file_ext == ".pdf":
            return PyMuPDFLoader(file_path=self.file_path)
        return None

    def get_file_content(self, file_name: str):
        loader = self.get_file_loader(file_name=file_name)
        if loader:
            return loader.load()
        else:
            return None

    def process_file_content(
        self,
        file_content: list,
        chunk_size: int = 100,
        chunk_overlap: int = 20,
    ):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )

        content = [rec.page_content for rec in file_content]
        chunks = text_splitter.split_text(" ".join(content))

        return chunks
