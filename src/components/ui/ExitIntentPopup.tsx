import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { X, Zap, ArrowRight, CheckCircle2 } from 'lucide-react';
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
          className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-slate-900/90 backdrop-blur-md"
          onClick={handleClose}
        >
          <motion.div
            initial={{ scale: 0.9, opacity: 0, y: 20 }}
            animate={{ scale: 1, opacity: 1, y: 0 }}
            exit={{ scale: 0.9, opacity: 0, y: 20 }}
            transition={{ type: 'spring', damping: 25, stiffness: 300 }}
            onClick={(e) => e.stopPropagation()}
            className="bg-white rounded-3xl max-w-lg w-full shadow-2xl relative overflow-hidden"
          >
            {/* Header gradient */}
            <div className="bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 px-6 py-8 md:px-8 md:py-10 text-center relative">
              <button
                onClick={handleClose}
                className="absolute top-4 right-4 text-white/60 hover:text-white transition-colors"
              >
                <X className="w-6 h-6" />
              </button>

              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: 0.2, type: 'spring', stiffness: 200 }}
                className="w-16 h-16 bg-orange-500 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg shadow-orange-500/30"
              >
                <Zap className="w-8 h-8 text-white" />
              </motion.div>

              <h2 className="text-2xl md:text-3xl font-black text-white mb-2">
                Wacht! Mis dit niet
              </h2>
              <p className="text-slate-300 text-sm md:text-base">
                Je vacature presteert waarschijnlijk onder de maat
              </p>
            </div>

            {/* Content */}
            <div className="px-6 py-6 md:px-8 md:py-8">
              <div className="space-y-3 mb-6">
                <div className="flex items-start gap-3">
                  <CheckCircle2 className="w-5 h-5 text-emerald-500 shrink-0 mt-0.5" />
                  <p className="text-slate-700 text-sm">
                    <strong>40-60% meer sollicitaties</strong> na optimalisatie
                  </p>
                </div>
                <div className="flex items-start gap-3">
                  <CheckCircle2 className="w-5 h-5 text-emerald-500 shrink-0 mt-0.5" />
                  <p className="text-slate-700 text-sm">
                    <strong>Binnen 24 uur</strong> verbeterde tekst in je inbox
                  </p>
                </div>
                <div className="flex items-start gap-3">
                  <CheckCircle2 className="w-5 h-5 text-emerald-500 shrink-0 mt-0.5" />
                  <p className="text-slate-700 text-sm">
                    <strong>100% gratis</strong> - geen verplichtingen
                  </p>
                </div>
              </div>

              <button
                onClick={handleCTA}
                className="w-full bg-orange-600 hover:bg-orange-500 text-white font-bold py-4 px-6 rounded-xl transition-all shadow-lg shadow-orange-600/20 flex items-center justify-center gap-2 text-base md:text-lg"
              >
                Ja, analyseer mijn vacature
                <ArrowRight className="w-5 h-5" />
              </button>

              <button
                onClick={handleClose}
                className="w-full text-slate-400 hover:text-slate-600 text-sm mt-4 py-2 transition-colors"
              >
                Nee bedankt, ik heb geen vacatures
              </button>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};
