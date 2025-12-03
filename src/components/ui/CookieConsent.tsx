import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { Cookie, X } from 'lucide-react';
import { Button } from './button';

export const CookieConsent = () => {
  const [showBanner, setShowBanner] = useState(false);

  useEffect(() => {
    const consent = localStorage.getItem('cookie-consent');
    if (!consent) {
      // Show banner after 1 second
      const timer = setTimeout(() => setShowBanner(true), 1000);
      return () => clearTimeout(timer);
    }
  }, []);

  const acceptCookies = () => {
    localStorage.setItem('cookie-consent', 'accepted');
    setShowBanner(false);
  };

  const declineCookies = () => {
    localStorage.setItem('cookie-consent', 'declined');
    setShowBanner(false);
  };

  return (
    <AnimatePresence>
      {showBanner && (
        <motion.div
          initial={{ y: 100, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          exit={{ y: 100, opacity: 0 }}
          className="fixed bottom-0 left-0 right-0 z-[60] p-4 md:p-6"
        >
          <div className="max-w-4xl mx-auto bg-white rounded-2xl shadow-2xl border border-slate-200 p-4 md:p-6">
            <div className="flex flex-col md:flex-row items-start md:items-center gap-4">
              <div className="flex items-start gap-3 flex-1">
                <div className="w-10 h-10 rounded-full bg-orange-100 flex items-center justify-center shrink-0">
                  <Cookie className="w-5 h-5 text-orange-600" />
                </div>
                <div>
                  <h3 className="font-bold text-slate-900 mb-1">Wij gebruiken cookies</h3>
                  <p className="text-sm text-slate-600">
                    We gebruiken cookies om je ervaring te verbeteren en onze service te optimaliseren.
                    Lees onze{' '}
                    <a
                      href="https://recruitin.nl/privacyverklaring-recruitin/"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-orange-600 hover:underline font-medium"
                    >
                      privacyverklaring
                    </a>
                    {' '}voor meer informatie.
                  </p>
                </div>
              </div>
              <div className="flex gap-2 w-full md:w-auto">
                <Button
                  onClick={declineCookies}
                  variant="outline"
                  className="flex-1 md:flex-none text-sm"
                >
                  Weigeren
                </Button>
                <Button
                  onClick={acceptCookies}
                  className="flex-1 md:flex-none bg-orange-600 hover:bg-orange-500 text-white text-sm"
                >
                  Accepteren
                </Button>
              </div>
            </div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};
