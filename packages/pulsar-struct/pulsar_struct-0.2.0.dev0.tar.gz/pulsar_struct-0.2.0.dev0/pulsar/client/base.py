from abc import ABC, abstractmethod
from typing import Any, Dict, Generator, Iterator, List, Optional, Protocol, Tuple, Union
from enum import Enum
import requests
import json
import logging
from time import sleep

from pulsar.prompt import build_prompt, DEFAULT_PROMPT

from pulsar.parser import parse
from .types import TokenUsage, CompletionResponse, StreamChunk, ChatResult
from .exceptions import LLMException, RetryableAPIError


_allowed_roles = ("user", "assistant", "tool")


class BaseLLMClient(ABC):
    """Abstract base class for LLM API clients"""
    
    def __init__(
        self, 
        api_key: str,
        base_url: str,
        max_retries: int = 0,
        retry_delay: float = 1.0,
        logger: Optional[logging.Logger] = None
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.logger = logger or logging.getLogger(__name__)
        
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })

    def _make_request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> Any:
        """Make HTTP request with retry logic"""
        url = f"{self.base_url}/{endpoint}"
        attempt = 0
        
        while attempt <= self.max_retries:
            try:
                response = self.session.request(method, url, **kwargs)
                response.raise_for_status()
                return response.json() if not kwargs.get('stream') else response
                
            except requests.RequestException as e:
                attempt += 1
                error = self._handle_request_error(e, attempt)
                
                if isinstance(error, RetryableAPIError) and error.is_retryable() and attempt <= self.max_retries:
                    sleep(error.retry_after + self.retry_delay)
                    continue
                    
                raise error

    @abstractmethod
    def _handle_request_error(self, error: requests.RequestException, attempt: int) -> Exception:
        """Handle provider-specific request errors"""
        pass

    @abstractmethod
    def _process_streaming_chunk(self, chunk: Dict[str, Any]) -> Tuple[Optional[str], Optional[TokenUsage]]:
        """Process a streaming response chunk"""
        pass

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
    ) -> ChatResult:
        """
        Generate chat completion
        
        Args:
            messages: List of conversation messages
            model: Model identifier
            system: Optional system message
            response_type: Return type (str or custom type)
            stream: Whether to stream the response
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate
            prompt_template: Use custom jinja2 prompt template
            **kwargs: Additional API parameters
            
        Returns:
            Tuple of (parsed_response, raw_response)
        """
        # Validate message roles
        for msg in messages:
            if msg["role"] not in _allowed_roles:
                raise ValueError(f"Invalid role: {msg['role']}")
        
        if prompt_template is None:
            prompt_template = DEFAULT_PROMPT

        prepared_messages = build_prompt(
            prompt_template=prompt_template,
            history=messages,
            system=system,
            response_type=response_type,
        )

        # Prepare request payload
        payload = {
            "model": model,
            "messages": prepared_messages,
            "temperature": temperature,
            "stream": stream,
            **kwargs
        }

        if max_tokens:
            payload["max_tokens"] = max_tokens

        self.logger.debug(f"Chat completion request: {payload}")

        if stream:
            payload.setdefault("stream_options", {"include_usage": True})
            return self._handle_streaming_response(payload, response_type)
        
        return self._handle_completion_response(payload, response_type)

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
            if data == b"[DONE]":
                break
            chunk_data = json.loads(data)
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

    def _handle_completion_response(
        self,
        payload: Dict[str, Any],
        response_type: type,
        endpoint: str = "chat/completions"
    ) -> ChatResult:
        """Handle regular completion API response"""
        response = self._make_request("POST", endpoint, json=payload)
        
        if not response or "choices" not in response:
            raise LLMException("Invalid response format")
            
        content = response["choices"][0]["message"]["content"]
        usage = self._extract_usage(response)
        
        chat_response = CompletionResponse(content=content, usage=usage)
        return self._parse_response(content, response_type), chat_response

    @abstractmethod
    def _extract_usage(self, response: Dict[str, Any]) -> Optional[TokenUsage]:
        """Extract token usage from response"""
        pass

    def _parse_response(self, content: str, response_type: type) -> Any:
        """Parse response content into requested type"""
        if response_type == str:
            return content
            
        return parse(content, response_type)