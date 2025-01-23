import pytest
from unittest.mock import Mock, patch
import os
import json
import requests

from pulsar.client import (
    Client, BaseLLMClient, OpenAIClient, AnthropicClient,
    LLMException, RetryableAPIError
)
from pulsar.client.types import TokenUsage, CompletionResponse

# Fixtures
@pytest.fixture
def mock_response():
    mock = Mock()
    mock.json.return_value = {
        "choices": [{"message": {"content": "test response"}}],
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 20,
            "total_tokens": 30
        }
    }
    return mock

@pytest.fixture
def mock_anthropic_response():
    mock = Mock()
    mock.json.return_value = {
        "content": [{"text": "test response"}],
        "usage": {
            "input_tokens": 10,
            "output_tokens": 20
        }
    }
    return mock

# Test Client Factory
def test_client_from_provider():
    client = Client.from_provider("openai", api_key="test-key")
    assert isinstance(client, OpenAIClient)
    
    client = Client.from_provider("anthropic", api_key="test-key")
    assert isinstance(client, AnthropicClient)

def test_client_from_provider_invalid():
    with pytest.raises(KeyError):
        Client.from_provider("invalid_provider")

# Test OpenAI Client
def test_openai_client_init():
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        client = OpenAIClient()
        assert client.api_key == "test-key"
        assert "Bearer test-key" in client.session.headers["Authorization"]

def test_openai_client_init_missing_key():
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError):
            OpenAIClient()

@patch("requests.Session.request")
def test_openai_chat_completion(mock_request, mock_response):
    mock_request.return_value = mock_response
    client = OpenAIClient(api_key="test-key")
    
    messages = [{"role": "user", "content": "test"}]
    response, raw = client.chat_completion(
        messages=messages,
        model="gpt-4",
        temperature=0.7
    )
    
    assert response == "test response"
    assert isinstance(raw, CompletionResponse)
    assert raw.usage.prompt_tokens == 10
    assert raw.usage.completion_tokens == 20

# Test Anthropic Client
def test_anthropic_client_init():
    with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}):
        client = AnthropicClient()
        assert client.api_key == "test-key"
        assert "x-api-key" in client.session.headers

@patch("requests.Session.request")
def test_anthropic_chat_completion(mock_request, mock_anthropic_response):
    mock_request.return_value = mock_anthropic_response
    client = AnthropicClient(api_key="test-key")
    
    messages = [{"role": "user", "content": "test"}]
    response, raw = client.chat_completion(
        messages=messages,
        model="claude-3",
        temperature=0.7
    )
    
    assert response == "test response"
    assert isinstance(raw, CompletionResponse)
    assert raw.usage.prompt_tokens == 10
    assert raw.usage.completion_tokens == 20

# Test Error Handling
@patch("requests.Session.request")
def test_retryable_error_handling(mock_request):
    mock_response = Mock()
    mock_response.status_code = 429
    mock_response.json.return_value = {"error": {"message": "Rate limit exceeded"}}
    mock_response.headers = {"Retry-After": "1"}
    
    mock_request.side_effect = requests.RequestException(response=mock_response)
    
    client = OpenAIClient(api_key="test-key", max_retries=2)
    messages = [{"role": "user", "content": "test"}]
    
    with pytest.raises(RetryableAPIError) as exc:
        client.chat_completion(messages=messages, model="gpt-4")
    assert exc.value.is_retryable()
    assert exc.value.retry_after == 1.0

# Test Streaming
@patch("requests.Session.request")
def test_streaming_response(mock_request):
    mock_response = Mock()
    mock_response.iter_lines.return_value = [
        b'data: {"choices":[{"delta":{"content":"Hello"}}]}',
        b'data: {"choices":[{"delta":{"content":" World"}}]}',
        b'data: [DONE]'
    ]
    mock_request.return_value = mock_response
    
    client = OpenAIClient(api_key="test-key")
    messages = [{"role": "user", "content": "test"}]
    
    stream = client.chat_completion(
        messages=messages,
        model="gpt-4",
        stream=True
    )
    
    chunks = [chunk for chunk, _ in stream]
    assert chunks == ["Hello", " World"]
