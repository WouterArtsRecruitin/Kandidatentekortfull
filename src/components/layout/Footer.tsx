import React from 'react';
import { Mail, Phone, Globe } from 'lucide-react';
import recruitinLogo from '../../assets/recruitin-logo-white.png';

export const Footer = () => {
  return (
    <footer className="bg-slate-950 text-slate-300 py-16 border-t border-slate-900">
      <div className="container mx-auto px-4 md:px-6">
        {/* Centered Footer Content */}
        <div className="flex flex-col items-center text-center space-y-6">
          
          {/* Logo */}
          <div className="flex flex-col items-center">
            <img 
              src={recruitinLogo} 
              alt="Recruitin - The right people, right now" 
              className="h-16 md:h-20 w-auto object-contain"
            />
          </div>

          {/* Contact Info - Horizontal */}
          <div className="flex flex-wrap items-center justify-center gap-6 md:gap-8 text-sm">
            <a 
              href="https://www.recruitin.nl" 
              target="_blank" 
              rel="noopener noreferrer" 
              className="flex items-center gap-2 hover:text-orange-500 transition-colors group"
            >
              <Globe className="w-4 h-4 text-slate-500 group-hover:text-orange-500 transition-colors" />
              <span>www.recruitin.nl</span>
            </a>
            
            <a 
              href="mailto:info@recruitin.nl" 
              className="flex items-center gap-2 hover:text-orange-500 transition-colors group"
            >
              <Mail className="w-4 h-4 text-slate-500 group-hover:text-orange-500 transition-colors" />
              <span>info@recruitin.nl</span>
            </a>
            
            <a 
              href="tel:+31313410507" 
              className="flex items-center gap-2 hover:text-orange-500 transition-colors group"
            >
              <Phone className="w-4 h-4 text-slate-500 group-hover:text-orange-500 transition-colors" />
              <span>+31 313 410 507</span>
            </a>
          </div>

        </div>

        {/* Bottom Bar */}
        <div className="pt-12 mt-12 border-t border-slate-900 text-center md:flex md:justify-between md:items-center text-xs text-slate-600">
          <p>&copy; {new Date().getFullYear()} Recruitin B.V. Alle rechten voorbehouden.</p>
          <div className="flex gap-6 justify-center mt-4 md:mt-0">
            <a href="https://recruitin.nl/privacyverklaring-recruitin/" target="_blank" rel="noopener noreferrer" className="hover:text-slate-400 transition-colors">Privacy Policy</a>
            <a href="/cookiebeleid.html" className="hover:text-slate-400 transition-colors">Cookiebeleid</a>
            <a href="https://recruitin.nl/contact/" target="_blank" rel="noopener noreferrer" className="hover:text-slate-400 transition-colors">Contact</a>
          </div>
        </div>
      </div>
    </footer>
  );
};