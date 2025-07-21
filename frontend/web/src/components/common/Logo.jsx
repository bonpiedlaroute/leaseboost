import React from 'react';


const Logo = () => {
  return (
    <div className="flex items-center gap-3">
      <div className="relative group">
        <svg 
          width="40" 
          height="40" 
          viewBox="0 0 40 40" 
          className="drop-shadow-sm transition-transform group-hover:scale-110"
        >
          <defs>
            <linearGradient id="logoGradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#0C7FF2" />
              <stop offset="100%" stopColor="#1E40AF" />
            </linearGradient>
            <linearGradient id="accentGradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#10B981" />
              <stop offset="100%" stopColor="#059669" />
            </linearGradient>
          </defs>
          
          {/* Base shape - Letter L stylized */}
          <path 
            d="M8 8 L8 28 L28 28 L28 24 L12 24 L12 8 Z" 
            fill="url(#logoGradient)"
            className="drop-shadow-sm"
          />
          
          {/* Data visualization elements */}
          <rect x="16" y="12" width="3" height="8" fill="url(#accentGradient)" rx="1" />
          <rect x="20" y="10" width="3" height="10" fill="url(#accentGradient)" rx="1" />
          <rect x="24" y="8" width="3" height="12" fill="url(#accentGradient)" rx="1" />
          
          {/* Animation dot */}
          <circle cx="32" cy="32" r="2" fill="#10B981" className="animate-pulse" />
        </svg>
      </div>
    </div>
  );
};

export default Logo;