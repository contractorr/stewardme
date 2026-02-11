"""Base LLM provider abstraction."""

from abc import ABC, abstractmethod


class LLMError(Exception):
    """Base LLM error."""


class LLMRateLimitError(LLMError):
    """Rate limit hit."""


class LLMAuthError(LLMError):
    """Authentication failure."""


class LLMProvider(ABC):
    """Abstract LLM provider interface."""

    provider_name: str = "base"

    @abstractmethod
    def generate(self, messages: list[dict], system: str | None = None, max_tokens: int = 2000) -> str:
        """Generate a response from messages.

        Args:
            messages: List of {"role": ..., "content": ...} dicts
            system: Optional system prompt
            max_tokens: Max response tokens

        Returns:
            Generated text
        """
        ...
