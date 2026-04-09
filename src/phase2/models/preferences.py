from typing import Any

from pydantic import BaseModel, Field, field_validator


class RecommendRequest(BaseModel):
    location: str = Field(min_length=1)
    budget: str
    cuisine: str | list[str]
    min_rating: float = Field(default=0.0, ge=0.0, le=5.0)
    additional_preferences: list[str] = Field(default_factory=list)
    top_k: int = Field(default=5, ge=1, le=20)

    @field_validator("budget")
    @classmethod
    def normalize_budget(cls, value: str) -> str:
        normalized = value.strip().lower()
        if normalized not in {"low", "medium", "high"}:
            raise ValueError("budget must be one of: low, medium, high")
        return normalized

    @field_validator("location")
    @classmethod
    def normalize_location(cls, value: str) -> str:
        cleaned = " ".join(value.strip().split())
        if not cleaned:
            raise ValueError("location cannot be empty")
        return cleaned


class NormalizedPreferenceProfile(BaseModel):
    preferred_city: str
    budget_bucket: str
    budget_range: dict[str, float]
    cuisine_tokens: list[str]
    rating_floor: float
    extra_tags: list[str]
    top_k: int


class RecommendIntakeResponse(BaseModel):
    status: str = "accepted"
    profile: NormalizedPreferenceProfile
    notes: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
