from __future__ import annotations

from src.phase0.llm.adapter import LLMClientAdapter
from src.phase2.models.preferences import NormalizedPreferenceProfile
from src.phase3.models.recommendation import CandidateRestaurant
from src.phase4.models.recommendation import LLMRecommendationItem
from src.phase4.services.grounding import GroundingGuard
from src.phase4.services.prompt_builder import PromptBuilder
from src.phase4.services.response_parser import LLMResponseParser


class LLMRankingService:
    def __init__(
        self,
        llm_adapter: LLMClientAdapter | None = None,
        prompt_builder: PromptBuilder | None = None,
        parser: LLMResponseParser | None = None,
        guard: GroundingGuard | None = None,
    ) -> None:
        self.llm_adapter = llm_adapter or LLMClientAdapter()
        self.prompt_builder = prompt_builder or PromptBuilder()
        self.parser = parser or LLMResponseParser()
        self.guard = guard or GroundingGuard()

    def rank(
        self,
        *,
        profile: NormalizedPreferenceProfile,
        candidates: list[CandidateRestaurant],
        top_k: int,
    ) -> tuple[list[LLMRecommendationItem], str | None]:
        prompt = self.prompt_builder.build(profile=profile, candidates=candidates, top_k=top_k)
        raw = self.llm_adapter.generate(prompt, metadata={"phase": "phase-4"})
        parsed, summary = self.parser.parse(raw)
        allowed_ids = {c.restaurant_id for c in candidates}
        grounded = self.guard.enforce(parsed, allowed_restaurant_ids=allowed_ids)
        unique_recommendations = self._ensure_unique_recommendations(grounded)
        unique_explanations = self._ensure_unique_explanations(unique_recommendations, candidates)
        completed = self._fill_missing_recommendations(unique_explanations, candidates, top_k=top_k)
        return completed[:top_k], summary

    def deterministic_fallback(
        self, candidates: list[CandidateRestaurant], *, top_k: int
    ) -> tuple[list[LLMRecommendationItem], str]:
        items: list[LLMRecommendationItem] = []
        for c in candidates[:top_k]:
            cuisine = c.cuisines[0] if c.cuisines else "Mixed"
            items.append(
                LLMRecommendationItem(
                    restaurant_id=c.restaurant_id,
                    name=c.name,
                    cuisine=cuisine,
                    rating=c.rating,
                    estimated_cost=c.average_cost_for_two,
                    explanation=(
                        "Selected using deterministic ranking due to temporary LLM unavailability."
                    ),
                )
            )
        return items, "Fallback summary: ranked by deterministic score."

    def _ensure_unique_explanations(
        self,
        recommendations: list[LLMRecommendationItem],
        candidates: list[CandidateRestaurant],
    ) -> list[LLMRecommendationItem]:
        by_id = {c.restaurant_id: c for c in candidates}
        seen_normalized: set[str] = set()
        fixed: list[LLMRecommendationItem] = []

        for rec in recommendations:
            text = rec.explanation.strip()
            normalized = " ".join(text.lower().split())
            if not normalized or normalized in seen_normalized:
                fixed_text = self._build_specific_explanation(rec, by_id.get(rec.restaurant_id))
                rec = rec.model_copy(update={"explanation": fixed_text})
                normalized = " ".join(fixed_text.lower().split())
            seen_normalized.add(normalized)
            fixed.append(rec)

        return fixed

    def _ensure_unique_recommendations(
        self, recommendations: list[LLMRecommendationItem]
    ) -> list[LLMRecommendationItem]:
        seen_ids: set[str] = set()
        seen_names: set[str] = set()
        unique: list[LLMRecommendationItem] = []

        for rec in recommendations:
            normalized_name = self._normalize_name(rec.name)
            if rec.restaurant_id in seen_ids or normalized_name in seen_names:
                continue
            seen_ids.add(rec.restaurant_id)
            seen_names.add(normalized_name)
            unique.append(rec)

        return unique

    def _fill_missing_recommendations(
        self,
        recommendations: list[LLMRecommendationItem],
        candidates: list[CandidateRestaurant],
        *,
        top_k: int,
    ) -> list[LLMRecommendationItem]:
        if len(recommendations) >= top_k:
            return recommendations

        existing_ids = {r.restaurant_id for r in recommendations}
        existing_names = {self._normalize_name(r.name) for r in recommendations}
        filled = list(recommendations)
        next_index = len(filled) + 1

        for c in candidates:
            if len(filled) >= top_k:
                break
            if c.restaurant_id in existing_ids:
                continue
            normalized_candidate_name = self._normalize_name(c.name)
            if normalized_candidate_name in existing_names:
                continue

            cuisine = c.cuisines[0] if c.cuisines else "Mixed"
            filled.append(
                LLMRecommendationItem(
                    restaurant_id=c.restaurant_id,
                    name=c.name,
                    cuisine=cuisine,
                    rating=c.rating,
                    estimated_cost=c.average_cost_for_two,
                    explanation=self._build_fill_explanation(c, rank_index=next_index),
                )
            )
            existing_ids.add(c.restaurant_id)
            existing_names.add(normalized_candidate_name)
            next_index += 1

        return filled

    def _build_specific_explanation(
        self,
        rec: LLMRecommendationItem,
        candidate: CandidateRestaurant | None,
    ) -> str:
        if candidate is None:
            return (
                f"{rec.name} matches your requested cuisine with a rating of {rec.rating:.1f} "
                f"and an estimated cost around Rs {rec.estimated_cost:.0f} for two."
            )

        cuisines = ", ".join(candidate.cuisines[:2]) if candidate.cuisines else rec.cuisine
        tag_text = f" It also offers {candidate.tags[0].replace('_', ' ')}." if candidate.tags else ""
        return (
            f"{candidate.name} is a strong fit for {candidate.city} with {cuisines} cuisine, "
            f"rated {candidate.rating:.1f}, and about Rs {candidate.average_cost_for_two:.0f} for two.{tag_text}"
        )

    def _build_fill_explanation(self, candidate: CandidateRestaurant, *, rank_index: int) -> str:
        cuisine_text = ", ".join(candidate.cuisines[:2]) if candidate.cuisines else "mixed"
        tag_text = f" Notable for {candidate.tags[0].replace('_', ' ')}." if candidate.tags else ""
        return (
            f"Pick {rank_index}: {candidate.name} in {candidate.city} serves {cuisine_text} with "
            f"a {candidate.rating:.1f} rating and around Rs {candidate.average_cost_for_two:.0f} for two.{tag_text}"
        )

    @staticmethod
    def _normalize_name(name: str) -> str:
        return " ".join(name.strip().lower().split())
