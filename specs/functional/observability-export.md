# Observability Export

## Problem
`Metrics` singleton collects counters/timers/tokens in memory but never exports. Invisible in prod.

## Desired Behavior
- `GET /metrics` returns Prometheus exposition format text
- Counters as `coach_{name} value`
- Timers as summary type with p50/p95/p99 quantiles
- Token usage as gauges
- Scraper health status included

## Acceptance Criteria
- `/metrics` is unauthenticated (for Prometheus scraping)
- Response content type is `text/plain; version=0.0.4; charset=utf-8`
- Valid Prometheus exposition format
- Includes scraper health when available
