import json
import sqlite3
from pathlib import Path

from src.phase2.models.preferences import NormalizedPreferenceProfile
from src.phase3.services.retrieval import CandidateRetrievalService, RestaurantQueryService


def _seed_restaurants(db_path: Path) -> None:
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE restaurants (
                restaurant_id TEXT,
                name TEXT,
                city TEXT,
                locality TEXT,
                cuisines TEXT,
                average_cost_for_two REAL,
                budget_bucket TEXT,
                rating REAL,
                tags TEXT
            )
            """
        )
        rows = [
            (
                "1",
                "Budget Italiano",
                "Bangalore",
                "Indiranagar",
                json.dumps(["Italian"]),
                700.0,
                "low",
                4.4,
                json.dumps(["quick service"]),
            ),
            (
                "2",
                "Premium Pasta",
                "Bangalore",
                "Koramangala",
                json.dumps(["Italian", "Continental"]),
                1900.0,
                "high",
                4.7,
                json.dumps(["family-friendly"]),
            ),
            (
                "3",
                "Noodle Point",
                "Bangalore",
                "HSR",
                json.dumps(["Chinese"]),
                650.0,
                "low",
                4.2,
                json.dumps([]),
            ),
        ]
        conn.executemany(
            """
            INSERT INTO restaurants(
                restaurant_id, name, city, locality, cuisines, average_cost_for_two,
                budget_bucket, rating, tags
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            rows,
        )
        conn.commit()


def test_candidate_retrieval_shortlists_and_ranks(tmp_path: Path) -> None:
    db_path = tmp_path / "restaurants.db"
    _seed_restaurants(db_path)
    profile = NormalizedPreferenceProfile(
        preferred_city="Bangalore",
        budget_bucket="low",
        budget_range={"min": 0.0, "max": 800.0},
        cuisine_tokens=["Italian"],
        rating_floor=4.0,
        extra_tags=["quick service"],
        top_k=2,
    )

    service = CandidateRetrievalService(query_service=RestaurantQueryService(db_path=db_path))
    candidates, relaxations, pool_count = service.shortlist(profile, pool_size=20)

    assert pool_count >= 1
    assert len(candidates) >= 1
    assert candidates[0].name == "Budget Italiano"
    assert "relaxed_additional_preferences" in relaxations
