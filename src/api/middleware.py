import time
import uuid
from contextvars import ContextVar
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

# Context variables for request tracking
request_id_var: ContextVar[str] = ContextVar("request_id", default="")
start_time_var: ContextVar[float] = ContextVar("start_time", default=0.0)


class RequestTrackingMiddleware(BaseHTTPMiddleware):
    """Middleware to add request ID and timing to every request."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Generate unique request ID
        req_id = str(uuid.uuid4())
        request_id_var.set(req_id)
        
        # Track start time
        start_time = time.time()
        start_time_var.set(start_time)
        
        # Store in request state for easy access
        request.state.request_id = req_id
        request.state.start_time = start_time
        
        # Process request
        response = await call_next(request)
        
        # Calculate processing time
        processing_ms = int((time.time() - start_time) * 1000)
        
        # Add headers
        response.headers["X-Request-ID"] = req_id
        response.headers["X-Processing-Time-Ms"] = str(processing_ms)
        
        return response


def get_request_id() -> str:
    """Get the current request ID from context."""
    return request_id_var.get()


def get_processing_time_ms(start_time: float) -> int:
    """Calculate processing time in milliseconds."""
    return int((time.time() - start_time) * 1000)
