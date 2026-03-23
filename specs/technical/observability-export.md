# Observability Export — Technical Spec

## Components

### `src/observability.py` — `Metrics` class extensions
- `prometheus_text()` method returning Prometheus exposition format string
- Percentiles (p50/p95/p99) added to timer output in `summary()`

### `src/web/routes/metrics.py` — new route
- `GET /metrics` — unauthed, Prometheus text format
- Registered directly on app (not in ROUTERS — no auth)
- Includes scraper health from `ScraperHealthTracker`

## Format
```
# TYPE coach_{counter} counter
coach_{counter} {value}

# TYPE coach_{timer} summary
coach_{timer}{quantile="0.5"} {p50}
coach_{timer}{quantile="0.95"} {p95}
coach_{timer}{quantile="0.99"} {p99}
coach_{timer}_count {count}
coach_{timer}_sum {total}

# TYPE coach_token_{model}_input gauge
coach_token_{model}_input {value}
```

## Files
- Modify: `src/observability.py`, `src/web/app.py`
- New: `src/web/routes/metrics.py`
