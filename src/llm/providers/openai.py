"""OpenAI LLM provider."""

from ..base import LLMAuthError, LLMError, LLMProvider, LLMRateLimitError

# Lazy exception references — set when package available
_openai_exceptions = None


def _get_openai_exceptions():
    global _openai_exceptions
    if _openai_exceptions is None:
        try:
            from openai import APIError, AuthenticationError, RateLimitError
            _openai_exceptions = (AuthenticationError, RateLimitError, APIError)
        except ImportError:
            _openai_exceptions = ()
    return _openai_exceptions


class OpenAIProvider(LLMProvider):
    """OpenAI GPT provider."""

    provider_name = "openai"

    def __init__(self, api_key: str | None = None, model: str | None = None, client=None):
        self.model = model or "gpt-4o"

        if client:
            self.client = client
            return

        try:
            from openai import OpenAI
        except ImportError:
            raise LLMError(
                "openai package not installed. Run: pip install 'ai-coach[openai]'"
            )

        self.client = OpenAI(api_key=api_key)

    def generate(self, messages: list[dict], system: str | None = None, max_tokens: int = 2000) -> str:
        full_messages = []
        if system:
            full_messages.append({"role": "system", "content": system})
        full_messages.extend(messages)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=full_messages,
            )
            return response.choices[0].message.content
        except Exception as e:
            # Map to unified exceptions if openai package available
            exc = _get_openai_exceptions()
            if exc and len(exc) == 3:
                AuthErr, RateErr, ApiErr = exc
                if isinstance(e, AuthErr):
                    raise LLMAuthError(f"OpenAI auth failed: {e}") from e
                if isinstance(e, RateErr):
                    raise LLMRateLimitError(f"OpenAI rate limit: {e}") from e
                if isinstance(e, ApiErr):
                    raise LLMError(f"OpenAI API error: {e}") from e
            raise LLMError(f"OpenAI error: {e}") from e
