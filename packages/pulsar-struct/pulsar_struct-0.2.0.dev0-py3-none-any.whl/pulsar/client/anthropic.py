from typing import Dict, Any, Optional, Tuple, List, Generator
import os
import requests
import json
import logging

from pulsar.prompt import build_prompt, DEFAULT_PROMPT

from .base import BaseLLMClient, _allowed_roles
from .exceptions import RetryableAPIError, LLMException
from .types import TokenUsage, CompletionResponse, StreamChunk, ChatResult


class AnthropicAPIError(RetryableAPIError):
    """Anthropic-specific API error"""
    pass


class AnthropicClient(BaseLLMClient):
    """Client for Anthropic's Claude API"""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        max_retries: int = 0,
        retry_delay: float = 1.0,
    ):
        if api_key is None:
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError(
                    "API key must be provided or set as ANTHROPIC_API_KEY environment variable"
                )
        
        super().__init__(
            api_key=api_key,
            base_url="https://api.anthropic.com/v1",
            max_retries=max_retries,
            retry_delay=retry_delay,
            logger=logging.getLogger(__name__)
        )
        
        # Add Anthropic-specific headers
        self.session.headers.update({
            "Accept": "application/json",
            "anthropic-version": "2023-06-01",
            "x-api-key": api_key,  # Anthropic uses x-api-key instead of Bearer token
        })
        # Remove default Authorization header since Anthropic uses x-api-key
        self.session.headers.pop("Authorization", None)

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str,
        system: Optional[str] = None,
        response_type: type = str,
        stream: bool = False,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        prompt_template: Optional[str] = None,
        **kwargs
    ) -> Any:
        """Override to handle Anthropic's specific API requirements"""
        # Validate message roles
        for msg in messages:
            if msg["role"] not in _allowed_roles:
                raise ValueError(f"Invalid role: {msg['role']}")
        
        if prompt_template is None:
            prompt_template = DEFAULT_PROMPT

        prepared_messages = build_prompt(
            prompt_template=prompt_template,
            history=messages,
            system=None,
            response_type=response_type,
        )

        payload = {
            "model": model,
            "system": system,
            "messages": prepared_messages,
            "temperature": temperature,
            "stream": stream,
            "max_tokens": max_tokens or 4096,  # Anthropic requires max_tokens
            **kwargs
        }


        endpoint = "messages"
        
        if stream:
            return self._handle_streaming_response(payload, response_type, endpoint)
        return self._handle_completion_response(payload, response_type, endpoint)

    def _handle_request_error(self, error: requests.RequestException, attempt: int) -> Exception:
        """Handle Anthropic-specific API errors"""
        if not error.response:
            return LLMException(f"Network error: {str(error)}")
            
        try:
            error_data = error.response.json()
            error_type = error_data.get("type", "")
            error_message = error_data.get("error", {}).get("message", str(error))
            
            # Add Anthropic error type to message if available
            if error_type:
                error_message = f"{error_type}: {error_message}"
                
        except (json.JSONDecodeError, AttributeError):
            error_message = str(error)
            
        return AnthropicAPIError.from_response(
            response=error.response,
            message=error_message
        )
    
    def _handle_streaming_response(
        self,
        payload: Dict[str, Any],
        response_type: type,
        endpoint: str = "chat/completions"
    ) -> Generator[ChatResult, None, None]:
        """Handle streaming API response"""
        response = self._make_request("POST", endpoint, json=payload, stream=True)
        buffer = ""
        
        for line in response.iter_lines():
            if not line or not line.startswith(b"data: "):
                continue
                
            data = line[6:]  # Remove "data: " prefix
            chunk_data = json.loads(data)
            if chunk_data["type"] == "message_stop":
                break

            content, usage = self._process_streaming_chunk(chunk_data)
            
            if content:
                buffer += content
            chunk_response = StreamChunk(content=buffer, chunk=content, usage=usage)
            
            if response_type == str:
                yield content, chunk_response
            else:
                try:
                    parsed = self._parse_response(buffer, response_type)
                    yield parsed, chunk_response
                except Exception as e:
                    self.logger.debug(f"Parsing error in stream: {e}")


    def _process_streaming_chunk(self, chunk: Dict[str, Any]) -> Tuple[Optional[str], Optional[TokenUsage]]:
        """Process Anthropic streaming response chunk"""
        if not chunk or "type" not in chunk:
            return None, None
        
        content = None
        usage = None
        if chunk["type"] == "content_block_delta":
            content = chunk.get("delta", {}).get("text")
        elif chunk["type"] == "message_delta":
            if "usage" in chunk and chunk["usage"] is not None:
                usage_data = chunk["usage"]
                usage = TokenUsage(
                    prompt_tokens=usage_data.get("input_tokens", 0),
                    completion_tokens=usage_data.get("output_tokens", 0),
                    total_tokens=usage_data.get("input_tokens", 0) + usage_data.get("output_tokens", 0)
                )
            
        return content, usage

    def _extract_usage(self, response: Dict[str, Any]) -> Optional[TokenUsage]:
        """Extract token usage from Anthropic response"""
        if "usage" in response:
            usage = response["usage"]
            return TokenUsage(
                prompt_tokens=usage.get("input_tokens", 0),
                completion_tokens=usage.get("output_tokens", 0),
                total_tokens=usage.get("input_tokens", 0) + usage.get("output_tokens", 0)
            )
        return None

    def _handle_completion_response(
        self,
        payload: Dict[str, Any],
        response_type: type,
        endpoint: str = "messages"
    ) -> ChatResult:
        """Handle Anthropic completion response format"""
        response = self._make_request("POST", endpoint, json=payload)
        
        if not response or "content" not in response:
            raise LLMException("Invalid response format")
            
        content = response["content"][0]["text"]  # Anthropic returns content as array
        usage = self._extract_usage(response)
        chat_response = CompletionResponse(content=content, usage=usage)

        return self._parse_response(content, response_type), chat_response
