"""
Quick test to see the actual API response
"""
import requests
import json

API_BASE = "http://localhost:8000"

print("Testing /recommend endpoint...")
print("=" * 70)

# Test request
payload = {
    "location": "Banashankari",
    "budget": "medium",
    "cuisine": "Chinese",
    "min_rating": 0,
    "top_k": 5
}

print(f"\nRequest payload:")
print(json.dumps(payload, indent=2))

try:
    response = requests.post(
        f"{API_BASE}/recommend",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response Headers:")
    print(f"  X-Request-ID: {response.headers.get('X-Request-ID', 'N/A')}")
    print(f"  X-Processing-Time-Ms: {response.headers.get('X-Processing-Time-Ms', 'N/A')}")
    
    if response.ok:
        data = response.json()
        print(f"\n✅ Success! Response structure:")
        print(f"  status: {data.get('status')}")
        print(f"  profile: {type(data.get('profile')).__name__}")
        print(f"  recommendations: {type(data.get('recommendations')).__name__} with {len(data.get('recommendations', []))} items")
        print(f"  summary: {data.get('summary')[:100] if data.get('summary') else 'None'}...")
        print(f"  candidates: {len(data.get('candidates', []))} items")
        print(f"  notes: {data.get('notes')}")
        print(f"  metadata: {data.get('metadata', {})}")
        
        if data.get('recommendations'):
            print(f"\n📋 First recommendation:")
            rec = data['recommendations'][0]
            print(f"  {json.dumps(rec, indent=2)}")
        else:
            print(f"\n⚠️  RECOMMENDATIONS ARRAY IS EMPTY!")
            print(f"\nFull response:")
            print(json.dumps(data, indent=2))
    else:
        print(f"\n❌ Error response:")
        print(response.text)
        
except requests.exceptions.ConnectionError:
    print(f"\n❌ Cannot connect to {API_BASE}")
    print("Make sure the server is running: uvicorn src.api.main:app --reload --port 8000")
except Exception as e:
    print(f"\n❌ Error: {e}")
