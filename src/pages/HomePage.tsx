import { useEffect } from 'react';
import { Hero } from '../components/sections/Hero';
import { VacancyAnalyzer } from '../components/sections/VacancyAnalyzer';

export const HomePage = () => {
  useEffect(() => {
    // Load Typeform embed script
    const script = document.createElement('script');
    script.src = '//embed.typeform.com/next/embed.js';
    script.async = true;
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
          <div data-tf-live="01K25SKWYTKZ05DAHER9D52J94"></div>
        </div>
      </section>
    </>
  );
};
