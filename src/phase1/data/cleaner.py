from __future__ import annotations

import json
import re
from datetime import datetime, timezone

import pandas as pd


def _first_match_column(df: pd.DataFrame, candidates: list[str]) -> str | None:
    lower_map = {col.lower().strip(): col for col in df.columns}
    for candidate in candidates:
        if candidate.lower() in lower_map:
            return lower_map[candidate.lower()]
    return None


def _normalize_city(value: object) -> str:
    if value is None or pd.isna(value):
        return "unknown"
    text = str(value).strip()
    if not text:
        return "unknown"
    return re.sub(r"\s+", " ", text).title()


def _normalize_name(value: object) -> str:
    if value is None or pd.isna(value):
        return ""
    return re.sub(r"\s+", " ", str(value)).strip()


def _parse_cuisines(value: object) -> list[str]:
    if value is None or pd.isna(value):
        return []
    text = str(value).strip()
    if not text:
        return []
    # Remove any surrounding quotes that might be in the data
    text = text.strip('"').strip("'")
    raw_tokens = [t.strip() for t in re.split(r"[,/|;]", text)]
    cleaned = []
    for token in raw_tokens:
        # Strip quotes and whitespace from each token
        token = token.strip().strip('"').strip("'").strip()
        if token:
            cleaned.append(token.title())
    return sorted(set(cleaned))


def _to_float(value: object, default: float = 0.0) -> float:
    if value is None or pd.isna(value):
        return default
    text = str(value).strip()
    
    # Handle rating format like "4.1/5"
    if "/" in text:
        try:
            parts = text.split("/")
            if len(parts) == 2:
                numerator = float(re.sub(r"[^\d.]", "", parts[0]))
                return numerator  # Already out of 5
        except (ValueError, IndexError):
            pass
    
    # Remove non-numeric characters except decimal point
    text = re.sub(r"[^\d.]", "", text)
    if not text:
        return default
    try:
        return float(text)
    except ValueError:
        return default


def _budget_bucket(cost_for_two: float) -> str:
    if cost_for_two <= 800:
        return "low"
    if cost_for_two <= 1800:
        return "medium"
    return "high"


class DataCleaner:
    def clean(self, raw_df: pd.DataFrame) -> pd.DataFrame:
        df = raw_df.copy()

        id_col = _first_match_column(df, ["restaurant_id", "id", "res_id"])
        name_col = _first_match_column(df, ["restaurant_name", "name"])
        city_col = _first_match_column(df, ["city", "location", "locality_verbose", "listed_in(city)"])
        locality_col = _first_match_column(df, ["locality", "address"])
        cuisine_col = _first_match_column(df, ["cuisines", "cuisine"])
        cost_col = _first_match_column(df, ["average_cost_for_two", "approx_cost(for two people)", "cost", "price_range"])
        rating_col = _first_match_column(df, ["aggregate_rating", "rate", "rating", "user_rating"])

        if name_col is None or city_col is None:
            raise ValueError("Required columns for name/city not found in dataset")

        now = datetime.now(timezone.utc).isoformat()
        cleaned = pd.DataFrame()
        cleaned["restaurant_id"] = (
            df[id_col].astype(str).str.strip()
            if id_col
            else (df.index.astype(str).map(lambda x: f"gen-{x}"))
        )
        cleaned["name"] = df[name_col].map(_normalize_name)
        cleaned["city"] = df[city_col].map(_normalize_city)
        cleaned["locality"] = df[locality_col].map(_normalize_name) if locality_col else None
        cleaned["cuisines"] = df[cuisine_col].map(_parse_cuisines) if cuisine_col else [[]] * len(df)
        cleaned["average_cost_for_two"] = (
            df[cost_col].map(_to_float) if cost_col else pd.Series([0.0] * len(df))
        )
        cleaned["budget_bucket"] = cleaned["average_cost_for_two"].map(_budget_bucket)
        cleaned["rating"] = (
            df[rating_col].map(lambda x: max(0.0, min(5.0, _to_float(x))))
            if rating_col
            else pd.Series([0.0] * len(df))
        )
        cleaned["tags"] = [[] for _ in range(len(df))]
        cleaned["last_updated_at"] = now
        cleaned = cleaned[cleaned["name"].str.len() > 0].copy()
        cleaned["cuisines"] = cleaned["cuisines"].map(lambda v: json.dumps(v))
        cleaned["tags"] = cleaned["tags"].map(lambda v: json.dumps(v))
        return cleaned
