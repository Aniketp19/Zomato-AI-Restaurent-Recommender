# Zomato AI Recommender

Phase 0 through Phase 6 (MVP UI) backend and frontend implementation based on `docs/phase-wise-architecture.md`.

## 🚀 Quick Start (3 Steps)

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the server:**
   ```bash
   setup_and_start.bat
   ```
   (Or manually: `python -m uvicorn src.phase0.api.main:app --reload --port 8000`)

3. **Open the app:**
   - Open `index.html` in your browser
   - Select location, budget, cuisine → Get recommendations!

**Having issues?** See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) or [START_HERE.md](START_HERE.md)

**Test the API:** Open `test_api.html` in your browser to verify endpoints are working.

## Implemented
- Project scaffold with modular `src/` layout.
- Environment-driven configuration via `.env`.
- Initial API contract (`docs/api-spec.yaml`) and `/health` endpoint.
- Phase 2 preference intake endpoint:
  - `POST /recommend`
  - request validation and normalization
  - structured `400` errors with suggestions for unknown location/cuisine
- Phase 3 candidate retrieval/ranking:
  - city/budget/rating/cuisine filtering from SQLite
  - constraint relaxation when result pool is sparse
  - deterministic weighted scoring and ranked shortlist
  - response contract ready for Groq LLM ranking in next phase
- Phase 4 Groq LLM ranking:
  - prompt builder from Phase 3 candidates
  - Groq-backed `LLMClientAdapter` with **Cloudflare bypass** (User-Agent header fix)
  - structured JSON parsing and grounding guard
  - deterministic fallback when LLM is unavailable/invalid
  - **✅ FIXED:** LLM now working - AI generates unique explanations for each recommendation
- **Phase 5 orchestration refinements**:
  - **Request ID tracking** for every API call via middleware
  - **Processing time tracking** (ms) included in responses
  - **Metadata endpoints**: `/meta/cities`, `/meta/cuisines`, `/meta/budgets`
  - Response headers: `X-Request-ID`, `X-Processing-Time-Ms`
- **Phase 6 Basic UI (MVP)**:
  - Single-page HTML/CSS/JavaScript interface
  - Dynamic form population from metadata endpoints
  - Real-time recommendation display with AI explanations
  - Error handling and loading states
  - Responsive design for desktop and mobile
- Data ingestion pipeline:
  - Hugging Face dataset loading
  - cleaning/normalization
  - quality validation
  - SQLite persistence + indexes
  - quality report artifact

## Setup

### 1. Backend Setup
1. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and update values:
   ```bash
   copy .env.example .env  # Windows
   cp .env.example .env    # Mac/Linux
   ```

4. Run the data ingestion pipeline (first time only):
   ```bash
   python -m src.data.pipeline
   ```
   This will create:
   - `data/restaurants.db` - SQLite database with restaurant data
   - `data/quality_report.json` - Data quality metrics

### 2. Start the Backend Server
```bash
uvicorn src.api.main:app --reload --port 8000
```

The API will be available at: `http://localhost:8000`

### 3. Open the Frontend
Simply open `index.html` in your browser:
- **Windows**: Double-click `index.html` or right-click → Open with → Browser
- **Mac/Linux**: Open from terminal: `open index.html` (Mac) or `xdg-open index.html` (Linux)
- **Or**: Navigate to `file:///path/to/zomato-pro/index.html` in your browser

The UI will automatically connect to the backend at `http://localhost:8000`

## API Endpoints
- `GET /health` - Health check with request tracking
- `POST /recommend` - Get AI-powered restaurant recommendations
- `GET /meta/cities` - List all available cities
- `GET /meta/cuisines` - List all available cuisines
- `GET /meta/budgets` - List budget options with ranges

## Testing End-to-End

### Quick API Test
```bash
# Test all metadata endpoints
python quick_api_test.py

# Or open visual tester in browser
# Open: test_api.html
```

### Test LLM Integration
```bash
# Test Groq API connection
python test_groq_api.py

# Test full LLM ranking flow
python test_llm_ranking.py
```

### Test Full Recommendation Flow
1. **Start the backend** (see above)
2. **Open index.html** in your browser
3. **Fill out the form**:
   - Select a location (populated from your database)
   - Choose a budget tier
   - Pick a cuisine type
   - Optionally set minimum rating and additional preferences
4. **Click "Get Recommendations"**
5. **View results** with **AI-generated explanations** from Groq LLM

**Expected:**
- Each restaurant has a unique AI-written explanation
- Summary paragraph explains the overall recommendations
- No "fallback" messages (LLM is now working!)
- **Real ratings** (0-5 scale) and **real costs** (₹100-₹5000+)

## Troubleshooting

### "Failed to load form options"
- Ensure the backend server is running at `http://localhost:8000`
- Check if data ingestion completed successfully
- Verify `data/restaurants.db` exists

### All restaurants showing 0.0 rating or ₹0 cost
- **FIXED**: Data ingestion now correctly maps `rate` and `approx_cost(for two people)` columns
- If you still see zeros, reload data: `python -m src.phase1.data.pipeline`
- Verify: Run `python investigate_db.py` to check database values

### No recommendations returned
- Try different location/cuisine combinations
- Lower the minimum rating requirement
- Check that the database has data for your selected city

### CORS errors in browser console
- The backend now includes CORS middleware
- If issues persist, ensure you're using a modern browser

### LLM fallback messages appearing
- **FIXED**: This was caused by Cloudflare blocking the API (HTTP 403)
- Solution: Added User-Agent header to bypass bot detection
- Verify fix: Run `python test_llm_ranking.py` - should show AI explanations
- If still seeing fallback, check `.env` has valid GROQ_API_KEY

## Project Structure
```
.
├── src/
│   ├── api/              # API layer
│   │   ├── middleware.py # Request tracking
│   │   └── main.py       # Exported API (imports from phase0)
│   ├── services/         # Business logic
│   │   ├── metadata.py   # Metadata queries
│   │   └── preferences.py
│   ├── models/           # Data models
│   │   ├── metadata.py   # Metadata response models
│   │   └── ...
│   ├── phase0-5/         # Phase implementations
│   └── data/             # Data pipeline
├── docs/                 # Documentation
├── data/                 # Generated data
│   ├── restaurants.db    # SQLite database
│   └── quality_report.json
├── tests/                # Test suite
├── index.html            # Frontend UI
└── requirements.txt      # Python dependencies
```

## Next Steps
- Phase 7: Add comprehensive test suite
- Phase 8: Production deployment and monitoring
- Enhance UI with React (optional)
- Add user authentication
- Implement caching for better performance
