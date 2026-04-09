import json

from src.phase2.models.preferences import NormalizedPreferenceProfile
from src.phase3.models.recommendation import CandidateRestaurant
from src.phase4.services.ranker import LLMRankingService


class _StubLLMAdapter:
    def __init__(self, raw_json: dict) -> None:
        self.raw_json = raw_json

    def generate(self, prompt: str, *, metadata: dict | None = None) -> str:
        return json.dumps(self.raw_json)


def _build_profile(top_k: int = 5) -> NormalizedPreferenceProfile:
    return NormalizedPreferenceProfile(
        preferred_city="Banashankari",
        budget_bucket="medium",
        budget_range={"min": 500.0, "max": 1500.0},
        cuisine_tokens=["Chinese"],
        rating_floor=0.0,
        extra_tags=[],
        top_k=top_k,
    )


def _build_candidates() -> list[CandidateRestaurant]:
    return [
        CandidateRestaurant(
            restaurant_id="r1",
            name="1947",
            city="Banashankari",
            locality="Area 1",
            cuisines=["Chinese"],
            average_cost_for_two=850.0,
            budget_bucket="medium",
            rating=4.0,
            tags=["casual"],
            score=0.91,
            score_breakdown={},
        ),
        CandidateRestaurant(
            restaurant_id="r2",
            name="Chung Wah",
            city="Banashankari",
            locality="Area 2",
            cuisines=["Chinese"],
            average_cost_for_two=900.0,
            budget_bucket="medium",
            rating=4.1,
            tags=["family_friendly"],
            score=0.89,
            score_breakdown={},
        ),
        CandidateRestaurant(
            restaurant_id="r3",
            name="Gustoes Beer House",
            city="Banashankari",
            locality="Area 3",
            cuisines=["Chinese", "Thai"],
            average_cost_for_two=1200.0,
            budget_bucket="medium",
            rating=4.2,
            tags=["bar"],
            score=0.86,
            score_breakdown={},
        ),
        CandidateRestaurant(
            restaurant_id="r4",
            name="K27 - The Pub",
            city="Banashankari",
            locality="Area 4",
            cuisines=["Chinese", "North Indian"],
            average_cost_for_two=1000.0,
            budget_bucket="medium",
            rating=4.0,
            tags=["pub"],
            score=0.83,
            score_breakdown={},
        ),
        CandidateRestaurant(
            restaurant_id="r5",
            name="Beijing Bites",
            city="Banashankari",
            locality="Area 5",
            cuisines=["Chinese"],
            average_cost_for_two=800.0,
            budget_bucket="medium",
            rating=3.9,
            tags=["quick_service"],
            score=0.81,
            score_breakdown={},
        ),
    ]


def test_rank_backfills_to_top_k_and_keeps_explanations_unique() -> None:
    candidates = _build_candidates()
    profile = _build_profile(top_k=5)

    llm_payload = {
        "recommendations": [
            {
                "restaurant_id": "r1",
                "name": "1947",
                "cuisine": "Chinese",
                "rating": 4.0,
                "estimated_cost": 850.0,
                "explanation": "Same explanation for all.",
            },
            {
                "restaurant_id": "r1",
                "name": "1947",
                "cuisine": "Chinese",
                "rating": 4.0,
                "estimated_cost": 850.0,
                "explanation": "Same explanation for all.",
            },
            {
                "restaurant_id": "r2",
                "name": "Chung Wah",
                "cuisine": "Chinese",
                "rating": 4.1,
                "estimated_cost": 900.0,
                "explanation": "Same explanation for all.",
            },
        ],
        "summary": "Test summary",
    }

    service = LLMRankingService(llm_adapter=_StubLLMAdapter(llm_payload))
    recs, _summary = service.rank(profile=profile, candidates=candidates, top_k=5)

    assert len(recs) == 5
    assert len({r.restaurant_id for r in recs}) == 5
    assert len({r.explanation.strip().lower() for r in recs}) == 5


def test_rank_removes_duplicate_restaurant_names() -> None:
    candidates = _build_candidates() + [
        CandidateRestaurant(
            restaurant_id="r6",
            name="Chung Wah",
            city="Banashankari",
            locality="Area 6",
            cuisines=["Chinese"],
            average_cost_for_two=950.0,
            budget_bucket="medium",
            rating=4.0,
            tags=["takeaway"],
            score=0.8,
            score_breakdown={},
        )
    ]
    profile = _build_profile(top_k=5)

    llm_payload = {
        "recommendations": [
            {
                "restaurant_id": "r2",
                "name": "Chung Wah",
                "cuisine": "Chinese",
                "rating": 4.1,
                "estimated_cost": 900.0,
                "explanation": "Unique A",
            },
            {
                "restaurant_id": "r6",
                "name": "Chung Wah",
                "cuisine": "Chinese",
                "rating": 4.0,
                "estimated_cost": 950.0,
                "explanation": "Unique B",
            },
            {
                "restaurant_id": "r1",
                "name": "1947",
                "cuisine": "Chinese",
                "rating": 4.0,
                "estimated_cost": 850.0,
                "explanation": "Unique C",
            },
        ],
        "summary": "Test summary",
    }

    service = LLMRankingService(llm_adapter=_StubLLMAdapter(llm_payload))
    recs, _summary = service.rank(profile=profile, candidates=candidates, top_k=5)

    normalized_names = {" ".join(r.name.strip().lower().split()) for r in recs}
    assert len(recs) == 5
    assert len(normalized_names) == len(recs)
