"""
Database investigation script to debug the "No Recommendations Found" issue.
"""
import sqlite3
from pathlib import Path

DB_PATH = Path("data/restaurants.db")

print("=" * 70)
print("DATABASE INVESTIGATION REPORT")
print("=" * 70)

if not DB_PATH.exists():
    print(f"❌ ERROR: Database not found at {DB_PATH}")
    exit(1)

print(f"✅ Database found at: {DB_PATH}")
print()

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 1. Check total restaurant count
print("1. TOTAL RESTAURANT COUNT")
print("-" * 70)
cursor.execute("SELECT COUNT(*) FROM restaurants")
total = cursor.fetchone()[0]
print(f"Total restaurants in database: {total}")
print()

# 2. Check if Indiranagar exists
print("2. INDIRANAGAR SPECIFIC CHECK")
print("-" * 70)
cursor.execute("SELECT COUNT(*) FROM restaurants WHERE city = 'Indiranagar'")
count = cursor.fetchone()[0]
print(f"Restaurants in 'Indiranagar' (exact match): {count}")
cursor.execute("SELECT COUNT(*) FROM restaurants WHERE city LIKE '%Indiranagar%'")
count_like = cursor.fetchone()[0]
print(f"Restaurants with 'Indiranagar' in city (LIKE): {count_like}")
print()

# 3. Check actual city values
print("3. ACTUAL CITY VALUES IN DATABASE")
print("-" * 70)
cursor.execute("SELECT DISTINCT city, COUNT(*) as count FROM restaurants GROUP BY city ORDER BY count DESC LIMIT 20")
cities = cursor.fetchall()
print(f"Top 20 cities by restaurant count:")
for city, count in cities:
    print(f"  - '{city}': {count} restaurants")
print()

# 4. Check cuisine format
print("4. CUISINE FORMAT CHECK")
print("-" * 70)
cursor.execute("SELECT cuisines FROM restaurants LIMIT 5")
cuisines_sample = cursor.fetchall()
print("Sample cuisine values (first 5):")
for i, (cuisines,) in enumerate(cuisines_sample, 1):
    print(f"  {i}. {repr(cuisines)}")
print()

# 5. Check budget_bucket values
print("5. BUDGET BUCKET VALUES")
print("-" * 70)
cursor.execute("SELECT DISTINCT budget_bucket, COUNT(*) FROM restaurants GROUP BY budget_bucket")
budgets = cursor.fetchall()
print("Budget distribution:")
for bucket, count in budgets:
    print(f"  - {bucket}: {count} restaurants")
print()

# 6. Check rating range
print("6. RATING DISTRIBUTION")
print("-" * 70)
cursor.execute("SELECT MIN(rating), MAX(rating), AVG(rating) FROM restaurants")
min_r, max_r, avg_r = cursor.fetchone()
print(f"Rating range: {min_r:.2f} - {max_r:.2f} (avg: {avg_r:.2f})")
cursor.execute("SELECT COUNT(*) FROM restaurants WHERE rating >= 3.0")
count_good = cursor.fetchone()[0]
print(f"Restaurants with rating >= 3.0: {count_good}")
print()

# 7. Sample full record
print("7. SAMPLE RESTAURANT RECORD")
print("-" * 70)
cursor.execute("SELECT * FROM restaurants LIMIT 1")
columns = [desc[0] for desc in cursor.description]
record = cursor.fetchone()
print("Columns and sample values:")
for col, val in zip(columns, record):
    print(f"  {col}: {repr(val)}")
print()

# 8. Test a realistic query
print("8. TEST REALISTIC QUERY")
print("-" * 70)
# Get first city
cursor.execute("SELECT DISTINCT city FROM restaurants LIMIT 1")
test_city = cursor.fetchone()[0]
print(f"Testing with city: '{test_city}'")

# Try query similar to what the app would do
query = """
SELECT * FROM restaurants 
WHERE city = ? 
  AND budget_bucket = 'medium'
  AND rating >= 0
LIMIT 5
"""
cursor.execute(query, (test_city,))
results = cursor.fetchall()
print(f"Query: {query}")
print(f"Results: {len(results)} restaurants found")
if results:
    print("\nSample result:")
    for col, val in zip(columns, results[0]):
        print(f"  {col}: {repr(val)}")
print()

# 9. Check for NULL or empty values
print("9. DATA QUALITY CHECK")
print("-" * 70)
cursor.execute("SELECT COUNT(*) FROM restaurants WHERE city IS NULL OR city = ''")
null_city = cursor.fetchone()[0]
print(f"Restaurants with NULL/empty city: {null_city}")
cursor.execute("SELECT COUNT(*) FROM restaurants WHERE cuisines IS NULL OR cuisines = ''")
null_cuisine = cursor.fetchone()[0]
print(f"Restaurants with NULL/empty cuisines: {null_cuisine}")
print()

conn.close()

print("=" * 70)
print("INVESTIGATION COMPLETE")
print("=" * 70)
print("\n💡 KEY FINDINGS:")
print(f"  - Total restaurants: {total}")
print(f"  - City values are stored as: {cities[0][0] if cities else 'N/A'}")
print(f"  - Cuisine format: JSON array strings")
print("  - Check if frontend city names match database city names!")
