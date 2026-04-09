"use client";

import { useState } from "react";
import Header from "@/components/Header";
import Hero from "@/components/Hero";
import SearchForm from "@/components/SearchForm";
import ResultsSection from "@/components/ResultsSection";
import apiClient from "@/lib/api";
import type { RecommendRequest, RecommendationResponse } from "@/types";

export default function Home() {
  const [results, setResults] = useState<RecommendationResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (request: RecommendRequest) => {
    try {
      setLoading(true);
      setError(null);
      
      // 🔧 FIXED: Only log in development
      if (process.env.NODE_ENV === 'development') {
        console.log("Sending recommendation request:", request);
      }
      
      const response = await apiClient.getRecommendations(request);
      
      if (process.env.NODE_ENV === 'development') {
        console.log("Received recommendations:", response);
      }
      
      setResults(response);
    } catch (err) {
      console.error("Failed to get recommendations:", err);
      setError(err instanceof Error ? err.message : "Failed to get recommendations");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <Hero />
      
      <div className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        <div className="mb-8">
          <SearchForm onSubmit={handleSearch} loading={loading} />
        </div>

        {error && (
          <div className="mb-8 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
            <strong>Error:</strong> {error}
          </div>
        )}

        <div className="bg-white rounded-lg shadow-md p-6">
          <ResultsSection results={results} loading={loading} />
        </div>
      </div>

      <footer className="bg-gray-800 text-white py-6 mt-12">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <p className="text-sm">
            © 2024 Zomato AI Recommender · Powered by Groq LLM & Next.js
          </p>
        </div>
      </footer>
    </div>
  );
}
