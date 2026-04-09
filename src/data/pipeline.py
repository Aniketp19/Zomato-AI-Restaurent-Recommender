from src.phase1.data.pipeline import run_ingestion


if __name__ == "__main__":
    import json

    output = run_ingestion()
    print(json.dumps({"status": "ok", "quality_report": str(output)}, indent=2))
