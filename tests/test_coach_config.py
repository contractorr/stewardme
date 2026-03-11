from pathlib import Path

from coach_config import load_config


def test_load_config_preserves_unknown_top_level_sections(tmp_path):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        """
logging:
  level: debug
profile:
  path: ~/custom/profile.yaml
journal:
  templates:
    custom:
      name: Custom
      type: daily
      content: hello
events:
  enabled: true
projects:
  github_issues:
    enabled: true
"""
    )

    config = load_config(config_path)

    assert config["logging"]["level"] == "DEBUG"
    assert config["profile"]["path"] == "~/custom/profile.yaml"
    assert config["journal"]["templates"]["custom"]["content"] == "hello"
    assert config["events"]["enabled"] is True
    assert config["projects"]["github_issues"]["enabled"] is True


def test_load_config_preserves_unknown_nested_source_sections(tmp_path):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        """
paths:
  journal_dir: ~/custom/journal
sources:
  enabled:
    - rss_feeds
  rss_feeds:
    - https://example.com/feed.xml
  arxiv:
    enabled: true
    categories:
      - cs.AI
  reddit:
    enabled: true
    subreddits:
      - python
"""
    )

    config = load_config(config_path)

    assert config["paths"]["journal_dir"] == Path("~/custom/journal").expanduser()
    assert config["sources"]["rss_feeds"] == ["https://example.com/feed.xml"]
    assert config["sources"]["arxiv"]["enabled"] is True
    assert config["sources"]["arxiv"]["categories"] == ["cs.AI"]
    assert config["sources"]["reddit"]["subreddits"] == ["python"]
