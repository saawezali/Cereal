"""
Unit tests for the auto-meme scheduling logic
Run with: python -m pytest tests/
"""

from datetime import datetime, timedelta

from cogs.automeme import (
    INTERVAL_CHOICES,
    MAX_CONSECUTIVE_FAILURES,
    MAX_INTERVAL_MINUTES,
    MEMES_PER_TICK,
    MEME_RETRIES,
    MIN_INTERVAL_MINUTES,
    is_due,
    validate_interval,
)


class TestScheduling:
    """Automeme scheduler predicate"""

    def test_due_when_never_sent(self):
        assert is_due(None, 15, datetime(2026, 1, 1)) is True

    def test_due_after_full_interval(self):
        sent = datetime(2026, 1, 1, 12, 0, 0)
        now = sent + timedelta(minutes=15)
        assert is_due(sent, 15, now) is True

    def test_not_due_minutes_before_interval(self):
        sent = datetime(2026, 1, 1, 12, 0, 0)
        now = sent + timedelta(minutes=14, seconds=59)
        assert is_due(sent, 15, now) is False

    def test_due_exact_boundary(self):
        sent = datetime(2026, 1, 1, 12, 0, 0)
        now = sent + timedelta(minutes=30)
        assert is_due(sent, 30, now) is True


class TestLoadThresholds:
    """Load thresholds decided in the automeme design"""

    def test_minimum_interval_is_15_minutes(self):
        assert MIN_INTERVAL_MINUTES == 15

    def test_max_interval_is_24_hours(self):
        assert MAX_INTERVAL_MINUTES == 1440

    def test_all_considered_intervals_are_valid(self):
        for minutes in INTERVAL_CHOICES:
            assert validate_interval(minutes) is True

    def test_out_of_bounds_intervals_rejected(self):
        assert validate_interval(0) is False
        assert validate_interval(MIN_INTERVAL_MINUTES - 1) is False
        assert validate_interval(MAX_INTERVAL_MINUTES + 1) is False

    def test_tick_budget_is_bounded(self):
        assert 1 <= MEMES_PER_TICK <= 20

    def test_retry_and_failure_limits(self):
        assert 1 <= MEME_RETRIES <= 3
        assert MAX_CONSECUTIVE_FAILURES == 5
