# 📚 Documentation and Helper Files Index

Welcome! This file helps you navigate all the documentation and helper files in this project.

## 🚀 Getting Started (Pick One)

Choose based on your preference:

1. **VISUAL_GUIDE.md** - Step-by-step guide with example outputs ⭐ **Recommended for first-time users**
2. **START_HERE.md** - Concise quick start guide
3. **README.md** - Full project documentation
4. **TROUBLESHOOTING.md** - Having issues? Start here

## 📖 Documentation Files

### Setup and Usage
- **VISUAL_GUIDE.md** - Illustrated step-by-step setup walkthrough
- **START_HERE.md** - Quick start guide with common commands
- **README.md** - Complete project documentation
- **QUICKSTART.md** - Ultra-fast getting started (minimal details)

### Help and Debugging
- **TROUBLESHOOTING.md** - Common issues and their solutions
- **REFERENCE_GUIDE.md** - (This file) Navigation guide

### Technical Documentation
- **docs/phase-wise-architecture.md** - Full system architecture
- **docs/api-spec.yaml** - API specification (OpenAPI format)

## 🛠️ Helper Scripts

### Setup and Testing
- **setup_and_start.bat** - One-click setup checker + server starter ⭐ **Easiest way**
- **start_server.bat** - Just start the server (no checks)
- **preflight_check.py** - Verify system is ready before starting

### Testing Tools
- **test_api.html** - Visual API endpoint tester (open in browser)
- **quick_api_test.py** - Command-line API endpoint tester
- **test_cuisines_parsing.py** - Debug cuisine data parsing
- **debug_recommend.py** - Trace recommendation flow end-to-end
- **investigate_db.py** - Inspect database contents
- **test_api.py** - Basic API request tester
- **test_fallback.py** - Test LLM fallback mechanism
- **test_recommend_api.py** - Test recommendation endpoint

## 🎯 Main Application Files

### Frontend
- **index.html** - Main web interface ⭐ **Open this to use the app**

### Backend Entry Point
- **src/phase0/api/main.py** - FastAPI application and endpoints

### Core Components
- **src/phase1/** - Data ingestion and cleaning
- **src/phase2/** - Preference intake and validation
- **src/phase3/** - Candidate retrieval and filtering
- **src/phase4/** - LLM ranking and explanations
- **src/phase5/** - (Covered in Phase 0 API layer)
- **src/services/** - Metadata and support services
- **src/api/** - Middleware and API utilities

## 🎯 Quick Reference by Task

### "I want to get started ASAP"
1. Run: `setup_and_start.bat`
2. Open: `index.html`
3. Done!

### "I want step-by-step instructions"
Read: **VISUAL_GUIDE.md**

### "Something isn't working"
1. Read: **TROUBLESHOOTING.md**
2. Run: `python preflight_check.py`
3. Open: `test_api.html` to diagnose

### "I want to understand the architecture"
Read: **docs/phase-wise-architecture.md**

### "I want to test the API manually"
1. Start server: `start_server.bat`
2. Open: `test_api.html` in browser
3. Or run: `python quick_api_test.py`

### "I want to debug why no recommendations appear"
1. Run: `python debug_recommend.py`
2. Check server logs for errors
3. Read: **TROUBLESHOOTING.md** → "No recommendations found"

### "I want to see what's in the database"
Run: `python investigate_db.py`

### "I want to develop/modify the code"
1. Read: **README.md** → "Development"
2. Read: **docs/phase-wise-architecture.md**
3. Check: **docs/api-spec.yaml** for API contracts

## 📊 File Purpose Quick Reference

| File | Purpose | When to Use |
|------|---------|-------------|
| setup_and_start.bat | Check + start server | First time or after problems |
| start_server.bat | Start server only | When you know it's ready |
| preflight_check.py | Verify prerequisites | Before starting |
| test_api.html | Visual API tester | Quick endpoint check |
| index.html | Main application | Using the app |
| VISUAL_GUIDE.md | Step-by-step setup | First time setup |
| TROUBLESHOOTING.md | Problem solving | When things break |
| README.md | Full documentation | Understanding the project |

## 🔗 External Resources

- **Groq API Docs:** https://console.groq.com/docs
- **FastAPI Docs:** https://fastapi.tiangolo.com
- **Dataset:** https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation

## 💡 Tips

1. **Always keep the server terminal open** - It shows important logs
2. **Use Ctrl+Shift+R in browser** - Hard refresh after code changes
3. **Check server logs first** - Most errors are visible there
4. **Start with preflight_check.py** - Saves time debugging
5. **Use test_api.html** - Fastest way to verify API health

## 🆘 Getting Help

If you're stuck:

1. **Check the logs** - Server terminal shows detailed errors
2. **Run diagnostics:**
   ```bash
   python preflight_check.py
   python quick_api_test.py
   python debug_recommend.py
   ```
3. **Read TROUBLESHOOTING.md** - Covers 90% of common issues
4. **Check browser console** - Press F12 → Console tab

## 📝 Notes

- All `.bat` files are for Windows. Mac/Linux users should run the Python commands directly.
- The `.env` file contains sensitive API keys - never commit it to version control.
- Database file (`data/restaurants.db`) is ~15MB - excluded from git by default.

---

**Quick Start Reminder:**
```bash
setup_and_start.bat    # Start server
# Then open index.html in browser
```

**Happy coding! 🎉**
