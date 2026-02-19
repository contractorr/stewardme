"""Tests for TopicSelector."""

from datetime import datetime, timedelta

import pytest

from journal.storage import JournalStorage
from research.topics import TopicSelector


@pytest.fixture
def research_journal(temp_dirs):
    """Journal with research-relevant entries."""
    storage = JournalStorage(temp_dirs["journal_dir"])

    # Create goal with research request
    storage.create(
        content="I want to research about machine learning in healthcare. Also need to understand RAG systems better.",
        entry_type="goal",
        title="Q1 Learning Goals",
        tags=["learning", "ai"],
    )

    # Create entries with recurring themes
    for i in range(5):
        storage.create(
            content="Today I worked on kubernetes deployment. Kubernetes is powerful for orchestration. Also explored kubernetes networking.",
            entry_type="daily",
            title=f"Day {i+1} Notes",
            tags=["work", "kubernetes"],
        )

    # Create old research entry (should be skipped)
    old_date = datetime.now() - timedelta(days=30)
    storage.create(
        content="Research on Docker containerization",
        entry_type="research",
        title="Research: Docker",
        tags=["research", "auto"],
        metadata={"topic": "Docker"},
    )

    return storage


class TestTopicSelector:
    """Tests for TopicSelector class."""

    def test_init(self, temp_dirs):
        """Test TopicSelector initialization."""
        storage = JournalStorage(temp_dirs["journal_dir"])
        selector = TopicSelector(storage)

        assert selector.max_topics == 2
        assert selector.theme_window_days == 30
        assert selector.min_mentions == 3

    def test_extract_goal_topics(self, research_journal):
        """Test extraction of topics from goals."""
        selector = TopicSelector(research_journal)
        topics = selector._extract_goal_topics()

        # Should find "machine learning in healthcare" and "RAG systems"
        topic_names = [t["topic"].lower() for t in topics]
        assert any("machine learning" in t or "healthcare" in t for t in topic_names)

    def test_cluster_journal_themes(self, research_journal):
        """Test clustering of recurring themes."""
        selector = TopicSelector(research_journal, min_mentions=3)
        themes = selector._cluster_journal_themes()

        # "kubernetes" appears 3+ times
        topic_names = [t["topic"].lower() for t in themes]
        assert any("kubernetes" in t for t in topic_names)

    def test_get_topics_deduplication(self, research_journal):
        """Test that topics are deduplicated."""
        selector = TopicSelector(research_journal, max_topics=5)
        topics = selector.get_topics()

        # No duplicate topics
        topic_names = [t["topic"].lower() for t in topics]
        assert len(topic_names) == len(set(topic_names))

    def test_get_topics_respects_max(self, research_journal):
        """Test max_topics limit is respected."""
        selector = TopicSelector(research_journal, max_topics=1)
        topics = selector.get_topics()

        assert len(topics) <= 1

    def test_get_topics_skips_researched(self, research_journal):
        """Test that recently researched topics are skipped."""
        selector = TopicSelector(research_journal, skip_researched_days=60)
        topics = selector.get_topics(researched_topics=["Kubernetes"])

        topic_names = [t["topic"].lower() for t in topics]
        assert "kubernetes" not in topic_names

    def test_get_recent_research_topics(self, research_journal):
        """Test retrieval of recently researched topics."""
        selector = TopicSelector(research_journal, skip_researched_days=60)
        recent = selector.get_recent_research_topics()

        # Should include "Docker" from the fixture
        assert any("docker" in t.lower() for t in recent)

    def test_stopwords_filtering(self, temp_dirs):
        """Test that stopwords are filtered from themes."""
        storage = JournalStorage(temp_dirs["journal_dir"])

        # Create entries with lots of stopwords
        for i in range(5):
            storage.create(
                content="This is about work working worked that with from have been",
                entry_type="daily",
                title=f"Entry {i}",
            )

        selector = TopicSelector(storage, min_mentions=3)
        themes = selector._cluster_journal_themes()

        stopwords = selector._get_stopwords()
        for theme in themes:
            assert theme["topic"].lower() not in stopwords
