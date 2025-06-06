import React from 'react';

const Button = ({ children, variant = 'primary', className = '', unstyled = false, ...props }) => {
  const baseClasses = "flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 px-4 text-sm font-bold leading-normal tracking-[0.015em]";
  
  const variantClasses = {
    primary: "bg-[#0c7ff2] text-slate-50",
    secondary: "bg-[#e7edf4] text-[#0d141c]",
    tertiary: "bg-[#e7edf4] text-[#0d141c] font-medium",
    impact: "bg-[#e7edf4] text-[#0d141c] h-8 font-medium"
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