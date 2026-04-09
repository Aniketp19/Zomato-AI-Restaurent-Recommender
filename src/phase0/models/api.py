from typing import Any

from pydantic import BaseModel, Field


class ErrorEnvelope(BaseModel):
    code: str
    message: str
    details: dict[str, Any] = Field(default_factory=dict)


class HealthResponse(BaseModel):
    status: str = "ok"
    app_name: str
    env: str
    request_id: str | None = None


class ErrorResponse(BaseModel):
    error: ErrorEnvelope
