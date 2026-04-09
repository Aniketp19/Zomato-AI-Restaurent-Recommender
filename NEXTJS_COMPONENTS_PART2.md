# Next.js Components - Part 2

This file contains the remaining React components for the Next.js frontend.

## 🎨 SearchForm Component

### `components/SearchForm.tsx`
```typescript
"use client";

import { useState, useEffect } from "react";
import { apiClient } from "@/lib/api";
import type { BudgetOption, RecommendationResponse } from "@/types";

interface SearchFormProps {
  onResults: (results: RecommendationResponse) => void;
  onLoadingChange: (loading: boolean) => void;
}

export default function SearchForm({ onResults, onLoadingChange }: SearchFormProps) {
  const [cities, setCities] = useState<string[]>([]);
  const [cuisines, setCuisines] = useState<string[]>([]);
  const [budgets, setBudgets] = useState<BudgetOption[]>([]);
  
  const [selectedCity, setSelectedCity] = useState("");
  const [selectedBudget, setSelectedBudget] = useState("");
  const [selectedCuisine, setSelectedCuisine] = useState("");
  const [minRating, setMinRating] = useState("0");
  const [topK, setTopK] = useState("5");
  const [additionalPrefs, setAdditionalPrefs] = useState("");
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [metaLoading, setMetaLoading] = useState(true);

  // Load metadata on mount
  useEffect(() => {
    loadMetadata();
  }, []);

  const loadMetadata = async () => {
    try {
      setMetaLoading(true);
      setError(null);
      
      const [citiesData, cuisinesData, budgetsData] = await Promise.all([
        apiClient.getCities(),
        apiClient.getCuisines(),
        apiClient.getBudgets(),
      ]);
      
      setCities(citiesData);
      setCuisines(cuisinesData);
      setBudgets(budgetsData.budgets);
      
      // Set defaults
      if (citiesData.length > 0) setSelectedCity(citiesData[0]);
      if (budgetsData.budgets.length > 0) setSelectedBudget(budgetsData.budgets[0].bucket);
      if (cuisinesData.length > 0) setSelectedCuisine(cuisinesData[0]);
      
    } catch (err) {
      console.error("Failed to load metadata:", err);
      setError("Failed to load form options. Please ensure the API server is running.");
    } finally {
      setMetaLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!selectedCity || !selectedBudget || !selectedCuisine) {
      setError("Please fill in all required fields");
      return;
    }
    
    setLoading(true);
    onLoadingChange(true);
    setError(null);
    
    try {
      const prefs = additionalPrefs
        ? additionalPrefs.split(",").map((p) => p.trim()).filter(Boolean)
        : [];
      
      const response = await apiClient.getRecommendations({
        location: selectedCity,
        budget: selectedBudget,
        cuisine: selectedCuisine,
        min_rating: parseFloat(minRating),
        additional_preferences: prefs,
        top_k: parseInt(topK),
      });
      
      onResults(response);
    } catch (err: any) {
      console.error("Search failed:", err);
      setError(err.response?.data?.error?.message || "Failed to get recommendations. Please try again.");
    } finally {
      setLoading(false);
      onLoadingChange(false);
    }
  };

  if (metaLoading) {
    return (
      <div className="bg-white rounded-2xl shadow-2xl p-8">
        <div className="flex items-center justify-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-zomato-red"></div>
        </div>
      </div>
    );
  }

  if (error && cities.length === 0) {
    return (
      <div className="bg-white rounded-2xl shadow-2xl p-8">
        <div className="text-center py-12">
          <svg
            className="w-16 h-16 text-red-500 mx-auto mb-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
          <p className="text-red-600 mb-4">{error}</p>
          <button
            onClick={loadMetadata}
            className="text-zomato-red hover:text-zomato-red-hover font-medium"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-2xl shadow-2xl p-8">
      <form onSubmit={handleSubmit} className="space-y-6">
        {error && cities.length > 0 && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
            {error}
          </div>
        )}
        
        {/* Row 1: Location, Budget, Cuisine */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Location */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              LOCATION
            </label>
            <select
              value={selectedCity}
              onChange={(e) => setSelectedCity(e.target.value)}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-zomato-red focus:border-transparent outline-none transition"
              required
            >
              {cities.map((city) => (
                <option key={city} value={city}>
                  {city}
                </option>
              ))}
            </select>
          </div>

          {/* Budget */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              BUDGET
            </label>
            <select
              value={selectedBudget}
              onChange={(e) => setSelectedBudget(e.target.value)}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-zomato-red focus:border-transparent outline-none transition"
              required
            >
              {budgets.map((budget) => (
                <option key={budget.bucket} value={budget.bucket}>
                  {budget.description} (₹{budget.approximate_cost_for_two_min}-₹
                  {budget.approximate_cost_for_two_max})
                </option>
              ))}
            </select>
          </div>

          {/* Cuisine */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              CUISINE
            </label>
            <select
              value={selectedCuisine}
              onChange={(e) => setSelectedCuisine(e.target.value)}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-zomato-red focus:border-transparent outline-none transition"
              required
            >
              {cuisines.map((cuisine) => (
                <option key={cuisine} value={cuisine}>
                  {cuisine}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Row 2: Min Rating, Number of Results */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Min Rating */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              MINIMUM RATING
            </label>
            <input
              type="number"
              min="0"
              max="5"
              step="0.1"
              value={minRating}
              onChange={(e) => setMinRating(e.target.value)}
              placeholder="e.g. 4.0"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-zomato-red focus:border-transparent outline-none transition"
            />
          </div>

          {/* Number of Results */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              NUMBER OF RESULTS
            </label>
            <input
              type="number"
              min="1"
              max="20"
              value={topK}
              onChange={(e) => setTopK(e.target.value)}
              placeholder="e.g. 5"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-zomato-red focus:border-transparent outline-none transition"
            />
          </div>
        </div>

        {/* Row 3: Additional Preferences */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            ADDITIONAL PREFERENCES
          </label>
          <textarea
            value={additionalPrefs}
            onChange={(e) => setAdditionalPrefs(e.target.value)}
            placeholder="e.g. Rooftop seating, pet friendly, good for date night"
            rows={3}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-zomato-red focus:border-transparent outline-none transition resize-none"
          />
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-zomato-red text-white py-4 px-6 rounded-lg font-semibold text-lg hover:bg-zomato-red-hover transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
        >
          {loading ? (
            <>
              <svg
                className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                ></circle>
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                ></path>
              </svg>
              Finding recommendations...
            </>
          ) : (
            <>
              <svg
                className="w-5 h-5 mr-2"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M13 10V3L4 14h7v7l9-11h-7z"
                />
              </svg>
              Get AI Recommendations
            </>
          )}
        </button>
      </form>
    </div>
  );
}
```

---

## 📊 Results Components

### `components/ResultsSection.tsx`
```typescript
import type { RecommendationResponse } from "@/types";
import RestaurantCard from "./RestaurantCard";

interface ResultsSectionProps {
  results: RecommendationResponse;
}

export default function ResultsSection({ results }: ResultsSectionProps) {
  const { recommendations, summary, profile, metadata } = results;

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="bg-white rounded-xl p-6 shadow-lg">
        <div className="flex items-start justify-between">
          <div>
            <h2 className="text-3xl font-bold text-gray-900 mb-2">
              Your Recommendations
            </h2>
            <p className="text-gray-600">
              Found {recommendations.length} perfect matches in {profile.preferred_city}
            </p>
          </div>
          <div className="text-right">
            <div className="text-sm text-gray-500">
              Processed in {metadata.processing_ms}ms
            </div>
            {!metadata.fallback_used && (
              <div className="flex items-center text-green-600 text-sm mt-1">
                <svg
                  className="w-4 h-4 mr-1"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fillRule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                    clipRule="evenodd"
                  />
                </svg>
                AI-Powered
              </div>
            )}
          </div>
        </div>
        
        {/* Summary */}
        {summary && (
          <div className="mt-4 p-4 bg-blue-50 border-l-4 border-blue-500 rounded">
            <p className="text-gray-700">{summary}</p>
          </div>
        )}
      </div>

      {/* Results */}
      {recommendations.length === 0 ? (
        <div className="bg-white rounded-xl p-12 text-center shadow-lg">
          <svg
            className="w-16 h-16 text-gray-400 mx-auto mb-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M12 12h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">
            No restaurants found
          </h3>
          <p className="text-gray-600">
            Try adjusting your search criteria or preferences
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {recommendations.map((restaurant, index) => (
            <RestaurantCard
              key={restaurant.restaurant_id}
              restaurant={restaurant}
              rank={index + 1}
            />
          ))}
        </div>
      )}
    </div>
  );
}
```

### `components/RestaurantCard.tsx`
```typescript
import type { Restaurant } from "@/types";

interface RestaurantCardProps {
  restaurant: Restaurant;
  rank: number;
}

export default function RestaurantCard({ restaurant, rank }: RestaurantCardProps) {
  return (
    <div className="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-2xl transition-shadow duration-300 group">
      {/* Header with Rank */}
      <div className="relative h-48 bg-gradient-to-br from-zomato-red to-pink-500 flex items-center justify-center">
        <div className="absolute top-4 left-4 bg-white text-zomato-red w-10 h-10 rounded-full flex items-center justify-center font-bold text-lg shadow-lg">
          {rank}
        </div>
        <div className="text-white text-center p-6">
          <h3 className="text-2xl font-bold mb-2 group-hover:scale-105 transition-transform">
            {restaurant.name}
          </h3>
          <p className="text-white/90">{restaurant.cuisine}</p>
        </div>
      </div>

      {/* Content */}
      <div className="p-6">
        {/* Rating and Cost */}
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center">
            <svg
              className="w-5 h-5 text-yellow-400 mr-1"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
            </svg>
            <span className="font-semibold text-gray-900">
              {restaurant.rating.toFixed(1)}
            </span>
            <span className="text-gray-500 text-sm ml-1">/5</span>
          </div>
          <div className="text-right">
            <div className="text-sm text-gray-500">For two</div>
            <div className="font-semibold text-gray-900">
              ₹{Math.round(restaurant.estimated_cost)}
            </div>
          </div>
        </div>

        {/* Explanation */}
        <div className="border-t pt-4">
          <p className="text-gray-700 text-sm leading-relaxed">
            {restaurant.explanation}
          </p>
        </div>
      </div>

      {/* Footer */}
      <div className="px-6 pb-6">
        <button className="w-full bg-zomato-red text-white py-3 rounded-lg font-medium hover:bg-zomato-red-hover transition-colors">
          View Details
        </button>
      </div>
    </div>
  );
}
```

---

## 🚀 Running the Application

### 1. Start Backend
```bash
cd "c:\Users\RYZEN\Downloads\zomato pro"
setup_and_start.bat
```

### 2. Start Frontend
```bash
cd "c:\Users\RYZEN\Downloads\zomato pro\frontend"
npm run dev
```

### 3. Open Browser
Visit [http://localhost:3000](http://localhost:3000)

---

## 🎨 Screenshots Expected

The application should look exactly like the provided screenshot with:
- Clean header with Zomato branding
- Hero section with gradient background
- Search form with all fields
- Beautiful result cards with rankings
- AI-generated explanations
- Smooth animations and transitions

---

## ✅ Checklist

- [ ] Next.js project created
- [ ] All dependencies installed
- [ ] All configuration files in place
- [ ] All components created
- [ ] Types and API client configured
- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Can see the search form
- [ ] Can submit and get results
- [ ] Results display correctly with AI explanations

---

**🎉 You're all set! Enjoy your modern Next.js frontend!**

