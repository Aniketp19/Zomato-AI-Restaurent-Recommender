from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os

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

# 🔧 FIXED: Production-ready CORS configuration
# Only allow specific origins in production
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS if settings.app_env == "production" else ["*"],
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


# 🔧 FIXED: Add startup validation
@app.on_event("startup")
async def startup_validation():
    """Validate critical resources on startup"""
    if not settings.sqlite_file.exists():
        raise RuntimeError(
            f"❌ Database not found at {settings.sqlite_file}. "
            f"Please run: python -m src.phase1.data.pipeline"
        )
    if not settings.groq_api_key:
        print("⚠️  Warning: GROQ_API_KEY not set. LLM ranking will be disabled.")


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


# ... rest of the file remains the same ...
# (Keep all other handlers and endpoints as is)

