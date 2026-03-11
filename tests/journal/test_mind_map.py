from journal.mind_map import JournalMindMapGenerator, JournalMindMapStore


def test_mind_map_store_round_trip(tmp_path):
    store = JournalMindMapStore(tmp_path / "mind_maps.db")
    artifact = {
        "entry_path": "journal/test.md",
        "entry_title": "Test entry",
        "source_hash": "abc123",
        "summary": "A test graph.",
        "rationale": "Built from tags and entry language.",
        "generator": "derived",
        "nodes": [
            {
                "id": "root",
                "label": "Test entry",
                "kind": "entry",
                "weight": 1.0,
                "confidence": 1.0,
                "is_root": True,
            }
        ],
        "edges": [],
    }

    store.upsert(artifact)
    loaded = store.get_by_entry("journal/test.md")

    assert loaded is not None
    assert loaded["entry_title"] == "Test entry"
    assert loaded["source_hash"] == "abc123"
    assert store.delete_by_entry("journal/test.md") is True
    assert store.get_by_entry("journal/test.md") is None


def test_mind_map_generator_uses_receipt_and_entry_signals(tmp_path):
    store = JournalMindMapStore(tmp_path / "mind_maps.db")
    generator = JournalMindMapGenerator(store)
    receipt = {
        "thread_label": "Career direction",
        "payload": {
            "themes": [{"label": "PM portfolio", "confidence": 0.84}],
            "memory_facts": [{"text": "User needs clearer case studies", "confidence": 0.8}],
            "goal_candidates": [{"title": "Ship PM portfolio draft", "confidence": 0.77}],
        },
    }

    artifact = generator.generate_for_entry(
        {
            "path": "journal/career.md",
            "title": "Career planning",
            "content": (
                "I need to focus on PM portfolio work this month. "
                "I am blocked by weak case studies and I am working on career direction."
            ),
            "tags": ["career", "portfolio"],
        },
        receipt=receipt,
        force=True,
    )

    assert artifact is not None
    labels = {node["label"] for node in artifact["nodes"]}
    kinds = {node["kind"] for node in artifact["nodes"]}
    assert "Career planning" in labels
    assert "PM portfolio" in labels
    assert "Ship PM portfolio draft" in labels
    assert "Career direction" in labels
    assert {"entry", "theme", "action"}.issubset(kinds)
    assert artifact["summary"]
    assert artifact["rationale"]


def test_mind_map_generator_returns_none_for_low_signal_entry(tmp_path):
    store = JournalMindMapStore(tmp_path / "mind_maps.db")
    generator = JournalMindMapGenerator(store)

    artifact = generator.generate_for_entry(
        {
            "path": "journal/short.md",
            "title": "Quick note",
            "content": "Tired today.",
            "tags": [],
        },
        force=True,
    )

    assert artifact is None


def test_mind_map_generator_falls_back_to_cached_artifact_when_external_context_fails(tmp_path):
    class BrokenIntelStorage:
        def get_recent(self, *args, **kwargs):
            raise RuntimeError("intel unavailable")

    store = JournalMindMapStore(tmp_path / "mind_maps.db")
    store.upsert(
        {
            "entry_path": "journal/career.md",
            "entry_title": "Career planning",
            "source_hash": "cached-hash",
            "summary": "Cached map.",
            "rationale": "Built from cached data.",
            "generator": "derived",
            "nodes": [
                {
                    "id": "root",
                    "label": "Career planning",
                    "kind": "entry",
                    "weight": 1.0,
                    "confidence": 1.0,
                    "is_root": True,
                },
                {
                    "id": "theme-1",
                    "label": "PM portfolio",
                    "kind": "theme",
                    "weight": 0.8,
                    "confidence": 0.8,
                    "is_root": False,
                },
            ],
            "edges": [
                {
                    "source": "root",
                    "target": "theme-1",
                    "label": "highlights",
                    "strength": 0.8,
                }
            ],
        }
    )
    generator = JournalMindMapGenerator(store, intel_storage=BrokenIntelStorage())

    artifact = generator.generate_for_entry(
        {
            "path": "journal/career.md",
            "title": "Career planning",
            "content": "I need to focus on PM portfolio work this month.",
            "tags": ["career", "portfolio"],
        },
        force=False,
    )

    assert artifact is not None
    assert artifact["summary"] == "Cached map."
    assert {node["kind"] for node in artifact["nodes"]} == {"entry", "theme"}


def test_mind_map_generator_still_builds_local_map_when_external_context_fails(tmp_path):
    class BrokenIntelStorage:
        def get_recent(self, *args, **kwargs):
            raise RuntimeError("intel unavailable")

    store = JournalMindMapStore(tmp_path / "mind_maps.db")
    generator = JournalMindMapGenerator(store, intel_storage=BrokenIntelStorage())

    artifact = generator.generate_for_entry(
        {
            "path": "journal/career.md",
            "title": "Career planning",
            "content": (
                "I need to focus on PM portfolio work this month. "
                "I am working on career direction."
            ),
            "tags": ["career", "portfolio"],
        },
        force=True,
    )

    assert artifact is not None
    assert "intel" not in {node["kind"] for node in artifact["nodes"]}


def test_mind_map_generator_uses_research_intel_and_conversation_signals(tmp_path):
    from intelligence.scraper import IntelItem, IntelStorage
    from journal.storage import JournalStorage
    from web.conversation_store import add_message, create_conversation
    from web.user_store import get_or_create_user, init_db

    journal_storage = JournalStorage(tmp_path / "journal")
    journal_storage.create(
        content=(
            "## What Changed\n- PM hiring is tightening and portfolio quality matters more.\n"
            "## Recommended Actions\n- Tighten portfolio case studies."
        ),
        entry_type="research",
        title="Research: PM portfolio hiring trends",
        tags=["research", "career", "portfolio"],
    )

    intel_storage = IntelStorage(tmp_path / "intel.db")
    intel_storage.save(
        IntelItem(
            source="rss:hackernews",
            title="Hiring managers are asking for better PM case studies",
            url="https://example.com/pm-case-studies",
            summary="A roundup of what PM candidates are missing in portfolio presentations.",
            tags=["career", "portfolio", "product"],
        )
    )

    users_db = tmp_path / "users.db"
    init_db(users_db)
    get_or_create_user("u1", db_path=users_db)
    conv_id = create_conversation("u1", "PM portfolio chat", db_path=users_db)
    add_message(
        conv_id,
        "user",
        "How should I improve my PM portfolio case studies before applying again?",
        db_path=users_db,
    )

    store = JournalMindMapStore(tmp_path / "mind_maps.db")
    generator = JournalMindMapGenerator(
        store,
        journal_storage=journal_storage,
        intel_storage=intel_storage,
        user_id="u1",
        users_db_path=users_db,
    )

    artifact = generator.generate_for_entry(
        {
            "path": "journal/career.md",
            "title": "Career planning",
            "content": (
                "I need to focus on PM portfolio work this month. "
                "I am blocked by weak case studies and I am working on career direction."
            ),
            "tags": ["career", "portfolio"],
        },
        force=True,
    )

    assert artifact is not None
    kinds = {node["kind"] for node in artifact["nodes"]}
    assert {"research", "intel", "conversation"}.issubset(kinds)
    assert "research" in artifact["rationale"].lower()
    assert "advisor conversations" in artifact["rationale"].lower()


def test_mind_map_generator_ignores_assistant_only_conversation_matches(tmp_path):
    from web.conversation_store import add_message, create_conversation
    from web.user_store import get_or_create_user, init_db

    users_db = tmp_path / "users.db"
    init_db(users_db)
    get_or_create_user("u1", db_path=users_db)
    conv_id = create_conversation("u1", "PM portfolio chat", db_path=users_db)
    add_message(conv_id, "user", "Thanks for the help.", db_path=users_db)
    add_message(
        conv_id,
        "assistant",
        "You should improve your PM portfolio case studies before interviews.",
        db_path=users_db,
    )

    store = JournalMindMapStore(tmp_path / "mind_maps.db")
    generator = JournalMindMapGenerator(
        store,
        user_id="u1",
        users_db_path=users_db,
    )

    artifact = generator.generate_for_entry(
        {
            "path": "journal/career.md",
            "title": "Career planning",
            "content": (
                "I need to focus on PM portfolio work this month. "
                "I am working on career direction."
            ),
            "tags": ["career", "portfolio"],
        },
        force=True,
    )

    assert artifact is not None
    assert "conversation" not in {node["kind"] for node in artifact["nodes"]}
