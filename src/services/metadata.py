import json
import sqlite3
from pathlib import Path


class MetadataService:
    """Service to retrieve available options from the database."""

    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path

    def get_available_cities(self) -> list[str]:
        """Retrieve distinct cities from the database."""
        if not self.db_path.exists():
            print(f"⚠️  Database not found at: {self.db_path}")
            return []
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT DISTINCT city FROM restaurants WHERE city IS NOT NULL ORDER BY city"
            )
            cities = [row[0] for row in cursor.fetchall()]
            print(f"✅ Loaded {len(cities)} cities from database")
            return cities

    def get_available_cuisines(self) -> list[str]:
        """Retrieve distinct cuisines from the database."""
        if not self.db_path.exists():
            print(f"⚠️  Database not found at: {self.db_path}")
            return []
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT DISTINCT cuisines FROM restaurants WHERE cuisines IS NOT NULL"
            )
            # Cuisines are stored as JSON arrays
            all_cuisines = set()
            for row in cursor.fetchall():
                cuisines_str = row[0]
                if cuisines_str:
                    try:
                        # Try JSON parsing first (e.g., '["Chinese", "Italian"]')
                        cuisines_list = json.loads(cuisines_str)
                        if isinstance(cuisines_list, list):
                            for c in cuisines_list:
                                c_clean = str(c).strip().strip('"').strip("'").strip()
                                if c_clean:
                                    all_cuisines.add(c_clean)
                    except json.JSONDecodeError:
                        # Fall back to comma-separated parsing
                        cuisines = [c.strip() for c in cuisines_str.split(",")]
                        cuisines = [c.strip('"').strip("'").strip() for c in cuisines]
                        cuisines = [c for c in cuisines if c]
                        all_cuisines.update(cuisines)
            
            result = sorted(list(all_cuisines))
            print(f"✅ Loaded {len(result)} cuisines from database")
            return result

    def get_budget_options(self) -> list[dict[str, str | int]]:
        """Return available budget buckets with their cost ranges."""
        # These are defined by the system's budget categorization
        budget_buckets = [
            {
                "bucket": "low",
                "description": "Budget-friendly dining",
                "approximate_cost_for_two_min": 0,
                "approximate_cost_for_two_max": 500,
            },
            {
                "bucket": "medium",
                "description": "Mid-range dining",
                "approximate_cost_for_two_min": 500,
                "approximate_cost_for_two_max": 1500,
            },
            {
                "bucket": "high",
                "description": "Premium dining experience",
                "approximate_cost_for_two_min": 1500,
                "approximate_cost_for_two_max": 10000,
            },
        ]
        
        return budget_buckets
