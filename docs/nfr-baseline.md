# Non-Functional Requirements Baseline

This baseline corresponds to Phase 0 implementation goals.

## Service targets
- **P95 `/recommend` latency**: <= 2500 ms (post-Phase 4 implementation)
- **P95 candidate retrieval latency**: <= 200 ms
- **Recommendation count default**: Top 5
- **Maximum acceptable API error rate**: <= 2% (5-minute window)

## Data quality targets
- **Critical null threshold**: <= 35%
- **Duplicate ratio warning threshold**: <= 40%
- **Rating range enforcement**: 0.0 to 5.0

## Reliability and observability
- Health endpoint available at `/health`.
- Ingestion must produce:
  - `data/restaurants.db`
  - `data/quality_report.json`
- Pipeline hard-fails if critical null threshold is breached.
