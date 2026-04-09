from __future__ import annotations

import json

from src.phase2.models.preferences import NormalizedPreferenceProfile
from src.phase3.models.recommendation import CandidateRestaurant


class PromptBuilder:
    def build(
        self,
        *,
        profile: NormalizedPreferenceProfile,
        candidates: list[CandidateRestaurant],
        top_k: int,
    ) -> str:
        candidate_payload = []
        for c in candidates:
            candidate_payload.append(
                {
                    "restaurant_id": c.restaurant_id,
                    "name": c.name,
                    "city": c.city,
                    "cuisines": c.cuisines,
                    "rating": c.rating,
                    "estimated_cost": c.average_cost_for_two,
                    "budget_bucket": c.budget_bucket,
                    "tags": c.tags,
                    "deterministic_score": c.score,
                }
            )

        instructions = {
            "task": "Rank restaurants and explain suitability for the user.",
            "strict_rules": [
                "Use ONLY restaurants listed in candidates.",
                "Do not invent restaurants, ratings, cuisines, or costs.",
                "Return valid JSON only (no markdown).",
                "Create UNIQUE, PERSONALIZED explanations for EACH restaurant.",
                "Base each explanation on the restaurant's SPECIFIC characteristics (cuisine, rating, cost, tags).",
                "DO NOT use generic or repetitive descriptions - every explanation must be DIFFERENT.",
                "Highlight what makes EACH restaurant unique and suitable for the user's preferences.",
            ],
            "output_schema": {
                "recommendations": [
                    {
                        "restaurant_id": "string",
                        "name": "string",
                        "cuisine": "string",
                        "rating": "number",
                        "estimated_cost": "number",
                        "explanation": "string (must be unique and specific to this restaurant)",
                    }
                ],
                "summary": "string",
            },
        }

        payload = {
            "user_profile": {
                "preferred_city": profile.preferred_city,
                "budget_bucket": profile.budget_bucket,
                "cuisine_tokens": profile.cuisine_tokens,
                "rating_floor": profile.rating_floor,
                "extra_tags": profile.extra_tags,
                "top_k": top_k,
            },
            "candidates": candidate_payload,
            "instructions": instructions,
        }
        return json.dumps(payload, ensure_ascii=True, indent=2)
