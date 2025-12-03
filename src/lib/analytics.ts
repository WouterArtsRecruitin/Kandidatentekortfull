import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// Analytics Types
type TrackingEvent = {
  name: string;
  properties?: Record<string, any>;
};

// Mock server-side tracking function to match HTML logic
async function sendServerSideEvent(eventName: string, customData = {}) {
  try {
    // In a real app, this would get cookies
    const fbp = 'mock_fbp'; 
    const fbc = 'mock_fbc';
    
    console.log(`[Server-Side Tracking] Sending ${eventName}`, {
      event_name: eventName,
      event_source_url: window.location.href,
      user_data: { fbp, fbc },
      custom_data: customData
    });

    // Simulating the fetch call to Netlify/Supabase function
    // const response = await fetch('/.netlify/functions/track-conversion', { ... });
  } catch (error) {
    console.error('❌ Tracking error:', error);
  }
}

export const trackEvent = async (eventName: string, data?: any) => {
  console.log(`[Analytics] Tracking Event: ${eventName}`, data);

  if (typeof window !== 'undefined') {
    // GA4
    // @ts-ignore
    if (window.gtag) {
      // @ts-ignore
      window.gtag('event', eventName, data);
    }
    
    // Facebook Pixel
    // @ts-ignore
    if (window.fbq) {
      // @ts-ignore
      window.fbq('track', eventName, data);
    }
    
    // Server-side event
    sendServerSideEvent(eventName, data);
  }
};

export const initAnalytics = () => {
  console.log('[Analytics] Initialized V3 Tracking Systems');
  
  // Load scripts dynamically if needed, or just rely on index.html if we could edit it. 
  // Since we can't edit index.html easily in this environment to add external scripts permanently,
  // we assume they might be added or we just log for now.
  
  // Initialize GA4 layer
  // @ts-ignore
  window.dataLayer = window.dataLayer || [];
  // @ts-ignore
  function gtag(){dataLayer.push(arguments);}
  // @ts-ignore
  gtag('js', new Date());
  // @ts-ignore
  gtag('config', 'G-67PJ02SXVN');

  // Initialize FB Pixel
  // @ts-ignore
  !function(f,b,e,v,n,t,s)
  {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
  n.callMethod.apply(n,arguments):n.queue.push(arguments)};
  if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
  n.queue=[];t=b.createElement(e);t.async=!0;
  t.src=v;s=b.getElementsByTagName(e)[0];
  s.parentNode.insertBefore(t,s)}(window, document,'script',
  'https://connect.facebook.com/en_US/fbevents.js');
  
  // @ts-ignore
  fbq('init', '1735907367288442');
  // @ts-ignore
  fbq('track', 'PageView');
};
