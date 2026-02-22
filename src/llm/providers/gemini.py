"""Google Gemini LLM provider."""

import uuid

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
    """Google Gemini provider."""

    provider_name = "gemini"

    def __init__(self, api_key: str | None = None, model: str | None = None, client=None):
        self.model_name = model or "gemini-2.0-flash"
        self._api_key = api_key

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
            import google.generativeai as genai
        except ImportError:
            raise LLMError("google-generativeai package not installed")

        try:
            # Build FunctionDeclarations
            func_decls = []
            for t in tools:
                # Strip unsupported keys from schema for Gemini
                schema = {k: v for k, v in t.input_schema.items() if k in ("type", "properties", "required")}
                func_decls.append(genai.types.FunctionDeclaration(
                    name=t.name,
                    description=t.description,
                    parameters=schema if schema.get("properties") else None,
                ))

            gemini_tools = [genai.types.Tool(function_declarations=func_decls)]

            # Build a model with tools + optional system instruction
            model = genai.GenerativeModel(
                self.model_name,
                tools=gemini_tools,
                system_instruction=system,
            )

            # Convert messages to Gemini Content format
            contents = self._convert_messages(messages)

            response = model.generate_content(
                contents,
                generation_config={"max_output_tokens": max_tokens},
            )

            # Parse response
            text_parts = []
            tool_calls = []

            if response.candidates:
                for part in response.candidates[0].content.parts:
                    if hasattr(part, "function_call") and part.function_call.name:
                        fc = part.function_call
                        tool_calls.append(ToolCall(
                            id=f"call_{uuid.uuid4().hex[:8]}",
                            name=fc.name,
                            arguments=dict(fc.args) if fc.args else {},
                        ))
                    elif hasattr(part, "text") and part.text:
                        text_parts.append(part.text)

            content = "\n".join(text_parts) if text_parts else None
            finish = "tool_calls" if tool_calls else "stop"

            return GenerateResponse(content=content, tool_calls=tool_calls, finish_reason=finish)

        except Exception as e:
            _handle_gemini_error(e)

    def _convert_messages(self, messages: list[dict]) -> list:
        """Convert generic messages to Gemini Content format."""
        import google.generativeai as genai

        contents = []
        for msg in messages:
            role = msg.get("role")

            if role == "user":
                contents.append({"role": "user", "parts": [msg["content"]]})

            elif role == "assistant":
                parts = []
                if msg.get("content"):
                    parts.append(msg["content"])
                if msg.get("tool_calls"):
                    for tc in msg["tool_calls"]:
                        parts.append(genai.protos.FunctionCall(
                            name=tc["name"],
                            args=tc["arguments"],
                        ))
                if parts:
                    contents.append({"role": "model", "parts": parts})

            elif role == "tool":
                contents.append({
                    "role": "user",
                    "parts": [genai.protos.FunctionResponse(
                        name=msg.get("name", "tool"),
                        response={"result": msg["content"]},
                    )],
                })

        return contents
