import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import Logo from '../common/Logo';

const Header = () => {
  const location = useLocation();

  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  
  //mapping of navigation name to react routes
  const getRouteForNavItem = (navItem) => {
    switch(navItem) {
      case 'Tableau de bord':
        return '/';
      case 'Portefeuille':
        return '/portfolio';
      case 'Analyse':
        return '/analysis';
      case 'Baux':
        return '/portfolio';
      case 'Rapports':
        return '/analysis';
      case 'Paramètres':
        return '/';
      default:
        return '/';
    }
  };
  const getPageData = () => {
    switch(location.pathname) {
      case '/analysis':
        return {
          nav: ['Tableau de bord', 'Portefeuille', 'Analyse', 'Rapports', 'Paramètres'],
          avatar: 'https://lh3.googleusercontent.com/aida-public/AB6AXuBQOTmSy8D0yAT-1Lkfif6yiWzW6XJcdaE407K-CgP1eb2DF1fp_r3QeCSrKpf-kpcCZEB3lr005004K7roUkKGl_k-IimvwAcPWW3Dv_zFvWdBaLu16gVEDc8Cit8GNlKqXLIIUw-ZCjtFCXrWR980BHMnnB7xirVA6tWs4LuoqT7DOJh6rtFrytpW1Vjc5Ev5jLQsPByOFRUGGlYOt274vZixbqp2_2ti0EQbjWE6cbkeY7XbrNyLRcsBicL9lTTWH-FK3GcaRmYn'
        };
      case '/portfolio':
        return {
          nav: ['Tableau de bord', 'Portefeuille', 'Baux', 'Rapports', 'Aide'],
          avatar: 'https://lh3.googleusercontent.com/aida-public/AB6AXuBQOTmSy8D0yAT-1Lkfif6yiWzW6XJcdaE407K-CgP1eb2DF1fp_r3QeCSrKpf-kpcCZEB3lr005004K7roUkKGl_k-IimvwAcPWW3Dv_zFvWdBaLu16gVEDc8Cit8GNlKqXLIIUw-ZCjtFCXrWR980BHMnnB7xirVA6tWs4LuoqT7DOJh6rtFrytpW1Vjc5Ev5jLQsPByOFRUGGlYOt274vZixbqp2_2ti0EQbjWE6cbkeY7XbrNyLRcsBicL9lTTWH-FK3GcaRmYn'
        };
      default: // Home
        return {
          nav: ['Tableau de bord', 'Portefeuille', 'Rapports', 'Aide'],
          avatar: 'https://lh3.googleusercontent.com/aida-public/AB6AXuBQOTmSy8D0yAT-1Lkfif6yiWzW6XJcdaE407K-CgP1eb2DF1fp_r3QeCSrKpf-kpcCZEB3lr005004K7roUkKGl_k-IimvwAcPWW3Dv_zFvWdBaLu16gVEDc8Cit8GNlKqXLIIUw-ZCjtFCXrWR980BHMnnB7xirVA6tWs4LuoqT7DOJh6rtFrytpW1Vjc5Ev5jLQsPByOFRUGGlYOt274vZixbqp2_2ti0EQbjWE6cbkeY7XbrNyLRcsBicL9lTTWH-FK3GcaRmYn'
        };
    }
  };

  const { nav, avatar } = getPageData();
  
  return (
    <header className="relative flex items-center justify-between whitespace-nowrap border-b border-solid border-b-[#e7edf4] px-4 sm:px-10 py-3">
      <div className="flex items-center gap-4 text-[#0d141c]">
        <Logo />
        <h2 className="text-[#0d141c] text-lg font-bold leading-tight tracking-[-0.015em] hidden sm:block">LeaseBoost</h2>
         <h2 className="text-[#0d141c] text-sm font-bold leading-tight tracking-[-0.015em] sm:hidden">LeaseBoost</h2>
      </div>
      <div className="hidden lg:flex flex-1 justify-end gap-8">
        <div className="flex items-center gap-9">
          {nav.map((item) => (
            <Link
              key={item}
              to={getRouteForNavItem(item)}
              className="text-[#0d141c] text-sm font-medium leading-normal"
            >
              {item}
            </Link>
          ))}
        </div>
        <div
          className="bg-center bg-no-repeat aspect-square bg-cover rounded-full size-10"
          style={{ backgroundImage: `url("${avatar}")` }}
        />
      </div>

      <div className="lg:hidden flex items-center gap-4">
        <div
          className="bg-center bg-no-repeat aspect-square bg-cover rounded-full size-8"
          style={{ backgroundImage: `url("${avatar}")` }}
        />
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
                {item}
              </Link>
            ))}
          </div>
        </div>
      )}
    </header>
  );
};

export default Header;