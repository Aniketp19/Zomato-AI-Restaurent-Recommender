"""
Test Groq API connection directly to see what's failing
"""
import json
import urllib.request
import urllib.error
from src.phase0.core.config import settings

def test_groq_connection():
    """Test Groq API with a simple request."""
    print("=" * 60)
    print("Testing Groq API Connection")
    print("=" * 60)
    
    # Check API key
    print(f"\n1. Checking API Key:")
    if not settings.groq_api_key:
        print("   ERROR: GROQ_API_KEY is not configured!")
        return False
    print(f"   OK: API Key configured: {settings.groq_api_key[:20]}...")
    print(f"   OK: Model: {settings.groq_model}")
    
    # Test simple API call
    print(f"\n2. Testing API Call:")
    api_url = "https://api.groq.com/openai/v1/chat/completions"
    
    payload = {
        "model": settings.groq_model,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant. Return JSON only."},
            {"role": "user", "content": 'Return this JSON: {"test": "success", "message": "API is working"}'},
        ],
        "temperature": 0.2,
        "max_tokens": 100,
        "response_format": {"type": "json_object"},
    }
    
    body = json.dumps(payload).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {settings.groq_api_key}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }
    
    try:
        print(f"   Sending request to: {api_url}")
        print(f"   Model: {settings.groq_model}")
        print(f"   Payload size: {len(body)} bytes")
        
        request = urllib.request.Request(
            api_url,
            data=body,
            headers=headers,
            method="POST",
        )
        
        with urllib.request.urlopen(request, timeout=30) as response:
            print(f"   OK: Response status: {response.status}")
            raw = response.read().decode("utf-8")
            parsed = json.loads(raw)
            
            print(f"\n3. Response Details:")
            print(f"   Model used: {parsed.get('model', 'N/A')}")
            print(f"   Choices: {len(parsed.get('choices', []))}")
            
            if parsed.get('choices'):
                content = parsed["choices"][0]["message"]["content"]
                print(f"   Content: {content}")
                
                # Try to parse the JSON content
                try:
                    json_content = json.loads(content)
                    print(f"   OK: Valid JSON response!")
                    print(f"   JSON: {json.dumps(json_content, indent=2)}")
                except json.JSONDecodeError:
                    print(f"   WARNING: Content is not valid JSON")
            
            print(f"\nSUCCESS: Groq API is working correctly!")
            return True
            
    except urllib.error.HTTPError as e:
        print(f"\n   ERROR: HTTP Error: {e.code} {e.reason}")
        try:
            error_body = e.read().decode("utf-8")
            print(f"   Error details: {error_body}")
        except:
            pass
        return False
        
    except urllib.error.URLError as e:
        print(f"\n   ERROR: URL Error: {e.reason}")
        print(f"   This might be a network/connection issue")
        return False
        
    except Exception as e:
        print(f"\n   ERROR: Unexpected error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_recommendation_prompt():
    """Test with a real recommendation-style prompt."""
    print("\n" + "=" * 60)
    print("Testing Recommendation-Style Prompt")
    print("=" * 60)
    
    from src.phase0.llm.adapter import LLMClientAdapter
    
    adapter = LLMClientAdapter()
    
    test_prompt = """
You are ranking restaurant recommendations.

User preferences:
- Location: Banashankari
- Budget: medium (Rs 500-1500)
- Cuisine: Chinese
- Min rating: 0

Candidate restaurants:
1. ID: r1, Name: Jalsa, Cuisines: [Chinese, Mughlai], Rating: 4.2, Cost: 800
2. ID: r2, Name: China Garden, Cuisines: [Chinese], Rating: 4.0, Cost: 600
3. ID: r3, Name: Mainland China, Cuisines: [Chinese], Rating: 4.5, Cost: 1200

Return JSON with this structure:
{
  "recommendations": [
    {
      "restaurant_id": "r3",
      "name": "Mainland China",
      "cuisine": "Chinese",
      "rating": 4.5,
      "estimated_cost": 1200,
      "explanation": "Brief reason why this is ranked first"
    }
  ],
  "summary": "Overall recommendation summary"
}

Rank top 3 restaurants and explain each choice.
"""
    
    try:
        print("   Sending recommendation prompt...")
        response = adapter.generate(test_prompt)
        print(f"   OK: Response received: {len(response)} characters")
        print(f"\n   Response:\n{response}")
        
        # Try to parse as JSON
        try:
            parsed = json.loads(response)
            print(f"\n   OK: Valid JSON!")
            print(f"   Recommendations: {len(parsed.get('recommendations', []))}")
        except json.JSONDecodeError:
            print(f"\n   WARNING: Response is not valid JSON")
        
        return True
        
    except Exception as e:
        print(f"   ERROR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result1 = test_groq_connection()
    
    if result1:
        print("\n" + "=" * 60)
        input("Press Enter to test with recommendation prompt...")
        result2 = test_recommendation_prompt()
        
        if result2:
            print("\n" + "=" * 60)
            print("SUCCESS: All tests passed! Groq API is working.")
            print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("FAILED: Groq API test failed. Check the error above.")
        print("=" * 60)
