"""
In-memory rate limiting.

Provides a thread-safe sliding-window rate limiter and FastAPI
dependencies that apply it to specific endpoints.

Scope and limitations:

This limiter keeps its state in a process-local dictionary. It works
correctly for a single running instance of the application. If the
application is horizontally scaled (multiple processes or replicas
behind a load balancer), each instance enforces its own independent
limit, so the effective limit is (per-instance limit x instance
count). A production multi-instance deployment should replace this
with a shared store (e.g. Redis, or Azure API Management's built-in
rate-limiting policies in front of the app).
"""

from __future__ import annotations

import threading
import time
from collections import defaultdict, deque

from fastapi import (
    Depends,
    HTTPException,
    Request,
    status,
)

from app.core.security import get_current_user


class RateLimiter:
    """
    Thread-safe sliding-window rate limiter.

    Tracks request timestamps per key (e.g. per user, per IP) and
    rejects requests once more than ``max_requests`` have been made
    within the trailing ``window_seconds``.
    """

    def __init__(
        self,
        max_requests: int,
        window_seconds: float,
    ) -> None:
        """
        Initialize the rate limiter.

        Args:
            max_requests: Maximum requests allowed per key within the
                window.
            window_seconds: Sliding window duration, in seconds.
        """

        self._max_requests = max_requests
        self._window_seconds = window_seconds
        self._hits: dict[str, deque[float]] = defaultdict(deque)
        self._lock = threading.Lock()

    @property
    def max_requests(self) -> int:
        return self._max_requests

    def check(
        self,
        key: str,
    ) -> tuple[bool, float]:
        """
        Check whether a request for ``key`` is allowed right now.

        If allowed, the request is recorded immediately (this method
        both checks and consumes a slot in one atomic step).

        Args:
            key: Identifier to rate-limit on (username, client IP, ...).

        Returns:
            A tuple of ``(allowed, retry_after_seconds)``. When
            ``allowed`` is ``False``, ``retry_after_seconds`` is how
            long the caller should wait before retrying.
        """

        now = time.monotonic()

        with self._lock:
            hits = self._hits[key]

            while hits and now - hits[0] > self._window_seconds:
                hits.popleft()

            if len(hits) >= self._max_requests:
                retry_after = self._window_seconds - (now - hits[0])
                return False, max(retry_after, 0.0)

            hits.append(now)

            return True, 0.0

    def reset(self) -> None:
        """
        Clear all tracked state.

        Intended for tests, so each test starts with a clean limiter
        instead of sharing state with previous tests.
        """

        with self._lock:
            self._hits.clear()


def _client_ip(request: Request) -> str:
    """
    Determine the client IP address for an incoming request.

    Args:
        request: The incoming FastAPI request.

    Returns:
        The client's IP address, or ``"unknown"`` if unavailable.
    """

    if request.client is not None:
        return request.client.host

    return "unknown"


def _too_many_requests(retry_after: float) -> HTTPException:
    """
    Build the standard 429 response for a rejected request.

    Args:
        retry_after: Seconds the caller should wait before retrying.

    Returns:
        A configured ``HTTPException``.
    """

    return HTTPException(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        detail="Rate limit exceeded. Please try again later.",
        headers={"Retry-After": str(max(int(retry_after) + 1, 1))},
    )


def make_ip_rate_limit_dependency(
    limiter: RateLimiter,
):
    """
    Build a FastAPI dependency that rate-limits by client IP.

    Intended for unauthenticated endpoints (e.g. login), where there
    is no user identity yet to key on.

    Args:
        limiter: The rate limiter instance to enforce.

    Returns:
        A FastAPI dependency callable.
    """

    def dependency(request: Request) -> None:
        allowed, retry_after = limiter.check(_client_ip(request))

        if not allowed:
            raise _too_many_requests(retry_after)

    return dependency


def make_user_rate_limit_dependency(
    limiter: RateLimiter,
):
    """
    Build a FastAPI dependency that rate-limits by authenticated user.

    Intended for authenticated endpoints, so limits apply per employee
    rather than per IP (multiple employees may share a NAT'd IP).

    Args:
        limiter: The rate limiter instance to enforce.

    Returns:
        A FastAPI dependency callable.
    """

    def dependency(
        user: dict[str, str] = Depends(get_current_user),
    ) -> None:
        allowed, retry_after = limiter.check(user["username"])

        if not allowed:
            raise _too_many_requests(retry_after)

    return dependency
