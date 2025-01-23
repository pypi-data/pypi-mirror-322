from dataclasses import dataclass
from typing import Optional, Any
import re


class LLMException(Exception):
    """Base exception for LLM-related errors"""
    def __init__(self, message: str, response: Optional[Any] = None):
        super().__init__(message)
        self.response = response

@dataclass
class RetryableAPIError(Exception):
    """Represents a retryable API error"""
    message: str
    status_code: int
    retry_after: Optional[float] = None

    def is_retryable(self) -> bool:
        """Determine if error is retryable based on status code and message"""
        if self.status_code in {408, 429, 500, 502, 503, 504}:
            return True
        return "rate limit" in self.message.lower()

    @classmethod
    def from_response(cls, response, message: str) -> 'RetryableAPIError':
        """Create error instance from response"""
        retry_after = 0.0
        
        # Check for rate limit retry header
        if 'Retry-After' in response.headers:
            retry_after = float(response.headers['Retry-After'])
        
        # Extract retry time from error message
        if not retry_after and "rate limit" in message.lower():
            match = re.search(r"try again in (\d+\.?\d*)s", message)
            if match:
                retry_after = float(match.group(1))
        
        return cls(
            message=message,
            status_code=response.status_code,
            retry_after=retry_after
        )