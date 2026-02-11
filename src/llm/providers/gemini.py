"""Google Gemini LLM provider."""

from ..base import LLMAuthError, LLMError, LLMProvider, LLMRateLimitError


class GeminiProvider(LLMProvider):
    """Google Gemini provider."""

    provider_name = "gemini"

    def __init__(self, api_key: str | None = None, model: str | None = None, client=None):
        self.model_name = model or "gemini-2.0-flash"

        if client:
            self.client = client
            return

        try:
            import google.generativeai as genai
        except ImportError:
            raise LLMError(
                "google-generativeai package not installed. Run: pip install 'ai-coach[gemini]'"
            )

        if api_key:
            genai.configure(api_key=api_key)

        self.client = genai.GenerativeModel(self.model_name)

    def generate(self, messages: list[dict], system: str | None = None, max_tokens: int = 2000) -> str:
        parts = []
        if system:
            parts.append(f"System: {system}\n")
        for msg in messages:
            parts.append(msg["content"])
        prompt = "\n".join(parts)

        try:
            response = self.client.generate_content(
                prompt,
                generation_config={"max_output_tokens": max_tokens},
            )
            return response.text
        except Exception as e:
            err_str = str(e).lower()
            if "api key" in err_str or "authentication" in err_str or "permission" in err_str:
                raise LLMAuthError(f"Gemini auth failed: {e}") from e
            if ("resource" in err_str and "exhausted" in err_str) or "rate" in err_str:
                raise LLMRateLimitError(f"Gemini rate limit: {e}") from e
            raise LLMError(f"Gemini API error: {e}") from e
