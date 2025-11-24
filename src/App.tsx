import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { HomePage } from './pages/HomePage';
import { MetaCampaignPage } from './pages/MetaCampaignPage';
import { Footer } from './components/layout/Footer';
import { SocialProofNotification } from './components/ui/SocialProofNotification';
import { Toaster } from './components/ui/sonner';
import { initAnalytics } from './lib/analytics';

function App() {
  React.useEffect(() => {
    initAnalytics();
  }, []);

  return (
    <div className="min-h-screen bg-slate-50 font-sans text-slate-900 antialiased selection:bg-orange-500/30">
      <main>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/meta" element={<MetaCampaignPage />} />
        </Routes>
      </main>
      <Footer />
      <SocialProofNotification />
      <Toaster />
    </div>
  );
}

export default App;