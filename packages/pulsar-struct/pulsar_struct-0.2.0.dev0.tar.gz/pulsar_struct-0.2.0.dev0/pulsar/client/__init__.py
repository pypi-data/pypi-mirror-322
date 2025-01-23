from typing import Union, Optional, List, Generator

from .groq import GroqClient

from .anthropic import AnthropicClient
from .base import BaseLLMClient
from .gemini import GeminiClient
from .ollama import OllamaClient
from .openaiapilike import OpenAIAPILikeClient
from .openai import OpenAIClient
from .openrouter import OpenRouterClient
from .exceptions import LLMException, RetryableAPIError


provide_map = {
    "groq": GroqClient,
    "openrouter": OpenRouterClient,
    "ollama": OllamaClient,
    "anthropic": AnthropicClient,
    "openaiapilike": OpenAIAPILikeClient,
    "openai": OpenAIClient,
    "gemini": GeminiClient,
}


class Client:
    @staticmethod
    def from_provider(provider: str, **kwargs):
        return provide_map[provider](**kwargs)

    def chat_completion(
        self,
        messages: List,
        model: str,
        system: Optional[str] = None,
        response_type: type = str,
        stream: bool = False,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        prompt_template: Optional[str] = None,
        **kwargs
    ) -> Union[str, dict, Generator]:
        provider = model.split("/")[0]
        model_name = "/".join(model.split("/")[1:])
        client = Client.from_provider(provider)
        return client.chat_completion(
            messages=messages,
            model=model_name,
            system=system,
            response_type=response_type,
            stream=stream,
            temperature=temperature,
            max_tokens=max_tokens,
            prompt_template=prompt_template,
            **kwargs
        )


__all__ = [
    "BaseLLMClient", "AnthropicClient", "GroqClient", 
    "OllamaCLient", "OpenAIAPILikeClient", "OpenAIClient",
    "OpenRouterClient", "GeminiClient", "Client", "LLMException", "RetryableAPIError"]