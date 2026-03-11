"""Tests for dossier escalation API routes."""

from fastapi import HTTPException


def test_accept_dossier_escalation_requires_personal_key(client, app, auth_headers):
    from web.deps import require_personal_research_key

    def _deny():
        raise HTTPException(status_code=403, detail="Deep research requires your own API key.")

    app.dependency_overrides[require_personal_research_key] = _deny
    try:
        response = client.post(
            "/api/dossier-escalations/escalation-123/accept",
            headers=auth_headers,
        )
    finally:
        app.dependency_overrides[require_personal_research_key] = lambda: None

    assert response.status_code == 403
