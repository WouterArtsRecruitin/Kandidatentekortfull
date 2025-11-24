import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from "motion/react";

const SOCIAL_PROOF_MESSAGES = [
  { name: "Martijn uit Arnhem", action: "optimaliseerde zijn Werkvoorbereider vacature", avatar: "👨" },
  { name: "Sarah uit Veghel", action: "kreeg 18 sollicitaties in 5 dagen", avatar: "👩" },
  { name: "Bas uit Eindhoven", action: "verhoogde zijn sollicitaties met 62%", avatar: "👨" },
  { name: "Lisa uit Nijmegen", action: "ontving haar Maintenance Engineer rapport", avatar: "👩" },
  { name: "Tom uit Breda", action: "optimaliseerde zijn Technisch Tekenaar rol", avatar: "👨" },
  { name: "Emma uit Apeldoorn", action: "kreeg net haar geoptimaliseerde vacature", avatar: "👩" },
  { name: "Peter uit Helmond", action: "verhoogde kwaliteit sollicitanten met 45%", avatar: "👨" },
  { name: "Sophie uit Tilburg", action: "kreeg 9 gekwalificeerde kandidaten", avatar: "👩" },
  { name: "Jan uit Ede", action: "optimaliseerde zijn Lasser vacature", avatar: "👨" },
  { name: "Linda uit Roosendaal", action: "ontving volledig rapport binnen 18 uur", avatar: "👩" },
];

export const SocialProofNotification = () => {
  const [currentMessage, setCurrentMessage] = useState<typeof SOCIAL_PROOF_MESSAGES[0] | null>(null);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    // Initial delay
    const startTimeout = setTimeout(() => {
      cycleMessage(0);
    }, 5000);

    return () => clearTimeout(startTimeout);
  }, []);

  const cycleMessage = (index: number) => {
    const msg = SOCIAL_PROOF_MESSAGES[index];
    setCurrentMessage(msg);
    setIsVisible(true);

    // Hide after 5 seconds
    setTimeout(() => {
      setIsVisible(false);
      
      // Wait 7 seconds before showing next (total 12s cycle like in HTML)
      setTimeout(() => {
        cycleMessage((index + 1) % SOCIAL_PROOF_MESSAGES.length);
      }, 7000);
    }, 5000);
  };

  return (
    <AnimatePresence>
      {isVisible && currentMessage && (
        <motion.div 
          initial={{ opacity: 0, x: -100 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -100 }}
          className="fixed top-24 md:top-28 left-4 md:left-6 z-40 max-w-[320px] w-full bg-white rounded-2xl p-4 shadow-[0_12px_32px_rgba(15,23,42,0.15)] border-l-4 border-emerald-500 flex items-center gap-3 pointer-events-none"
        >
          <div className="w-12 h-12 rounded-full bg-gradient-to-br from-emerald-100 to-blue-100 flex items-center justify-center text-xl shrink-0 border border-white shadow-sm">
            {currentMessage.avatar}
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-bold text-slate-900 truncate">{currentMessage.name}</p>
            <p className="text-xs text-slate-600 line-clamp-2 leading-snug">{currentMessage.action}</p>
            <p className="text-[10px] text-slate-400 mt-0.5 font-medium">Zojuist</p>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};
