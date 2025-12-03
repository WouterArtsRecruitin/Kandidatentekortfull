import React from 'react';
import { motion } from 'motion/react';
import { MessageCircle } from 'lucide-react';
import { trackEvent } from '../../lib/analytics';

// WhatsApp number - update this with Recruitin's number
const WHATSAPP_NUMBER = '31313410507';
const WHATSAPP_MESSAGE = 'Hoi! Ik heb een vraag over de vacature analyse.';

export const WhatsAppButton = () => {
  const handleClick = () => {
    trackEvent('whatsapp_click', { location: 'floating_button' });
    const url = `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(WHATSAPP_MESSAGE)}`;
    window.open(url, '_blank');
  };

  return (
    <motion.button
      onClick={handleClick}
      initial={{ scale: 0, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{ delay: 2, type: 'spring', stiffness: 200 }}
      whileHover={{ scale: 1.1 }}
      whileTap={{ scale: 0.95 }}
      className="fixed bottom-6 right-6 z-50 w-14 h-14 bg-[#25D366] hover:bg-[#20BD5A] rounded-full shadow-lg flex items-center justify-center group"
      aria-label="Contact via WhatsApp"
    >
      <MessageCircle className="w-7 h-7 text-white fill-white" />

      {/* Tooltip */}
      <span className="absolute right-full mr-3 px-3 py-2 bg-slate-900 text-white text-sm font-medium rounded-lg opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none">
        Chat met ons!
      </span>

      {/* Pulse animation */}
      <span className="absolute inset-0 rounded-full bg-[#25D366] animate-ping opacity-25" />
    </motion.button>
  );
};
