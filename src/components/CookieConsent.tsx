import React, { useState, useEffect } from 'react';
import { initializeTracking, TRACKING_CONFIG } from '../utils/tracking';

interface CookieConsentProps {
  onAccept?: () => void;
  onDecline?: () => void;
}

export function CookieConsent({ onAccept, onDecline }: CookieConsentProps) {
  const [isVisible, setIsVisible] = useState(false);
  const [showDetails, setShowDetails] = useState(false);

  useEffect(() => {
    // Check if consent was already given
    const consent = localStorage.getItem('cookie_consent');
    if (consent === null) {
      // Show banner after small delay for better UX
      setTimeout(() => setIsVisible(true), 1000);
    } else if (consent === 'accepted') {
      window.cookieConsent = true;
      initializeTracking();
    }
  }, []);

  const handleAccept = () => {
    localStorage.setItem('cookie_consent', 'accepted');
    localStorage.setItem('cookie_consent_date', new Date().toISOString());
    window.cookieConsent = true;
    initializeTracking();
    setIsVisible(false);
    onAccept?.();
  };

  const handleDecline = () => {
    localStorage.setItem('cookie_consent', 'declined');
    localStorage.setItem('cookie_consent_date', new Date().toISOString());
    window.cookieConsent = false;
    setIsVisible(false);
    onDecline?.();
  };

  const handleAcceptNecessary = () => {
    localStorage.setItem('cookie_consent', 'necessary_only');
    localStorage.setItem('cookie_consent_date', new Date().toISOString());
    window.cookieConsent = false;
    setIsVisible(false);
    onDecline?.();
  };

  if (!isVisible) return null;

  return (
    <div className="fixed bottom-0 left-0 right-0 z-[9999] print:hidden">
      {/* Backdrop */}
      <div className="absolute inset-0 bg-black/20 backdrop-blur-sm -z-10" />
      
      {/* Banner */}
      <div className="bg-white border-t border-slate-200 shadow-2xl">
        <div className="max-w-6xl mx-auto px-6 py-6">
          <div className="flex flex-col lg:flex-row lg:items-start lg:justify-between gap-6">
            {/* Text */}
            <div className="flex-1">
              <h3 className="text-lg font-semibold text-slate-900 mb-2">
                🍪 Cookies & Privacy
              </h3>
              <p className="text-slate-600 text-sm leading-relaxed">
                Wij gebruiken cookies om je ervaring te verbeteren en onze diensten te optimaliseren. 
                Met analytische cookies kunnen we zien hoe bezoekers onze site gebruiken. 
                Marketing cookies helpen ons relevante content te tonen.
              </p>
              
              {/* Details toggle */}
              <button
                onClick={() => setShowDetails(!showDetails)}
                className="text-sm text-blue-600 hover:text-blue-700 mt-2 underline"
              >
                {showDetails ? 'Verberg details' : 'Meer informatie'}
              </button>
              
              {/* Details */}
              {showDetails && (
                <div className="mt-4 p-4 bg-slate-50 rounded-lg text-sm">
                  <div className="space-y-3">
                    <div>
                      <strong className="text-slate-900">Noodzakelijke cookies</strong>
                      <p className="text-slate-600">Vereist voor basisfunctionaliteit. Altijd actief.</p>
                    </div>
                    <div>
                      <strong className="text-slate-900">Analytische cookies (Google Analytics)</strong>
                      <p className="text-slate-600">Helpen ons begrijpen hoe bezoekers de site gebruiken. ID: {TRACKING_CONFIG.GA4_ID}</p>
                    </div>
                    <div>
                      <strong className="text-slate-900">Marketing cookies (Meta Pixel)</strong>
                      <p className="text-slate-600">Worden gebruikt voor gepersonaliseerde advertenties en remarketing.</p>
                    </div>
                  </div>
                  <p className="mt-4 text-xs text-slate-500">
                    Lees ons{' '}
                    <a href="/privacy" className="text-blue-600 hover:underline">privacybeleid</a>
                    {' '}voor meer informatie.
                  </p>
                </div>
              )}
            </div>
            
            {/* Buttons */}
            <div className="flex flex-col sm:flex-row lg:flex-col gap-3 lg:min-w-[200px]">
              <button
                onClick={handleAccept}
                className="px-6 py-3 bg-slate-900 text-white font-medium rounded-lg hover:bg-slate-800 transition-colors text-sm"
              >
                Alles accepteren
              </button>
              <button
                onClick={handleAcceptNecessary}
                className="px-6 py-3 bg-slate-100 text-slate-700 font-medium rounded-lg hover:bg-slate-200 transition-colors text-sm"
              >
                Alleen noodzakelijk
              </button>
              <button
                onClick={handleDecline}
                className="px-6 py-3 text-slate-500 hover:text-slate-700 text-sm underline"
              >
                Weigeren
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default CookieConsent;
