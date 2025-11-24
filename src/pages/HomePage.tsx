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
          <div className="w-full max-w-4xl mx-auto" style={{ height: '600px' }}>
            <div
              data-tf-widget="01KARGCADMYDCG24PA4FWVKZJ2"
              data-tf-opacity="0"
              data-tf-iframe-props="title=Typeform"
              data-tf-transitive-search-params
              data-tf-medium="snippet"
              style={{ width: '100%', height: '100%' }}
            ></div>
          </div>
        </div>
      </section>
    </>
  );
};
