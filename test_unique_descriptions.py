"""
Test script to verify that LLM generates unique descriptions for each restaurant.
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.phase0.core.config import settings
from src.phase2.models.preferences import NormalizedPreferenceProfile
from src.phase3.models.recommendation import CandidateRestaurant
from src.phase4.services.ranker import LLMRankingService

def test_unique_descriptions():
    """Test that each restaurant gets a unique description."""
    print("\n" + "="*80)
    print("Testing Unique Restaurant Descriptions")
    print("="*80)
    
    # Create a sample profile
    profile = NormalizedPreferenceProfile(
        preferred_city="Delhi",
        budget_bucket="medium",
        cuisine_tokens=["Chinese", "Italian"],
        rating_floor=3.5,
        extra_tags=[],
    )
    
    # Create sample candidate restaurants with different characteristics
    candidates = [
        CandidateRestaurant(
            restaurant_id="1",
            name="Dragon Palace",
            city="Delhi",
            cuisines=["Chinese", "Asian"],
            rating=4.5,
            average_cost_for_two=800,
            budget_bucket="medium",
            tags=["authentic", "spicy"],
            score=0.95,
        ),
        CandidateRestaurant(
            restaurant_id="2",
            name="Pasta Milano",
            city="Delhi",
            cuisines=["Italian", "European"],
            rating=4.3,
            average_cost_for_two=900,
            budget_bucket="medium",
            tags=["romantic", "fine-dining"],
            score=0.92,
        ),
        CandidateRestaurant(
            restaurant_id="3",
            name="Sichuan House",
            city="Delhi",
            cuisines=["Chinese", "Szechuan"],
            rating=4.2,
            average_cost_for_two=700,
            budget_bucket="medium",
            tags=["spicy", "casual"],
            score=0.88,
        ),
    ]
    
    # Test with LLM service
    try:
        service = LLMRankingService()
        recommendations, summary = service.rank(
            profile=profile,
            candidates=candidates,
            top_k=3,
        )
        
        print(f"\n✅ LLM generated {len(recommendations)} recommendations")
        print(f"\n📝 Summary: {summary}\n")
        
        # Check descriptions for uniqueness
        descriptions = []
        for i, rec in enumerate(recommendations, 1):
            print(f"\n{i}. {rec.name} ({rec.cuisine})")
            print(f"   Rating: {rec.rating} | Cost: ₹{rec.estimated_cost}")
            print(f"   Explanation: {rec.explanation}")
            descriptions.append(rec.explanation.lower().strip())
        
        # Verify uniqueness
        print("\n" + "-"*80)
        print("Uniqueness Check:")
        print("-"*80)
        
        unique_descriptions = set(descriptions)
        if len(unique_descriptions) == len(descriptions):
            print("✅ SUCCESS: All descriptions are unique!")
        else:
            print(f"❌ FAILURE: Found {len(descriptions) - len(unique_descriptions)} duplicate(s)")
            for desc in descriptions:
                count = descriptions.count(desc)
                if count > 1:
                    print(f"   Duplicate: {desc[:100]}...")
        
        # Check for generic phrases
        generic_phrases = [
            "perfect match",
            "great choice",
            "highly recommended",
            "excellent option",
        ]
        generic_count = 0
        for desc in descriptions:
            for phrase in generic_phrases:
                if phrase in desc and descriptions.count(desc) > 1:
                    generic_count += 1
                    break
        
        if generic_count == 0:
            print("✅ No repetitive generic phrases detected")
        else:
            print(f"⚠️  Found {generic_count} potentially generic descriptions")
            
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "="*80)
    return True

if __name__ == "__main__":
    if not settings.groq_api_key:
        print("\n❌ Error: GROQ_API_KEY is not set in environment variables")
        print("Please set GROQ_API_KEY to run this test")
        sys.exit(1)
    
    success = test_unique_descriptions()
    sys.exit(0 if success else 1)
