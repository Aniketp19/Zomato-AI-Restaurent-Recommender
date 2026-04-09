// API Types
export interface BudgetOption {
  bucket: string;
  description: string;
  approximate_cost_for_two_min: number;
  approximate_cost_for_two_max: number;
}

export interface MetaCitiesResponse {
  cities: string[];
  count: number;
  request_id?: string;
}

export interface MetaCuisinesResponse {
  cuisines: string[];
  count: number;
  request_id?: string;
}

export interface MetaBudgetsResponse {
  budgets: BudgetOption[];
  count: number;
  request_id?: string;
}

export interface RecommendRequest {
  location: string;
  budget: string;
  cuisine: string;
  min_rating?: number;
  additional_preferences?: string[];
  top_k?: number;
}

export interface Restaurant {
  restaurant_id: string;
  name: string;
  cuisine: string;
  rating: number;
  estimated_cost: number;
  explanation: string;
}

export interface RecommendationResponse {
  status: string;
  profile: {
    preferred_city: string;
    budget_bucket: string;
    cuisine_tokens: string[];
    rating_floor: number;
  };
  recommendations: Restaurant[];
  summary: string | null;
  metadata: {
    request_id: string;
    processing_ms: number;
    fallback_used: boolean;
  };
}
