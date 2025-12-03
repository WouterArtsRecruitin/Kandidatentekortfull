import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { X, AlertTriangle, ArrowRight } from 'lucide-react';
import { Button } from './button';
import { trackEvent } from '../../lib/analytics';

export const ExitIntentPopup = () => {
  const [showPopup, setShowPopup] = useState(false);

  useEffect(() => {
    // Check if already shown this session
    const alreadyShown = sessionStorage.getItem('exit-intent-shown');
    if (alreadyShown) return;

    const handleMouseLeave = (e: MouseEvent) => {
      // Only trigger when mouse leaves from the top of the page
      if (e.clientY <= 0) {
        sessionStorage.setItem('exit-intent-shown', 'true');
        setShowPopup(true);
        trackEvent('exit_intent_shown', {});
      }
    };

    // Add listener after 5 seconds on page
    const timer = setTimeout(() => {
      document.addEventListener('mouseleave', handleMouseLeave);
    }, 5000);

    return () => {
      clearTimeout(timer);
      document.removeEventListener('mouseleave', handleMouseLeave);
    };
  }, []);

  const handleClose = () => {
    setShowPopup(false);
    trackEvent('exit_intent_closed', {});
  };

  const handleCTA = () => {
    setShowPopup(false);
    trackEvent('exit_intent_cta_clicked', {});
    // Scroll to the analyzer section
    document.getElementById('analyse-tool')?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <AnimatePresence>
      {showPopup && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-slate-900/80 backdrop-blur-sm"
          onClick={handleClose}
        >
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.9, opacity: 0 }}
            onClick={(e) => e.stopPropagation()}
            className="bg-white rounded-2xl p-6 md:p-8 max-w-md w-full shadow-2xl relative"
          >
            <button
              onClick={handleClose}
              className="absolute top-4 right-4 text-slate-400 hover:text-slate-600 transition-colors"
            >
              <X className="w-5 h-5" />
            </button>

            <div className="text-center">
              <div className="w-16 h-16 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <AlertTriangle className="w-8 h-8 text-orange-600" />
              </div>

              <h2 className="text-2xl font-black text-slate-900 mb-2">
                Wacht even!
              </h2>

              <p className="text-slate-600 mb-6">
                Je vacature laat waarschijnlijk <strong className="text-orange-600">40-60% potentiele kandidaten</strong> liggen.
                Ontdek gratis waar de verbeterpunten zitten.
              </p>

              <Button
                onClick={handleCTA}
                className="w-full bg-orange-600 hover:bg-orange-500 text-white font-bold py-4 rounded-xl"
              >
                <span className="flex items-center justify-center gap-2">
                  Gratis Analyse Starten
                  <ArrowRight className="w-5 h-5" />
                </span>
              </Button>

              <p className="text-xs text-slate-400 mt-4">
                Geen spam, geen verplichtingen. Direct resultaat.
              </p>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};
