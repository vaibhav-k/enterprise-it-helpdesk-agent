"""
Request audit middleware.

Tracks:

- Request method
- Endpoint path
- Response status
- Client information
"""

import time
from collections.abc import Awaitable, Callable

from fastapi import Request
from starlette.middleware.base import (
    BaseHTTPMiddleware,
)
from starlette.responses import Response

from app.core.logging import (
    get_logger,
)

logger = get_logger(
    "audit",
)


class AuditMiddleware(BaseHTTPMiddleware):
    """
    Security audit middleware.
    """

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:

        start_time = time.time()

        response = await call_next(request)

        duration = time.time() - start_time

        logger.info(
            "request=%s path=%s status=%s duration=%.3f",
            request.method,
            request.url.path,
            response.status_code,
            duration,
        )

        return response
