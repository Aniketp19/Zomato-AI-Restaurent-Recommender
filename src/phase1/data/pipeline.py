from __future__ import annotations

import json
from pathlib import Path

from src.phase0.core.config import settings
from src.phase1.data.cleaner import DataCleaner
from src.phase1.data.loader import DatasetLoader, DatasetRef
from src.phase1.data.validator import DataValidator
from src.phase1.data.writer import DataWriter


def run_ingestion() -> Path:
    loader = DatasetLoader(
        DatasetRef(dataset_id=settings.hf_dataset_id, split=settings.hf_dataset_split)
    )
    cleaner = DataCleaner()
    validator = DataValidator(
        critical_null_threshold=settings.critical_null_threshold,
        max_duplicate_ratio=settings.max_allowed_duplicate_ratio,
    )
    writer = DataWriter(settings.sqlite_file)

    raw_df = loader.load()
    cleaned_df = cleaner.clean(raw_df)
    report = validator.validate(raw_df=raw_df, cleaned_df=cleaned_df)
    writer.write(cleaned_df=cleaned_df)

    report_path = Path("data/quality_report.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report.model_dump_json(indent=2), encoding="utf-8")
    return report_path


if __name__ == "__main__":
    output = run_ingestion()
    print(json.dumps({"status": "ok", "quality_report": str(output)}, indent=2))
