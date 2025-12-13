// RecruitmentAPK Tracking Utilities
// Meta Pixel + GA4 integration

declare global {
  interface Window {
    fbq: any;
    gtag: any;
    dataLayer: any[];
    cookieConsent: boolean;
    initMetaPixel: (pixelId: string) => void;
    trackEvent: (eventName: string, params?: Record<string, any>) => void;
    trackMetaEvent: (eventName: string, params?: Record<string, any>) => void;
  }
}

// Configuration
export const TRACKING_CONFIG = {
  META_PIXEL_ID: '238226887541404',
  GA4_ID: 'G-XXXXXXXXXX', // TODO: Maak GA4 property aan voor recruitmentapk.nl
  LEAD_VALUE: 45.00,
  CURRENCY: 'EUR'
};

// Initialize tracking after consent
export function initializeTracking(): void {
  if (typeof window !== 'undefined' && window.cookieConsent) {
    // Initialize Meta Pixel
    if (window.initMetaPixel) {
      window.initMetaPixel();
    }
    console.log('[Tracking] Initialized with consent - Pixel: 238226887541404');
  }
}

// Track page view
export function trackPageView(pageName: string): void {
  // GA4
  if (window.trackEvent) {
    window.trackEvent('page_view', {
      page_title: pageName,
      page_location: window.location.href
    });
  }
  
  // Meta
  if (window.trackMetaEvent) {
    window.trackMetaEvent('ViewContent', {
      content_name: pageName,
      content_category: 'recruitment_apk'
    });
  }
}

// Track form view (when assessment form is shown)
export function trackFormView(): void {
  // GA4
  if (window.trackEvent) {
    window.trackEvent('view_form', {
      form_name: 'recruitment_apk_assessment',
      form_type: 'lead_form'
    });
  }
  
  // Meta
  if (window.trackMetaEvent) {
    window.trackMetaEvent('ViewContent', {
      content_name: 'Recruitment APK Form',
      content_category: 'lead_form'
    });
  }
}

// Track assessment start
export function trackAssessmentStart(): void {
  // GA4
  if (window.trackEvent) {
    window.trackEvent('begin_checkout', {
      value: 25.00,
      currency: TRACKING_CONFIG.CURRENCY,
      items: [{
        item_name: 'Recruitment APK Assessment',
        item_category: 'assessment'
      }]
    });
  }
  
  // Meta
  if (window.trackMetaEvent) {
    window.trackMetaEvent('InitiateCheckout', {
      content_name: 'Recruitment APK Started',
      value: 25.00,
      currency: TRACKING_CONFIG.CURRENCY
    });
  }
}

// Track assessment completion (MAIN CONVERSION)
export function trackAssessmentComplete(formData?: {
  company?: string;
  industry?: string;
  employees?: string;
  score?: number;
}): void {
  const params = {
    content_name: 'Recruitment APK Completed',
    value: TRACKING_CONFIG.LEAD_VALUE,
    currency: TRACKING_CONFIG.CURRENCY,
    content_category: 'recruitment_assessment',
    ...(formData?.company && { company: formData.company }),
    ...(formData?.industry && { industry: formData.industry }),
    ...(formData?.employees && { company_size: formData.employees }),
    ...(formData?.score && { score: formData.score })
  };
  
  // GA4 - Lead event
  if (window.trackEvent) {
    window.trackEvent('generate_lead', {
      ...params,
      lead_source: 'recruitment_apk'
    });
  }
  
  // Meta - Lead event (primary conversion)
  if (window.trackMetaEvent) {
    window.trackMetaEvent('Lead', params);
    
    // Also track as CompleteRegistration
    window.trackMetaEvent('CompleteRegistration', {
      content_name: 'Recruitment APK Complete',
      status: 'completed'
    });
  }
}

// Track report download
export function trackReportDownload(reportType: 'demo' | 'full'): void {
  // GA4
  if (window.trackEvent) {
    window.trackEvent('file_download', {
      file_name: `recruitment_apk_report_${reportType}`,
      file_extension: 'pdf'
    });
  }
  
  // Meta
  if (window.trackMetaEvent) {
    window.trackMetaEvent('Purchase', {
      content_name: `Recruitment APK Report - ${reportType}`,
      value: reportType === 'full' ? 50.00 : 0,
      currency: TRACKING_CONFIG.CURRENCY
    });
  }
}

// Track CTA click
export function trackCTAClick(ctaName: string, destination?: string): void {
  // GA4
  if (window.trackEvent) {
    window.trackEvent('cta_click', {
      cta_name: ctaName,
      cta_destination: destination || 'unknown'
    });
  }
  
  // Meta
  if (window.trackMetaEvent) {
    window.trackMetaEvent('Search', {
      search_string: ctaName,
      content_category: 'cta_interaction'
    });
  }
}

// Track engagement (time on page)
export function trackEngagement(seconds: number): void {
  if (seconds >= 60 && window.trackEvent) {
    window.trackEvent('engaged_user', {
      engagement_time_sec: seconds,
      engagement_level: seconds >= 180 ? 'high' : 'medium'
    });
  }
  
  if (seconds >= 60 && window.trackMetaEvent) {
    window.trackMetaEvent('ViewContent', {
      content_name: 'Engaged User',
      content_category: 'high_engagement'
    });
  }
}

// Track A/B/C version view
export function trackVersionView(version: 'a' | 'b' | 'c'): void {
  if (window.trackEvent) {
    window.trackEvent('experiment_view', {
      experiment_name: 'recruitment_apk_report_style',
      variant: version
    });
  }
}

export default {
  initializeTracking,
  trackPageView,
  trackFormView,
  trackAssessmentStart,
  trackAssessmentComplete,
  trackReportDownload,
  trackCTAClick,
  trackEngagement,
  trackVersionView,
  TRACKING_CONFIG
};
