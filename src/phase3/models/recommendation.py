from typing import Any

from pydantic import BaseModel, Field

from src.phase2.models.preferences import NormalizedPreferenceProfile


class CandidateRestaurant(BaseModel):
    restaurant_id: str
    name: str
    city: str
    locality: str | None = None
    cuisines: list[str] = Field(default_factory=list)
    average_cost_for_two: float
    budget_bucket: str
    rating: float
    tags: list[str] = Field(default_factory=list)
    score: float
    score_breakdown: dict[str, float] = Field(default_factory=dict)


class CandidateShortlistResponse(BaseModel):
    status: str = "accepted"
    profile: NormalizedPreferenceProfile
    candidates: list[CandidateRestaurant] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
