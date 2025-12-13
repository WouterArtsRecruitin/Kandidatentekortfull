import React, { useState, useEffect } from 'react';
import { ReportPreviewA } from './components/ReportPreviewA';
import { ReportPreviewB } from './components/ReportPreviewB';
import { ReportPreviewC } from './components/ReportPreviewC';
import { CookieConsent } from './components/CookieConsent';
import { trackVersionView, trackPageView, trackEngagement } from './utils/tracking';

export default function App() {
  const [version, setVersion] = useState<'a' | 'b' | 'c'>('a');
  const [startTime] = useState(Date.now());

  // Track page view on mount
  useEffect(() => {
    trackPageView('RecruitmentAPK - Home');
    
    // Track engagement every 60 seconds
    const engagementInterval = setInterval(() => {
      const secondsOnPage = Math.floor((Date.now() - startTime) / 1000);
      trackEngagement(secondsOnPage);
    }, 60000);
    
    return () => clearInterval(engagementInterval);
  }, [startTime]);

  // Track version changes
  useEffect(() => {
    trackVersionView(version);
  }, [version]);

  const handleVersionChange = (newVersion: 'a' | 'b' | 'c') => {
    setVersion(newVersion);
  };

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Cookie Consent Banner */}
      <CookieConsent />
      
      {/* Version Switcher */}
      <div className="sticky top-0 z-50 bg-white border-b border-slate-200 shadow-sm print:hidden">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <span className="text-sm font-medium text-slate-900">RecruitmentAPK.nl</span>
              <span className="text-sm text-slate-500">|</span>
              <span className="text-sm text-slate-600">A/B/C Test Varianten</span>
            </div>
            <div className="flex gap-2">
              <button
                onClick={() => handleVersionChange('a')}
                className={`px-6 py-2 text-sm rounded-sm transition-colors ${
                  version === 'a'
                    ? 'bg-slate-900 text-white'
                    : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                }`}
              >
                Versie A - Classic Report
              </button>
              <button
                onClick={() => handleVersionChange('b')}
                className={`px-6 py-2 text-sm rounded-sm transition-colors ${
                  version === 'b'
                    ? 'bg-slate-900 text-white'
                    : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                }`}
              >
                Versie B - Interactive Dashboard
              </button>
              <button
                onClick={() => handleVersionChange('c')}
                className={`px-6 py-2 text-sm rounded-sm transition-colors ${
                  version === 'c'
                    ? 'bg-slate-900 text-white'
                    : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                }`}
              >
                Versie C - Printable Report
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Content */}
      {version === 'a' ? <ReportPreviewA /> : version === 'b' ? <ReportPreviewB /> : <ReportPreviewC />}
    </div>
  );
}
