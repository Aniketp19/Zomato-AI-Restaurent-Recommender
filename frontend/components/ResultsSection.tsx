import React from "react";
import RestaurantCard from "./RestaurantCard";
import type { RecommendationResponse } from "@/types";

interface ResultsSectionProps {
  results: RecommendationResponse | null;
  loading: boolean;
}

export default function ResultsSection({ results, loading }: ResultsSectionProps) {
  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-[#E23744] mx-auto mb-4"></div>
        <p className="text-xl text-gray-600">Finding the perfect restaurants for you...</p>
      </div>
    );
  }

  if (!results) {
    return (
      <div className="text-center py-12">
        <div className="text-6xl mb-4">🍽️</div>
        <h3 className="text-2xl font-semibold text-gray-700 mb-2">
          Ready to Discover?
        </h3>
        <p className="text-gray-500">
          Fill in your preferences above and let AI find your perfect restaurant
        </p>
      </div>
    );
  }

  if (results.recommendations.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="text-6xl mb-4">😕</div>
        <h3 className="text-2xl font-semibold text-gray-700 mb-2">
          No Recommendations Found
        </h3>
        <p className="text-gray-500 mb-4">
          {results.summary || "Try adjusting your search criteria"}
        </p>
        <div className="text-sm text-gray-400">
          Request ID: {results.metadata.request_id}
        </div>
      </div>
    );
  }

  return (
    <div>
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">
            Your AI-Powered Recommendations
          </h2>
          <p className="text-gray-600 mt-1">
            {results.recommendations.length} restaurant{results.recommendations.length !== 1 ? 's' : ''} found in{' '}
            {results.profile.preferred_city} · {results.profile.budget_bucket} budget
          </p>
        </div>
        <div className="text-sm text-gray-500">
          ⚡ {results.metadata.processing_ms}ms
        </div>
      </div>

      {results.summary && (
        <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-6 rounded">
          <p className="text-sm text-yellow-800">
            💡 <strong>Note:</strong> {results.summary}
          </p>
        </div>
      )}

      <div className="space-y-4">
        {results.recommendations.map((restaurant, index) => (
          <RestaurantCard
            key={restaurant.restaurant_id}
            restaurant={restaurant}
            index={index}
          />
        ))}
      </div>

      <div className="mt-6 text-center text-xs text-gray-400">
        Request ID: {results.metadata.request_id}
        {results.metadata.fallback_used && " · Using fallback ranking"}
      </div>
    </div>
  );
}
