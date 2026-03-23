"""Tests for curriculum routes: tree, ready, next (DAG-aware), placement."""

from unittest.mock import AsyncMock, patch


def test_tree_endpoint(client, auth_headers):
    """GET /api/curriculum/tree returns tracks, nodes, edges."""
    # Sync catalog first
    client.post("/api/curriculum/sync", headers=auth_headers)

    resp = client.get("/api/curriculum/tree", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert "tracks" in data
    assert "nodes" in data
    assert "edges" in data
    assert isinstance(data["nodes"], list)
    assert isinstance(data["edges"], list)

    # If nodes exist, check structure
    if data["nodes"]:
        node = data["nodes"][0]
        assert "id" in node
        assert "position" in node
        assert "status" in node
        assert "is_entry_point" in node


def test_ready_endpoint(client, auth_headers):
    """GET /api/curriculum/ready returns list (possibly empty)."""
    client.post("/api/curriculum/sync", headers=auth_headers)
    resp = client.get("/api/curriculum/ready", headers=auth_headers)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_next_returns_entry_point_when_no_enrollment(client, auth_headers):
    """GET /api/curriculum/next suggests entry-point guide when nothing enrolled."""
    client.post("/api/curriculum/sync", headers=auth_headers)
    resp = client.get("/api/curriculum/next", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    # Should return either an entry point or fallback
    assert "reason" in data
    assert "guide_id" in data


def test_next_continues_enrolled_guide(client, auth_headers):
    """GET /api/curriculum/next continues enrolled guide."""
    client.post("/api/curriculum/sync", headers=auth_headers)

    # Get a guide and enroll
    guides_resp = client.get("/api/curriculum/guides", headers=auth_headers)
    guides = guides_resp.json()
    if not guides:
        return  # no content to test

    guide_id = guides[0]["id"]
    client.post(
        f"/api/curriculum/guides/{guide_id}/enroll?create_goal=false",
        headers=auth_headers,
    )

    # Mark a chapter as in_progress to create last-read
    guide_detail = client.get(f"/api/curriculum/guides/{guide_id}", headers=auth_headers).json()
    chapters = guide_detail.get("chapters", [])
    if chapters:
        client.post(
            "/api/curriculum/progress",
            headers=auth_headers,
            json={
                "chapter_id": chapters[0]["id"],
                "guide_id": guide_id,
                "status": "in_progress",
            },
        )

    resp = client.get("/api/curriculum/next", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["guide_id"] == guide_id
    assert "chapter" in data


def test_placement_generate_disabled(client, auth_headers):
    """POST placement/generate returns 400 when placement disabled."""
    client.post("/api/curriculum/sync", headers=auth_headers)
    guides = client.get("/api/curriculum/guides", headers=auth_headers).json()
    if not guides:
        return

    with patch("web.routes.curriculum.get_config") as mock_config:
        cfg = mock_config.return_value
        cfg.curriculum.placement_enabled = False
        cfg.curriculum.teachback_enabled = True
        cfg.curriculum.pre_reading_enabled = True
        cfg.curriculum.cross_guide_connections = True
        cfg.memory.enabled = False
        resp = client.post(
            f"/api/curriculum/guides/{guides[0]['id']}/placement/generate",
            headers=auth_headers,
        )
        assert resp.status_code == 400
        assert "disabled" in resp.json()["detail"].lower()


def test_placement_submit_expired(client, auth_headers):
    """POST placement/submit returns 410 when no cached session."""
    client.post("/api/curriculum/sync", headers=auth_headers)
    guides = client.get("/api/curriculum/guides", headers=auth_headers).json()
    if not guides:
        return

    resp = client.post(
        f"/api/curriculum/guides/{guides[0]['id']}/placement/submit",
        headers=auth_headers,
        json={"answers": {"q1": "answer"}},
    )
    assert resp.status_code == 410


def test_placement_generate_and_submit(client, auth_headers):
    """Full placement flow: generate → submit → verify result structure."""
    client.post("/api/curriculum/sync", headers=auth_headers)
    guides = client.get("/api/curriculum/guides", headers=auth_headers).json()
    if not guides:
        return

    guide_id = guides[0]["id"]

    # Mock the question generator to return predictable questions
    mock_questions = [
        {
            "id": "pq1",
            "question": "Test placement Q1",
            "expected_answer": "Answer 1",
            "bloom_level": "apply",
            "chapter_id": "ch1",
        },
        {
            "id": "pq2",
            "question": "Test placement Q2",
            "expected_answer": "Answer 2",
            "bloom_level": "analyze",
            "chapter_id": "ch1",
        },
    ]

    with patch("web.routes.curriculum.QuestionGenerator") as MockGen:
        gen_instance = MockGen.return_value
        gen_instance.generate_placement_questions = AsyncMock(return_value=mock_questions)
        gen_instance.grade_answer = AsyncMock(
            return_value=type(
                "R",
                (),
                {"grade": 4, "feedback": "Good", "correct_points": [], "missing_points": []},
            )()
        )

        # Generate
        resp = client.post(
            f"/api/curriculum/guides/{guide_id}/placement/generate",
            headers=auth_headers,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "questions" in data
        assert len(data["questions"]) > 0
        # Client should NOT see expected_answer
        for q in data["questions"]:
            assert "expected_answer" not in q

        # Submit
        answers = {q["id"]: "my answer" for q in data["questions"]}
        resp = client.post(
            f"/api/curriculum/guides/{guide_id}/placement/submit",
            headers=auth_headers,
            json={"answers": answers},
        )
        assert resp.status_code == 200
        result = resp.json()
        assert "results" in result
        assert "average_grade" in result
        assert "passed" in result
        assert "threshold" in result
