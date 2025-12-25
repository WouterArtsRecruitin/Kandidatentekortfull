// ===============================================
// Netlify Function - Server-Side Conversion Tracking
// Facebook CAPI & GA4 Measurement Protocol
// ===============================================

const crypto = require('crypto');

// Configuration
const FB_PIXEL_ID = '238226887541404';
const FB_ACCESS_TOKEN = process.env.FB_ACCESS_TOKEN || '';
const GA4_MEASUREMENT_ID = 'G-67PJ02SXVN';
const GA4_API_SECRET = process.env.GA4_API_SECRET || '';

const headers = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'Content-Type',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Content-Type': 'application/json'
};

// Hash function for Facebook CAPI
function hashData(data) {
  if (!data) return null;
  return crypto.createHash('sha256').update(data.toLowerCase().trim()).digest('hex');
}

exports.handler = async (event, context) => {
  // Handle preflight
  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: '' };
  }

  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      headers,
      body: JSON.stringify({ error: 'Method not allowed' })
    };
  }

  try {
    const data = JSON.parse(event.body || '{}');
    const {
      event_name,
      email,
      bedrijf_naam,
      functie_titel,
      score,
      sector,
      client_ip,
      user_agent,
      event_id
    } = data;

    const results = {
      facebook: null,
      ga4: null
    };

    // ===============================================
    // Facebook Conversions API
    // ===============================================
    if (FB_ACCESS_TOKEN) {
      const fbEventData = {
        data: [{
          event_name: event_name || 'Lead',
          event_time: Math.floor(Date.now() / 1000),
          event_id: event_id || `evt_${Date.now()}`,
          event_source_url: 'https://kandidatentekort.nl',
          action_source: 'website',
          user_data: {
            em: email ? [hashData(email)] : undefined,
            client_ip_address: client_ip || event.headers['x-forwarded-for']?.split(',')[0],
            client_user_agent: user_agent || event.headers['user-agent']
          },
          custom_data: {
            content_name: functie_titel || 'Vacature Analyse',
            content_category: sector || 'Technical',
            value: score ? parseFloat(score) : 0,
            currency: 'EUR'
          }
        }]
      };

      try {
        const fbResponse = await fetch(
          `https://graph.facebook.com/v18.0/${FB_PIXEL_ID}/events?access_token=${FB_ACCESS_TOKEN}`,
          {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(fbEventData)
          }
        );

        results.facebook = await fbResponse.json();
        console.log('Facebook CAPI response:', results.facebook);
      } catch (fbError) {
        console.error('Facebook CAPI error:', fbError);
        results.facebook = { error: fbError.message };
      }
    }

    // ===============================================
    // Google Analytics 4 Measurement Protocol
    // ===============================================
    if (GA4_API_SECRET) {
      const ga4EventData = {
        client_id: event_id || `client_${Date.now()}`,
        events: [{
          name: event_name || 'generate_lead',
          params: {
            engagement_time_msec: 1000,
            session_id: `session_${Date.now()}`,
            company_name: bedrijf_naam || '',
            job_title: functie_titel || '',
            sector: sector || '',
            score: score || 0
          }
        }]
      };

      try {
        const ga4Response = await fetch(
          `https://www.google-analytics.com/mp/collect?measurement_id=${GA4_MEASUREMENT_ID}&api_secret=${GA4_API_SECRET}`,
          {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(ga4EventData)
          }
        );

        results.ga4 = { status: ga4Response.status, success: ga4Response.ok };
        console.log('GA4 MP response:', results.ga4);
      } catch (ga4Error) {
        console.error('GA4 MP error:', ga4Error);
        results.ga4 = { error: ga4Error.message };
      }
    }

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        success: true,
        event_name,
        results,
        timestamp: new Date().toISOString()
      })
    };

  } catch (error) {
    console.error('Track conversion error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: error.message })
    };
  }
};
