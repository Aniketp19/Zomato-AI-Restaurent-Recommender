# Quick Start Guide - Zomato AI Recommender

## 🚀 Get Started in 3 Steps

### Step 1: Setup Backend (First Time Only)

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Configure environment (copy .env.example to .env)
# Edit GROQ_API_KEY if you want LLM ranking, otherwise fallback will work

# 3. Load restaurant data
python -m src.data.pipeline
```

**Expected output:**
- ✅ `data/restaurants.db` created
- ✅ `data/quality_report.json` generated

---

### Step 2: Start the Backend Server

```bash
uvicorn src.api.main:app --reload --port 8000
```

**Server running at:** http://localhost:8000

**Test it:**
```bash
# Health check
curl http://localhost:8000/health

# Get cities
curl http://localhost:8000/meta/cities
```

---

### Step 3: Open the Frontend

**Option A - Double Click:**
- Simply double-click `index.html` in your file explorer

**Option B - From Browser:**
- Open your browser
- File → Open File → Select `index.html`

**Option C - From Terminal:**
```bash
# Windows
start index.html

# Mac
open index.html

# Linux
xdg-open index.html
```

---

## 🎯 Testing the Complete Flow

1. **Open `index.html` in browser**
2. **Select preferences:**
   - Location: Mumbai (or any city from dropdown)
   - Budget: Medium
   - Cuisine: Italian
   - Min Rating: 3.5 (optional)
   - Number of Recommendations: 5

3. **Click "Get Recommendations"**

4. **View results:**
   - AI-generated summary
   - Top restaurant recommendations
   - Explanations for each recommendation
   - Request metadata (processing time, request ID, etc.)

---

## 🔍 What to Look For

### ✅ Success Indicators

1. **Form loads with real data:**
   - Cities dropdown populated
   - Cuisines dropdown populated
   - Budget options show price ranges

2. **Recommendations appear:**
   - Restaurant cards with rankings
   - AI explanations for each choice
   - Processing time shown
   - Request ID displayed

3. **Headers in browser DevTools:**
   - `X-Request-ID`: Unique identifier
   - `X-Processing-Time-Ms`: Processing time

### ❌ Common Issues

**"Failed to load form options"**
- ✅ Backend not running → Start backend (Step 2)
- ✅ Wrong port → Check backend is on port 8000

**"No recommendations found"**
- ✅ Try different city/cuisine combination
- ✅ Lower minimum rating
- ✅ Ensure data pipeline ran successfully

**CORS errors**
- ✅ Backend should have CORS middleware (already added)
- ✅ Use modern browser (Chrome, Firefox, Edge)

---

## 📊 Features to Test

### 1. Metadata Endpoints
```bash
# Get all cities
curl http://localhost:8000/meta/cities

# Get all cuisines
curl http://localhost:8000/meta/cuisines

# Get budget options
curl http://localhost:8000/meta/budgets
```

### 2. Recommendation Endpoint
```bash
curl -X POST http://localhost:8000/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "location": "Mumbai",
    "budget": "medium",
    "cuisine": "Italian",
    "min_rating": 3.5,
    "top_k": 5
  }'
```

### 3. Request Tracking
- Every request gets a unique `request_id`
- Processing time tracked in milliseconds
- Check response headers and body

### 4. LLM Ranking
- **With Groq API Key:** AI-generated explanations
- **Without API Key:** Deterministic fallback (still works!)
- Metadata shows `fallback_used: true/false`

---

## 🎨 UI Features

- **Dynamic Forms:** Dropdowns populated from real database
- **Loading States:** Spinner while fetching recommendations
- **Error Handling:** Clear error messages
- **Responsive Design:** Works on desktop and mobile
- **Rich Display:**
  - Restaurant rankings (1, 2, 3...)
  - Star ratings with color coding
  - Cost information
  - AI explanations
  - Request metadata

---

## 🔧 Development Tips

### Backend Development
```bash
# Run with auto-reload
uvicorn src.api.main:app --reload --port 8000 --log-level debug
```

### View Logs
- Backend logs show in terminal
- Frontend logs in browser DevTools (F12)

### Test Different Scenarios
1. **No API Key:** Fallback ranking works
2. **Different Cities:** Try Mumbai, Delhi, Bangalore
3. **Various Cuisines:** Italian, Chinese, North Indian
4. **Rating Filters:** High (4+), Medium (3+), Low (2+)
5. **Multiple Recommendations:** 1-10 results

---

## 📝 API Response Example

```json
{
  "status": "accepted",
  "profile": {
    "preferred_city": "Mumbai",
    "budget_bucket": "medium"
  },
  "recommendations": [
    {
      "restaurant_id": "123",
      "name": "Pizza Paradise",
      "cuisine": "Italian",
      "rating": 4.2,
      "estimated_cost": 800,
      "explanation": "Perfect match for your medium budget..."
    }
  ],
  "summary": "Here are 5 Italian restaurants in Mumbai...",
  "metadata": {
    "request_id": "abc-123-def-456",
    "processing_ms": 1234,
    "fallback_used": false,
    "candidate_count": 20
  }
}
```

---

## ✨ Next Steps

**Phase 7 - Testing:**
- Add unit tests
- Integration tests
- Performance benchmarks

**Phase 8 - Production:**
- Docker containerization
- Production deployment
- Monitoring setup

**Enhancements:**
- React frontend (optional)
- User authentication
- Favorites/history
- Caching layer

---

## 🆘 Need Help?

1. **Check backend logs** in terminal
2. **Check browser console** (F12) for frontend errors
3. **Verify data exists** in `data/restaurants.db`
4. **Test API directly** with curl commands
5. **Review `README.md`** for detailed setup

---

## ✅ You're All Set!

Your Zomato AI Recommender is ready for end-to-end testing. Enjoy exploring the recommendations! 🎉
