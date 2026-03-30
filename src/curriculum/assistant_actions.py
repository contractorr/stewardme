"""Assistant-facing helpers for creating and proposing curriculum guides."""

from __future__ import annotations

import asyncio
import hashlib
import re
from difflib import SequenceMatcher
from typing import Any

from advisor.recommendation_storage import Recommendation
from curriculum.models import GuideDepth
from shared_types import RecommendationStatus
from storage_access import create_recommendation_storage
from storage_paths import get_user_paths
from web.user_store import log_event

_PROACTIVE_GUIDE_CONFIDENCE_MIN = 0.8
_GUIDE_CANDIDATE_DEDUP_DAYS = 90
_GUIDE_MATCH_MIN_SCORE = 0.72
_GUIDE_MATCH_STRONG_SCORE = 0.86
_NORMALIZE_RE = re.compile(r"[^a-z0-9]+")


def _normalize_text(value: str) -> str:
    return _NORMALIZE_RE.sub(" ", value.lower()).strip()


def _tokenize(value: str) -> set[str]:
    normalized = _normalize_text(value)
    return {part for part in normalized.split() if part}


def _text_similarity(left: str, right: str) -> float:
    left_norm = _normalize_text(left)
    right_norm = _normalize_text(right)
    if not left_norm or not right_norm:
        return 0.0
    if left_norm == right_norm:
        return 1.0
    if left_norm in right_norm or right_norm in left_norm:
        return 0.93

    left_tokens = _tokenize(left_norm)
    right_tokens = _tokenize(right_norm)
    token_score = 0.0
    if left_tokens and right_tokens:
        token_score = len(left_tokens & right_tokens) / len(left_tokens | right_tokens)

    return max(SequenceMatcher(None, left_norm, right_norm).ratio(), token_score)


def _candidate_hash(topic: str) -> str:
    digest = hashlib.sha256(_normalize_text(topic).encode("utf-8")).hexdigest()
    return f"learning-guide:{digest}"


def _guide_match_score(query: str, guide: dict[str, Any]) -> float:
    scores = [
        _text_similarity(query, str(guide.get("title") or "")),
        _text_similarity(query, str(guide.get("id") or "")),
    ]
    topic_prompt = (
        (guide.get("metadata") or {}) if isinstance(guide.get("metadata"), dict) else {}
    ).get("topic_prompt")
    if isinstance(topic_prompt, str):
        scores.append(_text_similarity(query, topic_prompt))
    return max(scores)


def find_matching_guides(
    store,
    query: str,
    *,
    limit: int = 5,
    min_score: float = _GUIDE_MATCH_MIN_SCORE,
) -> list[dict[str, Any]]:
    query = query.strip()
    if not query:
        return []

    matches: list[dict[str, Any]] = []
    for guide in store.list_guides():
        score = _guide_match_score(query, guide)
        if score < min_score:
            continue
        matches.append(
            {
                "id": guide["id"],
                "title": guide["title"],
                "category": guide.get("category", ""),
                "difficulty": guide.get("difficulty", ""),
                "origin": guide.get("origin", ""),
                "kind": guide.get("kind", ""),
                "score": round(score, 2),
            }
        )
    matches.sort(key=lambda item: (-item["score"], item["title"].lower(), item["id"]))
    return matches[:limit]


def _resolve_guide_for_extension(
    user_id: str, guide_id_or_title: str
) -> tuple[dict | None, list[dict]]:
    from web.routes import curriculum as curriculum_routes

    store = curriculum_routes._get_store(user_id)
    scanner = curriculum_routes._get_scanner(user_id, store)
    direct_id = curriculum_routes._resolve_guide_id(scanner, guide_id_or_title)
    direct = store.get_guide(direct_id, user_id=user_id)
    if direct:
        return direct, []

    exact_title_matches = [
        guide
        for guide in store.list_guides()
        if _normalize_text(guide_id_or_title) == _normalize_text(str(guide.get("title") or ""))
    ]
    if len(exact_title_matches) == 1:
        resolved = store.get_guide(exact_title_matches[0]["id"], user_id=user_id)
        return resolved, []

    matches = find_matching_guides(store, guide_id_or_title)
    if not matches:
        return None, []
    if len(matches) == 1 and matches[0]["score"] >= _GUIDE_MATCH_STRONG_SCORE:
        resolved = store.get_guide(matches[0]["id"], user_id=user_id)
        return resolved, matches
    return None, matches


def _find_existing_candidate(rec_storage, topic: str):
    candidate_hash = _candidate_hash(topic)
    for recommendation in rec_storage.list_recent(days=365, limit=200):
        if recommendation.embedding_hash != candidate_hash:
            continue
        if recommendation.status in {
            RecommendationStatus.DISMISSED.value,
            RecommendationStatus.COMPLETED.value,
        }:
            continue
        metadata = recommendation.metadata or {}
        if metadata.get("recommendation_kind") != "learning_guide_candidate":
            continue
        return recommendation
    return None


def _complete_matching_candidates(user_id: str, topic: str) -> None:
    rec_storage = create_recommendation_storage(get_user_paths(user_id))
    candidate_hash = _candidate_hash(topic)
    for recommendation in rec_storage.list_recent(days=365, limit=200):
        if recommendation.embedding_hash != candidate_hash:
            continue
        metadata = recommendation.metadata or {}
        if metadata.get("recommendation_kind") != "learning_guide_candidate":
            continue
        if recommendation.id:
            rec_storage.update_status(recommendation.id, RecommendationStatus.COMPLETED.value)


def generate_guide_for_user(
    user_id: str,
    *,
    topic: str,
    depth: GuideDepth,
    audience: str,
    time_budget: str,
    instruction: str | None = None,
    allow_similar: bool = False,
) -> dict[str, Any]:
    from web.deps import get_config
    from web.routes import curriculum as curriculum_routes

    topic = topic.strip()
    audience = audience.strip()
    time_budget = time_budget.strip()
    instruction = instruction.strip() if instruction else None

    config = get_config()
    if len(topic) > config.curriculum.user_guide_max_topic_length:
        return {
            "created": False,
            "reason": "topic_too_long",
            "maximum_length": config.curriculum.user_guide_max_topic_length,
        }

    store = curriculum_routes._get_store(user_id)
    matches = find_matching_guides(store, topic)
    if matches and not allow_similar:
        return {"created": False, "reason": "similar_guide_exists", "matches": matches}

    service = curriculum_routes._build_guide_generation_service(user_id)
    artifact = asyncio.run(
        service.generate_guide(
            topic=topic,
            depth=depth,
            audience=audience,
            time_budget=time_budget,
            instruction=instruction,
        )
    )

    scanner = curriculum_routes._get_scanner(user_id, store)
    curriculum_routes._sync_catalog(store, user_id=user_id, scanner=scanner)
    program_lookup = curriculum_routes._build_program_lookup(scanner.get_learning_programs())
    created_guide = store.get_guide(artifact["guide_id"], user_id=user_id)
    if not created_guide:
        return {"created": False, "reason": "guide_missing_after_sync"}

    _complete_matching_candidates(user_id, topic)
    log_event(
        "curriculum_user_guide_created",
        user_id,
        {"guide_id": artifact["guide_id"], "source": "advisor_tool"},
    )
    return {
        "created": True,
        "guide": curriculum_routes._decorate_guide_payload(
            created_guide,
            scanner,
            program_lookup,
            store=store,
            user_id=user_id,
        ),
        "matches": matches,
    }


def extend_guide_for_user(
    user_id: str,
    *,
    guide_id_or_title: str,
    prompt: str,
    depth: GuideDepth | None = None,
    audience: str | None = None,
    time_budget: str | None = None,
    instruction: str | None = None,
) -> dict[str, Any]:
    from web.routes import curriculum as curriculum_routes

    prompt = prompt.strip()
    audience = audience.strip() if audience else None
    time_budget = time_budget.strip() if time_budget else None
    instruction = instruction.strip() if instruction else None

    source_guide, matches = _resolve_guide_for_extension(user_id, guide_id_or_title.strip())
    if not source_guide:
        return {"created": False, "reason": "guide_not_resolved", "matches": matches}

    store = curriculum_routes._get_store(user_id)
    scanner = curriculum_routes._get_scanner(user_id, store)
    linked_extensions = store.list_linked_extensions(source_guide["id"], user_id=user_id)
    extension_matches = find_matching_guides(
        store,
        prompt,
        limit=5,
        min_score=_GUIDE_MATCH_STRONG_SCORE,
    )
    extension_ids = {extension["id"] for extension in linked_extensions}
    extension_matches = [match for match in extension_matches if match["id"] in extension_ids]
    if extension_matches:
        return {
            "created": False,
            "reason": "similar_extension_exists",
            "guide_id": source_guide["id"],
            "matches": extension_matches,
        }

    service = curriculum_routes._build_guide_generation_service(user_id)
    artifact = asyncio.run(
        service.extend_guide(
            source_guide=source_guide,
            prompt=prompt,
            depth=depth,
            audience=audience,
            time_budget=time_budget,
            instruction=instruction,
        )
    )

    curriculum_routes._sync_catalog(store, user_id=user_id, scanner=scanner)
    program_lookup = curriculum_routes._build_program_lookup(scanner.get_learning_programs())
    created_guide = store.get_guide(artifact["guide_id"], user_id=user_id)
    if not created_guide:
        return {"created": False, "reason": "guide_missing_after_sync"}

    log_event(
        "curriculum_user_guide_extended",
        user_id,
        {
            "guide_id": artifact["guide_id"],
            "base_guide_id": source_guide["id"],
            "source": "advisor_tool",
        },
    )
    return {
        "created": True,
        "guide": curriculum_routes._decorate_guide_payload(
            created_guide,
            scanner,
            program_lookup,
            store=store,
            user_id=user_id,
        ),
        "source_guide": {"id": source_guide["id"], "title": source_guide["title"]},
    }


def suggest_guide_for_user(
    user_id: str,
    *,
    topic: str,
    rationale: str,
    confidence: float,
    depth: GuideDepth = GuideDepth.PRACTITIONER,
    audience: str = "A learner with the user's current goals and context",
    time_budget: str = "2-4 focused sessions",
    instruction: str | None = None,
) -> dict[str, Any]:
    topic = topic.strip()
    rationale = rationale.strip()
    audience = audience.strip()
    time_budget = time_budget.strip()
    instruction = instruction.strip() if instruction else None

    if confidence < _PROACTIVE_GUIDE_CONFIDENCE_MIN:
        return {
            "created": False,
            "reason": "confidence_too_low",
            "minimum_confidence": _PROACTIVE_GUIDE_CONFIDENCE_MIN,
        }

    from web.routes import curriculum as curriculum_routes

    store = curriculum_routes._get_store(user_id)
    matches = find_matching_guides(store, topic, min_score=_GUIDE_MATCH_STRONG_SCORE)
    if matches:
        return {"created": False, "reason": "similar_guide_exists", "matches": matches}

    rec_storage = create_recommendation_storage(get_user_paths(user_id))
    existing = _find_existing_candidate(rec_storage, topic)
    if existing:
        return {
            "created": False,
            "reason": "candidate_exists",
            "candidate": {
                "id": existing.id,
                "title": existing.title,
                "score": existing.score,
                "status": existing.status,
            },
        }

    recommendation = Recommendation(
        category="learning",
        title=topic,
        description=rationale,
        rationale=rationale,
        score=round(max(8.0, min(10.0, confidence * 10)), 2),
        status=RecommendationStatus.SUGGESTED.value,
        metadata={
            "recommendation_kind": "learning_guide_candidate",
            "topic": topic,
            "depth": depth.value,
            "audience": audience,
            "time_budget": time_budget,
            "instruction": instruction,
            "confidence": confidence,
            "rationale": rationale,
            "approval_required": True,
            "dedup_days": _GUIDE_CANDIDATE_DEDUP_DAYS,
        },
        embedding_hash=_candidate_hash(topic),
    )
    recommendation_id = rec_storage.save(recommendation)
    log_event(
        "curriculum_guide_candidate_created",
        user_id,
        {"recommendation_id": recommendation_id, "topic": topic, "confidence": confidence},
    )
    return {
        "created": True,
        "recommendation_id": recommendation_id,
        "title": topic,
        "score": recommendation.score,
        "confidence": confidence,
        "approval_required": True,
    }
