import type {
  MetaCitiesResponse,
  MetaCuisinesResponse,
  MetaBudgetsResponse,
  RecommendRequest,
  RecommendationResponse,
} from "@/types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const API_TIMEOUT = 30000; // 30 seconds

class ApiClient {
  private baseURL: string;

  constructor() {
    this.baseURL = API_BASE_URL;
  }

  // 🔧 FIXED: Added timeout handling
  private async request<T>(
    endpoint: string,
    options?: RequestInit
  ): Promise<T> {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), API_TIMEOUT);

    try {
      const response = await fetch(`${this.baseURL}${endpoint}`, {
        ...options,
        signal: controller.signal,
        headers: {
          "Content-Type": "application/json",
          ...options?.headers,
        },
      });

      clearTimeout(timeout);

      if (!response.ok) {
        throw new Error(`API Error: ${response.statusText}`);
      }

      return response.json();
    } catch (error) {
      clearTimeout(timeout);
      
      // Handle timeout errors
      if (error instanceof Error && error.name === 'AbortError') {
        throw new Error('Request timeout - please try again. The server may be slow or down.');
      }
      
      // Handle network errors
      if (error instanceof TypeError) {
        throw new Error('Network error - please check your internet connection.');
      }
      
      throw error;
    }
  }

  async getCities(): Promise<string[]> {
    const data = await this.request<MetaCitiesResponse>("/meta/cities");
    return data.cities;
  }

  async getCuisines(): Promise<string[]> {
    const data = await this.request<MetaCuisinesResponse>("/meta/cuisines");
    return data.cuisines;
  }

  async getBudgets(): Promise<MetaBudgetsResponse> {
    return this.request<MetaBudgetsResponse>("/meta/budgets");
  }

  async getRecommendations(
    request: RecommendRequest
  ): Promise<RecommendationResponse> {
    return this.request<RecommendationResponse>("/recommend", {
      method: "POST",
      body: JSON.stringify(request),
    });
  }

  async healthCheck(): Promise<{ status: string }> {
    return this.request("/health");
  }
}

export const apiClient = new ApiClient();
export default apiClient;
