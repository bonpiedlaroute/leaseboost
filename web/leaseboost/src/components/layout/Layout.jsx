import React from 'react';
import { useLocation } from 'react-router-dom';
import Header from './Header';

const Layout = ({ children }) => {
  const location = useLocation();
  
  return (
    <div 
      className="relative flex size-full min-h-screen flex-col bg-slate-50 group/design-root overflow-x-hidden" 
      style={{ fontFamily: 'Inter, "Noto Sans", sans-serif' }}
    >
      <div className="layout-container flex h-full grow flex-col">
        <Header />
        <div className="px-4 sm:px-8 lg:px-40 flex flex-1 justify-center py-5">
          {location.pathname === '/' ? (
            <div className="layout-content-container flex flex-col w-full max-w-[512px] lg:max-w-[960px] py-5 flex-1">
              {children}
            </div>
          ) : (
            <div className="layout-content-container flex flex-col w-full max-w-[960px] flex-1">
              {children}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Layout;