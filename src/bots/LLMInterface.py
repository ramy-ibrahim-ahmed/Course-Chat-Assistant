from abc import ABC, abstractmethod
from typing import List


class LLMInterface(ABC):
    @abstractmethod
    def set_embedding_model(model_name: str):
        pass

    @abstractmethod
    def embed_text(text: List[str]) -> List[List[float]]:
        pass

    @abstractmethod
    def set_generation_model(model_name: str):
        pass

    @abstractmethod
    def generate_response(chat_history, prompt):
        pass

    @abstractmethod
    def define_prompt(role, context):
        pass

    @abstractmethod
    def preprocess_context(context):
        pass
