// netlify/functions/track-conversion.js
// Facebook Conversions API - Server-Side Event Tracking

const crypto = require('crypto');

// Facebook credentials (from environment variables)
const FB_PIXEL_ID = '1735907367288442'; // Your Facebook App ID
const FB_ACCESS_TOKEN = process.env.FACEBOOK_API_TOKEN;
const FB_API_VERSION = 'v18.0';

exports.handler = async (event, context) => {
  // Only allow POST requests
  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      body: JSON.stringify({ error: 'Method Not Allowed' })
    };
  }

  try {
    const data = JSON.parse(event.body);
    const { event_name, user_data, custom_data, event_source_url } = data;

    // Hash user data for privacy (required by Facebook)
    const hashedUserData = {
      em: user_data.email ? hashData(user_data.email.toLowerCase()) : null,
      ph: user_data.phone ? hashData(user_data.phone.replace(/[^0-9]/g, '')) : null,
      client_ip_address: event.headers['x-forwarded-for'] || event.headers['client-ip'],
      client_user_agent: event.headers['user-agent'],
      fbc: user_data.fbc || null, // Facebook click ID from cookie
      fbp: user_data.fbp || null, // Facebook browser ID from cookie
    };

    // Remove null values
    Object.keys(hashedUserData).forEach(key => 
      hashedUserData[key] === null && delete hashedUserData[key]
    );

    // Build event payload
    const eventData = {
      data: [{
        event_name: event_name,
        event_time: Math.floor(Date.now() / 1000),
        event_source_url: event_source_url || 'https://kandidatentekort.nl',
        action_source: 'website',
        user_data: hashedUserData,
        custom_data: custom_data || {}
      }]
    };

    // Send to Facebook Conversions API
    const fbResponse = await fetch(
      `https://graph.facebook.com/${FB_API_VERSION}/${FB_PIXEL_ID}/events?access_token=${FB_ACCESS_TOKEN}`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(eventData)
      }
    );

    const result = await fbResponse.json();

    // Log for debugging
    console.log('Facebook Conversions API Response:', result);

    return {
      statusCode: 200,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
      },
      body: JSON.stringify({
        success: true,
        facebook_response: result,
        events_received: result.events_received || 0
      })
    };

  } catch (error) {
    console.error('Error tracking conversion:', error);
    
    return {
      statusCode: 500,
      body: JSON.stringify({
        success: false,
        error: error.message
      })
    };
  }
};

// SHA256 hash function (required by Facebook)
function hashData(data) {
  if (!data) return null;
  return crypto.createHash('sha256').update(data).digest('hex');
}
