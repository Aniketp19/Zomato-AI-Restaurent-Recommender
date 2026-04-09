from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field, field_validator


class RestaurantRecord(BaseModel):
    restaurant_id: str
    name: str
    city: str
    locality: str | None = None
    cuisines: list[str] = Field(default_factory=list)
    average_cost_for_two: float
    budget_bucket: str
    rating: float
    tags: list[str] = Field(default_factory=list)
    last_updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )

    @field_validator("budget_bucket")
    @classmethod
    def validate_budget_bucket(cls, value: str) -> str:
        valid = {"low", "medium", "high"}
        normalized = value.strip().lower()
        if normalized not in valid:
            raise ValueError(f"budget_bucket must be one of {valid}")
        return normalized

    @field_validator("rating")
    @classmethod
    def validate_rating(cls, value: float) -> float:
        if not 0 <= value <= 5:
            raise ValueError("rating must be between 0 and 5")
        return round(float(value), 2)


class QualityReport(BaseModel):
    raw_rows: int
    cleaned_rows: int
    dropped_rows: int
    duplicate_ratio: float
    critical_null_ratio: float
    warnings: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
