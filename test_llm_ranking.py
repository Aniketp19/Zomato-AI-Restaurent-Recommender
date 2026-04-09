"""
Test the full LLM ranking flow with the fixed adapter
"""
import sys
sys.path.insert(0, r"c:\Users\RYZEN\Downloads\zomato pro")

from src.phase0.llm.adapter import LLMClientAdapter
from src.phase2.models.preferences import NormalizedPreferenceProfile
from src.phase3.models.recommendation import CandidateRestaurant
from src.phase4.services.ranker import LLMRankingService

print("=" * 60)
print("Testing Full LLM Ranking Flow")
print("=" * 60)

# Create test data
print("\n1. Creating test data...")
profile = NormalizedPreferenceProfile(
    preferred_city="Banashankari",
    budget_bucket="medium",
    budget_range={"min": 500, "max": 1500},
    cuisine_tokens=["Chinese"],
    rating_floor=0.0,
    extra_tags=[],
    top_k=3,
)

candidates = [
    CandidateRestaurant(
        restaurant_id="r1",
        name="Jalsa",
        city="Banashankari",
        cuisines=["Chinese", "Mughlai", "North Indian"],
        rating=4.2,
        average_cost_for_two=800,
        budget_bucket="medium",
        score=0.85,
    ),
    CandidateRestaurant(
        restaurant_id="r2",
        name="China Garden",
        cuisines=["Chinese"],
        city="Banashankari",
        rating=4.0,
        average_cost_for_two=600,
        budget_bucket="medium",
        score=0.78,
    ),
    CandidateRestaurant(
        restaurant_id="r3",
        name="Mainland China",
        cuisines=["Chinese"],
        city="Banashankari",
        rating=4.5,
        average_cost_for_two=1200,
        budget_bucket="medium",
        score=0.92,
    ),
]

print(f"   Profile: {profile.preferred_city}, {profile.budget_bucket}, {profile.cuisine_tokens}")
print(f"   Candidates: {len(candidates)} restaurants")

# Test LLM ranking
print("\n2. Testing LLM ranking service...")
try:
    ranker = LLMRankingService()
    recommendations, summary = ranker.rank(
        profile=profile,
        candidates=candidates,
        top_k=3,
    )
    
    print(f"\n   SUCCESS! Got {len(recommendations)} recommendations")
    print(f"\n3. Results:")
    print(f"   Summary: {summary}")
    print(f"\n   Recommendations:")
    for i, rec in enumerate(recommendations, 1):
        print(f"\n   {i}. {rec.name}")
        print(f"      ID: {rec.restaurant_id}")
        print(f"      Cuisine: {rec.cuisine}")
        print(f"      Rating: {rec.rating}")
        print(f"      Cost: Rs {rec.estimated_cost}")
        print(f"      Explanation: {rec.explanation}")
    
    print("\n" + "=" * 60)
    print("LLM Ranking is now working! AI will generate explanations.")
    print("=" * 60)
    
except Exception as e:
    print(f"\n   ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
