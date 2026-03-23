"""Tests for Prometheus metrics endpoint."""

from observability import metrics


def test_metrics_endpoint(client):
    # Seed some metrics
    metrics.counter("test_requests", 5)
    with metrics.timer("test_latency"):
        pass  # near-zero duration
    metrics.token_usage("claude-sonnet", input_tokens=100, output_tokens=50)

    res = client.get("/metrics")
    assert res.status_code == 200
    assert "text/plain" in res.headers["content-type"]

    text = res.text
    assert "coach_test_requests 5" in text
    assert "coach_test_latency" in text
    assert 'quantile="0.5"' in text
    assert "coach_token_claude_sonnet_input 100" in text
    assert "coach_token_claude_sonnet_output 50" in text

    # Cleanup
    metrics.reset()


def test_metrics_unauthenticated(client):
    """Metrics endpoint requires no auth."""
    res = client.get("/metrics")
    assert res.status_code == 200


def test_metrics_empty(client):
    metrics.reset()
    res = client.get("/metrics")
    assert res.status_code == 200
