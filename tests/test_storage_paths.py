"""Tests for canonical user path resolution."""

import pytest

from storage_paths import get_single_user_paths, get_user_paths, safe_user_id


def test_get_user_paths_returns_canonical_user_and_shared_paths(tmp_path):
    paths = get_user_paths("google:123", coach_home=tmp_path)

    user_dir = tmp_path / "users" / "google_123"
    assert paths["data_dir"] == user_dir
    assert paths["journal_dir"] == user_dir / "journal"
    assert paths["journal_dir"].exists()
    assert paths["profile"] == user_dir / "profile.yaml"
    assert paths["profile_path"] == user_dir / "profile.yaml"
    assert paths["memory_db"] == user_dir / "memory.db"
    assert paths["threads_db"] == user_dir / "threads.db"
    assert paths["mind_maps_db"] == user_dir / "mind_maps.db"
    assert paths["watchlist_path"] == user_dir / "watchlist.json"
    assert paths["follow_up_path"] == user_dir / "intel_follow_ups.json"
    assert paths["intel_follow_ups_path"] == user_dir / "intel_follow_ups.json"
    assert paths["intel_db"] == tmp_path / "intel.db"


def test_get_single_user_paths_returns_rooted_local_paths(tmp_path):
    profile_path = tmp_path / "custom" / "profile.yaml"
    paths = get_single_user_paths(coach_home=tmp_path, profile_path=profile_path)

    assert paths["data_dir"] == tmp_path
    assert paths["journal_dir"] == tmp_path / "journal"
    assert paths["journal_dir"].exists()
    assert paths["profile"] == profile_path
    assert paths["profile_path"] == profile_path
    assert paths["memory_db"] == tmp_path / "memory.db"
    assert paths["threads_db"] == tmp_path / "threads.db"
    assert paths["mind_maps_db"] == tmp_path / "mind_maps.db"
    assert paths["watchlist_path"] == tmp_path / "watchlist.json"
    assert paths["follow_up_path"] == tmp_path / "intel_follow_ups.json"
    assert paths["intel_db"] == tmp_path / "intel.db"


@pytest.mark.parametrize(
    "user_id",
    ["12345", "github:12345", "google-oauth2:987"],
)
def test_safe_user_id_matches_legacy_mapping_for_deployed_id_formats(user_id):
    # Existing user directories were created under the old `:` -> `_` mapping;
    # the allowlist must keep mapping deployed OAuth sub formats identically.
    assert safe_user_id(user_id) == user_id.replace(":", "_")


@pytest.mark.parametrize(
    "user_id",
    ["/etc/passwd", "a/../../b", "a\x00b", "github:../../victim"],
)
def test_safe_user_id_neutralizes_path_characters(user_id, tmp_path):
    sanitized = safe_user_id(user_id)
    assert "/" not in sanitized
    assert "\\" not in sanitized
    assert "\x00" not in sanitized
    assert "." not in sanitized

    users_root = (tmp_path / "users").resolve()
    data_dir = get_user_paths(user_id, coach_home=tmp_path)["data_dir"].resolve()
    assert data_dir.is_relative_to(users_root)
    assert data_dir != users_root


@pytest.mark.parametrize("user_id", ["", "../", "..\\", "..", "___", ":::"])
def test_safe_user_id_rejects_empty_or_punctuation_only_ids(user_id):
    with pytest.raises(ValueError):
        safe_user_id(user_id)
