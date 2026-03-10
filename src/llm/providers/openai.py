"""OpenAI LLM provider."""

import json

from observability import metrics

from ..base import (
    GenerateResponse,
    LLMAuthError,
    LLMError,
    LLMProvider,
    LLMRateLimitError,
    ToolCall,
    ToolDefinition,
)

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


def _handle_openai_error(e: Exception):
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


class OpenAIProvider(LLMProvider):
    """OpenAI GPT provider."""

    provider_name = "openai"

    def __init__(self, api_key: str | None = None, model: str | None = None, client=None):
        self.model = model or "gpt-4o"
        self.model_name = self.model
        self._last_usage: dict | None = None

        if client:
            self.client = client
            return

        try:
            from openai import OpenAI
        except ImportError:
            raise LLMError("openai package not installed. Run: pip install 'stewardme[openai]'")

        self.client = OpenAI(api_key=api_key)

    def _extract_and_record_usage(self, response) -> dict | None:
        usage = getattr(response, "usage", None)
        if not usage:
            return None
        input_tokens = int(getattr(usage, "prompt_tokens", 0) or 0)
        output_tokens = int(getattr(usage, "completion_tokens", 0) or 0)
        metrics.token_usage(self.model, input_tokens, output_tokens)
        result = {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "billed_input_tokens": float(input_tokens),
        }
        self._last_usage = result
        return result

    def generate(
        self,
        messages: list[dict],
        system: str | None = None,
        max_tokens: int = 2000,
        use_thinking: bool = False,
    ) -> str:
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
            self._extract_and_record_usage(response)
            return self._strip_think_tags(response.choices[0].message.content)
        except Exception as e:
            _handle_openai_error(e)

    def generate_with_tools(
        self,
        messages: list[dict],
        tools: list[ToolDefinition],
        system: str | None = None,
        max_tokens: int = 2000,
        tool_choice: str = "auto",
    ) -> GenerateResponse:
        # Map ToolDefinitions to OpenAI function format
        tool_defs = [
            {
                "type": "function",
                "function": {
                    "name": t.name,
                    "description": t.description,
                    "parameters": t.input_schema,
                },
            }
            for t in tools
        ]

        # Build messages with system prompt
        api_messages = []
        if system:
            api_messages.append({"role": "system", "content": system})

        # Convert generic messages to OpenAI format
        for msg in messages:
            role = msg.get("role")

            if role == "assistant" and msg.get("tool_calls"):
                # Assistant message with tool calls
                oai_tool_calls = []
                for tc in msg["tool_calls"]:
                    oai_tool_calls.append(
                        {
                            "id": tc["id"],
                            "type": "function",
                            "function": {
                                "name": tc["name"],
                                "arguments": json.dumps(tc["arguments"]),
                            },
                        }
                    )
                api_messages.append(
                    {
                        "role": "assistant",
                        "content": msg.get("content"),
                        "tool_calls": oai_tool_calls,
                    }
                )

            elif role == "tool":
                api_messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": msg["tool_call_id"],
                        "content": msg["content"],
                    }
                )

            else:
                api_messages.append(msg)

        # Map tool_choice
        tc = tool_choice if tool_choice in ("auto", "required", "none") else "auto"

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=api_messages,
                tools=tool_defs,
                tool_choice=tc,
            )

            choice = response.choices[0]
            message = choice.message

            # Parse tool calls
            tool_calls = []
            if message.tool_calls:
                for tc_obj in message.tool_calls:
                    tool_calls.append(
                        ToolCall(
                            id=tc_obj.id,
                            name=tc_obj.function.name,
                            arguments=json.loads(tc_obj.function.arguments),
                        )
                    )

            content = self._strip_think_tags(message.content)

            if choice.finish_reason == "tool_calls":
                finish = "tool_calls"
            elif choice.finish_reason == "length":
                finish = "max_tokens"
            else:
                finish = "stop"

            usage = self._extract_and_record_usage(response)
            return GenerateResponse(
                content=content, tool_calls=tool_calls, finish_reason=finish, usage=usage
            )

        except Exception as e:
            _handle_openai_error(e)
