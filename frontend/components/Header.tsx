import React from "react";

export default function Header() {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-[#E23744] rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-xl">Z</span>
            </div>
            <h1 className="text-2xl font-bold text-gray-900">
              Zomato AI Recommender
            </h1>
          </div>
          <div className="text-sm text-gray-500">
            Powered by AI 🤖
          </div>
        </div>
      </div>
    </header>
  );
}
