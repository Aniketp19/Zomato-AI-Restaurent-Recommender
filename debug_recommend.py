"""
Enhanced debugging script to trace the exact flow of a recommendation request.
"""
import sys
import json
from pathlib import Path

# Add the project root to path
sys.path.insert(0, str(Path(__file__).parent))

from src.phase2.models.preferences import RecommendRequest
from src.phase2.services.preferences import PreferenceService
from src.phase3.services.retrieval import CandidateRetrievalService

print("=" * 70)
print("RECOMMENDATION FLOW DEBUG")
print("=" * 70)
print()

# Step 1: Load a valid city and cuisine from the database
import sqlite3
db_path = Path("data/restaurants.db")

if not db_path.exists():
    print(f"❌ Database not found at {db_path}")
    print("Please run: python -m src.data.pipeline")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("1. FETCHING AVAILABLE DATA FROM DATABASE")
print("-" * 70)

cursor.execute("SELECT COUNT(*) FROM restaurants")
total_count = cursor.fetchone()[0]
print(f"Total restaurants in DB: {total_count}")

if total_count == 0:
    print("❌ Database is empty! Run the data pipeline first.")
    exit(1)

# Get sample city
cursor.execute("SELECT DISTINCT city FROM restaurants WHERE city IS NOT NULL LIMIT 1")
sample_city_raw = cursor.fetchone()[0]
print(f"Sample city from DB: '{sample_city_raw}'")

# Get sample cuisine
cursor.execute("SELECT cuisines FROM restaurants WHERE cuisines IS NOT NULL AND cuisines != '[]' LIMIT 1")
sample_cuisine_raw = cursor.fetchone()[0]
print(f"Sample cuisine blob: {repr(sample_cuisine_raw)}")

# Parse cuisine
try:
    cuisines_list = json.loads(sample_cuisine_raw)
    if cuisines_list:
        sample_cuisine = cuisines_list[0]
    else:
        sample_cuisine = "Italian"
except:
    sample_cuisine = "Italian"

print(f"Selected test cuisine: '{sample_cuisine}'")
print()

# Step 2: Create a recommendation request
print("2. CREATING RECOMMENDATION REQUEST")
print("-" * 70)

test_request = RecommendRequest(
    location=sample_city_raw,
    budget="medium",
    cuisine=sample_cuisine,
    min_rating=0.0,
    top_k=5
)

print(f"Request object created:")
print(f"  location: '{test_request.location}'")
print(f"  budget: '{test_request.budget}'")
print(f"  cuisine: '{test_request.cuisine}'")
print()

# Step 3: Build preference profile
print("3. BUILDING PREFERENCE PROFILE")
print("-" * 70)

try:
    preference_service = PreferenceService()
    profile = preference_service.build_profile(test_request)
    
    print(f"✅ Profile built successfully:")
    print(f"  preferred_city: '{profile.preferred_city}'")
    print(f"  budget_bucket: '{profile.budget_bucket}'")
    print(f"  cuisine_tokens: {profile.cuisine_tokens}")
    print(f"  rating_floor: {profile.rating_floor}")
    print()
except Exception as e:
    print(f"❌ Failed to build profile: {e}")
    if hasattr(e, 'details'):
        print(f"   Details: {e.details}")
    exit(1)

# Step 4: Test database query directly
print("4. TESTING DATABASE QUERY DIRECTLY")
print("-" * 70)

test_city = profile.preferred_city
print(f"Querying for city: '{test_city}'")

# Test exact match
cursor.execute("SELECT COUNT(*) FROM restaurants WHERE city = ?", (test_city,))
exact_match = cursor.fetchone()[0]
print(f"  Exact match (city = '{test_city}'): {exact_match} restaurants")

# Test case-insensitive
cursor.execute("SELECT COUNT(*) FROM restaurants WHERE lower(city) = lower(?)", (test_city,))
case_insensitive = cursor.fetchone()[0]
print(f"  Case-insensitive (lower(city) = lower('{test_city}')): {case_insensitive} restaurants")

# Show actual city values
cursor.execute("SELECT DISTINCT city FROM restaurants WHERE lower(city) = lower(?) LIMIT 5", (test_city,))
matching_cities = cursor.fetchall()
print(f"  Matching city values in DB:")
for city, in matching_cities:
    print(f"    - '{city}'")

print()

# Step 5: Test retrieval service
print("5. TESTING CANDIDATE RETRIEVAL")
print("-" * 70)

try:
    candidate_service = CandidateRetrievalService()
    candidates, relaxations, pool_count = candidate_service.shortlist(
        profile=profile,
        pool_size=20
    )
    
    print(f"✅ Retrieval completed:")
    print(f"  Total pool: {pool_count} restaurants")
    print(f"  Candidates returned: {len(candidates)}")
    print(f"  Relaxations applied: {relaxations}")
    
    if candidates:
        print(f"\n  Top candidate:")
        top = candidates[0]
        print(f"    Name: {top.name}")
        print(f"    City: {top.city}")
        print(f"    Cuisines: {top.cuisines}")
        print(f"    Rating: {top.rating}")
        print(f"    Score: {top.score}")
    else:
        print(f"\n  ❌ NO CANDIDATES RETURNED!")
        print(f"\n  Debugging filtering logic:")
        
        # Manually test the filtering
        from src.phase3.services.retrieval import RestaurantQueryService
        query_service = RestaurantQueryService()
        city_rows = query_service.fetch_city_candidates(profile.preferred_city)
        print(f"    City candidates fetched: {len(city_rows)}")
        
        if city_rows:
            sample = city_rows[0]
            print(f"    Sample restaurant:")
            print(f"      Name: {sample['name']}")
            print(f"      City: {sample['city']}")
            print(f"      Cuisines: {sample['cuisines']}")
            print(f"      Budget: {sample['budget_bucket']}")
            print(f"      Rating: {sample['rating']}")
            
            print(f"\n    Checking filter conditions:")
            print(f"      Requested cuisine: {profile.cuisine_tokens}")
            print(f"      Restaurant cuisines: {sample['cuisines']}")
            requested_cuisines = {c.lower() for c in profile.cuisine_tokens}
            restaurant_cuisines = {c.lower() for c in sample['cuisines']}
            cuisine_match = requested_cuisines & restaurant_cuisines
            print(f"      Cuisine match: {cuisine_match}")
            print(f"      Budget match: {sample['budget_bucket']} vs requested {profile.budget_bucket}")
            print(f"      Rating check: {sample['rating']} >= {profile.rating_floor}")
        else:
            print(f"    ❌ No city candidates found!")
            print(f"    This means the city query is failing.")
            
except Exception as e:
    print(f"❌ Retrieval failed: {e}")
    import traceback
    traceback.print_exc()

print()

conn.close()

print("=" * 70)
print("DEBUG COMPLETE")
print("=" * 70)
