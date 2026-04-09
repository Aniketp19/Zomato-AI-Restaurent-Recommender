# 🎬 Visual Setup Guide

## Step-by-Step with Screenshots

### 📋 Prerequisites Check

Before starting, make sure you have:
- ✅ Python 3.8 or higher installed
- ✅ Internet connection (for first-time setup)
- ✅ A web browser (Chrome, Firefox, Edge)

**Verify Python:**
```bash
python --version
```
Should show: `Python 3.8.x` or higher

---

### 🔧 Step 1: Install Dependencies

Open Command Prompt or PowerShell in the project folder:

```bash
pip install -r requirements.txt
```

**What you'll see:**
```
Collecting fastapi
Collecting uvicorn
Collecting pydantic
...
Successfully installed fastapi-0.109.0 uvicorn-0.27.0 ...
```

⏱️ Takes about 1-2 minutes

---

### 🗄️ Step 2: Load the Database (First Time Only)

If `data/restaurants.db` doesn't exist, run:

```bash
python -m src.phase1.load_data
```

**What you'll see:**
```
📥 Downloading dataset from Hugging Face...
🧹 Cleaning and normalizing data...
💾 Saved 51,717 restaurants to database
✅ Quality report saved to data/quality_report.json
```

⏱️ Takes about 2-3 minutes
💾 Creates a ~15MB database file

**Skip this step if:** `data/restaurants.db` already exists

---

### ✅ Step 3: Run Pre-flight Check

Make sure everything is ready:

```bash
python preflight_check.py
```

**Expected output:**
```
🔍 Checking dependencies...
  ✅ fastapi
  ✅ uvicorn
  ✅ pydantic
  ...

🔍 Checking database...
  ✅ Database found (14.52 MB)
  ✅ 51,717 restaurants loaded

🔍 Checking environment configuration...
  ✅ .env file exists
  ✅ GROQ_API_KEY is set

🔍 Checking if port 8000 is available...
  ✅ Port 8000 is available

📊 Summary:
  ✅ PASS - Dependencies
  ✅ PASS - Database
  ✅ PASS - Environment
  ✅ PASS - Port

✅ All checks passed! You're ready to start.
```

**If anything fails:** See the error message and fix it before continuing

---

### 🚀 Step 4: Start the API Server

**Option A - Automated (Easiest):**
```bash
setup_and_start.bat
```

**Option B - Manual:**
```bash
python -m uvicorn src.phase0.api.main:app --reload --port 8000
```

**What you'll see:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345]
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
✅ Loaded 56 cities from database
✅ Loaded 129 cuisines from database
INFO:     Application startup complete.
```

**✅ Success indicators:**
- You see "Application startup complete"
- You see "Loaded X cities/cuisines"
- No red error messages

**⚠️ Keep this window open** - this is your server running!

---

### 🧪 Step 5: Test the API (Optional but Recommended)

**Option A - Visual test page:**
1. Open `test_api.html` in your browser
2. You'll see a test page load
3. Click "Test All Endpoints"
4. All tests should show green ✅

**Option B - Quick Python test:**
```bash
# Open a NEW terminal (keep the server running!)
python quick_api_test.py
```

**Expected output:**
```
Testing API Endpoints
============================================================

1. Testing /health endpoint:
   Status: 200
   Response: {
     "status": "ok",
     "timestamp": "2024-01-15T10:30:00"
   }

2. Testing /meta/cities endpoint:
   Status: 200
   Count: 56
   Sample cities: ['BTM', 'Banashankari', 'Bangalore', ...]

3. Testing /meta/cuisines endpoint:
   Status: 200
   Count: 129
   Sample cuisines: ['American', 'Asian', 'Bakery', ...]

4. Testing /meta/budgets endpoint:
   Status: 200
   Count: 3
   Budgets: [
     {"bucket": "low", ...},
     {"bucket": "medium", ...},
     {"bucket": "high", ...}
   ]
```

---

### 🌐 Step 6: Open the Frontend

**Two ways:**

**Method 1 - File Explorer:**
1. Navigate to the project folder
2. Find `index.html`
3. Double-click to open in your default browser

**Method 2 - Drag and Drop:**
1. Open your browser
2. Drag `index.html` into the browser window

**What you should see:**

1. **Page loads** with a beautiful gradient background
2. **Form appears** with 4 dropdowns:
   - Location (50+ cities)
   - Budget (Low/Medium/High)
   - Cuisine (100+ options)
   - Min Rating (0-5)
3. **No error messages**

**If you see an error:**
- "Failed to load form options" → Server not running
- Go back to Step 4 and make sure the server is running

---

### 🎯 Step 7: Get Your First Recommendation!

1. **Select preferences:**
   - Location: `Banashankari` (good test data)
   - Budget: `Medium`
   - Cuisine: `Chinese`
   - Min Rating: `0` (recommended for testing)

2. **Click "Find Restaurants"**

3. **See results:**
   - Loading spinner appears
   - 5 restaurant cards show up
   - Each card shows:
     - Restaurant name
     - Cuisine type
     - Rating (may be 0.0 in test data)
     - Cost for two
     - AI-generated explanation

---

### 🎉 Success!

You should now have:
- ✅ API server running on port 8000
- ✅ Frontend loading successfully
- ✅ Form populated with options
- ✅ Recommendations working

---

## 🐛 Common Issues and Fixes

### Issue: "Failed to load form options"

**Cause:** Server not running

**Fix:**
1. Check server window - is it still running?
2. Visit http://localhost:8000/health in browser
3. Should see `{"status":"ok",...}`
4. If not, restart server (Step 4)

---

### Issue: "No recommendations found"

**Causes:**
1. Min rating too high (many restaurants have 0.0)
2. No data for that city/cuisine combo

**Fix:**
1. Set min rating to 0
2. Try: Banashankari + Chinese + Medium
3. Run `python debug_recommend.py` to see what's happening

---

### Issue: Port 8000 already in use

**Fix:**
```bash
# Find the process
netstat -ano | findstr :8000

# Kill it (replace 12345 with actual PID)
taskkill /PID 12345 /F

# Or use a different port
python -m uvicorn src.phase0.api.main:app --reload --port 8001
```

If using port 8001, update line 383 in `index.html`:
```javascript
const API_BASE = 'http://localhost:8001';  // Changed from 8000
```

---

### Issue: Blank dropdown menus

**Causes:**
1. CORS error
2. Wrong API URL
3. Database empty

**Fix:**
1. Press F12 → Console tab → Check for errors
2. Make sure API_BASE in index.html is `http://localhost:8000`
3. Run `python test_cuisines_parsing.py` to check database
4. Hard refresh: Ctrl+Shift+R

---

## 📚 Next Steps

Once everything works:

1. **Try different cities:** Explore the 50+ locations
2. **Adjust preferences:** See how results change
3. **Check the LLM:** Look for AI-generated explanations
4. **Review the code:** Explore `src/` to understand the architecture
5. **Improve the data:** Fix 0.0 ratings and costs (see Phase 7 in docs)

---

## 🆘 Still Stuck?

Run the full diagnostic:

```bash
python preflight_check.py          # System check
python test_cuisines_parsing.py   # Database check
python debug_recommend.py          # Flow check
python quick_api_test.py          # API check
```

Or check:
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Detailed fixes
- [START_HERE.md](START_HERE.md) - Complete setup guide
- [README.md](README.md) - Full documentation

---

**Made with ❤️ for easy setup and testing**
