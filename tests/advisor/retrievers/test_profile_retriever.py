"""Tests for ProfileRetriever."""

import time
from unittest.mock import MagicMock, patch

from advisor.retrievers.profile import ProfileRetriever


class TestProfileRetriever:
    def test_load_missing_file(self):
        pr = ProfileRetriever("/nonexistent/profile.yaml")
        assert pr.load() is None

    def test_load_caches_by_mtime(self, tmp_path):
        f = tmp_path / "profile.yaml"
        f.write_text("name: test")
        pr = ProfileRetriever(str(f))

        profile = MagicMock()
        ps = MagicMock()
        ps.load.return_value = profile

        with patch("profile.storage.ProfileStorage", return_value=ps):
            pr.load()
            pr.load()

        ps.load.assert_called_once()

    def test_load_reloads_on_mtime_change(self, tmp_path):
        import os

        f = tmp_path / "profile.yaml"
        f.write_text("v1")
        pr = ProfileRetriever(str(f))

        profile = MagicMock()
        ps = MagicMock()
        ps.load.return_value = profile

        with patch("profile.storage.ProfileStorage", return_value=ps):
            pr.load()
            time.sleep(0.05)
            f.write_text("v2")
            os.utime(f, None)
            pr.load()

        assert ps.load.call_count == 2

    def test_get_profile_context_structured(self, tmp_path):
        f = tmp_path / "profile.yaml"
        f.write_text("name: test")
        pr = ProfileRetriever(str(f))

        profile = MagicMock()
        profile.structured_summary.return_value = "STRUCTURED"
        ps = MagicMock()
        ps.load.return_value = profile

        with patch("profile.storage.ProfileStorage", return_value=ps):
            result = pr.get_profile_context(structured=True)
        assert "STRUCTURED" in result

    def test_get_profile_context_compact(self, tmp_path):
        f = tmp_path / "profile.yaml"
        f.write_text("name: test")
        pr = ProfileRetriever(str(f))

        profile = MagicMock()
        profile.summary.return_value = "compact"
        ps = MagicMock()
        ps.load.return_value = profile

        with patch("profile.storage.ProfileStorage", return_value=ps):
            result = pr.get_profile_context(structured=False)
        assert "USER PROFILE" in result
        assert "compact" in result

    def test_get_profile_context_no_profile(self):
        pr = ProfileRetriever("/nonexistent/profile.yaml")
        assert pr.get_profile_context() == ""

    def test_get_profile_keywords_populated(self, tmp_path):
        f = tmp_path / "profile.yaml"
        f.write_text("name: test")
        pr = ProfileRetriever(str(f))

        skill = MagicMock()
        skill.name = "Python"
        profile = MagicMock()
        profile.skills = [skill]
        profile.languages_frameworks = ["FastAPI"]
        profile.technologies_watching = []
        profile.industries_watching = []
        profile.interests = []
        profile.active_projects = []
        ps = MagicMock()
        ps.load.return_value = profile

        with patch("profile.storage.ProfileStorage", return_value=ps):
            kw = pr.get_profile_keywords()
        assert "python" in kw
        assert "fastapi" in kw

    def test_get_profile_keywords_no_profile(self):
        pr = ProfileRetriever("/nonexistent/profile.yaml")
        assert pr.get_profile_keywords() == []

    def test_load_profile_terms(self, tmp_path):
        f = tmp_path / "profile.yaml"
        f.write_text("name: test")
        pr = ProfileRetriever(str(f))

        ps = MagicMock()
        ps.load.return_value = None
        with patch("profile.storage.ProfileStorage", return_value=ps):
            terms = pr.load_profile_terms()
        assert terms.is_empty
