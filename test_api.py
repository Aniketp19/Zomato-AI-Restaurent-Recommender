"""
Test script to verify the Zomato AI Recommender setup.
Run this after starting the backend server.
"""

import requests
import sys

API_BASE = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("🏥 Testing /health endpoint...")
    try:
        response = requests.get(f"{API_BASE}/health")
        response.raise_for_status()
        data = response.json()
        print(f"   ✅ Health check passed: {data.get('status')}")
        print(f"   📋 App: {data.get('app_name')}")
        print(f"   🆔 Request ID: {data.get('request_id', 'N/A')}")
        return True
    except Exception as e:
        print(f"   ❌ Health check failed: {e}")
        return False

def test_meta_cities():
    """Test cities metadata endpoint"""
    print("\n🏙️  Testing /meta/cities endpoint...")
    try:
        response = requests.get(f"{API_BASE}/meta/cities")
        response.raise_for_status()
        data = response.json()
        print(f"   ✅ Found {data.get('count', 0)} cities")
        if data.get('cities'):
            print(f"   📍 Sample cities: {', '.join(data['cities'][:5])}")
        return True
    except Exception as e:
        print(f"   ❌ Cities endpoint failed: {e}")
        return False

def test_meta_cuisines():
    """Test cuisines metadata endpoint"""
    print("\n🍴 Testing /meta/cuisines endpoint...")
    try:
        response = requests.get(f"{API_BASE}/meta/cuisines")
        response.raise_for_status()
        data = response.json()
        print(f"   ✅ Found {data.get('count', 0)} cuisines")
        if data.get('cuisines'):
            print(f"   🍽️  Sample cuisines: {', '.join(data['cuisines'][:5])}")
        return True
    except Exception as e:
        print(f"   ❌ Cuisines endpoint failed: {e}")
        return False

def test_meta_budgets():
    """Test budgets metadata endpoint"""
    print("\n💰 Testing /meta/budgets endpoint...")
    try:
        response = requests.get(f"{API_BASE}/meta/budgets")
        response.raise_for_status()
        data = response.json()
        print(f"   ✅ Found {data.get('count', 0)} budget options")
        for budget in data.get('budgets', []):
            print(f"   💵 {budget['bucket'].upper()}: ₹{budget['approximate_cost_for_two_min']}-{budget['approximate_cost_for_two_max']}")
        return True
    except Exception as e:
        print(f"   ❌ Budgets endpoint failed: {e}")
        return False

def test_recommend():
    """Test recommendation endpoint"""
    print("\n🎯 Testing /recommend endpoint...")
    try:
        # First, get a valid city
        cities_response = requests.get(f"{API_BASE}/meta/cities")
        cities_data = cities_response.json()
        
        if not cities_data.get('cities'):
            print("   ⚠️  No cities available in database")
            return False
        
        # Get a valid cuisine
        cuisines_response = requests.get(f"{API_BASE}/meta/cuisines")
        cuisines_data = cuisines_response.json()
        
        if not cuisines_data.get('cuisines'):
            print("   ⚠️  No cuisines available in database")
            return False
        
        # Make recommendation request
        test_city = cities_data['cities'][0]
        test_cuisine = cuisines_data['cuisines'][0]
        
        print(f"   📍 Testing with city: {test_city}")
        print(f"   🍽️  Testing with cuisine: {test_cuisine}")
        
        payload = {
            "location": test_city,
            "budget": "medium",
            "cuisine": test_cuisine,
            "min_rating": 0,
            "top_k": 3
        }
        
        response = requests.post(
            f"{API_BASE}/recommend",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        data = response.json()
        
        recommendations = data.get('recommendations', [])
        metadata = data.get('metadata', {})
        
        print(f"   ✅ Got {len(recommendations)} recommendations")
        print(f"   ⏱️  Processing time: {metadata.get('processing_ms', 'N/A')}ms")
        print(f"   🤖 Fallback used: {metadata.get('fallback_used', 'N/A')}")
        print(f"   🆔 Request ID: {metadata.get('request_id', 'N/A')}")
        
        if recommendations:
            print(f"\n   🏆 Top recommendation: {recommendations[0].get('name')}")
            print(f"      ⭐ Rating: {recommendations[0].get('rating')}")
            print(f"      💵 Cost: ₹{recommendations[0].get('estimated_cost')}")
        
        return True
    except Exception as e:
        print(f"   ❌ Recommendation endpoint failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 70)
    print("🧪 Zomato AI Recommender - API Test Suite")
    print("=" * 70)
    print(f"\n🌐 Testing API at: {API_BASE}")
    print("⚠️  Make sure the backend server is running!\n")
    
    results = []
    
    # Run tests
    results.append(("Health Check", test_health()))
    results.append(("Cities Metadata", test_meta_cities()))
    results.append(("Cuisines Metadata", test_meta_cuisines()))
    results.append(("Budgets Metadata", test_meta_budgets()))
    results.append(("Recommendations", test_recommend()))
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 Test Summary")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your setup is working correctly.")
        print("👉 Next step: Open index.html in your browser")
        return 0
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")
        print("💡 Tips:")
        print("   - Ensure backend is running: uvicorn src.api.main:app --reload --port 8000")
        print("   - Ensure data pipeline ran: python -m src.data.pipeline")
        print("   - Check data/restaurants.db exists")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
