"""Tests for AgenticOrchestrator and agentic engine integration."""

from unittest.mock import MagicMock, patch

import pytest

from advisor.agentic import AgenticOrchestrator
from advisor.tools import ToolRegistry
from llm.base import GenerateResponse, ToolCall, ToolDefinition


@pytest.fixture
def mock_components(tmp_path):
    from journal.storage import JournalStorage
    from journal.embeddings import EmbeddingManager
    from journal.search import JournalSearch
    from intelligence.scraper import IntelStorage
    from advisor.rag import RAGRetriever

    journal_dir = tmp_path / "journal"
    journal_dir.mkdir()

    storage = JournalStorage(journal_dir)
    embeddings = EmbeddingManager(tmp_path / "chroma", collection_name="test")
    intel_storage = IntelStorage(tmp_path / "intel.db")
    journal_search = JournalSearch(storage, embeddings)
    rag = RAGRetriever(journal_search=journal_search, intel_db_path=tmp_path / "intel.db")

    return {
        "storage": storage,
        "embeddings": embeddings,
        "intel_storage": intel_storage,
        "rag": rag,
        "profile_path": str(tmp_path / "profile.yaml"),
        "recommendations_dir": tmp_path / "recommendations",
    }


@pytest.fixture
def registry(mock_components):
    return ToolRegistry(mock_components)


class TestAgenticOrchestrator:
    def test_immediate_text_response(self, registry):
        """LLM returns text on first call — no tool use."""
        mock_llm = MagicMock()
        mock_llm.generate_with_tools.return_value = GenerateResponse(
            content="Here's my advice.",
            finish_reason="stop",
        )

        orch = AgenticOrchestrator(mock_llm, registry, "system prompt")
        result = orch.run("What should I do?")

        assert result == "Here's my advice."
        assert mock_llm.generate_with_tools.call_count == 1

    def test_single_tool_call_then_text(self, registry):
        """LLM calls one tool, then responds with text."""
        mock_llm = MagicMock()

        # First call: tool use
        mock_llm.generate_with_tools.side_effect = [
            GenerateResponse(
                content=None,
                tool_calls=[ToolCall(id="t1", name="goals_list", arguments={})],
                finish_reason="tool_calls",
            ),
            # Second call: text response after getting tool result
            GenerateResponse(
                content="You have no goals yet.",
                finish_reason="stop",
            ),
        ]

        orch = AgenticOrchestrator(mock_llm, registry, "system prompt")
        result = orch.run("What are my goals?")

        assert result == "You have no goals yet."
        assert mock_llm.generate_with_tools.call_count == 2

        # Verify tool result was passed back in messages
        second_call_messages = mock_llm.generate_with_tools.call_args_list[1].kwargs["messages"]
        # user, assistant(tool_calls), tool(result)
        assert len(second_call_messages) == 3
        assert second_call_messages[0]["role"] == "user"
        assert second_call_messages[1]["role"] == "assistant"
        assert "tool_calls" in second_call_messages[1]
        assert second_call_messages[2]["role"] == "tool"

    def test_multiple_tool_calls_in_one_turn(self, registry):
        """LLM requests two tools in parallel."""
        mock_llm = MagicMock()
        mock_llm.generate_with_tools.side_effect = [
            GenerateResponse(
                content=None,
                tool_calls=[
                    ToolCall(id="t1", name="goals_list", arguments={}),
                    ToolCall(id="t2", name="intel_get_recent", arguments={"days": 7}),
                ],
                finish_reason="tool_calls",
            ),
            GenerateResponse(content="Combined analysis.", finish_reason="stop"),
        ]

        orch = AgenticOrchestrator(mock_llm, registry, "system prompt")
        result = orch.run("How do my goals relate to recent news?")

        assert result == "Combined analysis."
        # Should have 4 messages: user, assistant, tool(t1), tool(t2)
        second_call_messages = mock_llm.generate_with_tools.call_args_list[1].kwargs["messages"]
        assert len(second_call_messages) == 4
        tool_msgs = [m for m in second_call_messages if m["role"] == "tool"]
        assert len(tool_msgs) == 2

    def test_multi_iteration_tool_calls(self, registry):
        """LLM calls tools across multiple iterations."""
        mock_llm = MagicMock()
        mock_llm.generate_with_tools.side_effect = [
            # Iteration 1: list goals
            GenerateResponse(
                content=None,
                tool_calls=[ToolCall(id="t1", name="goals_list", arguments={})],
                finish_reason="tool_calls",
            ),
            # Iteration 2: search intel
            GenerateResponse(
                content=None,
                tool_calls=[ToolCall(id="t2", name="intel_search", arguments={"query": "rust"})],
                finish_reason="tool_calls",
            ),
            # Iteration 3: final response
            GenerateResponse(content="Final answer.", finish_reason="stop"),
        ]

        orch = AgenticOrchestrator(mock_llm, registry, "system prompt")
        result = orch.run("Analyze everything")

        assert result == "Final answer."
        assert mock_llm.generate_with_tools.call_count == 3

    def test_max_iterations_reached(self, registry):
        """Loop terminates at max_iterations."""
        mock_llm = MagicMock()
        # Always return tool calls, never stop
        mock_llm.generate_with_tools.return_value = GenerateResponse(
            content=None,
            tool_calls=[ToolCall(id="t1", name="goals_list", arguments={})],
            finish_reason="tool_calls",
        )

        orch = AgenticOrchestrator(mock_llm, registry, "system prompt", max_iterations=3)
        result = orch.run("infinite loop?")

        assert mock_llm.generate_with_tools.call_count == 3
        assert "wasn't able to complete" in result

    def test_max_iterations_with_partial_content(self, registry):
        """Returns partial content when max iterations hit and LLM produced text."""
        mock_llm = MagicMock()
        mock_llm.generate_with_tools.return_value = GenerateResponse(
            content="Partial thought...",
            tool_calls=[ToolCall(id="t1", name="goals_list", arguments={})],
            finish_reason="tool_calls",
        )

        orch = AgenticOrchestrator(mock_llm, registry, "system prompt", max_iterations=2)
        result = orch.run("question")

        assert result == "Partial thought..."

    def test_tool_error_passed_back(self, registry):
        """Tool execution error is returned to LLM, not raised."""
        mock_llm = MagicMock()
        mock_llm.generate_with_tools.side_effect = [
            GenerateResponse(
                content=None,
                tool_calls=[ToolCall(id="t1", name="journal_read", arguments={"filename": "nonexistent.md"})],
                finish_reason="tool_calls",
            ),
            GenerateResponse(content="That entry doesn't exist.", finish_reason="stop"),
        ]

        orch = AgenticOrchestrator(mock_llm, registry, "system prompt")
        result = orch.run("Read my entry")

        assert result == "That entry doesn't exist."
        # Verify error was in tool result message
        second_call_messages = mock_llm.generate_with_tools.call_args_list[1].kwargs["messages"]
        tool_msg = [m for m in second_call_messages if m["role"] == "tool"][0]
        assert tool_msg["is_error"] is True

    def test_unknown_tool_returns_error(self, registry):
        """Unknown tool name returns error to LLM."""
        mock_llm = MagicMock()
        mock_llm.generate_with_tools.side_effect = [
            GenerateResponse(
                content=None,
                tool_calls=[ToolCall(id="t1", name="fake_tool", arguments={})],
                finish_reason="tool_calls",
            ),
            GenerateResponse(content="Sorry, that tool doesn't exist.", finish_reason="stop"),
        ]

        orch = AgenticOrchestrator(mock_llm, registry, "system prompt")
        result = orch.run("Do something weird")

        assert result == "Sorry, that tool doesn't exist."

    def test_system_prompt_passed(self, registry):
        """System prompt is forwarded to LLM."""
        mock_llm = MagicMock()
        mock_llm.generate_with_tools.return_value = GenerateResponse(content="ok", finish_reason="stop")

        orch = AgenticOrchestrator(mock_llm, registry, "You are a coach.")
        orch.run("hi")

        call_kwargs = mock_llm.generate_with_tools.call_args.kwargs
        assert call_kwargs["system"] == "You are a coach."

    def test_assistant_text_with_tool_calls_preserved(self, registry):
        """When LLM returns both text and tool_calls, text is in assistant msg."""
        mock_llm = MagicMock()
        mock_llm.generate_with_tools.side_effect = [
            GenerateResponse(
                content="Let me check your goals.",
                tool_calls=[ToolCall(id="t1", name="goals_list", arguments={})],
                finish_reason="tool_calls",
            ),
            GenerateResponse(content="Here are your goals: none.", finish_reason="stop"),
        ]

        orch = AgenticOrchestrator(mock_llm, registry, "system")
        orch.run("goals?")

        second_call_messages = mock_llm.generate_with_tools.call_args_list[1].kwargs["messages"]
        assistant_msg = second_call_messages[1]
        assert assistant_msg["content"] == "Let me check your goals."
        assert "tool_calls" in assistant_msg


class TestAgenticEngineIntegration:
    def test_engine_with_use_tools(self, mock_components):
        """AdvisorEngine routes to orchestrator when use_tools=True."""
        from advisor.engine import AdvisorEngine
        from advisor.rag import RAGRetriever

        mock_client = MagicMock()
        # generate_with_tools returns text immediately
        resp = MagicMock()
        resp.content = [MagicMock(type="text", text="Agentic response")]
        resp.stop_reason = "end_turn"
        mock_client.messages.create.return_value = resp

        engine = AdvisorEngine(
            rag=mock_components["rag"],
            provider="claude",
            client=mock_client,
            use_tools=True,
            components=mock_components,
        )

        assert engine._orchestrator is not None
        result = engine.ask("What are my goals?")
        assert isinstance(result, str)

    def test_engine_without_use_tools(self, mock_components):
        """AdvisorEngine uses classic RAG when use_tools=False."""
        from advisor.engine import AdvisorEngine

        mock_client = MagicMock()
        resp = MagicMock()
        resp.content = [MagicMock(text="RAG response")]
        mock_client.messages.create.return_value = resp

        engine = AdvisorEngine(
            rag=mock_components["rag"],
            provider="claude",
            client=mock_client,
            use_tools=False,
        )

        assert engine._orchestrator is None
        result = engine.ask("What should I learn?")
        assert result == "RAG response"

    def test_engine_use_tools_without_components_no_orchestrator(self, mock_components):
        """use_tools=True but no components dict → no orchestrator (falls back to RAG)."""
        from advisor.engine import AdvisorEngine

        mock_client = MagicMock()
        resp = MagicMock()
        resp.content = [MagicMock(text="RAG fallback")]
        mock_client.messages.create.return_value = resp

        engine = AdvisorEngine(
            rag=mock_components["rag"],
            provider="claude",
            client=mock_client,
            use_tools=True,
            components=None,
        )

        assert engine._orchestrator is None
