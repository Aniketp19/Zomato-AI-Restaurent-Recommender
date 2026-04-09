# 🚀 Quick Start Guide - Zomato AI Recommender

## Prerequisites
- Python 3.8+ installed
- Internet connection for first-time setup

## Step 1: Install Dependencies

Open Command Prompt or PowerShell in the project directory and run:

```bash
pip install -r requirements.txt
```

## Step 2: Configure Environment

Create a `.env` file in the project root (if not exists):

```bash
# Copy the example file
copy .env.example .env
```

Make sure your `.env` file has:
```
GROQ_API_KEY=gsk_YOUR_API_KEY_HERE
GROQ_MODEL=llama-3.1-8b-instant
SQLITE_PATH=data/restaurants.db
```

## Step 3: Load Data (First Time Only)

If you haven't loaded the restaurant data yet:

```bash
python -m src.phase1.load_data
```

This will download the Zomato dataset and populate the database.

## Step 4: Start the API Server

### Option A: Using the batch script (Recommended)
```bash
start_server.bat
```

### Option B: Manual start
```bash
python -m uvicorn src.phase0.api.main:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## Step 5: Test the API

### Quick Test
Open a new terminal and run:
```bash
python quick_api_test.py
```

Or use the batch file:
```bash
test_api_quick.bat
```

### Manual Test with curl
```bash
curl http://localhost:8000/health
curl http://localhost:8000/meta/cities
curl http://localhost:8000/meta/cuisines
curl http://localhost:8000/meta/budgets
```

## Step 6: Open the Frontend

Open `index.html` in your web browser:
- Double-click the file, OR
- Right-click → Open with → Your browser

The page should:
1. Load the form with dropdowns populated from the API
2. Allow you to select location, budget, cuisine, and rating
3. Submit and get restaurant recommendations

## Troubleshooting

### Error: "Failed to load form options"

**Cause:** API server is not running or not accessible.

**Solutions:**
1. Check if the server is running (you should see the Uvicorn output)
2. Make sure the port 8000 is not blocked
3. Try accessing http://localhost:8000/health in your browser
4. Check the server terminal for error messages

### Error: "ModuleNotFoundError"

**Cause:** Dependencies not installed.

**Solution:**
```bash
pip install -r requirements.txt
```

### Error: "Database not found"

**Cause:** Data not loaded yet.

**Solution:**
```bash
python -m src.phase1.load_data
```

### Error: "No recommendations found"

**Possible causes:**
1. **Too high min_rating**: Try setting min_rating to 0
2. **No data for that location**: Try a different city like "Banashankari"
3. **Cuisine mismatch**: Make sure you select a cuisine from the dropdown

**Debug:**
```bash
python debug_recommend.py
```

### CORS Errors in Browser Console

**Cause:** CORS middleware not configured or server not running.

**Solution:** 
1. Make sure you start the server (it has CORS enabled by default)
2. Clear browser cache (Ctrl+Shift+R)

### Port 8000 Already in Use

**Solution:**
1. Find the process:
   ```bash
   netstat -ano | findstr :8000
   ```
2. Kill it:
   ```bash
   taskkill /PID <process_id> /F
   ```
3. Or use a different port:
   ```bash
   python -m uvicorn src.phase0.api.main:app --reload --port 8001
   ```
   (Then update the frontend URL in index.html)

## Testing Recommendations

Good test inputs:
- **Location:** Banashankari (has 906 restaurants)
- **Budget:** medium
- **Cuisine:** Chinese (widely available)
- **Min Rating:** 0 (since many restaurants have 0.0 rating in test data)

## API Endpoints

- `GET /health` - Health check
- `GET /meta/cities` - Available cities
- `GET /meta/cuisines` - Available cuisines
- `GET /meta/budgets` - Budget options
- `POST /recommend` - Get recommendations

Example recommendation request:
```json
{
  "location": "Banashankari",
  "budget": "medium",
  "cuisine": "Chinese",
  "min_rating": 0,
  "top_k": 5
}
```

## Next Steps

- Improve LLM integration (currently using fallback)
- Add data quality improvements (fix 0.0 ratings and costs)
- Add caching for better performance
- Deploy to production

## Support

Check the debug scripts:
- `investigate_db.py` - Inspect database contents
- `debug_recommend.py` - Trace recommendation flow
- `quick_api_test.py` - Test API endpoints
- `test_cuisines_parsing.py` - Test cuisine parsing

For more details, see `README.md` or `docs/api-spec.yaml`.
