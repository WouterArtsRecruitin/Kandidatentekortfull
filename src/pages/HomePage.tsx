import { useEffect } from 'react';
import { Hero } from '../components/sections/Hero';
import { VacancyAnalyzer } from '../components/sections/VacancyAnalyzer';

export const HomePage = () => {
  useEffect(() => {
    // Check if script is already loaded
    const existingScript = document.querySelector('script[src*="embed.typeform.com"]');
    if (existingScript) {
      return;
    }

    // Load Typeform embed script with explicit HTTPS
    const script = document.createElement('script');
    script.src = 'https://embed.typeform.com/next/embed.js';
    script.async = true;
    script.onload = () => {
      console.log('Typeform script loaded successfully');
    };
    script.onerror = () => {
      console.error('Failed to load Typeform script');
    };
    document.body.appendChild(script);

    // Cleanup function to remove script when component unmounts
    return () => {
      if (document.body.contains(script)) {
        document.body.removeChild(script);
      }
    };
  }, []);

  return (
    <>
      <Hero />
      <VacancyAnalyzer />
      {/* Typeform Embed */}
      <section className="py-16 bg-slate-50">
        <div className="container mx-auto px-4 md:px-6">
          <div className="w-full max-w-4xl mx-auto min-h-[600px]">
            <div data-tf-live="01K25SKWYTKZ05DAHER9D52J94"></div>
          </div>
        </div>
      </section>
    </>
  );
};
