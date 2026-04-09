from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd


class DataWriter:
    def __init__(self, sqlite_path: Path) -> None:
        self.sqlite_path = sqlite_path

    def write(self, cleaned_df: pd.DataFrame) -> None:
        self.sqlite_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.sqlite_path) as conn:
            cleaned_df.to_sql("restaurants", conn, if_exists="replace", index=False)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_restaurants_city ON restaurants(city)")
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_restaurants_budget ON restaurants(budget_bucket)"
            )
            conn.execute("CREATE INDEX IF NOT EXISTS idx_restaurants_rating ON restaurants(rating)")

            meta = pd.DataFrame(
                {
                    "cities": [cleaned_df["city"].nunique()],
                    "budget_buckets": [cleaned_df["budget_bucket"].nunique()],
                    "average_rating": [cleaned_df["rating"].mean()],
                    "row_count": [len(cleaned_df)],
                }
            )
            meta.to_sql("dataset_metadata", conn, if_exists="replace", index=False)
