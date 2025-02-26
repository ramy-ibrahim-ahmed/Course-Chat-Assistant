from enum import Enum


class LLMProvider(Enum):
    OLLAMA = "OLLAMA"


class OllamaRolesEnums(Enum):
    SYSTEM = "system"
    ASSISTANT = "assistant"
    USER = "user"
