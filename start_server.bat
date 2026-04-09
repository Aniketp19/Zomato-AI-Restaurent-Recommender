@echo off
echo Starting Zomato Recommender API Server...
echo.
python -m uvicorn src.phase0.api.main:app --reload --port 8000
