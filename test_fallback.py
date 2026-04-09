"""
Simple test to verify the fallback mechanism works directly
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.phase2.models.preferences import RecommendRequest
from src.phase2.services.preferences import PreferenceService
from src.phase3.services.retrieval import CandidateRetrievalService
from src.phase4.services.ranker import LLMRankingService

print("=" * 70)
print("TESTING FALLBACK MECHANISM")
print("=" * 70)

# Create services
preference_service = PreferenceService()
candidate_service = CandidateRetrievalService()
llm_service = LLMRankingService()

# Create request
req = RecommendRequest(
    location="Banashankari",
    budget="medium",
    cuisine="Chinese",
    min_rating=0.0,
    top_k=5
)

print(f"\n1. Building profile...")
profile = preference_service.build_profile(req)
print(f"   ✅ Profile: {profile.preferred_city}, {profile.cuisine_tokens}")

print(f"\n2. Getting candidates...")
candidates, relaxations, pool_count = candidate_service.shortlist(profile=profile, pool_size=20)
selected_candidates = candidates[:20]
print(f"   ✅ Found {len(selected_candidates)} candidates from pool of {pool_count}")

if selected_candidates:
    print(f"\n3. Testing FALLBACK directly...")
    recommendations, summary = llm_service.deterministic_fallback(
        selected_candidates, top_k=req.top_k
    )
    
    print(f"   ✅ Fallback returned {len(recommendations)} recommendations")
    print(f"   Summary: {summary}")
    
    if recommendations:
        print(f"\n4. First recommendation:")
        rec = recommendations[0]
        print(f"   restaurant_id: {rec.restaurant_id}")
        print(f"   name: {rec.name}")
        print(f"   cuisine: {rec.cuisine}")
        print(f"   rating: {rec.rating}")
        print(f"   estimated_cost: {rec.estimated_cost}")
        print(f"   explanation: {rec.explanation}")
        
        print(f"\n✅ SUCCESS! Fallback mechanism works correctly.")
        print(f"   The API should return these {len(recommendations)} recommendations.")
    else:
        print(f"\n❌ PROBLEM: Fallback returned empty list!")
else:
    print(f"\n❌ PROBLEM: No candidates found!")

print("\n" + "=" * 70)
