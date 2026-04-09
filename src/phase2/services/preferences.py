from __future__ import annotations

import difflib
import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path

from src.phase0.core.config import settings
from src.phase2.models.preferences import NormalizedPreferenceProfile, RecommendRequest


@dataclass
class KnownValues:
    cities: set[str]
    cuisines: set[str]


class PreferenceValidationError(Exception):
    def __init__(self, message: str, details: dict) -> None:
        super().__init__(message)
        self.message = message
        self.details = details


class PreferenceService:
    _budget_ranges = {
        "low": {"min": 0.0, "max": 800.0},
        "medium": {"min": 801.0, "max": 1800.0},
        "high": {"min": 1801.0, "max": 100000.0},
    }

    def __init__(self, db_path: Path | None = None) -> None:
        self.db_path = db_path or settings.sqlite_file

    def build_profile(self, req: RecommendRequest) -> NormalizedPreferenceProfile:
        known = self._load_known_values()
        city = self._normalize_text(req.location, title_case=True)
        cuisine_tokens = self._normalize_cuisine(req.cuisine)
        extras = [self._normalize_text(x) for x in req.additional_preferences if x.strip()]
        self._validate_against_known_values(city=city, cuisine_tokens=cuisine_tokens, known=known)
        return NormalizedPreferenceProfile(
            preferred_city=city,
            budget_bucket=req.budget,
            budget_range=self._budget_ranges[req.budget],
            cuisine_tokens=cuisine_tokens,
            rating_floor=req.min_rating,
            extra_tags=extras,
            top_k=req.top_k,
        )

    def _load_known_values(self) -> KnownValues:
        if not self.db_path.exists():
            return KnownValues(cities=set(), cuisines=set())
        cities: set[str] = set()
        cuisines: set[str] = set()
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            try:
                rows = cur.execute("SELECT DISTINCT city, cuisines FROM restaurants").fetchall()
            except sqlite3.Error:
                return KnownValues(cities=set(), cuisines=set())
            for city, cuisines_blob in rows:
                if city:
                    cities.add(self._normalize_text(str(city), title_case=True))
                if cuisines_blob:
                    parsed = self._parse_cuisines_blob(cuisines_blob)
                    cuisines.update(parsed)
        return KnownValues(cities=cities, cuisines=cuisines)

    def _parse_cuisines_blob(self, cuisines_blob: str) -> set[str]:
        text = str(cuisines_blob).strip()
        if not text:
            return set()
        try:
            parsed = json.loads(text)
            if isinstance(parsed, list):
                return {self._normalize_text(item, title_case=True) for item in parsed if str(item).strip()}
        except json.JSONDecodeError:
            pass
        parts = [p.strip() for p in text.split(",") if p.strip()]
        return {self._normalize_text(part, title_case=True) for part in parts}

    def _normalize_text(self, value: str, *, title_case: bool = False) -> str:
        cleaned = " ".join(str(value).strip().split())
        if title_case:
            return cleaned.title()
        return cleaned.lower()

    def _normalize_cuisine(self, cuisine: str | list[str]) -> list[str]:
        raw_tokens = [cuisine] if isinstance(cuisine, str) else cuisine
        tokens = [self._normalize_text(token, title_case=True) for token in raw_tokens if str(token).strip()]
        unique = sorted(set(tokens))
        if not unique:
            raise PreferenceValidationError(
                "Cuisine cannot be empty.",
                details={"field": "cuisine", "suggestions": []},
            )
        return unique

    def _validate_against_known_values(
        self, *, city: str, cuisine_tokens: list[str], known: KnownValues
    ) -> None:
        if not known.cities and not known.cuisines:
            return
        errors: dict[str, dict] = {}
        if known.cities and city not in known.cities:
            errors["location"] = {
                "message": f"Unknown location: {city}",
                "suggestions": difflib.get_close_matches(city, list(known.cities), n=5, cutoff=0.5),
            }
        unknown_cuisines = [c for c in cuisine_tokens if known.cuisines and c not in known.cuisines]
        if unknown_cuisines:
            suggestions = {}
            for item in unknown_cuisines:
                suggestions[item] = difflib.get_close_matches(item, list(known.cuisines), n=5, cutoff=0.5)
            errors["cuisine"] = {
                "message": f"Unknown cuisine values: {', '.join(unknown_cuisines)}",
                "suggestions": suggestions,
            }
        if errors:
            raise PreferenceValidationError(
                "Preference validation failed against known values.",
                details=errors,
            )
