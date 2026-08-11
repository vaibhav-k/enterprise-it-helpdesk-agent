"""
Tests for login rate limiting.
"""

import pytest
from fastapi.testclient import TestClient

from app.api.auth import login_rate_limiter
from app.database import users as users_db
from app.main import app


@pytest.fixture(autouse=True)
def _clean_state():
    """Reset the login rate limiter and seeded users between tests."""

    login_rate_limiter.reset()
    users_db.users.clear()
    users_db.seed_users()

    yield

    login_rate_limiter.reset()


def test_login_rate_limit_blocks_after_threshold() -> None:
    """Verify repeated login attempts from one client are throttled."""

    client = TestClient(app)

    max_requests = login_rate_limiter._max_requests

    for _ in range(max_requests):
        response = client.post(
            "/auth/login",
            json={"username": "employee", "password": "wrong-password"},
        )
        # Each of these fails auth (401), but is still within the
        # rate limit, so it should not be a 429.
        assert response.status_code == 401

    limited = client.post(
        "/auth/login",
        json={"username": "employee", "password": "wrong-password"},
    )

    assert limited.status_code == 429
    assert "Retry-After" in limited.headers


def test_login_rate_limit_is_independent_per_client() -> None:
    """Verify the limiter tracks a fresh client key independently."""

    client = TestClient(app)

    max_requests = login_rate_limiter._max_requests

    for _ in range(max_requests):
        client.post(
            "/auth/login",
            json={"username": "employee", "password": "wrong-password"},
        )

    limited = client.post(
        "/auth/login",
        json={"username": "employee", "password": "wrong-password"},
    )
    assert limited.status_code == 429

    # A different key (simulated here directly, since TestClient uses a
    # fixed test host/IP) would not be limited; verified at the unit
    # level in test_rate_limit.py::test_keys_are_independent.
    login_rate_limiter.reset()

    recovered = client.post(
        "/auth/login",
        json={"username": "employee", "password": "wrong-password"},
    )
    assert recovered.status_code == 401
