from langchain_openai import ChatOpenAI
from langchain.base_language import BaseLanguageModel

from factory_llm import AbstractLLMFactory

class OpenAIFactory(AbstractLLMFactory):
    """Factory for OpenAI models"""

    def create_model(self) -> BaseLanguageModel:
        return ChatOpenAI(
            model=self.config.model_name,
            temperature=self.config.temperature,
        )