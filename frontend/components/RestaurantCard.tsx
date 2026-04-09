import React from "react";
import type { Restaurant } from "@/types";

interface RestaurantCardProps {
  restaurant: Restaurant;
  index: number;
}

export default function RestaurantCard({ restaurant, index }: RestaurantCardProps) {
  const getRatingColor = (rating: number) => {
    if (rating >= 4.0) return "bg-green-500";
    if (rating >= 3.0) return "bg-yellow-500";
    return "bg-orange-500";
  };

  return (
    <div className="bg-white rounded-lg shadow-md hover:shadow-xl transition-shadow duration-300 overflow-hidden border border-gray-200">
      <div className="p-6">
        <div className="flex items-start justify-between mb-3">
          <div className="flex-1">
            <div className="flex items-center space-x-2 mb-1">
              <span className="inline-flex items-center justify-center w-6 h-6 bg-[#E23744] text-white text-xs font-bold rounded-full">
                {index + 1}
              </span>
              <h3 className="text-xl font-bold text-gray-900">
                {restaurant.name}
              </h3>
            </div>
            <p className="text-gray-600 text-sm">{restaurant.cuisine}</p>
          </div>
          <div className={`${getRatingColor(restaurant.rating)} text-white px-3 py-1 rounded-lg font-semibold flex items-center space-x-1`}>
            <span>{restaurant.rating.toFixed(1)}</span>
            <span>⭐</span>
          </div>
        </div>

        <div className="flex items-center justify-between mb-4 text-sm text-gray-600">
          <div className="flex items-center space-x-4">
            <span className="font-semibold text-[#E23744]">
              ₹{restaurant.estimated_cost} for two
            </span>
          </div>
        </div>

        <div className="bg-blue-50 border-l-4 border-blue-500 p-3 rounded">
          <div className="flex items-start">
            <span className="text-blue-500 mr-2 mt-0.5">🤖</span>
            <p className="text-sm text-gray-700 italic">
              {restaurant.explanation}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
