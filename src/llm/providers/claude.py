"""Claude (Anthropic) LLM provider."""

from ..base import LLMAuthError, LLMError, LLMProvider, LLMRateLimitError


class ClaudeProvider(LLMProvider):
    """Anthropic Claude provider."""

    provider_name = "claude"

    def __init__(self, api_key: str | None = None, model: str | None = None, client=None):
        self.model = model or "claude-sonnet-4-20250514"

        if client:
            self.client = client
            return

        try:
            from anthropic import Anthropic
        except ImportError:
            raise LLMError("anthropic package not installed. Run: pip install anthropic")

        self.client = Anthropic(api_key=api_key)

    def generate(self, messages: list[dict], system: str | None = None, max_tokens: int = 2000) -> str:
        try:
            from anthropic import APIError, AuthenticationError, RateLimitError
        except ImportError:
            raise LLMError("anthropic package not installed")

        try:
            kwargs = {
                "model": self.model,
                "max_tokens": max_tokens,
                "messages": messages,
            }
            if system:
                kwargs["system"] = system

            response = self.client.messages.create(**kwargs)
            return response.content[0].text
        except AuthenticationError as e:
            raise LLMAuthError(f"Claude auth failed: {e}") from e
        except RateLimitError as e:
            raise LLMRateLimitError(f"Claude rate limit: {e}") from e
        except APIError as e:
            raise LLMError(f"Claude API error: {e}") from e
