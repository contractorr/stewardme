"""Tests for outbound query hygiene and the research audit log."""

import json
from unittest.mock import MagicMock, patch

from research.outbound import OutboundLogger, sanitize_outbound_query
from research.web_search import SearchResult, WebSearchClient


class TestSanitizeOutboundQuery:
    def test_clean_topic_phrase_passes_unchanged(self):
        assert sanitize_outbound_query("Rust Web Frameworks") == "Rust Web Frameworks"

    def test_personal_feelings_sentence_dropped(self):
        assert sanitize_outbound_query("I am worried my startup is failing") is None
        assert sanitize_outbound_query("feeling burned out at work lately") is None

    def test_first_person_sentence_reduced_to_topic_core(self):
        result = sanitize_outbound_query("I want to learn more about rust web frameworks")
        assert result is not None
        assert "I" not in result.split()
        assert "my" not in result.lower().split()
        assert "rust" in result.lower()
        assert "frameworks" in result.lower()

    def test_long_sentence_truncated_to_content_words(self):
        query = (
            "the current state of the art in large language model evaluation "
            "for enterprise deployments across regulated industries this year"
        )
        result = sanitize_outbound_query(query)
        assert result is not None
        assert len(result.split()) <= 10
        assert "language" in result.lower()

    def test_short_topic_with_first_person_marker_stripped(self):
        result = sanitize_outbound_query("my LP discovery conversations pipeline")
        assert result is not None
        assert "my" not in result.lower().split()

    def test_empty_and_whitespace_dropped(self):
        assert sanitize_outbound_query("") is None
        assert sanitize_outbound_query("   ") is None

    def test_all_function_words_dropped(self):
        assert sanitize_outbound_query("I want to know about it") is None


class TestOutboundLogger:
    def test_record_appends_jsonl(self, tmp_path):
        log_path = tmp_path / "research" / "outbound_log.jsonl"
        logger = OutboundLogger(log_path)

        entry1 = logger.record("rust frameworks", "tavily")
        entry2 = logger.record("llm evaluation", "duckduckgo")

        lines = log_path.read_text().strip().splitlines()
        assert [json.loads(line) for line in lines] == [entry1, entry2]
        assert entry1["provider"] == "tavily"
        assert entry1["query"] == "rust frameworks"
        assert "timestamp" in entry1

    def test_default_path_under_coach_home(self, tmp_path, monkeypatch):
        monkeypatch.setenv("COACH_HOME", str(tmp_path))
        logger = OutboundLogger()
        assert logger.log_path == tmp_path / "research" / "outbound_log.jsonl"


class TestWebSearchClientHygiene:
    def _client(self, tmp_path):
        return WebSearchClient(
            api_key="tavily-key",
            outbound_logger=OutboundLogger(tmp_path / "outbound_log.jsonl"),
        )

    def test_sanitized_query_is_what_gets_sent_and_logged(self, tmp_path):
        client = self._client(tmp_path)
        with patch.object(client, "_tavily_search", return_value=[]) as tavily:
            client.search("I want to learn more about rust web frameworks")

        sent_query = tavily.call_args[0][0]
        assert "I " not in f"{sent_query} "
        logged = [json.loads(line) for line in (tmp_path / "outbound_log.jsonl").open()]
        assert [e["query"] for e in logged] == [sent_query]
        assert logged[0]["provider"] == "tavily"

    def test_dropped_query_never_sent_or_logged(self, tmp_path):
        client = self._client(tmp_path)
        with patch.object(client, "_tavily_search", return_value=[]) as tavily:
            results = client.search("I feel anxious about my career")

        assert results == []
        tavily.assert_not_called()
        assert not (tmp_path / "outbound_log.jsonl").exists()

    def test_log_failure_blocks_the_search(self, tmp_path):
        client = self._client(tmp_path)
        client._outbound.record = MagicMock(side_effect=OSError("disk full"))
        with patch.object(client, "_tavily_search", return_value=[]) as tavily:
            try:
                client.search("rust frameworks")
                raised = False
            except OSError:
                raised = True
        assert raised
        tavily.assert_not_called()


class TestResearchRunAuditTrail:
    def test_run_logs_exactly_issued_queries_and_report_section(self, tmp_path):
        from journal.storage import JournalStorage
        from research.agent import DeepResearchAgent

        journal_dir = tmp_path / "journal"
        journal_dir.mkdir()
        journal = JournalStorage(journal_dir)

        log_path = tmp_path / "outbound_log.jsonl"
        client = WebSearchClient(api_key="tavily-key", outbound_logger=OutboundLogger(log_path))
        results = [SearchResult(title="t", url="https://example.com", content="c")]

        synthesizer = MagicMock()
        synthesizer.synthesize.return_value = "## Summary\nFindings."

        agent = DeepResearchAgent(
            journal_storage=journal,
            intel_storage=MagicMock(),
            embeddings=MagicMock(),
            search_client=client,
            synthesizer=synthesizer,
        )

        with patch.object(client, "_tavily_search", return_value=results):
            run_results = agent.run(specific_topic="rust web frameworks")

        assert run_results[0]["success"] is True
        logged = [json.loads(line) for line in log_path.open()]
        assert [e["query"] for e in logged] == ["rust web frameworks"]
        assert run_results[0]["outbound_queries"] == logged

        report = run_results[0]["content"]
        assert "## Outbound Queries" in report
        assert "rust web frameworks" in report.split("## Outbound Queries")[1]

        stored = journal.read(run_results[0]["filepath"])
        assert "## Outbound Queries" in stored.content
