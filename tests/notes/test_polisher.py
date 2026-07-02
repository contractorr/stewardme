"""Tests for the note polisher LLM pipeline."""

import json

import pytest

from notes.polisher import MAX_NOTE_CHARS, NotePolisher, NotePolishError, compute_diff


class FakeLLM:
    def __init__(self, response):
        self.response = response
        self.calls = []

    def generate(self, messages, system=None, max_tokens=2000, **kwargs):
        self.calls.append({"messages": messages, "system": system})
        return self.response


def test_polish_parses_json_response():
    response = json.dumps(
        {
            "polished_markdown": "# Note\n\nFixed text.",
            "corrections": [
                {"type": "spelling", "original": "teh", "corrected": "the", "reason": "typo"},
                {
                    "type": "removal",
                    "original": "duplicate para",
                    "corrected": "",
                    "reason": "repeated",
                },
            ],
        }
    )
    result = NotePolisher(FakeLLM(response)).polish("teh note\nduplicate para")
    assert result.polished_markdown.startswith("# Note")
    assert [c["type"] for c in result.corrections] == ["spelling", "removal"]
    assert "-teh note" in result.diff
    assert "+# Note" in result.diff


def test_polish_handles_fenced_json():
    response = "```json\n" + json.dumps({"polished_markdown": "clean", "corrections": []}) + "\n```"
    result = NotePolisher(FakeLLM(response)).polish("dirty")
    assert result.polished_markdown == "clean"


def test_polish_falls_back_to_raw_text_on_malformed_json():
    result = NotePolisher(FakeLLM("Just a polished note, no JSON.")).polish("messy")
    assert result.polished_markdown == "Just a polished note, no JSON."
    assert result.corrections == []


def test_polish_normalizes_unknown_correction_types():
    response = json.dumps(
        {
            "polished_markdown": "ok",
            "corrections": [{"type": "style!!", "original": "a", "corrected": "b"}],
        }
    )
    result = NotePolisher(FakeLLM(response)).polish("input")
    assert result.corrections[0]["type"] == "rewording"


def test_polish_rejects_empty_input():
    with pytest.raises(NotePolishError):
        NotePolisher(FakeLLM("x")).polish("   ")


def test_polish_rejects_oversized_input():
    with pytest.raises(NotePolishError, match="character limit"):
        NotePolisher(FakeLLM("x")).polish("a" * (MAX_NOTE_CHARS + 1))


def test_polish_raises_on_empty_llm_response():
    with pytest.raises(NotePolishError):
        NotePolisher(FakeLLM("")).polish("note")


def test_diff_is_computed_locally_not_trusted_from_llm():
    response = json.dumps({"polished_markdown": "line one", "corrections": [], "diff": "FAKE DIFF"})
    result = NotePolisher(FakeLLM(response)).polish("line 1")
    assert "FAKE DIFF" not in result.diff
    assert "-line 1" in result.diff
    assert "+line one" in result.diff


def test_compute_diff_empty_when_identical():
    assert compute_diff("same", "same") == ""
