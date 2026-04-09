# 🎯 QUICK FIX - "Failed to load form options" Error

## Problem
The frontend (index.html) shows: **"Failed to load form options. Please ensure the API server is running at http://localhost:8000"**

## Root Cause
The API server is not running. The frontend needs the backend API to be active to load cities, cuisines, and budgets.

## Solution - Follow These Steps

### Step 1: Check Prerequisites
Run the pre-flight check:
```bash
python preflight_check.py
```

This will verify:
- ✅ All dependencies installed
- ✅ Database exists with data
- ✅ .env file configured
- ✅ Port 8000 available

### Step 2: Start the API Server

**Option A - Automated (Recommended):**
```bash
setup_and_start.bat
```

**Option B - Manual:**
```bash
python -m uvicorn src.phase0.api.main:app --reload --port 8000
```

You should see output like:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
✅ Loaded 56 cities from database
✅ Loaded 129 cuisines from database
```

### Step 3: Verify Server is Running

**Option A - Use the test page:**
1. Open `test_api.html` in your browser
2. Click "Test All Endpoints"
3. All tests should show ✅ Success

**Option B - Use curl/browser:**
- Visit http://localhost:8000/health in your browser
- You should see: `{"status":"ok","timestamp":"..."}`

**Option C - Use the test script:**
```bash
python quick_api_test.py
```

### Step 4: Open the Frontend
1. Open `index.html` in your browser
2. The form should load with all dropdown options
3. Select your preferences and get recommendations!

## Troubleshooting

### Server Won't Start

**Error: "ModuleNotFoundError: No module named 'fastapi'"**
```bash
pip install -r requirements.txt
```

**Error: "FileNotFoundError: data/restaurants.db"**
```bash
python -m src.phase1.load_data
```

**Error: "Port 8000 is already in use"**
```bash
# Find and kill the process
netstat -ano | findstr :8000
taskkill /PID <process_id> /F

# Or use a different port
python -m uvicorn src.phase0.api.main:app --reload --port 8001
```
(If using port 8001, update `API_BASE` in index.html line 383)

### Frontend Still Shows Error

**Clear browser cache:**
- Press `Ctrl + Shift + R` (hard reload)
- Or clear browser cache completely

**Check browser console:**
- Press `F12` to open developer tools
- Look at the Console tab for error messages
- Look at the Network tab to see if requests are failing

**CORS errors:**
- Make sure the server is running (it has CORS enabled by default)
- Check that you're using `localhost` not `127.0.0.1` (or vice versa)

### Database Issues

**No cities/cuisines showing:**
```bash
python test_cuisines_parsing.py
```

This will show what's in the database and how it's being parsed.

**Database corruption:**
```bash
# Delete and reload
del data\restaurants.db
python -m src.phase1.load_data
```

## Quick Test Command Chain

All in one (copy-paste):
```bash
python preflight_check.py && python -m uvicorn src.phase0.api.main:app --reload --port 8000
```

## Expected Output

When working correctly:

1. **Server terminal:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
✅ Loaded 56 cities from database
✅ Loaded 129 cuisines from database
INFO:     127.0.0.1:xxxxx - "GET /meta/cities HTTP/1.1" 200 OK
INFO:     127.0.0.1:xxxxx - "GET /meta/cuisines HTTP/1.1" 200 OK
INFO:     127.0.0.1:xxxxx - "GET /meta/budgets HTTP/1.1" 200 OK
```

2. **Browser (index.html):**
- Location dropdown populated with 50+ cities
- Cuisine dropdown populated with 100+ cuisines
- Budget dropdown showing Low/Medium/High options
- No error messages

3. **After submitting a search:**
- Loading spinner shows
- 5 restaurant cards appear with details
- Each card shows name, cuisine, rating, cost, explanation

## Files You Need

All created for you:
- ✅ `start_server.bat` - Start the API server
- ✅ `setup_and_start.bat` - Check everything then start
- ✅ `preflight_check.py` - Verify system is ready
- ✅ `test_api.html` - Visual API endpoint tester
- ✅ `quick_api_test.py` - Command-line API tester
- ✅ `test_cuisines_parsing.py` - Debug cuisine parsing
- ✅ `START_HERE.md` - Complete setup guide

## Still Having Issues?

Run this debug sequence:

```bash
# 1. Check system
python preflight_check.py

# 2. Test database
python test_cuisines_parsing.py

# 3. Test recommendation flow
python debug_recommend.py

# 4. Start server
python -m uvicorn src.phase0.api.main:app --reload --port 8000

# 5. In another terminal, test API
python quick_api_test.py
```

Compare your output with the expected output above.

## Success Checklist

- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Database exists with data (51,717 restaurants)
- [ ] .env file has GROQ_API_KEY
- [ ] Server started successfully
- [ ] http://localhost:8000/health returns {"status":"ok"}
- [ ] test_api.html shows all endpoints working
- [ ] index.html loads without errors
- [ ] Dropdowns populated with options
- [ ] Can submit and get recommendations

Once all checked, you're good to go! 🎉
