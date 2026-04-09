# Quick Test Script for API
import requests
import json

BASE_URL = "http://localhost:8000"

def test_endpoints():
    """Test all metadata endpoints."""
    
    print("Testing API Endpoints")
    print("=" * 60)
    
    # Test health
    print("\n1. Testing /health endpoint:")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test cities
    print("\n2. Testing /meta/cities endpoint:")
    try:
        response = requests.get(f"{BASE_URL}/meta/cities", timeout=5)
        print(f"   Status: {response.status_code}")
        data = response.json()
        print(f"   Count: {data.get('count', 0)}")
        print(f"   Sample cities: {data.get('cities', [])[:5]}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test cuisines
    print("\n3. Testing /meta/cuisines endpoint:")
    try:
        response = requests.get(f"{BASE_URL}/meta/cuisines", timeout=5)
        print(f"   Status: {response.status_code}")
        data = response.json()
        print(f"   Count: {data.get('count', 0)}")
        print(f"   Sample cuisines: {data.get('cuisines', [])[:10]}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test budgets
    print("\n4. Testing /meta/budgets endpoint:")
    try:
        response = requests.get(f"{BASE_URL}/meta/budgets", timeout=5)
        print(f"   Status: {response.status_code}")
        data = response.json()
        print(f"   Count: {data.get('count', 0)}")
        print(f"   Budgets: {json.dumps(data.get('budgets', []), indent=2)}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("Test Complete")

if __name__ == "__main__":
    test_endpoints()
