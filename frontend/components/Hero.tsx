import React from "react";

export default function Hero() {
  return (
    <div className="relative bg-gradient-to-r from-[#E23744] to-[#CF2533] text-white overflow-hidden">
      <div className="absolute inset-0 bg-black opacity-30"></div>
      <div 
        className="absolute inset-0 opacity-20"
        style={{
          backgroundImage: "url('https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?ixlib=rb-4.0.3')",
          backgroundSize: "cover",
          backgroundPosition: "center",
        }}
      ></div>
      <div className="relative max-w-7xl mx-auto px-4 py-16 sm:px-6 lg:px-8 text-center">
        <h2 className="text-4xl md:text-5xl font-bold mb-4">
          Discover Your Perfect Restaurant
        </h2>
        <p className="text-xl md:text-2xl opacity-90">
          AI-powered recommendations tailored just for you
        </p>
      </div>
    </div>
  );
}
