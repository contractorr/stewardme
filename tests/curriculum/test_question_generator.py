"""Regression tests: QuestionGenerator must work with the real (sync) LLMProvider interface.

These deliberately use a synchronous provider double shaped like LLMProvider
(generate is sync and takes a message list) — NOT AsyncMock — so an interface
mismatch fails here instead of being swallowed by the broad exception fallbacks.
"""

import json
from unittest.mock import MagicMock

from curriculum.models import BloomLevel, ReviewItemType
from curriculum.question_generator import QuestionGenerator
from llm import LLMProvider


def _sync_provider(response: str) -> MagicMock:
    provider = MagicMock(spec=LLMProvider)
    provider.provider_name = "mock"
    provider.generate.return_value = response
    return provider


def _assert_called_with_message_list(provider: MagicMock) -> None:
    messages = provider.generate.call_args.args[0]
    assert isinstance(messages, list)
    assert messages[0]["role"] == "user"
    assert isinstance(messages[0]["content"], str)


async def test_generate_questions_with_sync_provider():
    response = json.dumps(
        [
            {
                "question": "What is spaced repetition?",
                "expected_answer": "Reviewing material at increasing intervals.",
                "bloom_level": "understand",
            },
            {
                "question": "Why does retrieval practice work?",
                "expected_answer": "Recall strengthens memory traces.",
                "bloom_level": "apply",
            },
        ]
    )
    gen = QuestionGenerator(cheap_llm_provider=_sync_provider(response))

    items = await gen.generate_questions(
        content="Chapter content about spaced repetition.",
        chapter_title="Memory",
        guide_title="Learning",
        count=2,
        chapter_id="ch1",
        guide_id="g1",
        user_id="u1",
    )

    assert len(items) == 2
    assert items[0].question == "What is spaced repetition?"
    assert items[0].bloom_level == BloomLevel.UNDERSTAND
    _assert_called_with_message_list(gen.cheap_llm)


async def test_generate_placement_questions_with_sync_provider():
    response = json.dumps(
        [
            {
                "question": "Apply SM-2 to this schedule...",
                "expected_answer": "Interval doubles on success.",
                "bloom_level": "apply",
            }
        ]
    )
    gen = QuestionGenerator(cheap_llm_provider=_sync_provider(response))

    questions = await gen.generate_placement_questions(
        content="Chapter content.",
        chapter_title="Memory",
        guide_title="Learning",
        count=1,
    )

    assert len(questions) == 1
    assert questions[0]["id"]
    _assert_called_with_message_list(gen.cheap_llm)


async def test_grade_answer_uses_llm_not_keyword_fallback():
    response = json.dumps(
        {
            "grade": 4,
            "feedback": "Good reasoning.",
            "correct_points": ["mechanism"],
            "missing_points": ["edge case"],
        }
    )
    gen = QuestionGenerator(cheap_llm_provider=_sync_provider(response))

    result = await gen.grade_answer(
        question="Why does retrieval practice work?",
        expected_answer="Recall strengthens memory traces.",
        student_answer="Actively recalling makes memories stronger.",
        bloom_level=BloomLevel.APPLY,
    )

    # LLM grading happened: keyword fallback would produce "Keyword match" feedback
    assert result.grade == 4
    assert result.feedback == "Good reasoning."
    _assert_called_with_message_list(gen.cheap_llm)


async def test_generate_teachback_with_sync_provider():
    response = json.dumps(
        {
            "concept": "Spacing effect",
            "description": "Distributed practice beats massed practice.",
        }
    )
    gen = QuestionGenerator(cheap_llm_provider=_sync_provider(response))

    item = await gen.generate_teachback(
        content="Chapter content.",
        chapter_title="Memory",
        guide_title="Learning",
        chapter_id="ch1",
        guide_id="g1",
        user_id="u1",
    )

    assert item is not None
    assert item.item_type == ReviewItemType.TEACHBACK
    assert "Spacing effect" in item.question
    _assert_called_with_message_list(gen.cheap_llm)


async def test_grade_teachback_with_sync_provider():
    response = json.dumps({"grade": 5, "feedback": "Crystal clear."})
    gen = QuestionGenerator(llm_provider=_sync_provider(response))

    result = await gen.grade_teachback(
        concept="Spacing effect",
        expected_answer="Distributed practice beats massed practice.",
        student_answer="Spreading study out works better than cramming.",
        chapter_title="Memory",
        guide_title="Learning",
    )

    assert result.grade == 5
    assert result.feedback == "Crystal clear."
    _assert_called_with_message_list(gen.llm)


async def test_grade_applied_assessment_with_sync_provider():
    response = json.dumps({"grade": 3, "feedback": "Solid draft."})
    gen = QuestionGenerator(llm_provider=_sync_provider(response))

    result = await gen.grade_applied_assessment(
        guide_title="Learning",
        assessment_type="decision_memo",
        assessment_prompt="Write a memo.",
        evaluation_focus=["trade-offs", "failure modes"],
        student_answer="A memo with trade-offs and failure modes considered. " * 10,
    )

    assert result.grade == 3
    assert result.feedback == "Solid draft."
    _assert_called_with_message_list(gen.llm)


async def test_async_provider_double_still_supported():
    """Test doubles whose generate returns an awaitable keep working."""

    class AsyncDouble:
        def __init__(self, response: str):
            self.response = response

        def generate(self, messages, **kwargs):
            async def _coro():
                return self.response

            return _coro()

    response = json.dumps({"grade": 2, "feedback": "Partial."})
    gen = QuestionGenerator(cheap_llm_provider=AsyncDouble(response))

    result = await gen.grade_answer(
        question="Q",
        expected_answer="A",
        student_answer="B",
        bloom_level=BloomLevel.APPLY,
    )

    assert result.grade == 2
    assert result.feedback == "Partial."
