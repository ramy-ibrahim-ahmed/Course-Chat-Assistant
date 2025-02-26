from .providers import OpenAIProvider
from .LLMEnums import LLMProvider


class LLMFactory:
    def __init__(self, input_max_tokens=1000, output_max_tokens=None, temperature=None):
        self.input_max_tokens = input_max_tokens
        self.output_max_tokens = output_max_tokens
        self.temperature = temperature

    def create(self, provider: str):
        if provider == LLMProvider.OLLAMA.value:
            llm = OpenAIProvider(
                input_max_tokens=self.input_max_tokens,
                output_max_tokens=self.input_max_tokens,
                temperature=self.temperature,
            )
            return llm
        return None
