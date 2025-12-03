import React from 'react';
import logoImg from "../../assets/recruitin-logo.png";

export const Header = () => {
  return (
    <header className="sticky top-0 z-50 bg-white/95 backdrop-blur-md border-b border-slate-200">
      <div className="container mx-auto px-4 md:px-6 h-20 flex items-center justify-between">
        {/* Logo */}
        <a href="/" className="flex items-center">
          <img src={logoImg} alt="Recruitin Logo" className="h-10 w-auto" />
        </a>

        {/* Right Side Stats */}
        <div className="flex flex-col items-end">
          <span className="text-[10px] md:text-xs font-bold text-slate-500 uppercase tracking-wider">Bewezen Resultaat</span>
          <span className="text-xl md:text-2xl font-black bg-gradient-to-br from-orange-500 to-orange-600 bg-clip-text text-transparent leading-none">
            40-60%
          </span>
        </div>
      </div>
    </header>
  );
};
