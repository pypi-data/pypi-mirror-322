from typing import Dict, Any, Optional, Tuple
import os
import requests
import json
import logging

from .base import BaseLLMClient
from .exceptions import RetryableAPIError, LLMException
from .types import TokenUsage


class GroqAPIError(RetryableAPIError):
    """Groq-specific API error"""
    pass

class GroqClient(BaseLLMClient):
    """Client for Groq's LLM API"""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        max_retries: int = 3,
        retry_delay: float = 2.0,
    ):
        if api_key is None:
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                raise ValueError(
                    "API key must be provided or set as GROQ_API_KEY environment variable"
                )
        
        super().__init__(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1",
            max_retries=max_retries,
            retry_delay=retry_delay,
            logger=logging.getLogger(__name__)
        )
        
        # Add Groq-specific headers
        self.session.headers.update({
            "Accept": "application/json",
        })

    def _handle_request_error(self, error: requests.RequestException, attempt: int) -> Exception:
        """Handle Groq-specific API errors"""
        if not error.response:
            return LLMException(f"Network error: {str(error)}")
            
        try:
            error_data = error.response.json()
            error_message = error_data.get("error", {}).get("message", str(error))
        except (json.JSONDecodeError, AttributeError):
            error_message = str(error)
            
        return GroqAPIError.from_response(
            response=error.response,
            message=error_message
        )

    def _process_streaming_chunk(self, chunk: Dict[str, Any]) -> Tuple[Optional[str], Optional[TokenUsage]]:
        """Process Groq streaming response chunk"""
        if not chunk or "choices" not in chunk:
            return None, None
            
        delta = chunk["choices"][0].get("delta", {})
        content = delta.get("content")
        
        # Extract usage if available
        usage = None
        if "x_groq" in chunk and "usage" in chunk["x_groq"]:
            usage_data = chunk["x_groq"]["usage"]
            usage = TokenUsage(
                prompt_tokens=usage_data.get("prompt_tokens", 0),
                completion_tokens=usage_data.get("completion_tokens", 0),
                total_tokens=usage_data.get("total_tokens", 0)
            )
            
        return content, usage

    def _extract_usage(self, response: Dict[str, Any]) -> Optional[TokenUsage]:
        """Extract token usage from Groq response"""
        if "usage" in response:
            usage = response["usage"]
            return TokenUsage(
                prompt_tokens=usage.get("prompt_tokens", 0),
                completion_tokens=usage.get("completion_tokens", 0),
                total_tokens=usage.get("total_tokens", 0)
            )
        return None