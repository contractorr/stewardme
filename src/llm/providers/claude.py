"""Claude (Anthropic) LLM provider."""

from ..base import (
    GenerateResponse,
    LLMAuthError,
    LLMError,
    LLMProvider,
    LLMRateLimitError,
    ToolCall,
    ToolDefinition,
)


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

    def _get_exceptions(self):
        from anthropic import APIError, AuthenticationError, RateLimitError

        return AuthenticationError, RateLimitError, APIError

    def _handle_error(self, e: Exception):
        AuthenticationError, RateLimitError, APIError = self._get_exceptions()
        if isinstance(e, AuthenticationError):
            raise LLMAuthError(f"Claude auth failed: {e}") from e
        if isinstance(e, RateLimitError):
            raise LLMRateLimitError(f"Claude rate limit: {e}") from e
        if isinstance(e, APIError):
            raise LLMError(f"Claude API error: {e}") from e
        raise LLMError(f"Claude error: {e}") from e

    def generate(
        self, messages: list[dict], system: str | None = None, max_tokens: int = 2000
    ) -> str:
        try:
            self._get_exceptions()
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
        except Exception as e:
            self._handle_error(e)

    def generate_with_tools(
        self,
        messages: list[dict],
        tools: list[ToolDefinition],
        system: str | None = None,
        max_tokens: int = 2000,
        tool_choice: str = "auto",
    ) -> GenerateResponse:
        try:
            self._get_exceptions()
        except ImportError:
            raise LLMError("anthropic package not installed")

        try:
            # Map ToolDefinitions to Anthropic format (already matches)
            tool_defs = [
                {"name": t.name, "description": t.description, "input_schema": t.input_schema}
                for t in tools
            ]

            # Map tool_choice
            if tool_choice == "required":
                tc = {"type": "any"}
            else:
                tc = {"type": "auto"}

            # Convert messages — handle tool results for Anthropic format
            api_messages = self._convert_messages(messages)

            kwargs = {
                "model": self.model,
                "max_tokens": max_tokens,
                "messages": api_messages,
                "tools": tool_defs,
                "tool_choice": tc,
            }
            if system:
                kwargs["system"] = system

            response = self.client.messages.create(**kwargs)

            # Parse response blocks
            text_parts = []
            tool_calls = []
            for block in response.content:
                if block.type == "text":
                    text_parts.append(block.text)
                elif block.type == "tool_use":
                    tool_calls.append(
                        ToolCall(
                            id=block.id,
                            name=block.name,
                            arguments=block.input,
                        )
                    )

            content = "\n".join(text_parts) if text_parts else None

            if response.stop_reason == "tool_use":
                finish = "tool_calls"
            elif response.stop_reason == "max_tokens":
                finish = "max_tokens"
            else:
                finish = "stop"

            return GenerateResponse(content=content, tool_calls=tool_calls, finish_reason=finish)

        except Exception as e:
            self._handle_error(e)

    def _convert_messages(self, messages: list[dict]) -> list[dict]:
        """Convert generic messages to Anthropic format.

        Handles tool_calls and tool_result messages:
        - {"role": "assistant", "tool_calls": [...]} → assistant with tool_use content blocks
        - {"role": "tool", "tool_call_id": ..., "content": ...} → user with tool_result content block
        """
        api_messages = []
        i = 0
        while i < len(messages):
            msg = messages[i]
            role = msg.get("role")

            if role == "assistant" and msg.get("tool_calls"):
                # Build content blocks: optional text + tool_use blocks
                content = []
                if msg.get("content"):
                    content.append({"type": "text", "text": msg["content"]})
                for tc in msg["tool_calls"]:
                    content.append(
                        {
                            "type": "tool_use",
                            "id": tc["id"],
                            "name": tc["name"],
                            "input": tc["arguments"],
                        }
                    )
                api_messages.append({"role": "assistant", "content": content})

            elif role == "tool":
                # Collect consecutive tool results into one user message
                tool_results = []
                while i < len(messages) and messages[i].get("role") == "tool":
                    tr = messages[i]
                    tool_results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": tr["tool_call_id"],
                            "content": tr["content"],
                            **({"is_error": True} if tr.get("is_error") else {}),
                        }
                    )
                    i += 1
                api_messages.append({"role": "user", "content": tool_results})
                continue  # skip i += 1 at bottom

            else:
                api_messages.append(msg)

            i += 1

        return api_messages
