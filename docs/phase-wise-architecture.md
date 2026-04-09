# Phase-Wise Architecture: AI-Powered Restaurant Recommendation System

This document expands the architecture for each project phase from problem definition to production deployment.

---

## 1) Target Architecture (High Level)

### Core layers
- **Data Layer**: dataset ingestion, cleaning, normalized storage, metadata indexing.
- **Application Layer**: preference normalization, candidate retrieval, ranking orchestration.
- **LLM Layer**: prompt construction, response validation, explanation generation.
- **Experience Layer**: API contracts and frontend rendering.
- **Operations Layer**: testing, monitoring, deployment, and cost controls.

### End-to-end flow
1. Load and preprocess Zomato dataset.
2. Persist standardized restaurant records.
3. Accept user preferences.
4. Retrieve/filter candidates via deterministic rules.
5. Ask LLM to rank and explain top choices.
6. Return structured recommendations to UI.
7. Track latency, quality, and failures.

---

## 2) Phase 0 - Foundation and Scope

### Goal
Establish project boundaries, tech stack, and baseline interfaces before implementation.

### Architecture decisions
- **Backend**: FastAPI (Python) for rapid API + data workflows.
- **Storage**: SQLite for local MVP; Postgres for production.
- **Data tooling**: Pandas for preprocessing.
- **LLM provider abstraction**: wrapper service so provider can be swapped.
- **Frontend**: React for production UX (or Streamlit as MVP accelerator).

### Key deliverables
- Project scaffold with modular directories.
- `.env.example` for secrets and configuration.
- Initial API specification and JSON schemas.
- Non-functional requirements baseline:
  - P95 response time target
  - recommendation count (Top K)
  - max acceptable failure rate

### Suggested project structure
- `src/api/` - REST endpoints
- `src/services/` - business logic
- `src/data/` - ingestion and transformations
- `src/models/` - pydantic models / schemas
- `src/llm/` - prompt templates + adapters
- `tests/` - unit and integration tests
- `docs/` - architecture and runbooks

---

## 3) Phase 1 - Data Ingestion and Preprocessing

### Goal
Transform raw dataset into a clean, queryable restaurant repository.

### Component design
- **DatasetLoader**
  - pulls data from Hugging Face dataset URL.
  - handles version pinning to ensure reproducibility.
- **DataCleaner**
  - standardizes city/location names.
  - parses cuisine into canonical list.
  - normalizes cost field to numeric and budget buckets.
  - ensures ratings are numeric and bounded.
- **DataValidator**
  - checks schema completeness.
  - flags invalid/missing records.
- **DataWriter**
  - writes cleaned records to database table(s).

### Data model (restaurant)
- `restaurant_id` (string/int)
- `name` (string)
- `city` (string)
- `locality` (string, optional)
- `cuisines` (array[string] or normalized relation)
- `average_cost_for_two` (number)
- `budget_bucket` (`low|medium|high`)
- `rating` (number)
- `tags` (array[string], optional)
- `last_updated_at` (timestamp)

### Processing pipeline
1. Extract raw dataset snapshot.
2. Apply transformations and normalization.
3. Validate quality thresholds (duplicate %, null %, range checks).
4. Persist cleaned data.
5. Build lookup metadata (distinct cities/cuisines/budget ranges).

### Failure handling
- Continue pipeline with warnings for partial invalid rows.
- Hard fail if critical fields exceed null threshold.
- Log each stage summary with row counts.

### Deliverables
- Repeatable ingestion job.
- Cleaned DB table and metadata indices.
- Data quality report artifact.

---

## 4) Phase 2 - User Preference Intake

### Goal
Convert user input into validated, machine-friendly preference objects.

### Component design
- **PreferenceAPI** (`POST /recommend`)
  - receives user input payload.
- **PreferenceNormalizer**
  - standardizes budget and location values.
  - resolves synonyms/typos for cuisine/location.
- **PreferenceValidator**
  - validates required fields and ranges (e.g., rating 0-5).
- **PreferenceProfileBuilder**
  - creates normalized internal profile for downstream services.

### Input contract (request schema)
- `location` (string, required)
- `budget` (`low|medium|high`, required)
- `cuisine` (string or list[string], required)
- `min_rating` (float, optional default 0)
- `additional_preferences` (list[string], optional)
- `top_k` (int, optional default 5)

### Internal normalized profile example
- `preferred_city`: canonical city token
- `budget_range`: min/max numeric cost
- `cuisine_tokens`: normalized cuisine set
- `rating_floor`: numeric threshold
- `extra_tags`: normalized preference tags

### Failure handling
- Return `400` with field-level validation errors.
- Offer fallback suggestions for unknown location/cuisine.

### Deliverables
- Typed request/response models.
- Validation and normalization service.
- API error contract for client UX.

---

## 5) Phase 3 - Candidate Retrieval and Rule-Based Ranking

### Goal
Efficiently shortlist high-fit restaurants before calling LLM.

### Component design
- **RestaurantQueryService**
  - database filtering by city, budget range, cuisine, rating.
- **CandidateScoringService**
  - computes deterministic score:
    - rating weight
    - cuisine match score
    - budget fit score
    - optional tag match bonus
- **ConstraintRelaxationService**
  - broadens filters when results are too sparse.

### Candidate retrieval strategy
1. Strict match with all constraints.
2. If < threshold results:
   - relax extra preferences
   - widen budget tolerance
   - reduce rating floor slightly
3. Return top `N` candidates (e.g., 20) for LLM reasoning.

### Deterministic scoring example
- `score = 0.4*rating_norm + 0.3*cuisine_match + 0.2*budget_fit + 0.1*extras_fit`

### Performance requirements
- Candidate retrieval in < 200 ms for local indexed DB.
- Build indexes on city, rating, budget, and cuisine tokens.

### Deliverables
- Filtering repository methods.
- Fallback strategy implementation.
- Candidate list contract for LLM stage.
- LLM provider decision finalized for next stage: **Groq LLM**.

---

## 6) Phase 4 - LLM Ranking and Explanation Engine

### Goal
Use LLM to produce human-like ranking and concise reasons using only shortlisted candidates.

### Component design
- **PromptBuilder**
  - injects normalized preferences + candidate table.
  - includes strict instructions and output JSON schema.
- **LLMClientAdapter**
  - provider-agnostic wrapper for model invocation.
- **LLMResponseParser**
  - validates JSON shape.
  - retries if malformed.
- **GroundingGuard**
  - rejects hallucinated restaurants not in candidate set.

### Prompt design requirements
- Must include:
  - user preferences summary
  - structured candidate rows
  - ranking criteria and tie-break rules
  - required output schema
- Must enforce:
  - "Use only provided candidate list."
  - "Do not invent cost/rating/details."

### Output contract
- `recommendations`: list of top K items
  - `restaurant_id`
  - `name`
  - `cuisine`
  - `rating`
  - `estimated_cost`
  - `explanation`
- `summary`: optional high-level rationale paragraph

### Reliability patterns
- Timeout + retry with exponential backoff.
- Fallback to deterministic ranked list if LLM unavailable.
- Log prompt/response metadata (not sensitive raw user text if policy requires).

### Deliverables
- Prompt templates (versioned).
- LLM adapter and parser with schema checks.
- Hallucination guard + fallback flow.

---

## 7) Phase 5 - API Orchestration Layer

### Goal
Coordinate all services in a single robust request lifecycle.

### Orchestration flow
1. Validate request.
2. Normalize preferences.
3. Retrieve and score candidates.
4. Invoke LLM for final ranking and explanations.
5. Validate and format response.
6. Return top recommendations.

### API endpoints
- `POST /recommend`
  - input: preference payload
  - output: ranked recommendations + summary + metadata
- `GET /health`
  - liveness/readiness checks
- `GET /meta/cities`
- `GET /meta/cuisines`
- `GET /meta/budgets`

### Response metadata (recommended)
- `request_id`
- `processing_ms`
- `candidate_count`
- `fallback_used` (boolean)
- `model_version`

### Deliverables
- API router + service wiring.
- Standard error envelope (`code`, `message`, `details`).
- Request tracing identifiers.

---

## 8) Phase 6 - Frontend and Result Experience

### Goal
Deliver a clear and trustworthy user experience for recommendation consumption.

### Execution note
- Frontend implementation is intentionally scheduled after backend completion and validation of Phases 0-5.
- Current delivery mode is **backend-first** (API, retrieval, Groq LLM ranking, reliability), then UI integration.

### UI component architecture
- **SearchForm**
  - location, budget, cuisine, rating, extra preferences.
- **RecommendationList**
  - top cards with restaurant attributes and AI explanation.
- **SummaryPanel**
  - concise "why these picks" summary.
- **StateManager**
  - loading, error, success, empty state handling.

### UX requirements
- Show ranking order and key fit indicators.
- Display useful error messages with recovery actions.
- Preserve previous query for iterative refinement.

### Accessibility and quality
- Keyboard-accessible form controls.
- Proper labels and readable contrast.
- Responsive layout for desktop/mobile.

### Deliverables
- Functional recommendation page.
- Error/loading/empty states.
- Basic telemetry events (search submitted, result viewed).

---

## 9) Phase 7 - Testing, Evaluation, and Safety

### Goal
Ensure correctness, quality, and predictable behavior across deterministic and LLM components.

### Test architecture
- **Unit tests**
  - data normalization
  - filtering/scoring logic
  - schema validation
- **Integration tests**
  - end-to-end `POST /recommend`
  - fallback behavior when LLM fails
- **Contract tests**
  - request/response schema stability
- **Prompt regression tests**
  - fixed candidate sets and expected ranking behavior bands

### Evaluation metrics
- Recommendation fit score (constraint satisfaction rate).
- Precision@K for known preference sets.
- Explanation usefulness rubric (human review).
- Latency and error rates.

### Safety and governance
- Prevent prompt injection from free-text preferences.
- Avoid exposing sensitive internal metadata in responses.
- Add rate limits and abuse controls at API gateway.

### Deliverables
- CI test pipeline.
- Baseline evaluation report.
- Runbook for common failures.

---

## 10) Phase 8 - Deployment, Monitoring, and Cost Optimization

### Goal
Run reliably in production with measurable quality and controlled cost.

### Deployment architecture
- **Containerized backend** (Docker).
- **Managed DB** (Postgres preferred for scale).
- **Frontend hosting** (static or server-rendered).
- **Secrets management** for API keys.

### Monitoring stack
- Application logs with request IDs.
- Metrics:
  - request volume
  - response latency (P50/P95/P99)
  - LLM error/timeout rate
  - fallback rate
  - token usage and cost per request
- Alerting for SLA breaches and error spikes.

### Cost control patterns
- Cache repeated query combinations.
- Shortlist candidates deterministically to reduce token load.
- Limit explanation length and top K defaults.
- Add model tiering (cheap model default, premium optional).

### Deliverables
- Production deployment pipeline.
- Dashboards + alerts.
- Cost and performance optimization report.

---

## 11) Cross-Cutting Architecture Standards

### Security
- Input sanitization and strict schema validation.
- API key protection via environment/secrets manager.
- Optional auth layer for user-specific history features.

### Observability
- Correlated logs across API, retrieval, and LLM calls.
- Structured events for recommendation lifecycle.

### Scalability
- Stateless API workers behind load balancer.
- Read replicas/search indices when data grows.

### Maintainability
- Versioned prompts and schema migrations.
- Clear module boundaries and dependency inversion for LLM client.

---

## 12) Suggested Execution Timeline

- **Week 1**: Phase 0 + Phase 1 (foundation + data readiness)
- **Week 2**: Phase 2 + Phase 3 (input + retrieval)
- **Week 3**: Phase 4 + Phase 5 (Groq LLM ranking + API orchestration, backend completion)
- **Week 4**: Phase 7 (backend evaluation/testing hardening)
- **Week 5**: Phase 6 (frontend integration and UX rollout)
- **Week 6**: Phase 8 (deployment, monitoring, optimization)

---

## 13) Definition of Done (Project)

- End users can submit preferences and receive top restaurant recommendations.
- Each recommendation includes required fields and meaningful AI explanation.
- System handles invalid inputs, sparse data, and LLM failures gracefully.
- Quality, latency, and cost are measured with dashboards and alerts.
- Documentation and runbooks are complete for handover.

