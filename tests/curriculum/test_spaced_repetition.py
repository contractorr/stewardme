"""Tests for SM-2 spaced repetition algorithm."""

from curriculum.spaced_repetition import sm2_update


def test_perfect_score_increases_interval():
    r = sm2_update(2.5, 1, 0, 5)
    assert r.interval_days == 1
    assert r.repetitions == 1
    assert r.easiness_factor > 2.5


def test_second_rep_gives_6_day_interval():
    r = sm2_update(2.5, 1, 1, 4)
    assert r.interval_days == 6
    assert r.repetitions == 2


def test_third_rep_uses_ef_multiplier():
    r = sm2_update(2.5, 6, 2, 4)
    assert r.interval_days == round(6 * r.easiness_factor)
    assert r.repetitions == 3


def test_fail_resets_reps_and_interval():
    r = sm2_update(2.5, 10, 5, 2)
    assert r.interval_days == 1
    assert r.repetitions == 0


def test_blackout_resets():
    r = sm2_update(2.5, 10, 5, 0)
    assert r.interval_days == 1
    assert r.repetitions == 0


def test_ef_never_below_1_3():
    r = sm2_update(1.3, 1, 0, 0)
    assert r.easiness_factor >= 1.3


def test_grade_3_is_passing():
    r = sm2_update(2.5, 1, 0, 3)
    assert r.repetitions == 1  # successful


def test_grade_clamped():
    r = sm2_update(2.5, 1, 0, 10)
    assert r.repetitions == 1  # treated as grade=5
    r2 = sm2_update(2.5, 1, 0, -5)
    assert r2.repetitions == 0  # treated as grade=0


def test_interval_never_below_1():
    r = sm2_update(1.3, 1, 2, 3)
    assert r.interval_days >= 1
