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

// UTM Parameters
interface UTMParams {
  utm_source?: string;
  utm_medium?: string;
  utm_campaign?: string;
  utm_term?: string;
  utm_content?: string;
}

// Get and store UTM parameters
export const getUTMParams = (): UTMParams => {
  if (typeof window === 'undefined') return {};

  // Check localStorage first (for session persistence)
  const stored = localStorage.getItem('utm_params');
  let utmParams: UTMParams = stored ? JSON.parse(stored) : {};

  // Parse current URL for UTM params
  const urlParams = new URLSearchParams(window.location.search);
  const utmKeys = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content'];

  let hasNewParams = false;
  utmKeys.forEach(key => {
    const value = urlParams.get(key);
    if (value) {
      utmParams[key as keyof UTMParams] = value;
      hasNewParams = true;
    }
  });

  // Store if we found new params
  if (hasNewParams) {
    localStorage.setItem('utm_params', JSON.stringify(utmParams));
    console.log('[UTM] Stored params:', utmParams);
  }

  return utmParams;
};

// Generate UTM link
export const generateUTMLink = (
  baseUrl: string = 'https://kandidatentekort.nl',
  source: string,
  medium: string,
  campaign: string,
  content?: string,
  term?: string
): string => {
  const params = new URLSearchParams({
    utm_source: source,
    utm_medium: medium,
    utm_campaign: campaign,
    ...(content && { utm_content: content }),
    ...(term && { utm_term: term })
  });
  return `${baseUrl}?${params.toString()}`;
};

// Pre-configured UTM links for common channels
export const UTM_LINKS = {
  facebook_ads: generateUTMLink('https://kandidatentekort.nl', 'facebook', 'cpc', 'vacature_analyse'),
  facebook_organic: generateUTMLink('https://kandidatentekort.nl', 'facebook', 'organic', 'social_post'),
  linkedin_ads: generateUTMLink('https://kandidatentekort.nl', 'linkedin', 'cpc', 'vacature_analyse'),
  linkedin_organic: generateUTMLink('https://kandidatentekort.nl', 'linkedin', 'organic', 'social_post'),
  email_newsletter: generateUTMLink('https://kandidatentekort.nl', 'email', 'newsletter', 'weekly'),
  email_direct: generateUTMLink('https://kandidatentekort.nl', 'email', 'direct', 'outreach'),
  whatsapp: generateUTMLink('https://kandidatentekort.nl', 'whatsapp', 'referral', 'share'),
  google_ads: generateUTMLink('https://kandidatentekort.nl', 'google', 'cpc', 'vacature_analyse'),
};

// Server-side tracking via Netlify function (FB CAPI + GA4 MP)
async function sendServerSideEvent(eventName: string, customData: Record<string, any> = {}) {
  try {
    // Get Facebook cookies for better matching
    const getCookie = (name: string) => {
      const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
      return match ? match[2] : null;
    };

    const fbp = getCookie('_fbp');
    const fbc = getCookie('_fbc');

    const payload = {
      event_name: eventName,
      event_id: `evt_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      client_ip: '', // Will be filled by server
      user_agent: navigator.userAgent,
      fbp,
      fbc,
      ...customData
    };

    const response = await fetch('/.netlify/functions/track-conversion', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (response.ok) {
      console.log(`[Server-Side Tracking] ✅ ${eventName} sent successfully`);
    }
  } catch (error) {
    console.error('❌ Server-side tracking error:', error);
  }
}

export const trackEvent = async (eventName: string, data?: any) => {
  // Get UTM params and merge with event data
  const utmParams = getUTMParams();
  const enrichedData = { ...data, ...utmParams };

  console.log(`[Analytics] Tracking Event: ${eventName}`, enrichedData);

  if (typeof window !== 'undefined') {
    // GA4
    // @ts-ignore
    if (window.gtag) {
      // @ts-ignore
      window.gtag('event', eventName, enrichedData);
    }

    // Facebook Pixel
    // @ts-ignore
    if (window.fbq) {
      // @ts-ignore
      window.fbq('track', eventName, enrichedData);
    }

    // Server-side event with UTM
    sendServerSideEvent(eventName, enrichedData);
  }
};

export const initAnalytics = () => {
  console.log('[Analytics] Initialized V3 Tracking Systems');

  // Capture UTM params on page load
  const utmParams = getUTMParams();
  if (Object.keys(utmParams).length > 0) {
    console.log('[Analytics] UTM params captured:', utmParams);
  }

  // Initialize GA4 layer
  // @ts-ignore
  window.dataLayer = window.dataLayer || [];
  // @ts-ignore
  function gtag(){dataLayer.push(arguments);}
  // @ts-ignore
  gtag('js', new Date());
  // @ts-ignore
  gtag('config', 'G-67PJ02SXVN', {
    // Pass UTM params to GA4
    campaign_source: utmParams.utm_source,
    campaign_medium: utmParams.utm_medium,
    campaign_name: utmParams.utm_campaign,
    campaign_term: utmParams.utm_term,
    campaign_content: utmParams.utm_content
  });

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
  fbq('track', 'PageView', utmParams);
};

// Print all UTM links for marketing use
export const printUTMLinks = () => {
  console.log('\n========== UTM LINKS ==========\n');
  Object.entries(UTM_LINKS).forEach(([name, url]) => {
    console.log(`${name}:\n${url}\n`);
  });
  console.log('================================\n');
  return UTM_LINKS;
};
