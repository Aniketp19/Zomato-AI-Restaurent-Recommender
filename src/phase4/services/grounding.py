from __future__ import annotations

from src.phase4.models.recommendation import LLMRecommendationItem


class GroundingGuardError(Exception):
    pass


class GroundingGuard:
    def enforce(
        self,
        recommendations: list[LLMRecommendationItem],
        *,
        allowed_restaurant_ids: set[str],
    ) -> list[LLMRecommendationItem]:
        grounded: list[LLMRecommendationItem] = []
        seen_ids: set[str] = set()
        for rec in recommendations:
            if rec.restaurant_id not in allowed_restaurant_ids:
                raise GroundingGuardError(
                    f"Hallucinated restaurant detected: {rec.restaurant_id} not in candidate set."
                )
            if rec.restaurant_id in seen_ids:
                continue
            seen_ids.add(rec.restaurant_id)
            grounded.append(rec)
        return grounded
