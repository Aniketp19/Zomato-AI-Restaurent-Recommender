from pydantic import BaseModel


class MetaCitiesResponse(BaseModel):
    """Response model for available cities."""
    cities: list[str]
    count: int
    request_id: str | None = None


class MetaCuisinesResponse(BaseModel):
    """Response model for available cuisines."""
    cuisines: list[str]
    count: int
    request_id: str | None = None


class BudgetOption(BaseModel):
    """Budget bucket details."""
    bucket: str
    description: str
    approximate_cost_for_two_min: int
    approximate_cost_for_two_max: int


class MetaBudgetsResponse(BaseModel):
    """Response model for budget options."""
    budgets: list[BudgetOption]
    count: int
    request_id: str | None = None
