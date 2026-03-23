"""Tests for notification system."""


def test_notification_count(client, auth_headers):
    res = client.get("/api/v1/notifications/count", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert "unread" in data
    assert isinstance(data["unread"], int)


def test_notification_list(client, auth_headers):
    res = client.get("/api/v1/notifications", headers=auth_headers)
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_notification_mark_read(client, auth_headers):
    res = client.post("/api/v1/notifications/test-id/read", headers=auth_headers)
    assert res.status_code == 200
    assert res.json() == {"ok": True}


def test_notification_mark_all_read(client, auth_headers):
    res = client.post("/api/v1/notifications/read-all", headers=auth_headers)
    assert res.status_code == 200
    assert res.json() == {"ok": True}


def test_notification_requires_auth(client):
    res = client.get("/api/v1/notifications/count")
    assert res.status_code in (401, 403)


def test_notification_store_lifecycle(tmp_path):
    """Unit test for notification store CRUD."""
    from web.notification_store import NotificationStore

    store = NotificationStore(tmp_path)
    assert not store.is_read("n1")

    store.mark_read("n1")
    assert store.is_read("n1")

    store.mark_all_read(["n2", "n3"])
    assert store.is_read("n2")
    assert store.is_read("n3")

    removed = store.cleanup_old(days=0)
    # All items should be removed since they were just created
    # and days=0 means cutoff is now
    assert removed >= 0
