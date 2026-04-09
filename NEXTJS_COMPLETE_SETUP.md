# Next.js Frontend - Complete Setup Guide

## 🎯 Overview

This guide provides ALL the code needed to create a Next.js frontend matching the Zomato screenshot design.

## 📦 Step 1: Create Next.js Project

```bash
cd "c:\Users\RYZEN\Downloads\zomato pro"

# Create Next.js app with TypeScript and Tailwind
npx create-next-app@latest frontend --typescript --tailwind --app --no-src-dir --import-alias "@/*"

cd frontend

# Install additional dependencies
npm install axios

# Create folder structure
mkdir components lib types
mkdir public\images
```

## 📄 Step 2: Configuration Files

### `next.config.js`
```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/:path*',
      },
    ];
  },
};

module.exports = nextConfig;
```

### `.env.local`
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### `tailwind.config.ts`
```typescript
import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        zomato: {
          red: "#E23744",
          "red-hover": "#CF2533",
          dark: "#1C1C1C",
          gray: {
            100: "#F5F5F5",
            200: "#EBEBEB",
            300: "#CFCFCF",
            400: "#9C9C9C",
          },
        },
      },
    },
  },
  plugins: [],
};
export default config;
```

## 🎨 Step 3: Global Styles

### `app/globals.css`
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --foreground-rgb: 0, 0, 0;
  --background-start-rgb: 214, 219, 220;
  --background-end-rgb: 255, 255, 255;
}

body {
  color: rgb(var(--foreground-rgb));
}

::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #555;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.animate-spin-slow {
  animation: spin 2s linear infinite;
}
```

### `app/layout.tsx`
```typescript
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Zomato AI Recommender - Find Your Perfect Restaurant",
  description: "AI-powered restaurant recommendations for Bangalore's best dining",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  );
}
```

### `app/page.tsx`
```typescript
"use client";

import { useState } from "react";
import Header from "@/components/Header";
import Hero from "@/components/Hero";
import SearchForm from "@/components/SearchForm";
import ResultsSection from "@/components/ResultsSection";
import { RecommendationResponse } from "@/types";

export default function Home() {
  const [results, setResults] = useState<RecommendationResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSearch = (data: RecommendationResponse) => {
    setResults(data);
  };

  const handleLoadingChange = (loading: boolean) => {
    setIsLoading(loading);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      {!results ? (
        <>
          <Hero />
          <div className="container mx-auto px-4 -mt-32 relative z-10 pb-20">
            <SearchForm 
              onResults={handleSearch} 
              onLoadingChange={handleLoadingChange}
            />
          </div>
        </>
      ) : (
        <div className="container mx-auto px-4 py-8">
          <button
            onClick={() => setResults(null)}
            className="mb-6 flex items-center text-zomato-red hover:text-zomato-red-hover transition-colors font-medium"
          >
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
                d="M15 19l-7-7 7-7"
              />
            </svg>
            Back to Search
          </button>
          <ResultsSection results={results} />
        </div>
      )}
    </div>
  );
}
```

## 📦 Step 4: TypeScript Types

### `types/index.ts`
```typescript
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
```

## 🔧 Step 5: API Client

### `lib/api.ts`
```typescript
import axios from "axios";
import type {
  MetaCitiesResponse,
  MetaCuisinesResponse,
  MetaBudgetsResponse,
  RecommendRequest,
  RecommendationResponse,
} from "@/types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export const apiClient = {
  async getCities(): Promise<string[]> {
    const response = await api.get<MetaCitiesResponse>("/meta/cities");
    return response.data.cities;
  },

  async getCuisines(): Promise<string[]> {
    const response = await api.get<MetaCuisinesResponse>("/meta/cuisines");
    return response.data.cuisines;
  },

  async getBudgets(): Promise<MetaBudgetsResponse> {
    const response = await api.get<MetaBudgetsResponse>("/meta/budgets");
    return response.data;
  },

  async getRecommendations(
    request: RecommendRequest
  ): Promise<RecommendationResponse> {
    const response = await api.post<RecommendationResponse>("/recommend", request);
    return response.data;
  },

  async healthCheck(): Promise<{ status: string }> {
    const response = await api.get("/health");
    return response.data;
  },
};

export default apiClient;
```

---

## 🎨 Components (Part 1/2)

### `components/Header.tsx`
```typescript
export default function Header() {
  return (
    <header className="bg-white shadow-sm sticky top-0 z-50">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center space-x-8">
            <h1 className="text-2xl font-bold text-zomato-red">Zomato</h1>
          </div>

          {/* Navigation */}
          <nav className="hidden md:flex items-center space-x-6">
            <a
              href="#"
              className="text-gray-700 hover:text-zomato-red transition-colors"
            >
              Add Restaurant
            </a>
            <a
              href="#"
              className="text-gray-700 hover:text-zomato-red transition-colors"
            >
              Log in
            </a>
            <button className="bg-zomato-red text-white px-6 py-2 rounded-lg hover:bg-zomato-red-hover transition-colors">
              Sign up
            </button>
          </nav>

          {/* Mobile menu button */}
          <button className="md:hidden">
            <svg
              className="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M4 6h16M4 12h16M4 18h16"
              />
            </svg>
          </button>
        </div>
      </div>
    </header>
  );
}
```

### `components/Hero.tsx`
```typescript
export default function Hero() {
  return (
    <div className="relative bg-gradient-to-r from-purple-900 via-blue-900 to-indigo-900 text-white overflow-hidden">
      {/* Background Image Overlay */}
      <div 
        className="absolute inset-0 opacity-40"
        style={{
          backgroundImage: "url('https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=1920')",
          backgroundSize: "cover",
          backgroundPosition: "center",
        }}
      />

      {/* Content */}
      <div className="relative container mx-auto px-4 py-32 md:py-48">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-4xl md:text-6xl font-bold mb-6 leading-tight">
            Find Your Perfect Restaurant
          </h1>
          <p className="text-xl md:text-2xl text-gray-200">
            AI-powered recommendations for Bangalore&apos;s best dining
          </p>
        </div>
      </div>

      {/* Bottom Wave */}
      <div className="absolute bottom-0 w-full">
        <svg
          viewBox="0 0 1440 120"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M0 0L60 10C120 20 240 40 360 46.7C480 53 600 47 720 43.3C840 40 960 40 1080 46.7C1200 53 1320 67 1380 73.3L1440 80V120H1380C1320 120 1200 120 1080 120C960 120 840 120 720 120C600 120 480 120 360 120C240 120 120 120 60 120H0V0Z"
            fill="#F9FAFB"
          />
        </svg>
      </div>
    </div>
  );
}
```

---

*Continued in next message due to length...*

## 🚀 Quick Start Commands

```bash
# Navigate to project
cd "c:\Users\RYZEN\Downloads\zomato pro"

# Create Next.js app
npx create-next-app@latest frontend --typescript --tailwind --app --no-src-dir --import-alias "@/*"

cd frontend

# Install dependencies
npm install axios

# Create folders
mkdir components lib types

# Copy all the code files above into their respective locations

# Start development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser!

**Note:** Make sure the FastAPI backend is running on port 8000 first.

---

