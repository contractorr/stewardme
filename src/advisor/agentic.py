"""Agentic orchestrator — LLM tool-calling loop."""

import concurrent.futures
import json
import uuid
from collections.abc import Callable

import structlog

from llm.base import LLMProvider
from services.tool_registry import ToolRegistry

from .context_compressor import ContextCompressor
from .trace import (
    make_answer_entry,
    make_llm_entry,
    make_max_iter_entry,
    make_nudge_entry,
    make_session_entry,
    make_tool_done_entry,
    make_tool_start_entry,
)

logger = structlog.get_logger()


def _is_tool_error(result_text: str) -> bool:
    """Check if a tool result is a structured error from ToolRegistry.

    ToolRegistry.execute() returns JSON with an "error" key on failure.
    Parse instead of string-matching to avoid false positives on content
    that happens to contain the word "error".
    """
    try:
        parsed = json.loads(result_text)
        return isinstance(parsed, dict) and "error" in parsed
    except (json.JSONDecodeError, TypeError):
        return False


_NUDGE_TEMPLATE = (
    "You've only used {used} tool(s) so far ({used_names}). "
    "Consider using additional tools for a more thorough answer. "
    "Unused tools: {unused_names}"
)


class AgenticOrchestrator:
    """Runs an LLM tool-calling loop until the model responds with text."""

    def __init__(
        self,
        llm: LLMProvider,
        registry: ToolRegistry,
        system_prompt: str,
        max_iterations: int = 10,
        min_tool_calls: int = 2,
        cheap_llm: LLMProvider | None = None,
        token_threshold: int = 100_000,
        tool_timeout: float = 60.0,
    ):
        self.llm = llm
        self.registry = registry
        self.system_prompt = system_prompt
        self.max_iterations = max_iterations
        self.min_tool_calls = min_tool_calls
        self.tool_timeout = tool_timeout
        self.compressor = ContextCompressor(
            cheap_llm=cheap_llm,
            token_threshold=token_threshold,
        )
        self._total_input_tokens = 0
        self._total_usage: dict = {"input_tokens": 0, "output_tokens": 0, "billed_input_tokens": 0}
        self._session_id: str = ""
        self._trace: list[dict] = []

    def _build_nudge(self, used_tools: set[str], available_tools: list[str]) -> str:
        unused = sorted(set(available_tools) - used_tools)
        return _NUDGE_TEMPLATE.format(
            used=len(used_tools),
            used_names=", ".join(sorted(used_tools)),
            unused_names=", ".join(unused[:5]),  # cap at 5 to avoid huge prompts
        )

    def run(
        self,
        user_message: str,
        conversation_history: list[dict] | None = None,
        event_callback: Callable[[dict], None] | None = None,
    ) -> str:
        # Reset trace and usage for this run
        self._session_id = uuid.uuid4().hex[:16]
        self._trace = [make_session_entry(self._session_id, user_message)]
        self._total_usage = {"input_tokens": 0, "output_tokens": 0, "billed_input_tokens": 0}

        messages = list(conversation_history or [])
        messages.append({"role": "user", "content": user_message})
        tools = self.registry.get_definitions()
        available_tool_names = [t.name for t in tools]
        used_tools: set[str] = set()
        nudged = False

        for iteration in range(self.max_iterations):
            response = self.llm.generate_with_tools(
                messages=messages,
                tools=tools,
                system=self.system_prompt,
            )

            logger.debug(
                "agentic_iteration",
                iteration=iteration,
                finish_reason=response.finish_reason,
                tool_call_count=len(response.tool_calls) if response.tool_calls else 0,
            )
            input_tokens = 0
            if response.usage:
                input_tokens = int(response.usage.get("input_tokens", 0))
                self._total_input_tokens += input_tokens
                for k in ("input_tokens", "output_tokens", "billed_input_tokens"):
                    self._total_usage[k] = self._total_usage.get(k, 0) + int(
                        response.usage.get(k, 0)
                    )
            else:
                logger.warning("agentic_usage_missing", iteration=iteration)

            self._trace.append(
                make_llm_entry(
                    iteration=iteration,
                    finish_reason=response.finish_reason,
                    tool_call_count=len(response.tool_calls) if response.tool_calls else 0,
                    input_tokens=input_tokens,
                )
            )

            # LLM finished with text — check minimum tool call enforcement
            if response.finish_reason == "stop" or not response.tool_calls:
                if len(used_tools) < self.min_tool_calls and not nudged and available_tool_names:
                    # Not enough tools used — nudge and continue
                    nudged = True
                    nudge = self._build_nudge(used_tools, available_tool_names)
                    logger.info(
                        "agentic_nudge",
                        used=len(used_tools),
                        min=self.min_tool_calls,
                    )
                    self._trace.append(make_nudge_entry(len(used_tools), self.min_tool_calls))
                    # Append the LLM's premature answer + a user nudge
                    if response.content:
                        messages.append({"role": "assistant", "content": response.content})
                    messages.append({"role": "user", "content": nudge})
                    continue

                logger.info("agentic_complete", iterations=iteration + 1)
                content = response.content or ""
                self._trace.append(make_answer_entry(iteration, len(content)))
                if event_callback:
                    event_callback({"type": "answer", "content": content})
                return content

            # Build assistant message with tool calls
            assistant_msg = {
                "role": "assistant",
                "tool_calls": [
                    {"id": tc.id, "name": tc.name, "arguments": tc.arguments}
                    for tc in response.tool_calls
                ],
            }
            if response.content:
                assistant_msg["content"] = response.content
            messages.append(assistant_msg)

            # Execute each tool call and append results
            for tc in response.tool_calls:
                used_tools.add(tc.name)
                logger.info("tool_call", tool=tc.name, args=list(tc.arguments.keys()))
                if event_callback:
                    event_callback({"type": "tool_start", "tool": tc.name})
                self._trace.append(make_tool_start_entry(tc.name, tc.id, list(tc.arguments.keys())))

                try:
                    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
                        future = pool.submit(self.registry.execute, tc.name, tc.arguments)
                        result_text = future.result(timeout=self.tool_timeout)
                except concurrent.futures.TimeoutError:
                    logger.error("tool_timeout", tool=tc.name, timeout=self.tool_timeout)
                    result_text = json.dumps(
                        {"error": f"{tc.name}: timed out after {self.tool_timeout}s"}
                    )
                is_error = _is_tool_error(result_text)

                logger.info(
                    "tool_result",
                    tool=tc.name,
                    chars=len(result_text),
                    is_error=is_error,
                )
                if event_callback:
                    event_callback({"type": "tool_done", "tool": tc.name, "is_error": is_error})
                self._trace.append(make_tool_done_entry(tc.name, tc.id, len(result_text), is_error))

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "name": tc.name,
                        "content": result_text,
                        "is_error": is_error,
                    }
                )

            messages = self.compressor.compress_if_needed(messages, self._total_input_tokens)

        # Max iterations reached - return whatever we have
        logger.warning("agentic_max_iterations", max=self.max_iterations)
        self._trace.append(make_max_iter_entry(self.max_iterations))
        if response.content:
            return response.content
        return "I wasn't able to complete that request within the allowed steps."
