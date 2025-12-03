import React from 'react';
import { Header } from './components/layout/Header';
import { Hero } from './components/sections/Hero';
import { VacancyAnalyzer } from './components/sections/VacancyAnalyzer';
import { Footer } from './components/layout/Footer';
import { SocialProofNotification } from './components/ui/SocialProofNotification';
import { initAnalytics } from './lib/analytics';

function App() {
  React.useEffect(() => {
    initAnalytics();
  }, []);

  return (
    <div className="min-h-screen bg-slate-50 font-sans text-slate-900 antialiased selection:bg-orange-500/30">
      <Header />
      <main>
        <Hero />
        <VacancyAnalyzer />
      </main>
      <Footer />
      <SocialProofNotification />
    </div>
  );
}

export default App;