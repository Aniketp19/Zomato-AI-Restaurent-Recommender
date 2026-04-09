import sqlite3
from pathlib import Path

from src.models.preferences import RecommendRequest
from src.services.preferences import PreferenceService, PreferenceValidationError


def test_preference_profile_normalization_without_db() -> None:
    service = PreferenceService(db_path=Path("data/does-not-exist.db"))
    req = RecommendRequest(
        location="  bangalore ",
        budget="MEDIUM",
        cuisine=["italian", "Chinese"],
        min_rating=4.1,
        additional_preferences=[" Family-Friendly ", "Quick Service"],
    )
    profile = service.build_profile(req)

    assert profile.preferred_city == "Bangalore"
    assert profile.budget_bucket == "medium"
    assert profile.cuisine_tokens == ["Chinese", "Italian"]
    assert profile.extra_tags == ["family-friendly", "quick service"]


def test_preference_validation_with_suggestions(tmp_path: Path) -> None:
    db_path = tmp_path / "restaurants.db"
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            "CREATE TABLE restaurants (city TEXT, cuisines TEXT)"
        )
        conn.execute(
            "INSERT INTO restaurants(city, cuisines) VALUES (?, ?)",
            ("Bangalore", '["Italian", "Chinese"]'),
        )
        conn.commit()

    service = PreferenceService(db_path=db_path)
    req = RecommendRequest(
        location="Bengaluru",
        budget="low",
        cuisine=["Italin"],
    )

    try:
        service.build_profile(req)
        assert False, "Expected PreferenceValidationError"
    except PreferenceValidationError as exc:
        assert "location" in exc.details
        assert "cuisine" in exc.details
