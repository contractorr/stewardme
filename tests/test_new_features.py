"""Tests for new features: templates, sentiment, export."""

import json

from journal.sentiment import analyze_sentiment
from journal.storage import JournalStorage
from journal.templates import get_template, list_templates


class TestJournalTemplates:
    def test_builtin_templates_exist(self):
        templates = list_templates()
        assert "daily" in templates
        assert "weekly" in templates
        assert "goal" in templates
        assert "project" in templates
        assert "learning" in templates

    def test_get_template(self):
        tmpl = get_template("daily")
        assert tmpl is not None
        assert "What went well" in tmpl["content"]
        assert tmpl["type"] == "daily"

    def test_custom_template_override(self):
        custom = {"daily": {"name": "My Daily", "type": "daily", "content": "Custom"}}
        tmpl = get_template("daily", custom)
        assert tmpl["content"] == "Custom"

    def test_unknown_template_returns_none(self):
        assert get_template("nonexistent") is None


class TestSentiment:
    def test_positive_sentiment(self):
        result = analyze_sentiment("Today was great! I feel productive and motivated.")
        assert result["label"] == "positive"
        assert result["score"] > 0

    def test_negative_sentiment(self):
        result = analyze_sentiment("I'm frustrated and stressed. Everything is difficult.")
        assert result["label"] == "negative"
        assert result["score"] < 0

    def test_neutral_sentiment(self):
        result = analyze_sentiment("The meeting was at 3pm in the conference room.")
        assert result["label"] == "neutral"
        assert result["score"] == 0

    def test_mixed_sentiment(self):
        result = analyze_sentiment("Good progress on the project but stressed about deadline.")
        assert result["label"] in ("mixed", "positive", "negative")


class TestExportBackup:
    def test_export_json(self, tmp_path):
        from cli.commands.export import _export_json

        journal_dir = tmp_path / "journal"
        journal_dir.mkdir()
        storage = JournalStorage(journal_dir)
        storage.create(content="Test entry", entry_type="daily", title="Test")

        paths = {
            "journal_dir": journal_dir,
            "intel_db": tmp_path / "intel.db",
        }

        output = tmp_path / "export.json"
        _export_json(paths, output)
        assert output.exists()

        data = json.loads(output.read_text())
        assert len(data["journal"]) == 1
        assert data["journal"][0]["content"] == "Test entry"

    def test_export_markdown(self, tmp_path):
        from cli.commands.export import _export_markdown

        journal_dir = tmp_path / "journal"
        journal_dir.mkdir()
        storage = JournalStorage(journal_dir)
        storage.create(content="Test entry", entry_type="daily", title="Test Export")

        paths = {
            "journal_dir": journal_dir,
            "intel_db": tmp_path / "intel.db",
        }

        output = tmp_path / "export.md"
        _export_markdown(paths, output)
        assert output.exists()
        content = output.read_text()
        assert "Test Export" in content
        assert "Test entry" in content
