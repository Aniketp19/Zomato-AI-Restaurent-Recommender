import sqlite3
import json

# Test database and cuisines parsing
db_path = "data/restaurants.db"

with sqlite3.connect(db_path) as conn:
    # Check database structure
    print("Database Tables:")
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
    print([row[0] for row in cursor.fetchall()])
    
    # Check sample cuisines
    print("\nSample Cuisines (first 5 rows):")
    cursor = conn.execute("SELECT cuisines FROM restaurants LIMIT 5")
    for row in cursor.fetchall():
        print(f"  Raw: {repr(row[0])}")
        if row[0]:
            try:
                parsed = json.loads(row[0])
                print(f"  Parsed: {parsed}")
            except:
                print(f"  Not JSON, trying split: {row[0].split(',')}")
    
    # Try to parse all cuisines
    print("\nParsing all cuisines...")
    cursor = conn.execute("SELECT DISTINCT cuisines FROM restaurants WHERE cuisines IS NOT NULL")
    all_cuisines = set()
    errors = 0
    
    for row in cursor.fetchall():
        cuisines_str = row[0]
        if cuisines_str:
            try:
                # Try JSON parsing first
                cuisines_list = json.loads(cuisines_str)
                if isinstance(cuisines_list, list):
                    for c in cuisines_list:
                        c_clean = str(c).strip().strip('"').strip("'").strip()
                        if c_clean:
                            all_cuisines.add(c_clean)
            except json.JSONDecodeError:
                # Fall back to comma-separated
                cuisines = [c.strip().strip('"').strip("'").strip() for c in cuisines_str.split(",")]
                cuisines = [c for c in cuisines if c]
                all_cuisines.update(cuisines)
            except Exception as e:
                errors += 1
    
    print(f"\nTotal unique cuisines: {len(all_cuisines)}")
    print(f"Parsing errors: {errors}")
    print(f"Sample cuisines: {sorted(list(all_cuisines))[:15]}")
