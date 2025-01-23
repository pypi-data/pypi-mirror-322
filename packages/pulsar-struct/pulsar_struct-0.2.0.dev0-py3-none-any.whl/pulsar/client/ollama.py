from typing import Dict, Any, Optional, Tuple
import os
import requests
import json
import logging

from .base import BaseLLMClient
from .exceptions import RetryableAPIError, LLMException
from .types import TokenUsage


class OllamaAPIError(RetryableAPIError):
    """Ollama-specific API error"""
    pass

class OllamaClient(BaseLLMClient):
    """Client for Ollama's LLM API"""
    
    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        max_retries: int = 0,
        retry_delay: float = 1.0,
    ):
        base_url = base_url[:-1] if base_url.endswith("/") else base_url
        super().__init__(
            api_key="",
            base_url=f"{base_url}/v1",
            max_retries=max_retries,
            retry_delay=retry_delay,
            logger=logging.getLogger(__name__)
        )
        
        # Remove authorization header since Ollama doesn't use it
        self.session.headers.pop("Authorization", None)
        
        # Add Ollama-specific headers
        self.session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json"
        })

    def _handle_request_error(self, error: requests.RequestException, attempt: int) -> Exception:
        """Handle Ollama-specific API errors"""
        if not error.response:
            return LLMException(f"Network error: {str(error)}")
            
        try:
            error_data = error.response.json()
            error_message = error_data.get("error", str(error))
        except (json.JSONDecodeError, AttributeError):
            error_message = str(error)
            
        return OllamaAPIError.from_response(
            response=error.response,
            message=error_message
        )

    def _process_streaming_chunk(self, chunk: Dict[str, Any]) -> Tuple[Optional[str], Optional[TokenUsage]]:
        """Process Ollama streaming response chunk"""
        if not chunk or "choices" not in chunk:
            return None, None
        
        content = None
        if len(chunk["choices"]) > 0:
            delta = chunk["choices"][0].get("delta", {})
            content = delta.get("content")
        
        # Extract usage if available
        usage = None
        if "usage" in chunk and chunk["usage"] is not None:
            usage_data = chunk["usage"]
            usage = TokenUsage(
                prompt_tokens=usage_data.get("prompt_tokens", 0),
                completion_tokens=usage_data.get("completion_tokens", 0),
                total_tokens=usage_data.get("total_tokens", 0)
            )
            
        return content, usage

    def _extract_usage(self, response: Dict[str, Any]) -> Optional[TokenUsage]:
        """Extract token usage from Ollama response"""
        if "usage" in response:
            usage = response["usage"]
            return TokenUsage(
                prompt_tokens=usage.get("prompt_tokens", 0),
                completion_tokens=usage.get("completion_tokens", 0),
                total_tokens=usage.get("total_tokens", 0)
            )
        return None