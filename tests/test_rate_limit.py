"""
Unit tests for the in-memory sliding-window rate limiter.
"""

from unittest.mock import patch

from app.core.rate_limit import RateLimiter


def test_allows_requests_within_the_limit() -> None:
    """Verify requests under the limit are all allowed."""

    limiter = RateLimiter(max_requests=3, window_seconds=60.0)

    for _ in range(3):
        allowed, retry_after = limiter.check("user-a")
        assert allowed
        assert retry_after == 0.0


def test_blocks_requests_over_the_limit() -> None:
    """Verify the request beyond the limit is rejected."""

    limiter = RateLimiter(max_requests=2, window_seconds=60.0)

    assert limiter.check("user-a")[0] is True
    assert limiter.check("user-a")[0] is True

    allowed, retry_after = limiter.check("user-a")

    assert allowed is False
    assert retry_after > 0.0


def test_keys_are_independent() -> None:
    """Verify one key's usage does not affect another key's limit."""

    limiter = RateLimiter(max_requests=1, window_seconds=60.0)

    assert limiter.check("user-a")[0] is True
    assert limiter.check("user-b")[0] is True

    # Both are now at their limit, independently of each other.
    assert limiter.check("user-a")[0] is False
    assert limiter.check("user-b")[0] is False


def test_window_slides_and_old_hits_expire() -> None:
    """Verify requests outside the window no longer count against the limit."""

    limiter = RateLimiter(max_requests=1, window_seconds=10.0)

    with patch("app.core.rate_limit.time.monotonic", return_value=0.0):
        assert limiter.check("user-a")[0] is True
        assert limiter.check("user-a")[0] is False

    with patch("app.core.rate_limit.time.monotonic", return_value=11.0):
        allowed, _ = limiter.check("user-a")
        assert allowed is True


def test_reset_clears_all_state() -> None:
    """Verify reset() clears tracked usage for every key."""

    limiter = RateLimiter(max_requests=1, window_seconds=60.0)

    limiter.check("user-a")
    assert limiter.check("user-a")[0] is False

    limiter.reset()

    assert limiter.check("user-a")[0] is True
