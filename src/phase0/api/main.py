import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.api.middleware import RequestTrackingMiddleware
from src.phase0.llm.adapter import LLMConnectionError
from src.phase0.core.config import settings
from src.phase0.models.api import ErrorEnvelope, ErrorResponse, HealthResponse
from src.models.metadata import BudgetOption, MetaBudgetsResponse, MetaCitiesResponse, MetaCuisinesResponse
from src.phase2.models.preferences import RecommendRequest
from src.phase2.services.preferences import PreferenceService, PreferenceValidationError
from src.phase3.services.retrieval import CandidateRetrievalService, RetrievalError
from src.phase4.models.recommendation import FinalRecommendationResponse
from src.phase4.services.grounding import GroundingGuardError
from src.phase4.services.ranker import LLMRankingService
from src.phase4.services.response_parser import LLMResponseParserError
from src.services.metadata import MetadataService

app = FastAPI(title=settings.app_name)


def _cors_origins() -> list[str]:
    if settings.app_env.lower() != "production":
        return ["*"]

    raw = os.getenv("ALLOWED_ORIGINS", "").strip()
    if not raw:
        return ["http://localhost:3000"]
    return [origin.strip() for origin in raw.split(",") if origin.strip()]

# Add CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins(),
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-Request-ID"],
)

# Add request tracking middleware
app.add_middleware(RequestTrackingMiddleware)

# Initialize services
preference_service = PreferenceService()
candidate_service = CandidateRetrievalService()
llm_ranking_service = LLMRankingService()
metadata_service = MetadataService(db_path=settings.sqlite_file)


@app.exception_handler(PreferenceValidationError)
def handle_preference_validation_error(
    _request: Request, exc: PreferenceValidationError
) -> JSONResponse:
    error = ErrorEnvelope(
        code="INVALID_PREFERENCES",
        message=exc.message,
        details=exc.details,
    )
    return JSONResponse(status_code=400, content={"error": error.model_dump()})


@app.exception_handler(RetrievalError)
def handle_retrieval_error(_request: Request, exc: RetrievalError) -> JSONResponse:
    error = ErrorEnvelope(
        code="RETRIEVAL_ERROR",
        message=str(exc),
        details={},
    )
    return JSONResponse(status_code=400, content={"error": error.model_dump()})


@app.exception_handler(LLMConnectionError)
def handle_llm_connection_error(_request: Request, exc: LLMConnectionError) -> JSONResponse:
    error = ErrorEnvelope(
        code="LLM_CONNECTION_ERROR",
        message=str(exc),
        details={},
    )
    return JSONResponse(status_code=400, content={"error": error.model_dump()})


@app.get("/health", response_model=HealthResponse)
def health(request: Request) -> HealthResponse:
    return HealthResponse(
        app_name=settings.app_name,
        env=settings.app_env,
        request_id=getattr(request.state, "request_id", None),
    )


@app.post(
    "/recommend",
    response_model=FinalRecommendationResponse,
    responses={400: {"model": ErrorResponse}},
)
def recommend(req: RecommendRequest, request: Request) -> FinalRecommendationResponse:
    start_time = getattr(request.state, "start_time", 0.0)
    request_id = getattr(request.state, "request_id", None)
    
    # Build profile
    print(f"\n🔍 Processing recommendation request for {req.location}, {req.cuisine}")
    profile = preference_service.build_profile(req)
    print(f"   Profile: city={profile.preferred_city}, cuisine={profile.cuisine_tokens}, budget={profile.budget_bucket}")
    
    # Get candidates
    candidates, relaxations, pool_count = candidate_service.shortlist(profile=profile, pool_size=20)
    selected_candidates = candidates[:20]
    print(f"   Candidates: {len(selected_candidates)} selected from pool of {pool_count}")

    # Attempt LLM ranking with comprehensive error handling
    fallback_used = False
    summary: str | None = None
    notes = ["Phase 5 orchestration: Groq LLM ranking + explanation attempted."]
    recommendations: list = []
    
    if not selected_candidates:
        print(f"   ⚠️  No candidates found, returning empty recommendations")
        recommendations = []
        summary = "No restaurants match your criteria. Try adjusting your preferences."
        fallback_used = True
    else:
        try:
            print(f"   🤖 Attempting LLM ranking with {len(selected_candidates)} candidates...")
            recommendations, summary = llm_ranking_service.rank(
                profile=profile,
                candidates=selected_candidates,
                top_k=req.top_k,
            )
            print(f"   ✅ LLM ranking succeeded: {len(recommendations)} recommendations")
        except (LLMConnectionError, LLMResponseParserError, GroundingGuardError) as e:
            print(f"   ⚠️  LLM ranking failed ({type(e).__name__}): {str(e)[:100]}")
            recommendations, summary = llm_ranking_service.deterministic_fallback(
                selected_candidates, top_k=req.top_k
            )
            fallback_used = True
            notes.append(f"Deterministic fallback used: {type(e).__name__}")
        except Exception as e:
            # Catch any unexpected errors
            print(f"   ❌ Unexpected error in LLM ranking: {type(e).__name__}: {str(e)[:100]}")
            import traceback
            traceback.print_exc()
            recommendations, summary = llm_ranking_service.deterministic_fallback(
                selected_candidates, top_k=req.top_k
            )
            fallback_used = True
            notes.append(f"Deterministic fallback used due to unexpected error: {type(e).__name__}")

    # Calculate processing time
    import time
    processing_ms = int((time.time() - start_time) * 1000) if start_time > 0 else 0

    print(f"   📊 Response: {len(recommendations)} recommendations, fallback={fallback_used}, time={processing_ms}ms\n")

    return FinalRecommendationResponse(
        profile=profile,
        candidates=selected_candidates,
        recommendations=recommendations,
        summary=summary,
        notes=notes,
        metadata={
            "request_id": request_id,
            "processing_ms": processing_ms,
            "phase": "phase-5",
            "pool_size_before_top_k": pool_count,
            "requested_top_k": req.top_k,
            "applied_relaxations": relaxations,
            "fallback_used": fallback_used,
            "model_version": settings.groq_model,
        },
    )


@app.get("/meta/cities", response_model=MetaCitiesResponse)
def get_cities(request: Request) -> MetaCitiesResponse:
    """Get list of available cities from the database."""
    cities = metadata_service.get_available_cities()
    return MetaCitiesResponse(
        cities=cities,
        count=len(cities),
        request_id=getattr(request.state, "request_id", None),
    )


@app.get("/meta/cuisines", response_model=MetaCuisinesResponse)
def get_cuisines(request: Request) -> MetaCuisinesResponse:
    """Get list of available cuisines from the database."""
    cuisines = metadata_service.get_available_cuisines()
    return MetaCuisinesResponse(
        cuisines=cuisines,
        count=len(cuisines),
        request_id=getattr(request.state, "request_id", None),
    )


@app.get("/meta/budgets", response_model=MetaBudgetsResponse)
def get_budgets(request: Request) -> MetaBudgetsResponse:
    """Get list of budget options with their ranges."""
    budget_options = metadata_service.get_budget_options()
    budgets = [BudgetOption(**opt) for opt in budget_options]
    return MetaBudgetsResponse(
        budgets=budgets,
        count=len(budgets),
        request_id=getattr(request.state, "request_id", None),
    )
