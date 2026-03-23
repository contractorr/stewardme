"""Tests for degradation collector."""

from degradation_collector import (
    clear_collector,
    get_degradations,
    init_collector,
    record_degradation,
)


def test_lifecycle():
    init_collector()
    assert get_degradations() == []

    record_degradation("graceful.advisor.cache_init")
    degs = get_degradations()
    assert len(degs) == 1
    assert degs[0]["component"] == "graceful.advisor.cache_init"
    assert degs[0]["message"] == "Context cache unavailable"

    clear_collector()
    assert get_degradations() == []


def test_no_init_noop():
    """record_degradation is a no-op if collector not initialized."""
    clear_collector()
    record_degradation("something")
    assert get_degradations() == []


def test_unknown_metric_generic_message():
    init_collector()
    record_degradation("graceful.unknown.thing")
    degs = get_degradations()
    assert degs[0]["message"] == "Some data sources were unavailable"
    clear_collector()


def test_custom_message():
    init_collector()
    record_degradation("custom", message="Custom failure")
    degs = get_degradations()
    assert degs[0]["message"] == "Custom failure"
    clear_collector()
