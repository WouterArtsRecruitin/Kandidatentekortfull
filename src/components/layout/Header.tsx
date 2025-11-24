import React from 'react';
import { motion, AnimatePresence } from "motion/react";
import { CheckCircle2, X } from "lucide-react";
import logoImg from "figma:asset/09ea8267eac5f2dc8b43b1c872493f46ab50ea58.png";

export const Header = () => {
  return (
    <header className="sticky top-0 z-50 bg-white/95 backdrop-blur-md border-b border-slate-200">
      <div className="container mx-auto px-4 md:px-6 h-20 flex items-center justify-between">
        {/* Logo Section */}
        <div className="flex items-center gap-4">
          <a href="/" className="flex items-center gap-2">
             {/* Using the imported Figma asset for the logo */}
            <img src={logoImg} alt="Recruitin Logo" className="h-10 w-auto object-contain" />
          </a>
          
          <div className="hidden sm:flex items-center gap-1.5 px-3 py-1.5 bg-blue-50/50 border border-emerald-500/20 rounded-full text-xs font-bold text-emerald-600">
            <CheckCircle2 className="w-3.5 h-3.5 fill-emerald-100 text-emerald-600" />
            Expert Verified
          </div>
        </div>

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
