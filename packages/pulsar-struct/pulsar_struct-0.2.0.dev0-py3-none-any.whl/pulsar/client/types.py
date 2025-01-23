from typing import Optional, Tuple, Union, Any, Iterator
from dataclasses import dataclass


@dataclass(frozen=True)
class TokenUsage:
    """Represents token usage statistics for an API request"""
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

@dataclass
class CompletionResponse:
    """Base response structure for chat completions"""
    content: str
    usage: Optional[TokenUsage] = None

@dataclass
class StreamChunk(CompletionResponse):
    """Represents a streaming chunk response"""
    chunk: Optional[str] = None

ChatResult = Tuple[Union[str, Any], Union[CompletionResponse, Iterator[StreamChunk]]]
