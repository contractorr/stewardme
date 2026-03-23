"""Tests for context_budget utilities."""

from advisor.context_budget import (
    tokens_to_chars,
    truncate_lines_to_tokens,
    truncate_to_token_budget,
)
from services.tokens import count_tokens


class TestTokensToChars:
    def test_basic(self):
        assert tokens_to_chars(100) == 400

    def test_zero(self):
        assert tokens_to_chars(0) == 0


class TestTruncateLinesToTokens:
    def test_within_budget_unchanged(self):
        assert truncate_lines_to_tokens("short", 1000) == "short"

    def test_truncates_at_line_boundary(self):
        text = "\n".join(f"line {i}" for i in range(100))
        result = truncate_lines_to_tokens(text, 5)
        assert count_tokens(result) <= 5
        assert result  # not empty

    def test_empty_string(self):
        assert truncate_lines_to_tokens("", 10) == ""


class TestTruncateToTokenBudget:
    def test_within_budget_unchanged(self):
        j, i = truncate_to_token_budget("journal", "intel", 0.7, 5000)
        assert j == "journal"
        assert i == "intel"

    def test_over_budget_truncated(self):
        long_j = "word " * 200
        long_i = "item " * 200
        j, i = truncate_to_token_budget(long_j, long_i, 0.7, 10)
        total = count_tokens(j) + count_tokens(i)
        assert total < count_tokens(long_j) + count_tokens(long_i)
