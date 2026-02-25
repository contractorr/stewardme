"""Capability horizon model — aggregates scraper data into structured AI capability estimates."""

import json
from datetime import datetime
from pathlib import Path
from typing import Literal

import structlog
from pydantic import BaseModel, Field, ValidationError

from db import wal_connect
from intelligence.scraper import IntelItem
from llm.factory import create_cheap_provider

logger = structlog.get_logger().bind(source="capability_model")

CAPABILITY_DOMAINS = [
    "software_engineering",
    "data_analysis",
    "creative_writing",
    "scientific_research",
    "legal_reasoning",
    "medical_diagnosis",
    "customer_service",
    "physical_world_interaction",
    "long_horizon_planning",
    "multimodal_understanding",
]

# Static fallback data from ai_capabilities_kb, mapped to CAPABILITY_DOMAINS
_STATIC_FALLBACK: dict[str, dict] = {
    "software_engineering": {
        "current_level": 0.7,
        "months_to_next_threshold": 6,
        "confidence": "high",
        "key_signals": [
            "SWE-bench ~70% solve rate",
            "Agentic coding tools maturing",
            "Multi-file edits reliable",
        ],
    },
    "data_analysis": {
        "current_level": 0.65,
        "months_to_next_threshold": 8,
        "confidence": "medium",
        "key_signals": [
            "Strong at SQL and pandas",
            "Visualization generation improving",
            "Statistical reasoning moderate",
        ],
    },
    "creative_writing": {
        "current_level": 0.6,
        "months_to_next_threshold": 12,
        "confidence": "medium",
        "key_signals": [
            "Marketing copy near-commercial",
            "Long-form coherence limited",
            "Style control improving",
        ],
    },
    "scientific_research": {
        "current_level": 0.4,
        "months_to_next_threshold": 18,
        "confidence": "medium",
        "key_signals": [
            "GPQA Diamond ~70%",
            "FrontierMath <5%",
            "Lit review strong, novelty weak",
        ],
    },
    "legal_reasoning": {
        "current_level": 0.55,
        "months_to_next_threshold": 12,
        "confidence": "medium",
        "key_signals": [
            "Bar exam pass rates improving",
            "Contract review accuracy high",
            "Nuanced case law analysis limited",
        ],
    },
    "medical_diagnosis": {
        "current_level": 0.45,
        "months_to_next_threshold": 18,
        "confidence": "low",
        "key_signals": [
            "USMLE-level questions strong",
            "Diagnosis from symptoms moderate",
            "No physical exam capability",
        ],
    },
    "customer_service": {
        "current_level": 0.75,
        "months_to_next_threshold": 4,
        "confidence": "high",
        "key_signals": [
            "Chatbot deployment widespread",
            "Multi-turn resolution good",
            "Escalation judgment improving",
        ],
    },
    "physical_world_interaction": {
        "current_level": 0.15,
        "months_to_next_threshold": 36,
        "confidence": "low",
        "key_signals": [
            "Robotics integration early",
            "Spatial reasoning weak",
            "Sim-to-real gap large",
        ],
    },
    "long_horizon_planning": {
        "current_level": 0.35,
        "months_to_next_threshold": 12,
        "confidence": "medium",
        "key_signals": [
            "METR ~4hr task horizon",
            "WebArena ~35%",
            "Error recovery poor in novel situations",
        ],
    },
    "multimodal_understanding": {
        "current_level": 0.6,
        "months_to_next_threshold": 8,
        "confidence": "medium",
        "key_signals": [
            "Vision strong for images",
            "Video understanding emerging",
            "Audio transcription mature",
        ],
    },
}


class CapabilityDomain(BaseModel):
    """Per-domain capability estimate with strict validation."""

    name: str
    current_level: float = Field(ge=0.0, le=1.0)
    months_to_next_threshold: int = Field(ge=0, le=120)
    confidence: Literal["low", "medium", "high"]
    key_signals: list[str] = Field(min_length=1, max_length=6)
    last_updated: datetime


class CapabilityHorizonModel:
    """Aggregates scraped data into structured capability estimates per domain."""

    MAX_ROWS = 10

    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path).expanduser()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
        self._domains: list[CapabilityDomain] = []

    def _init_db(self):
        with wal_connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS capability_model (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    refreshed_at TEXT NOT NULL,
                    model_json TEXT NOT NULL
                )
            """)

    def refresh(self, scraper_results: list[IntelItem]) -> None:
        """Synthesize scraper results into per-domain estimates via LLM."""
        # Build context from scraper results
        context_parts = []
        for item in scraper_results[:50]:  # cap input to avoid huge prompts
            context_parts.append(f"[{item.source}] {item.title}: {item.summary[:300]}")
        scraper_context = (
            "\n".join(context_parts) if context_parts else "No scraper data available."
        )

        domains_list = ", ".join(CAPABILITY_DOMAINS)
        prompt = (
            "Given the following AI capability intelligence data, estimate the current state "
            "of AI for each of these domains:\n"
            f"{domains_list}\n\n"
            "For each domain, provide:\n"
            "- name: the domain name exactly as listed\n"
            "- current_level: float 0.0-1.0 (fraction of human-expert performance)\n"
            "- months_to_next_threshold: int 0-120 (months until next major capability jump)\n"
            '- confidence: "low", "medium", or "high"\n'
            "- key_signals: list of 1-6 short strings describing evidence\n\n"
            "Return ONLY a valid JSON array of objects. No other text.\n\n"
            f"INTELLIGENCE DATA:\n{scraper_context}"
        )

        validated_domains: list[CapabilityDomain] = []
        now = datetime.now()

        try:
            provider = create_cheap_provider()
            response = provider.generate(
                messages=[{"role": "user", "content": prompt}],
                max_tokens=3000,
            )
            # Parse JSON
            cleaned = response.strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.split("\n", 1)[-1]
                if cleaned.endswith("```"):
                    cleaned = cleaned[: cleaned.rfind("```")]
            parsed = json.loads(cleaned)
            if not isinstance(parsed, list):
                parsed = [parsed]

            for item in parsed:
                item["last_updated"] = now.isoformat()
                try:
                    domain = CapabilityDomain(**item)
                    if domain.name in CAPABILITY_DOMAINS:
                        validated_domains.append(domain)
                except ValidationError as e:
                    logger.warning("capability_domain.validation_failed", error=str(e), raw=item)
                    continue

        except Exception as e:
            logger.warning("capability_model_llm_failed", error=str(e))

        # Fill gaps with static fallback
        covered = {d.name for d in validated_domains}
        for domain_name in CAPABILITY_DOMAINS:
            if domain_name not in covered:
                fallback = _STATIC_FALLBACK.get(domain_name)
                if fallback:
                    try:
                        validated_domains.append(
                            CapabilityDomain(
                                name=domain_name,
                                last_updated=now,
                                **fallback,
                            )
                        )
                    except ValidationError as e:
                        logger.warning(
                            "capability_domain.static_fallback_failed",
                            domain=domain_name,
                            error=str(e),
                        )

        # If still empty (all scrapers empty + no DB), populate entirely from static
        if not validated_domains:
            logger.warning("capability_model.all_empty_using_static_kb")
            for domain_name, data in _STATIC_FALLBACK.items():
                try:
                    validated_domains.append(
                        CapabilityDomain(name=domain_name, last_updated=now, **data)
                    )
                except ValidationError:
                    continue

        self._domains = validated_domains
        self._persist()

    def _persist(self):
        """Save current model to SQLite and prune old rows."""
        model_json = json.dumps(
            [d.model_dump(mode="json") for d in self._domains],
            default=str,
        )
        with wal_connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO capability_model (refreshed_at, model_json) VALUES (?, ?)",
                (datetime.now().isoformat(), model_json),
            )
            # Prune beyond MAX_ROWS
            conn.execute(
                """
                DELETE FROM capability_model
                WHERE id NOT IN (
                    SELECT id FROM capability_model ORDER BY id DESC LIMIT ?
                )
                """,
                (self.MAX_ROWS,),
            )

    def load(self) -> bool:
        """Load most recent model from DB. Returns True if loaded."""
        with wal_connect(self.db_path) as conn:
            row = conn.execute(
                "SELECT model_json FROM capability_model ORDER BY id DESC LIMIT 1"
            ).fetchone()
        if not row:
            return False

        try:
            parsed = json.loads(row[0])
            self._domains = []
            for item in parsed:
                try:
                    self._domains.append(CapabilityDomain(**item))
                except ValidationError:
                    continue
            return bool(self._domains)
        except (json.JSONDecodeError, TypeError):
            return False

    def get_horizon_context(self) -> str:
        """Return formatted summary, hard-capped at 2000 chars."""
        if not self._domains:
            self.load()
        if not self._domains:
            return "No capability model available."

        lines = ["AI Capability Horizon:"]
        for d in self._domains:
            lines.append(
                f"  {d.name}: level={d.current_level:.2f} "
                f"next_threshold={d.months_to_next_threshold}mo "
                f"conf={d.confidence}"
            )

        result = "\n".join(lines)
        if len(result) > 2000:
            result = result[:1997] + "..."
        return result

    def get_domain_trajectory(self, domain: str) -> str:
        """Return 2-3 sentence narrative for a specific domain."""
        if not self._domains:
            self.load()

        target = next((d for d in self._domains if d.name == domain), None)
        if not target:
            return f"No data available for domain: {domain}"

        signals = "; ".join(target.key_signals[:3])
        return (
            f"{domain.replace('_', ' ').title()} is currently at "
            f"~{target.current_level:.1f} human-level. "
            f"Projected threshold crossing within {target.months_to_next_threshold} months "
            f"(confidence: {target.confidence}). "
            f"Key signals: {signals}."
        )

    @property
    def domains(self) -> list[CapabilityDomain]:
        if not self._domains:
            self.load()
        return self._domains
