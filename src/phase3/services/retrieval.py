from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from src.phase0.core.config import settings
from src.phase2.models.preferences import NormalizedPreferenceProfile
from src.phase3.models.recommendation import CandidateRestaurant


class RetrievalError(Exception):
    pass


class RestaurantQueryService:
    def __init__(self, db_path: Path | None = None) -> None:
        self.db_path = db_path or settings.sqlite_file

    def fetch_city_candidates(self, city: str) -> list[dict]:
        if not self.db_path.exists():
            raise RetrievalError(
                f"Dataset not found at {self.db_path}. Run ingestion before recommendation."
            )
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            rows = cur.execute(
                """
                SELECT restaurant_id, name, city, locality, cuisines, average_cost_for_two,
                       budget_bucket, rating, tags
                FROM restaurants
                WHERE lower(city) = lower(?)
                """,
                (city,),
            ).fetchall()

        results: list[dict] = []
        for row in rows:
            cuisines = self._safe_json_list(row[4])
            tags = self._safe_json_list(row[8])
            results.append(
                {
                    "restaurant_id": str(row[0]),
                    "name": str(row[1]),
                    "city": str(row[2]),
                    "locality": row[3],
                    "cuisines": cuisines,
                    "average_cost_for_two": float(row[5] or 0.0),
                    "budget_bucket": str(row[6]).lower(),
                    "rating": float(row[7] or 0.0),
                    "tags": tags,
                }
            )
        return results

    def _safe_json_list(self, raw_value: object) -> list[str]:
        if raw_value is None:
            return []
        text = str(raw_value).strip()
        if not text:
            return []
        try:
            parsed = json.loads(text)
            if isinstance(parsed, list):
                return [str(x).strip() for x in parsed if str(x).strip()]
        except json.JSONDecodeError:
            pass
        return [part.strip() for part in text.split(",") if part.strip()]


class CandidateScoringService:
    _budget_adjacency = {
        "low": {"low", "medium"},
        "medium": {"low", "medium", "high"},
        "high": {"medium", "high"},
    }

    def score(
        self, restaurant: dict, profile: NormalizedPreferenceProfile
    ) -> tuple[float, dict[str, float]]:
        requested_cuisines = {c.lower() for c in profile.cuisine_tokens}
        restaurant_cuisines = {c.lower() for c in restaurant.get("cuisines", [])}

        rating_norm = max(0.0, min(1.0, float(restaurant.get("rating", 0.0)) / 5.0))
        cuisine_match = (
            len(requested_cuisines & restaurant_cuisines) / max(1, len(requested_cuisines))
        )
        budget_fit = self._budget_fit(
            requested=profile.budget_bucket, actual=str(restaurant.get("budget_bucket", "")).lower()
        )
        extras_fit = self._extras_fit(profile.extra_tags, restaurant.get("tags", []))

        score = (0.4 * rating_norm) + (0.3 * cuisine_match) + (0.2 * budget_fit) + (0.1 * extras_fit)
        breakdown = {
            "rating_norm": round(rating_norm, 4),
            "cuisine_match": round(cuisine_match, 4),
            "budget_fit": round(budget_fit, 4),
            "extras_fit": round(extras_fit, 4),
        }
        return round(score, 4), breakdown

    def _budget_fit(self, requested: str, actual: str) -> float:
        if requested == actual:
            return 1.0
        if actual in self._budget_adjacency.get(requested, set()):
            return 0.6
        return 0.2

    def _extras_fit(self, requested_tags: list[str], restaurant_tags: list[str]) -> float:
        if not requested_tags:
            return 1.0
        normalized_requested = {x.lower().strip() for x in requested_tags}
        normalized_actual = {str(x).lower().strip() for x in restaurant_tags}
        if not normalized_actual:
            return 0.0
        return len(normalized_requested & normalized_actual) / len(normalized_requested)


class ConstraintRelaxationService:
    def __init__(self, min_pool_size: int = 20) -> None:
        self.min_pool_size = min_pool_size

    def apply(
        self,
        all_city_rows: list[dict],
        profile: NormalizedPreferenceProfile,
    ) -> tuple[list[dict], list[str]]:
        relaxations: list[str] = []
        working = self._filter_rows(
            rows=all_city_rows,
            profile=profile,
            allowed_budgets={profile.budget_bucket},
            rating_floor=profile.rating_floor,
        )

        if len(working) >= self.min_pool_size:
            return working, relaxations

        # Step 1: Relax additional preferences as hard constraints (already soft),
        # record explicitly for traceability and alignment with architecture.
        relaxations.append("relaxed_additional_preferences")

        # Step 2: Widen budget tolerance.
        widened_budget = self._widen_budget(profile.budget_bucket)
        widened = self._filter_rows(
            rows=all_city_rows,
            profile=profile,
            allowed_budgets=widened_budget,
            rating_floor=profile.rating_floor,
        )
        if len(widened) > len(working):
            working = widened
            relaxations.append("widened_budget_tolerance")

        if len(working) >= self.min_pool_size:
            return working, relaxations

        # Step 3: Reduce rating floor by 0.5 then 1.0 (bounded at 0.0).
        for delta in (0.5, 1.0):
            new_floor = max(0.0, profile.rating_floor - delta)
            lowered = self._filter_rows(
                rows=all_city_rows,
                profile=profile,
                allowed_budgets=widened_budget,
                rating_floor=new_floor,
            )
            if len(lowered) > len(working):
                working = lowered
                relaxations.append(f"reduced_rating_floor_to_{new_floor:.1f}")
            if len(working) >= self.min_pool_size:
                break

        return working, relaxations

    def _filter_rows(
        self,
        *,
        rows: list[dict],
        profile: NormalizedPreferenceProfile,
        allowed_budgets: set[str],
        rating_floor: float,
    ) -> list[dict]:
        requested_cuisines = {c.lower() for c in profile.cuisine_tokens}
        results: list[dict] = []
        for row in rows:
            if str(row.get("budget_bucket", "")).lower() not in allowed_budgets:
                continue
            if float(row.get("rating", 0.0)) < rating_floor:
                continue
            row_cuisines = {str(c).lower() for c in row.get("cuisines", [])}
            if not (requested_cuisines & row_cuisines):
                continue
            results.append(row)
        return results

    def _widen_budget(self, budget: str) -> set[str]:
        if budget == "low":
            return {"low", "medium"}
        if budget == "high":
            return {"medium", "high"}
        return {"low", "medium", "high"}


class CandidateRetrievalService:
    def __init__(
        self,
        query_service: RestaurantQueryService | None = None,
        scoring_service: CandidateScoringService | None = None,
        relaxation_service: ConstraintRelaxationService | None = None,
    ) -> None:
        self.query_service = query_service or RestaurantQueryService()
        self.scoring_service = scoring_service or CandidateScoringService()
        self.relaxation_service = relaxation_service or ConstraintRelaxationService()

    def shortlist(
        self,
        profile: NormalizedPreferenceProfile,
        *,
        pool_size: int = 20,
    ) -> tuple[list[CandidateRestaurant], list[str], int]:
        city_rows = self.query_service.fetch_city_candidates(profile.preferred_city)
        filtered_rows, relaxations = self.relaxation_service.apply(city_rows, profile)

        scored: list[CandidateRestaurant] = []
        for row in filtered_rows:
            score, breakdown = self.scoring_service.score(row, profile)
            scored.append(
                CandidateRestaurant(
                    restaurant_id=row["restaurant_id"],
                    name=row["name"],
                    city=row["city"],
                    locality=row.get("locality"),
                    cuisines=row.get("cuisines", []),
                    average_cost_for_two=row.get("average_cost_for_two", 0.0),
                    budget_bucket=row.get("budget_bucket", ""),
                    rating=row.get("rating", 0.0),
                    tags=row.get("tags", []),
                    score=score,
                    score_breakdown=breakdown,
                )
            )

        ranked = sorted(scored, key=lambda x: (x.score, x.rating), reverse=True)
        return ranked[:pool_size], relaxations, len(filtered_rows)
