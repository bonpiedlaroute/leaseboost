import React from 'react';

const Button = ({ children, variant = 'primary', className = '', unstyled = false, ...props }) => {
  const baseClasses = "flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 px-4 text-sm font-bold leading-normal tracking-[0.015em] transition-all duration-300";
  
  const variantClasses = {
  primary: "bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white transform hover:scale-105 shadow-sm hover:shadow-md",
  secondary: "bg-gradient-to-r from-gray-100 to-gray-200 hover:from-gray-200 hover:to-gray-300 text-gray-700 transform hover:scale-105",
  tertiary: "bg-gradient-to-r from-blue-50 to-indigo-50 hover:from-blue-100 hover:to-indigo-100 text-blue-600 font-medium transform hover:scale-105",
  impact: "bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600 text-white h-8 font-medium transform hover:scale-105"
};
  
  // Si unstyled=true, on utilise seulement className
  const finalClassName = unstyled 
    ? className 
    : `${baseClasses} ${variantClasses[variant]} ${className}`;
  
  return (
    <button
      className={finalClassName}
      {...props}
    >
      <span className="truncate">{children}</span>
    </button>
  );
};

export default Button;