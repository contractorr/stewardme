"""Tests for LLM provider adapters."""

from unittest.mock import MagicMock

import pytest

from llm import LLMAuthError, LLMError, LLMRateLimitError
from llm.providers.claude import ClaudeProvider
from llm.providers.gemini import GeminiProvider
from llm.providers.openai import OpenAIProvider


class TestClaudeProvider:
    def test_generate(self):
        mock_client = MagicMock()
        mock_resp = MagicMock()
        mock_resp.content = [MagicMock(text="Hello from Claude")]
        mock_client.messages.create.return_value = mock_resp

        provider = ClaudeProvider(client=mock_client)
        result = provider.generate(
            messages=[{"role": "user", "content": "hi"}],
            system="Be helpful",
            max_tokens=100,
        )

        assert result == "Hello from Claude"
        mock_client.messages.create.assert_called_once_with(
            model="claude-sonnet-4-6",
            max_tokens=100,
            messages=[{"role": "user", "content": "hi"}],
            system="Be helpful",
        )

    def test_generate_no_system(self):
        mock_client = MagicMock()
        mock_resp = MagicMock()
        mock_resp.content = [MagicMock(text="response")]
        mock_client.messages.create.return_value = mock_resp

        provider = ClaudeProvider(client=mock_client)
        provider.generate(messages=[{"role": "user", "content": "hi"}])

        call_kwargs = mock_client.messages.create.call_args.kwargs
        assert "system" not in call_kwargs

    def test_auth_error(self):
        from anthropic import AuthenticationError

        mock_client = MagicMock()
        mock_client.messages.create.side_effect = AuthenticationError(
            message="bad key", response=MagicMock(status_code=401), body={}
        )

        provider = ClaudeProvider(client=mock_client)
        with pytest.raises(LLMAuthError):
            provider.generate(messages=[{"role": "user", "content": "hi"}])

    def test_rate_limit_error(self):
        from anthropic import RateLimitError

        mock_client = MagicMock()
        mock_client.messages.create.side_effect = RateLimitError(
            message="rate limited", response=MagicMock(status_code=429), body={}
        )

        provider = ClaudeProvider(client=mock_client)
        with pytest.raises(LLMRateLimitError):
            provider.generate(messages=[{"role": "user", "content": "hi"}])

    def test_api_error(self):
        from anthropic import APIError

        mock_client = MagicMock()
        mock_client.messages.create.side_effect = APIError(
            message="server error", request=MagicMock(), body=None
        )

        provider = ClaudeProvider(client=mock_client)
        with pytest.raises(LLMError):
            provider.generate(messages=[{"role": "user", "content": "hi"}])


class TestOpenAIProvider:
    def test_generate(self):
        mock_client = MagicMock()
        mock_resp = MagicMock()
        mock_resp.choices = [MagicMock(message=MagicMock(content="Hello from GPT"))]
        mock_client.chat.completions.create.return_value = mock_resp

        provider = OpenAIProvider(client=mock_client)
        result = provider.generate(
            messages=[{"role": "user", "content": "hi"}],
            system="Be helpful",
        )

        assert result == "Hello from GPT"
        call_kwargs = mock_client.chat.completions.create.call_args.kwargs
        # System message should be prepended
        assert call_kwargs["messages"][0] == {"role": "system", "content": "Be helpful"}
        assert call_kwargs["messages"][1] == {"role": "user", "content": "hi"}

    def test_generate_no_system(self):
        mock_client = MagicMock()
        mock_resp = MagicMock()
        mock_resp.choices = [MagicMock(message=MagicMock(content="response"))]
        mock_client.chat.completions.create.return_value = mock_resp

        provider = OpenAIProvider(client=mock_client)
        provider.generate(messages=[{"role": "user", "content": "hi"}])

        call_kwargs = mock_client.chat.completions.create.call_args.kwargs
        assert len(call_kwargs["messages"]) == 1  # No system prepended


class TestGeminiProvider:
    def test_generate(self):
        mock_client = MagicMock()
        mock_resp = MagicMock()
        mock_resp.text = "Hello from Gemini"
        mock_client.models.generate_content.return_value = mock_resp

        provider = GeminiProvider(client=mock_client)
        result = provider.generate(
            messages=[{"role": "user", "content": "hi"}],
            system="Be helpful",
        )

        assert result == "Hello from Gemini"
        call_kwargs = mock_client.models.generate_content.call_args.kwargs
        assert "Be helpful" in call_kwargs["contents"]
        assert "hi" in call_kwargs["contents"]

    def test_generate_no_system(self):
        mock_client = MagicMock()
        mock_resp = MagicMock()
        mock_resp.text = "response"
        mock_client.models.generate_content.return_value = mock_resp

        provider = GeminiProvider(client=mock_client)
        provider.generate(messages=[{"role": "user", "content": "hi"}])

        call_kwargs = mock_client.models.generate_content.call_args.kwargs
        assert "System:" not in call_kwargs["contents"]

    def test_auth_error(self):
        mock_client = MagicMock()
        mock_client.models.generate_content.side_effect = Exception("API key not valid")

        provider = GeminiProvider(client=mock_client)
        with pytest.raises(LLMAuthError):
            provider.generate(messages=[{"role": "user", "content": "hi"}])

    def test_generic_error(self):
        mock_client = MagicMock()
        mock_client.models.generate_content.side_effect = Exception("something broke")

        provider = GeminiProvider(client=mock_client)
        with pytest.raises(LLMError):
            provider.generate(messages=[{"role": "user", "content": "hi"}])
