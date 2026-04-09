@echo off
echo Testing API endpoints...
echo.
echo Testing /health endpoint:
curl http://localhost:8000/health
echo.
echo.
echo Testing /meta/cities endpoint:
curl http://localhost:8000/meta/cities
echo.
echo.
echo Testing /meta/cuisines endpoint:
curl http://localhost:8000/meta/cuisines
echo.
echo.
echo Testing /meta/budgets endpoint:
curl http://localhost:8000/meta/budgets
echo.
pause
