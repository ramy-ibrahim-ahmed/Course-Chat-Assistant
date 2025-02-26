from typing import List
import logging
from openai import OpenAI
import ollama

from ..LLMInterface import LLMInterface
from ..LLMEnums import OllamaRolesEnums


class OpenAIProvider(LLMInterface):
    def __init__(self, input_max_tokens=None, output_max_tokens=None, temperature=None):
        self.input_max_tokens = input_max_tokens
        self.ouput_max_tokens = output_max_tokens
        self.temperature = temperature
        self.roles = OllamaRolesEnums

        self.client = OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama",
        )

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

    def set_embedding_model(self, model_name: str):
        self.embed_model = model_name

    def embed_text(self, texts: List[str]):
        proccessed_text = [self.preprocess_context(text) for text in texts]
        embeds = ollama.embed(
            model=self.embed_model,
            input=proccessed_text,
        )
        return embeds.embeddings

    def set_generation_model(self, model_name):
        self.generate_model = model_name

    def generate_response(self, chat_history: list, prompt: dict):
        if not self.client:
            self.logger.error("Generation model client is not defined!")
            raise

        chat_history.append(prompt)
        response = self.client.chat.completions.create(
            model=self.generate_model,
            messages=chat_history,
        )

        response_content = response.choices[0].message.content
        if not response_content or len(response_content) == 0:
            self.logger.error("Generation model did not answer!")
            raise
        return response_content

    def define_prompt(self, role, content):
        return {"role": role, "content": self.preprocess_context(content)}

    def preprocess_context(self, content: str):
        return content[: self.input_max_tokens].strip()
