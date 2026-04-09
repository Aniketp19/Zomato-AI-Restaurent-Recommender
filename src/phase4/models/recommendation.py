from typing import Any

from pydantic import BaseModel, Field

from src.phase2.models.preferences import NormalizedPreferenceProfile
from src.phase3.models.recommendation import CandidateRestaurant


class LLMRecommendationItem(BaseModel):
    restaurant_id: str
    name: str
    cuisine: str
    rating: float
    estimated_cost: float
    explanation: str


class FinalRecommendationResponse(BaseModel):
    status: str = "accepted"
    profile: NormalizedPreferenceProfile
    recommendations: list[LLMRecommendationItem] = Field(default_factory=list)
    summary: str | None = None
    candidates: list[CandidateRestaurant] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
