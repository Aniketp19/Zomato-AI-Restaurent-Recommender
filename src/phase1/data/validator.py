from __future__ import annotations

import pandas as pd

from src.phase1.models.restaurant import QualityReport


class DataValidator:
    def __init__(self, critical_null_threshold: float, max_duplicate_ratio: float) -> None:
        self.critical_null_threshold = critical_null_threshold
        self.max_duplicate_ratio = max_duplicate_ratio

    def validate(self, raw_df: pd.DataFrame, cleaned_df: pd.DataFrame) -> QualityReport:
        critical_columns = ["restaurant_id", "name", "city", "average_cost_for_two", "rating"]
        missing_columns = [c for c in critical_columns if c not in cleaned_df.columns]
        if missing_columns:
            raise ValueError(f"Missing critical columns after cleaning: {missing_columns}")

        critical_null_ratio = (
            cleaned_df[critical_columns].isnull().sum().sum()
            / max(1, len(cleaned_df) * len(critical_columns))
        )
        duplicate_ratio = cleaned_df.duplicated(subset=["name", "city"]).mean() if len(cleaned_df) else 0.0

        warnings: list[str] = []
        if duplicate_ratio > self.max_duplicate_ratio:
            warnings.append(
                f"High duplicate ratio detected: {duplicate_ratio:.2%} (threshold {self.max_duplicate_ratio:.2%})"
            )
        if cleaned_df["rating"].max() > 5 or cleaned_df["rating"].min() < 0:
            warnings.append("Rating values outside expected range were detected before clamping.")

        if critical_null_ratio > self.critical_null_threshold:
            raise ValueError(
                "Critical null ratio exceeded threshold: "
                f"{critical_null_ratio:.2%} > {self.critical_null_threshold:.2%}"
            )

        return QualityReport(
            raw_rows=len(raw_df),
            cleaned_rows=len(cleaned_df),
            dropped_rows=max(0, len(raw_df) - len(cleaned_df)),
            duplicate_ratio=float(duplicate_ratio),
            critical_null_ratio=float(critical_null_ratio),
            warnings=warnings,
            metadata={},
        )
