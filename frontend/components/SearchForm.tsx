"use client";

import React, { useState, useEffect } from "react";
import apiClient from "@/lib/api";
import type { RecommendRequest, BudgetOption } from "@/types";

interface SearchFormProps {
  onSubmit: (request: RecommendRequest) => void;
  loading: boolean;
}

export default function SearchForm({ onSubmit, loading }: SearchFormProps) {
  const [cities, setCities] = useState<string[]>([]);
  const [cuisines, setCuisines] = useState<string[]>([]);
  const [budgets, setBudgets] = useState<BudgetOption[]>([]);
  const [loadingMeta, setLoadingMeta] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [formData, setFormData] = useState<RecommendRequest>({
    location: "",
    budget: "",
    cuisine: "",
    min_rating: 0,
    top_k: 5,
    additional_preferences: [],
  });

  useEffect(() => {
    loadMetadata();
  }, []);

  const loadMetadata = async () => {
    try {
      setLoadingMeta(true);
      setError(null);
      
      const [citiesData, cuisinesData, budgetsData] = await Promise.all([
        apiClient.getCities(),
        apiClient.getCuisines(),
        apiClient.getBudgets(),
      ]);

      setCities(citiesData);
      setCuisines(cuisinesData);
      setBudgets(budgetsData.budgets);
      
      if (citiesData.length > 0) setFormData(prev => ({ ...prev, location: citiesData[0] }));
      if (budgetsData.budgets.length > 0) setFormData(prev => ({ ...prev, budget: budgetsData.budgets[0].bucket }));
      if (cuisinesData.length > 0) setFormData(prev => ({ ...prev, cuisine: cuisinesData[0] }));
      
    } catch (err) {
      console.error("Failed to load metadata:", err);
      setError("Failed to load form options. Please ensure the API server is running.");
    } finally {
      setLoadingMeta(false);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.location || !formData.budget || !formData.cuisine) {
      setError("Please fill in all required fields");
      return;
    }
    
    onSubmit(formData);
  };

  const handleChange = (field: keyof RecommendRequest, value: string | number) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  if (loadingMeta) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="text-center py-8">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[#E23744] mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading form options...</p>
        </div>
      </div>
    );
  }

  if (error && cities.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="text-center py-8">
          <div className="text-red-500 mb-4">⚠️ {error}</div>
          <button
            onClick={loadMetadata}
            className="px-4 py-2 bg-[#E23744] text-white rounded-lg hover:bg-[#CF2533]"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <form onSubmit={handleSubmit} className="space-y-6">
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
            {error}
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label htmlFor="location" className="block text-sm font-medium text-gray-700 mb-2">
              Location <span className="text-red-500">*</span>
            </label>
            <select
              id="location"
              value={formData.location}
              onChange={(e) => handleChange("location", e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#E23744] focus:border-transparent"
              required
            >
              {cities.map((city) => (
                <option key={city} value={city}>
                  {city}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label htmlFor="budget" className="block text-sm font-medium text-gray-700 mb-2">
              Budget <span className="text-red-500">*</span>
            </label>
            <select
              id="budget"
              value={formData.budget}
              onChange={(e) => handleChange("budget", e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#E23744] focus:border-transparent"
              required
            >
              {budgets.map((budget) => (
                <option key={budget.bucket} value={budget.bucket}>
                  {budget.bucket} - {budget.description}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label htmlFor="cuisine" className="block text-sm font-medium text-gray-700 mb-2">
              Cuisine <span className="text-red-500">*</span>
            </label>
            <select
              id="cuisine"
              value={formData.cuisine}
              onChange={(e) => handleChange("cuisine", e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#E23744] focus:border-transparent"
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

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label htmlFor="min_rating" className="block text-sm font-medium text-gray-700 mb-2">
              Minimum Rating
            </label>
            <input
              type="number"
              id="min_rating"
              min="0"
              max="5"
              step="0.5"
              value={formData.min_rating}
              onChange={(e) => handleChange("min_rating", parseFloat(e.target.value) || 0)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#E23744] focus:border-transparent"
            />
          </div>

          <div>
            <label htmlFor="top_k" className="block text-sm font-medium text-gray-700 mb-2">
              Number of Results
            </label>
            <input
              type="number"
              id="top_k"
              min="1"
              max="20"
              value={formData.top_k}
              onChange={(e) => handleChange("top_k", parseInt(e.target.value) || 5)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#E23744] focus:border-transparent"
            />
          </div>
        </div>

        <div className="flex justify-center">
          <button
            type="submit"
            disabled={loading}
            className="px-8 py-3 bg-[#E23744] text-white text-lg font-semibold rounded-lg hover:bg-[#CF2533] transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? (
              <span className="flex items-center space-x-2">
                <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span>Searching...</span>
              </span>
            ) : (
              "Get AI Recommendations 🤖"
            )}
          </button>
        </div>
      </form>
    </div>
  );
}
