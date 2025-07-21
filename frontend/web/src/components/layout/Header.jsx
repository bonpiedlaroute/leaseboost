import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import Logo from '../common/Logo';

const Header = () => {
  const location = useLocation();

  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  
  //mapping of navigation name to react routes
  const getRouteForNavItem = (navItem) => {
    switch(navItem) {
      case 'Accueil':
        return '/';
      case 'Analyse':
        return '/analysis';
      case 'A propos':
        return '/';
      default:
        return '/';
    }
  };
  const getPageData = () => {
    switch(location.pathname) {
      case '/analysis':
        return {
          nav: ['Accueil', 'Nouvelle Analyse', 'Contact'],
          showStatus: true
        };
      default: // Home
        return {
          nav: ['Accueil', 'A propos', 'Contact'],
          showStatus: false
        };
    }
  };

  const { nav, showStatus } = getPageData();
  
    return (
    <header className="relative flex items-center justify-between whitespace-nowrap border-b border-solid border-b-[#e7edf4] px-4 sm:px-10 py-3 bg-white">
      <div className="flex items-center gap-4 text-[#0d141c]">
        <Logo />
        <Link to="/" className="flex items-center gap-2">
          <h2 className="text-[#0d141c] text-lg font-bold leading-tight tracking-[-0.015em] hidden sm:block">
            LeaseBoost
          </h2>
          <h2 className="text-[#0d141c] text-sm font-bold leading-tight tracking-[-0.015em] sm:hidden">
            LeaseBoost
          </h2>
        </Link>
        {showStatus && (
          <div className="hidden md:flex items-center gap-2 ml-4 px-3 py-1 bg-green-50 rounded-full border border-green-200">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
            <span className="text-sm text-green-700 font-medium">Analyse active</span>
          </div>
        )}
      </div>

      {/* Desktop Navigation */}
      <div className="hidden lg:flex flex-1 justify-end gap-8">
        <div className="flex items-center gap-6">
          {nav.map((item) => (
            <Link
              key={item}
              to={getRouteForNavItem(item)}
              className={`text-sm font-medium leading-normal transition-colors ${
                (item === 'Accueil' && location.pathname === '/') ||
                (item === 'Analyse' && location.pathname === '/analysis')
                  ? 'text-[#0c7ff2]'
                  : 'text-[#0d141c] hover:text-[#0c7ff2]'
              }`}
            >
              {item === 'Nouvelle Analyse' ? '+ Nouvelle Analyse' : item}
            </Link>
          ))}
          
          <a href="mailto:info@leaseboost.fr"
            className="group relative overflow-hidden bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-all duration-300 transform hover:scale-105 shadow-sm hover:shadow-md"
          >
            <div className="flex items-center gap-2 relative z-10">
              <span>📧</span>
              <span>Contact</span>
            </div>
            
            <div className="absolute inset-0 -top-2 -bottom-2 bg-gradient-to-r from-transparent via-white/20 to-transparent transform -skew-x-12 translate-x-full group-hover:translate-x-[-200%] transition-transform duration-700"></div>
          </a>
        </div>
      </div>

      {/* Mobile Navigation */}
      <div className="lg:hidden flex items-center gap-4">
        <button
          onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
          className="text-[#0d141c] p-2"
          aria-label="Menu"
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
      </div>

      {isMobileMenuOpen && (
        <div className="absolute top-full left-0 right-0 bg-white border-b border-[#e7edf4] shadow-lg lg:hidden z-50">
          <div className="flex flex-col py-2">
            {nav.map((item) => (
              <Link
                key={item}
                to={getRouteForNavItem(item)}
                className="text-[#0d141c] text-sm font-medium leading-normal px-4 py-3 hover:bg-gray-50"
                onClick={() => setIsMobileMenuOpen(false)}
              >
                {item === 'Nouvelle Analyse' ? '+ Nouvelle Analyse' : item}
              </Link>
            ))}
            
            <a  href="mailto:info@leaseboost.fr"
              className="text-[#0c7ff2] text-sm font-medium leading-normal px-4 py-3 hover:bg-gray-50"
              onClick={() => setIsMobileMenuOpen(false)}
            >
              📧 Contact
            </a>
          </div>
        </div>
      )}
    </header>
  );
};

export default Header;