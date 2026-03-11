"""Derived mind-map artifacts for journal entries."""

from __future__ import annotations

import hashlib
import json
import re
import sqlite3
import uuid
from collections import Counter
from datetime import datetime
from pathlib import Path

import structlog

from db import wal_connect

logger = structlog.get_logger()

_WHITESPACE_RE = re.compile(r"\s+")
_PUNCT_RE = re.compile(r"[^\w\s-]")
_LEADING_USER_RE = re.compile(
    r"^user\s+(?:is|has|needs|wants|prefers|feels|can|cannot|can't|should|plans?\s+to)\s+",
    re.IGNORECASE,
)
_TRAILING_CLAUSE_RE = re.compile(r"\s+(?:because|which|that|while|but|and)\s+.*$", re.IGNORECASE)

_ACTION_PATTERNS = (
    re.compile(
        r"\b(?:need to|want to|plan to|focus on|should|must|next step(?: is)? to)\s+([^.!\n]+)",
        re.IGNORECASE,
    ),
    re.compile(r"\b(?:going to|trying to|aim to)\s+([^.!\n]+)", re.IGNORECASE),
)
_THEME_PATTERNS = (
    re.compile(
        r"\b(?:working on|thinking about|struggling with|blocked by|worried about|excited about|learning about)\s+([^.!\n]+)",
        re.IGNORECASE,
    ),
    re.compile(r"\b(?:this is about|the main theme is)\s+([^.!\n]+)", re.IGNORECASE),
)

_STOPWORDS = {
    "about",
    "after",
    "also",
    "been",
    "being",
    "from",
    "have",
    "into",
    "just",
    "more",
    "need",
    "next",
    "plan",
    "really",
    "should",
    "that",
    "them",
    "then",
    "they",
    "this",
    "want",
    "with",
    "work",
}

_ROLE_LABELS = {
    "theme": "highlights",
    "action": "points to",
    "memory": "reinforces",
    "thread": "recurs as",
    "research": "expanded by",
    "intel": "echoed by",
    "conversation": "discussed in",
    "tag": "tagged",
}


def _now() -> str:
    return datetime.now().isoformat()


def _normalize_text(value: str) -> str:
    return _WHITESPACE_RE.sub(" ", value.strip())


def _trim_phrase(value: str, *, limit: int = 56) -> str:
    cleaned = _normalize_text(value)
    cleaned = cleaned.strip("-:;,.'\" ")
    cleaned = _TRAILING_CLAUSE_RE.sub("", cleaned)
    cleaned = cleaned[:limit].strip("-:;,.'\" ")
    return cleaned


def _normalize_key(value: str) -> str:
    lowered = _trim_phrase(value).lower()
    return _PUNCT_RE.sub("", lowered)


def _tokenize(value: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9]+", value.lower())
        if len(token) >= 4 and token not in _STOPWORDS
    }


def _safe_float(value, default: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _pluralize(count: int, singular: str, plural: str | None = None) -> str:
    if count == 1:
        return singular
    return plural or f"{singular}s"


class JournalMindMapStore:
    """SQLite-backed cache for per-entry journal mind maps."""

    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path).expanduser()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self) -> None:
        with wal_connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS journal_mind_maps (
                    map_id TEXT PRIMARY KEY,
                    entry_path TEXT NOT NULL UNIQUE,
                    entry_title TEXT NOT NULL,
                    source_hash TEXT NOT NULL,
                    summary TEXT NOT NULL DEFAULT '',
                    rationale TEXT NOT NULL DEFAULT '',
                    generator TEXT NOT NULL DEFAULT 'derived',
                    payload_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_journal_mind_maps_entry_path ON journal_mind_maps(entry_path)"
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_journal_mind_maps_updated_at ON journal_mind_maps(updated_at DESC)"
            )

    def upsert(self, artifact: dict) -> str:
        created_at = artifact.get("created_at") or _now()
        updated_at = _now()
        map_id = artifact.get("map_id") or uuid.uuid4().hex[:16]
        entry_path = str(artifact["entry_path"])
        payload = {
            "nodes": artifact.get("nodes") or [],
            "edges": artifact.get("edges") or [],
        }

        with wal_connect(self.db_path) as conn:
            existing = conn.execute(
                "SELECT map_id, created_at FROM journal_mind_maps WHERE entry_path = ?",
                (entry_path,),
            ).fetchone()
            if existing:
                map_id = existing[0]
                created_at = existing[1]

            conn.execute(
                """
                INSERT INTO journal_mind_maps (
                    map_id, entry_path, entry_title, source_hash, summary, rationale,
                    generator, payload_json, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(entry_path) DO UPDATE SET
                    entry_title = excluded.entry_title,
                    source_hash = excluded.source_hash,
                    summary = excluded.summary,
                    rationale = excluded.rationale,
                    generator = excluded.generator,
                    payload_json = excluded.payload_json,
                    updated_at = excluded.updated_at
                """,
                (
                    map_id,
                    entry_path,
                    str(artifact.get("entry_title") or Path(entry_path).stem),
                    str(artifact.get("source_hash") or ""),
                    str(artifact.get("summary") or ""),
                    str(artifact.get("rationale") or ""),
                    str(artifact.get("generator") or "derived"),
                    json.dumps(payload),
                    created_at,
                    updated_at,
                ),
            )
        return map_id

    def get_by_entry(self, entry_path: str) -> dict | None:
        with wal_connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                "SELECT * FROM journal_mind_maps WHERE entry_path = ?",
                (str(entry_path),),
            ).fetchone()
        if not row:
            return None
        try:
            payload = json.loads(row["payload_json"] or "{}")
        except json.JSONDecodeError:
            logger.warning("journal.mind_map_malformed", entry_path=entry_path)
            return None
        return {
            "map_id": row["map_id"],
            "entry_path": row["entry_path"],
            "entry_title": row["entry_title"],
            "source_hash": row["source_hash"],
            "summary": row["summary"],
            "rationale": row["rationale"],
            "generator": row["generator"],
            "nodes": payload.get("nodes") or [],
            "edges": payload.get("edges") or [],
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
        }

    def delete_by_entry(self, entry_path: str) -> bool:
        with wal_connect(self.db_path) as conn:
            result = conn.execute(
                "DELETE FROM journal_mind_maps WHERE entry_path = ?",
                (str(entry_path),),
            )
        return bool(result.rowcount)


class JournalMindMapGenerator:
    """Build small, user-readable concept graphs from journal entries."""

    def __init__(
        self,
        store: JournalMindMapStore,
        *,
        journal_storage=None,
        intel_storage=None,
        user_id: str | None = None,
        users_db_path: str | Path | None = None,
        max_total_nodes: int = 10,
        min_non_root_nodes: int = 2,
        max_external_nodes: int = 4,
    ):
        self.store = store
        self.journal_storage = journal_storage
        self.intel_storage = intel_storage
        self.user_id = user_id
        self.users_db_path = Path(users_db_path).expanduser() if users_db_path else None
        self.max_total_nodes = max_total_nodes
        self.min_non_root_nodes = min_non_root_nodes
        self.max_external_nodes = max_external_nodes

    def generate_for_entry(
        self,
        entry: dict,
        *,
        receipt: dict | None = None,
        force: bool = False,
    ) -> dict | None:
        entry_path = str(entry["path"])
        existing = self.store.get_by_entry(entry_path)
        external_context, external_context_degraded = self._collect_external_context(entry)
        if existing and external_context_degraded and not force:
            return self.public_artifact(existing)

        source_hash = self._build_source_hash(entry, receipt, external_context)
        if existing and existing.get("source_hash") == source_hash and not force:
            return self.public_artifact(existing)

        artifact = self._build_artifact(entry, receipt, external_context, source_hash)
        if not artifact:
            if force:
                self.store.delete_by_entry(entry_path)
            return None

        self.store.upsert(artifact)
        stored = self.store.get_by_entry(entry_path)
        return self.public_artifact(stored or artifact)

    @staticmethod
    def public_artifact(artifact: dict | None) -> dict | None:
        if not artifact:
            return None
        public = dict(artifact)
        public.pop("source_hash", None)
        return public

    def _build_source_hash(
        self, entry: dict, receipt: dict | None, external_context: dict | None
    ) -> str:
        payload = {
            "title": entry.get("title") or "",
            "content": entry.get("content") or "",
            "tags": entry.get("tags") or [],
            "created": entry.get("created") or "",
            "receipt": {
                "thread_label": (receipt or {}).get("thread_label"),
                "updated_at": (receipt or {}).get("updated_at"),
                "themes": ((receipt or {}).get("payload") or {}).get("themes") or [],
                "memory_facts": ((receipt or {}).get("payload") or {}).get("memory_facts") or [],
                "goal_candidates": ((receipt or {}).get("payload") or {}).get("goal_candidates")
                or [],
            },
            "external": (external_context or {}).get("signature") or {},
        }
        encoded = json.dumps(payload, sort_keys=True).encode("utf-8")
        return hashlib.sha1(encoded).hexdigest()

    def _build_artifact(
        self,
        entry: dict,
        receipt: dict | None,
        external_context: dict | None,
        source_hash: str,
    ) -> dict | None:
        title = _trim_phrase(str(entry.get("title") or "")) or "Journal entry"
        content = str(entry.get("content") or "")
        tags = [str(tag).strip() for tag in (entry.get("tags") or []) if str(tag).strip()]
        receipt_payload = ((receipt or {}).get("payload") or {}) if receipt else {}
        external_context = external_context or {}

        root = {
            "id": "root",
            "label": title,
            "kind": "entry",
            "weight": 1.0,
            "confidence": 1.0,
            "is_root": True,
            "source_type": None,
            "source_label": "",
            "source_ref": "",
        }

        candidates: list[dict] = []
        sources_used: list[str] = []

        for theme in receipt_payload.get("themes") or []:
            label = _trim_phrase(str(theme.get("label") or ""))
            if label:
                candidates.append(
                    {
                        "label": label,
                        "kind": "theme",
                        "weight": min(1.0, _safe_float(theme.get("confidence"), 0.78)),
                        "confidence": min(1.0, _safe_float(theme.get("confidence"), 0.78)),
                    }
                )
        if receipt_payload.get("themes"):
            sources_used.append("themes")

        for goal in receipt_payload.get("goal_candidates") or []:
            label = _trim_phrase(str(goal.get("title") or ""))
            if label:
                candidates.append(
                    {
                        "label": label,
                        "kind": "action",
                        "weight": min(1.0, _safe_float(goal.get("confidence"), 0.76)),
                        "confidence": min(1.0, _safe_float(goal.get("confidence"), 0.76)),
                    }
                )
        if receipt_payload.get("goal_candidates"):
            sources_used.append("goal candidates")

        for fact in receipt_payload.get("memory_facts") or []:
            label = self._condense_memory_fact(str(fact.get("text") or ""))
            if label:
                candidates.append(
                    {
                        "label": label,
                        "kind": "memory",
                        "weight": min(1.0, _safe_float(fact.get("confidence"), 0.72)),
                        "confidence": min(1.0, _safe_float(fact.get("confidence"), 0.72)),
                    }
                )
        if receipt_payload.get("memory_facts"):
            sources_used.append("memory facts")

        thread_label = _trim_phrase(str((receipt or {}).get("thread_label") or ""))
        if thread_label and _normalize_key(thread_label) != _normalize_key(title):
            candidates.append(
                {
                    "label": thread_label,
                    "kind": "thread",
                    "weight": 0.78,
                    "confidence": 0.78,
                }
            )
            sources_used.append("thread match")

        for tag in tags[:2]:
            label = _trim_phrase(tag)
            if label:
                candidates.append(
                    {
                        "label": label,
                        "kind": "tag",
                        "weight": 0.62,
                        "confidence": 1.0,
                    }
                )
        if tags:
            sources_used.append("tags")

        extracted = self._extract_content_candidates(content)
        if extracted:
            candidates.extend(extracted)
            sources_used.append("entry language")

        external_candidates = []
        for family, label in (
            ("research", "research"),
            ("intel", "RSS intel"),
            ("conversations", "advisor conversations"),
        ):
            items = external_context.get(family) or []
            if items:
                external_candidates.extend(items)
                sources_used.append(label)

        candidates.extend(external_candidates[: self.max_external_nodes])

        selected_nodes = self._select_nodes(root, candidates)
        non_root_nodes = [node for node in selected_nodes if not node.get("is_root")]
        if len(non_root_nodes) < self.min_non_root_nodes:
            return None

        edges = self._build_edges(selected_nodes)
        summary = self._build_summary(non_root_nodes)
        rationale = self._build_rationale(sources_used)

        return {
            "entry_path": str(entry["path"]),
            "entry_title": title,
            "source_hash": source_hash,
            "summary": summary,
            "rationale": rationale,
            "generator": "derived",
            "nodes": selected_nodes,
            "edges": edges,
        }

    def _select_nodes(self, root: dict, candidates: list[dict]) -> list[dict]:
        deduped: dict[str, dict] = {}
        for candidate in candidates:
            label = _trim_phrase(str(candidate.get("label") or ""))
            key = _normalize_key(label)
            if not label or not key or key == _normalize_key(root["label"]):
                continue
            existing = deduped.get(key)
            if existing and existing.get("weight", 0.0) >= candidate.get("weight", 0.0):
                continue
            deduped[key] = {
                "id": f"{candidate.get('kind', 'theme')}-{hashlib.sha1(key.encode('utf-8')).hexdigest()[:8]}",
                "label": label,
                "kind": candidate.get("kind") or "theme",
                "weight": min(1.0, _safe_float(candidate.get("weight"), 0.7)),
                "confidence": min(1.0, _safe_float(candidate.get("confidence"), 0.7)),
                "is_root": False,
                "source_type": candidate.get("source_type"),
                "source_label": candidate.get("source_label") or "",
                "source_ref": candidate.get("source_ref") or "",
            }

        nodes = sorted(
            deduped.values(),
            key=lambda item: (item.get("weight", 0.0), item.get("confidence", 0.0)),
            reverse=True,
        )
        return [root, *nodes[: max(0, self.max_total_nodes - 1)]]

    def _extract_content_candidates(self, content: str) -> list[dict]:
        text = content[:2500]
        extracted: list[dict] = []
        for pattern in _ACTION_PATTERNS:
            for match in pattern.finditer(text):
                phrase = _trim_phrase(match.group(1))
                if len(_tokenize(phrase)) >= 1:
                    extracted.append(
                        {
                            "label": phrase,
                            "kind": "action",
                            "weight": 0.68,
                            "confidence": 0.63,
                        }
                    )
        for pattern in _THEME_PATTERNS:
            for match in pattern.finditer(text):
                phrase = _trim_phrase(match.group(1))
                if len(_tokenize(phrase)) >= 1:
                    extracted.append(
                        {
                            "label": phrase,
                            "kind": "theme",
                            "weight": 0.66,
                            "confidence": 0.61,
                        }
                    )
        return extracted

    def _build_edges(self, nodes: list[dict]) -> list[dict]:
        if not nodes:
            return []

        root = nodes[0]
        edges: list[dict] = []
        for node in nodes[1:]:
            edges.append(
                {
                    "source": root["id"],
                    "target": node["id"],
                    "label": _ROLE_LABELS.get(node["kind"], "connects"),
                    "strength": round(max(0.5, _safe_float(node.get("weight"), 0.7)), 2),
                }
            )

        themes = [node for node in nodes if node.get("kind") == "theme"]
        actions = [node for node in nodes if node.get("kind") == "action"]
        memories = [node for node in nodes if node.get("kind") == "memory"]
        threads = [node for node in nodes if node.get("kind") == "thread"]
        research = [node for node in nodes if node.get("kind") == "research"]
        intel = [node for node in nodes if node.get("kind") == "intel"]
        conversations = [node for node in nodes if node.get("kind") == "conversation"]

        for edge in self._secondary_edges(actions, themes, "advances"):
            edges.append(edge)
        for edge in self._secondary_edges(memories, themes, "explains"):
            edges.append(edge)
        for edge in self._secondary_edges(threads, themes, "echoes"):
            edges.append(edge)
        for edge in self._secondary_edges(research, themes, "supports"):
            edges.append(edge)
        for edge in self._secondary_edges(intel, themes, "signals"):
            edges.append(edge)
        for edge in self._secondary_edges(conversations, themes, "revisits"):
            edges.append(edge)

        return edges[: max(0, (self.max_total_nodes * 2) - 2)]

    def _secondary_edges(
        self,
        sources: list[dict],
        targets: list[dict],
        label: str,
    ) -> list[dict]:
        secondary: list[dict] = []
        for source in sources:
            source_tokens = _tokenize(source["label"])
            for target in targets:
                overlap = source_tokens & _tokenize(target["label"])
                if not overlap:
                    continue
                secondary.append(
                    {
                        "source": source["id"],
                        "target": target["id"],
                        "label": label,
                        "strength": round(
                            min(
                                0.88,
                                max(
                                    0.55,
                                    (
                                        _safe_float(source.get("weight"), 0.7)
                                        + _safe_float(target.get("weight"), 0.7)
                                    )
                                    / 2,
                                ),
                            ),
                            2,
                        ),
                    }
                )
        return secondary[:2]

    def _build_summary(self, non_root_nodes: list[dict]) -> str:
        counts = Counter(node.get("kind") for node in non_root_nodes)
        parts = []
        for kind, label in (
            ("theme", "theme"),
            ("action", "next step"),
            ("memory", "lasting signal"),
            ("thread", "recurring thread"),
            ("research", "research link"),
            ("intel", "RSS signal"),
            ("conversation", "conversation link"),
            ("tag", "tag"),
        ):
            count = counts.get(kind, 0)
            if count:
                parts.append(f"{count} {_pluralize(count, label)}")

        if not parts:
            return "This map highlights the strongest signals in this entry."
        if len(parts) == 1:
            return f"This map surfaces {parts[0]} from this entry."
        return f"This map surfaces {', '.join(parts[:-1])}, and {parts[-1]} from this entry."

    def _build_rationale(self, sources_used: list[str]) -> str:
        ordered = []
        for source in sources_used:
            if source not in ordered:
                ordered.append(source)
        if not ordered:
            return "Built from the journal entry text."
        if len(ordered) == 1:
            return f"Built from {ordered[0]}."
        return f"Built from {', '.join(ordered[:-1])}, and {ordered[-1]}."

    def _condense_memory_fact(self, text: str) -> str:
        cleaned = _normalize_text(text)
        cleaned = _LEADING_USER_RE.sub("", cleaned)
        cleaned = _trim_phrase(cleaned)
        if not cleaned:
            return ""
        return cleaned[0].upper() + cleaned[1:] if len(cleaned) > 1 else cleaned.upper()

    def _collect_external_context(self, entry: dict) -> tuple[dict, bool]:
        collected: dict[str, list[dict]] = {
            "research": [],
            "intel": [],
            "conversations": [],
        }
        degraded = False
        for key, collector in (
            ("research", self._collect_research_candidates),
            ("intel", self._collect_rss_candidates),
            ("conversations", self._collect_conversation_candidates),
        ):
            try:
                collected[key] = collector(entry)
            except Exception as exc:
                degraded = True
                logger.warning(
                    "journal.mind_map_external_context_failed",
                    entry_path=str(entry.get("path") or ""),
                    source=key,
                    error=str(exc),
                )
                collected[key] = []

        context = {
            "research": collected["research"],
            "intel": collected["intel"],
            "conversations": collected["conversations"],
            "signature": {
                "research": [
                    {
                        "label": item.get("label"),
                        "source_ref": item.get("source_ref"),
                        "source_label": item.get("source_label"),
                    }
                    for item in collected["research"]
                ],
                "intel": [
                    {
                        "label": item.get("label"),
                        "source_ref": item.get("source_ref"),
                        "source_label": item.get("source_label"),
                    }
                    for item in collected["intel"]
                ],
                "conversations": [
                    {
                        "label": item.get("label"),
                        "source_ref": item.get("source_ref"),
                        "source_label": item.get("source_label"),
                    }
                    for item in collected["conversations"]
                ],
            },
        }
        return context, degraded

    def _collect_research_candidates(self, entry: dict) -> list[dict]:
        if not self.journal_storage:
            return []

        entry_terms = self._entry_terms(entry)
        candidates: list[tuple[float, dict]] = []
        for research_entry in self.journal_storage.list_entries(entry_type="research", limit=25):
            if str(research_entry.get("path")) == str(entry.get("path")):
                continue
            title = str(research_entry.get("title") or "")
            text = " ".join(
                [
                    title,
                    str(research_entry.get("preview") or ""),
                    " ".join(research_entry.get("tags") or []),
                ]
            )
            score = self._overlap_score(entry_terms, text)
            if score < 0.12:
                continue
            label = _trim_phrase(
                title.replace("Research Update:", "").replace("Research:", "").strip(),
                limit=48,
            )
            if not label:
                continue
            candidates.append(
                (
                    score,
                    {
                        "label": label,
                        "kind": "research",
                        "weight": min(0.72, 0.56 + score),
                        "confidence": min(0.78, 0.58 + score),
                        "source_type": "research",
                        "source_label": title,
                        "source_ref": str(research_entry.get("path") or ""),
                    },
                )
            )

        candidates.sort(key=lambda item: item[0], reverse=True)
        return [candidate for _, candidate in candidates[:2]]

    def _collect_rss_candidates(self, entry: dict) -> list[dict]:
        if not self.intel_storage:
            return []

        entry_terms = self._entry_terms(entry)
        candidates: list[tuple[float, dict]] = []
        for item in self.intel_storage.get_recent(days=21, limit=120):
            source = str(item.get("source") or "").lower()
            if not source.startswith("rss:"):
                continue
            text = " ".join(
                [
                    str(item.get("title") or ""),
                    str(item.get("summary") or ""),
                    " ".join(item.get("tags") or []),
                ]
            )
            score = self._overlap_score(entry_terms, text)
            if score < 0.16:
                continue
            label = _trim_phrase(str(item.get("title") or ""), limit=48)
            if not label:
                continue
            candidates.append(
                (
                    score,
                    {
                        "label": label,
                        "kind": "intel",
                        "weight": min(0.68, 0.5 + score),
                        "confidence": min(0.74, 0.54 + score),
                        "source_type": "rss",
                        "source_label": str(item.get("source") or ""),
                        "source_ref": str(item.get("url") or ""),
                    },
                )
            )

        candidates.sort(key=lambda item: item[0], reverse=True)
        return [candidate for _, candidate in candidates[:2]]

    def _collect_conversation_candidates(self, entry: dict) -> list[dict]:
        if not self.user_id or not self.users_db_path:
            return []

        try:
            from web.conversation_store import get_conversation, list_conversations
        except Exception:
            return []

        entry_terms = self._entry_terms(entry)
        candidates: list[tuple[float, dict]] = []
        for conversation in list_conversations(
            self.user_id,
            limit=8,
            db_path=self.users_db_path,
        ):
            detail = get_conversation(conversation["id"], self.user_id, db_path=self.users_db_path)
            if not detail:
                continue
            for message in reversed(detail.get("messages") or []):
                if str(message.get("role") or "") != "user":
                    continue
                excerpt = _trim_phrase(str(message.get("content") or ""), limit=56)
                if not excerpt:
                    continue
                score = self._overlap_score(entry_terms, excerpt)
                if score < 0.12:
                    continue
                candidates.append(
                    (
                        score,
                        {
                            "label": excerpt,
                            "kind": "conversation",
                            "weight": min(0.64, 0.48 + score),
                            "confidence": min(0.72, 0.52 + score),
                            "source_type": "conversation",
                            "source_label": str(conversation.get("title") or "Conversation"),
                            "source_ref": str(conversation.get("id") or ""),
                        },
                    )
                )
                break

        candidates.sort(key=lambda item: item[0], reverse=True)
        deduped: list[dict] = []
        seen_refs: set[str] = set()
        for _, candidate in candidates:
            ref = candidate.get("source_ref") or ""
            if ref in seen_refs:
                continue
            seen_refs.add(ref)
            deduped.append(candidate)
            if len(deduped) >= 2:
                break
        return deduped

    def _entry_terms(self, entry: dict) -> set[str]:
        text = " ".join(
            [
                str(entry.get("title") or ""),
                " ".join(entry.get("tags") or []),
                str(entry.get("content") or "")[:1600],
            ]
        )
        return _tokenize(text)

    @staticmethod
    def _overlap_score(entry_terms: set[str], text: str) -> float:
        target_terms = _tokenize(text)
        if not entry_terms or not target_terms:
            return 0.0
        overlap = entry_terms & target_terms
        if not overlap:
            return 0.0
        return min(1.0, len(overlap) / max(3, min(len(entry_terms), len(target_terms))))
