"""Google Gemini LLM provider using google-genai SDK."""

import uuid

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


def _handle_gemini_error(e: Exception):
    err_str = str(e).lower()
    if "api key" in err_str or "authentication" in err_str or "permission" in err_str:
        raise LLMAuthError(f"Gemini auth failed: {e}") from e
    if ("resource" in err_str and "exhausted" in err_str) or "rate" in err_str:
        raise LLMRateLimitError(f"Gemini rate limit: {e}") from e
    raise LLMError(f"Gemini API error: {e}") from e


class GeminiProvider(LLMProvider):
    """Google Gemini provider (google-genai SDK)."""

    provider_name = "gemini"

    def __init__(self, api_key: str | None = None, model: str | None = None, client=None):
        self.model_name = model or "gemini-2.5-flash"
        self._api_key = api_key
        self._last_usage: dict | None = None

        if client:
            self.client = client
            return

        try:
            from google import genai
        except ImportError:
            raise LLMError(
                "google-genai package not installed. Run: pip install 'stewardme[gemini]'"
            )

        self.client = genai.Client(api_key=api_key)

    def _extract_and_record_usage(self, response) -> dict | None:
        usage = getattr(response, "usage_metadata", None)
        if not usage:
            return None
        input_tokens = int(getattr(usage, "prompt_token_count", 0) or 0)
        output_tokens = int(getattr(usage, "candidates_token_count", 0) or 0)
        metrics.token_usage(self.model_name, input_tokens, output_tokens)
        result = {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "billed_input_tokens": float(input_tokens),
        }
        self._last_usage = result
        return result

    @staticmethod
    def _get_genai_types():
        try:
            from google.genai import types
        except ImportError:
            return None
        return types

    @staticmethod
    def _make_content(types_module, role: str, parts: list):
        if types_module:
            return types_module.Content(role=role, parts=parts)
        return {"role": role, "parts": parts}

    @staticmethod
    def _make_text_part(types_module, text: str):
        if types_module:
            return types_module.Part.from_text(text)
        return {"text": text}

    @staticmethod
    def _make_function_call_part(types_module, name: str, args: dict):
        if types_module:
            return types_module.Part.from_function_call(name=name, args=args)
        return {"function_call": {"name": name, "args": args}}

    @staticmethod
    def _make_function_response_part(types_module, name: str, response: dict):
        if types_module:
            return types_module.Part.from_function_response(name=name, response=response)
        return {"function_response": {"name": name, "response": response}}

    def generate(
        self,
        messages: list[dict],
        system: str | None = None,
        max_tokens: int = 2000,
        use_thinking: bool = False,
    ) -> str:
        types_module = self._get_genai_types()
        contents = self._convert_messages(messages, types_module=types_module)

        try:
            if types_module:
                config = types_module.GenerateContentConfig(
                    max_output_tokens=max_tokens,
                    system_instruction=system,
                )
            else:
                config = {"max_output_tokens": max_tokens}
                if system:
                    config["system_instruction"] = system
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=contents,
                config=config,
            )
            self._extract_and_record_usage(response)
            return self._strip_think_tags(response.text)
        except Exception as e:
            _handle_gemini_error(e)

    def generate_with_tools(
        self,
        messages: list[dict],
        tools: list[ToolDefinition],
        system: str | None = None,
        max_tokens: int = 2000,
        tool_choice: str = "auto",
    ) -> GenerateResponse:
        try:
            from google.genai import types
        except ImportError:
            raise LLMError("google-genai package not installed")

        try:
            # Build FunctionDeclarations
            func_decls = []
            for t in tools:
                schema = {
                    k: v
                    for k, v in t.input_schema.items()
                    if k in ("type", "properties", "required")
                }
                func_decls.append(
                    types.FunctionDeclaration(
                        name=t.name,
                        description=t.description,
                        parameters=schema if schema.get("properties") else None,
                    )
                )

            gemini_tools = [types.Tool(function_declarations=func_decls)]

            # Convert messages to Gemini Content format
            contents = self._convert_messages(messages)

            response = self.client.models.generate_content(
                model=self.model_name,
                contents=contents,
                config=types.GenerateContentConfig(
                    tools=gemini_tools,
                    system_instruction=system,
                    max_output_tokens=max_tokens,
                ),
            )

            # Parse response
            text_parts = []
            tool_calls = []

            if response.candidates:
                for part in response.candidates[0].content.parts:
                    if part.function_call and part.function_call.name:
                        fc = part.function_call
                        tool_calls.append(
                            ToolCall(
                                id=f"call_{uuid.uuid4().hex[:8]}",
                                name=fc.name,
                                arguments=dict(fc.args) if fc.args else {},
                            )
                        )
                    elif part.text:
                        text_parts.append(part.text)

            content = self._strip_think_tags("\n".join(text_parts)) if text_parts else None
            finish = "tool_calls" if tool_calls else "stop"

            usage = self._extract_and_record_usage(response)
            return GenerateResponse(
                content=content, tool_calls=tool_calls, finish_reason=finish, usage=usage
            )

        except Exception as e:
            _handle_gemini_error(e)

    def _convert_messages(self, messages: list[dict], types_module=None) -> list:
        """Convert generic messages to Gemini Content format."""
        types_module = types_module or self._get_genai_types()

        contents = []
        for msg in messages:
            role = msg.get("role")

            if role == "user":
                contents.append(
                    self._make_content(
                        types_module,
                        role="user",
                        parts=[self._make_text_part(types_module, msg["content"])],
                    )
                )

            elif role == "assistant":
                parts = []
                if msg.get("content"):
                    parts.append(self._make_text_part(types_module, msg["content"]))
                if msg.get("tool_calls"):
                    for tc in msg["tool_calls"]:
                        parts.append(
                            self._make_function_call_part(
                                types_module,
                                name=tc["name"],
                                args=tc["arguments"],
                            )
                        )
                if parts:
                    contents.append(self._make_content(types_module, role="model", parts=parts))

            elif role == "tool":
                contents.append(
                    self._make_content(
                        types_module,
                        role="user",
                        parts=[
                            self._make_function_response_part(
                                types_module,
                                name=msg.get("name", "tool"),
                                response={"result": msg["content"]},
                            )
                        ],
                    )
                )

        return contents
