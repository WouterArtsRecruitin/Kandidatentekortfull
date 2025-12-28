// Facebook Lead Ads Webhook → Pipedrive Integration
// Receives leads from Facebook and creates persons in Pipedrive

const crypto = require('crypto');

exports.handler = async (event, context) => {
  // Facebook webhook verification (GET request)
  if (event.httpMethod === 'GET') {
    const params = event.queryStringParameters || {};
    const mode = params['hub.mode'];
    const token = params['hub.verify_token'];
    const challenge = params['hub.challenge'];

    const VERIFY_TOKEN = process.env.FB_WEBHOOK_VERIFY_TOKEN || 'kandidatentekort_webhook_2024';

    if (mode === 'subscribe' && token === VERIFY_TOKEN) {
      console.log('Webhook verified successfully');
      return {
        statusCode: 200,
        body: challenge
      };
    } else {
      console.error('Webhook verification failed');
      return {
        statusCode: 403,
        body: 'Verification failed'
      };
    }
  }

  // Handle POST requests (actual lead data)
  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      body: JSON.stringify({ error: 'Method Not Allowed' })
    };
  }

  // Parse webhook payload
  let payload;
  try {
    payload = JSON.parse(event.body);
  } catch (error) {
    console.error('Invalid JSON:', error);
    return {
      statusCode: 400,
      body: JSON.stringify({ error: 'Invalid JSON payload' })
    };
  }

  console.log('Received webhook payload:', JSON.stringify(payload, null, 2));

  // Environment variables
  const FACEBOOK_PAGE_TOKEN = process.env.FACEBOOK_PAGE_ACCESS_TOKEN;
  const PIPEDRIVE_API_KEY = process.env.PIPEDRIVE_API_KEY;

  if (!FACEBOOK_PAGE_TOKEN || !PIPEDRIVE_API_KEY) {
    console.error('Missing environment variables');
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Server configuration error - missing API keys' })
    };
  }

  // Process Facebook lead entries
  const results = [];

  try {
    // Facebook sends leadgen webhooks in this format
    if (payload.entry) {
      for (const entry of payload.entry) {
        if (entry.changes) {
          for (const change of entry.changes) {
            if (change.field === 'leadgen' && change.value) {
              const leadgenId = change.value.leadgen_id;
              const formId = change.value.form_id;
              const pageId = change.value.page_id;

              console.log(`Processing lead: ${leadgenId} from form: ${formId}`);

              // Fetch lead details from Facebook Graph API
              const leadData = await fetchLeadFromFacebook(leadgenId, FACEBOOK_PAGE_TOKEN);

              if (leadData) {
                // Create person in Pipedrive
                const pipedriveResult = await createPipedrivePerson(leadData, PIPEDRIVE_API_KEY);
                results.push({
                  leadgen_id: leadgenId,
                  pipedrive_result: pipedriveResult,
                  success: pipedriveResult.success
                });
              }
            }
          }
        }
      }
    }

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        success: true,
        processed: results.length,
        results
      })
    };

  } catch (error) {
    console.error('Webhook processing error:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({
        error: 'Processing failed',
        message: error.message
      })
    };
  }
};

// Fetch lead details from Facebook Graph API
async function fetchLeadFromFacebook(leadId, accessToken) {
  try {
    const url = `https://graph.facebook.com/v18.0/${leadId}?access_token=${accessToken}`;
    const response = await fetch(url);
    const data = await response.json();

    if (data.error) {
      console.error('Facebook API error:', data.error);
      return null;
    }

    console.log('Lead data from Facebook:', JSON.stringify(data, null, 2));

    // Parse field_data into a more usable format
    const fields = {};
    if (data.field_data) {
      for (const field of data.field_data) {
        fields[field.name] = field.values?.[0] || '';
      }
    }

    return {
      id: data.id,
      created_time: data.created_time,
      email: fields.email || '',
      first_name: fields.first_name || '',
      last_name: fields.last_name || '',
      phone_number: fields.phone_number || '',
      company_name: fields.company_name || '',
      full_name: fields.full_name || `${fields.first_name || ''} ${fields.last_name || ''}`.trim()
    };

  } catch (error) {
    console.error('Error fetching lead from Facebook:', error);
    return null;
  }
}

// Create a person in Pipedrive
async function createPipedrivePerson(leadData, apiKey) {
  try {
    const personData = {
      name: leadData.full_name || leadData.first_name || 'Onbekend',
      email: leadData.email ? [{ value: leadData.email, primary: true }] : undefined,
      phone: leadData.phone_number ? [{ value: leadData.phone_number, primary: true }] : undefined,
      visible_to: 3, // Visible to everyone
      // Add custom fields or notes
      // You can add org_id if you want to link to an organization
    };

    // If company name provided, first create or find organization
    let orgId = null;
    if (leadData.company_name) {
      orgId = await findOrCreateOrganization(leadData.company_name, apiKey);
      if (orgId) {
        personData.org_id = orgId;
      }
    }

    const url = `https://api.pipedrive.com/v1/persons?api_token=${apiKey}`;
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(personData)
    });

    const result = await response.json();

    if (result.success) {
      console.log('Person created in Pipedrive:', result.data.id);

      // Also create a lead/deal for follow-up
      await createPipedriveLead(result.data.id, leadData, apiKey);

      return {
        success: true,
        person_id: result.data.id,
        org_id: orgId
      };
    } else {
      console.error('Pipedrive error:', result.error);
      return {
        success: false,
        error: result.error
      };
    }

  } catch (error) {
    console.error('Error creating Pipedrive person:', error);
    return {
      success: false,
      error: error.message
    };
  }
}

// Find or create organization in Pipedrive
async function findOrCreateOrganization(companyName, apiKey) {
  try {
    // First search for existing organization
    const searchUrl = `https://api.pipedrive.com/v1/organizations/search?term=${encodeURIComponent(companyName)}&api_token=${apiKey}`;
    const searchResponse = await fetch(searchUrl);
    const searchResult = await searchResponse.json();

    if (searchResult.success && searchResult.data?.items?.length > 0) {
      return searchResult.data.items[0].item.id;
    }

    // Create new organization
    const createUrl = `https://api.pipedrive.com/v1/organizations?api_token=${apiKey}`;
    const createResponse = await fetch(createUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        name: companyName,
        visible_to: 3
      })
    });

    const createResult = await createResponse.json();

    if (createResult.success) {
      console.log('Organization created:', createResult.data.id);
      return createResult.data.id;
    }

    return null;

  } catch (error) {
    console.error('Error with organization:', error);
    return null;
  }
}

// Create a lead in Pipedrive for follow-up
async function createPipedriveLead(personId, leadData, apiKey) {
  try {
    const leadPayload = {
      title: `Vacature Analyse - ${leadData.full_name || leadData.email}`,
      person_id: personId,
      // Source channel - Facebook Lead Ads
      '67bfc338be9f4390c99e60a100b436d668c08b2a': 'Facebook Lead Ads', // Lead Source field
      // Add note about the source
      note: `Lead via Facebook Lead Ads - Kandidatentekort.nl\nAangevraagd: ${leadData.created_time || new Date().toISOString()}`
    };

    const url = `https://api.pipedrive.com/v1/leads?api_token=${apiKey}`;
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(leadPayload)
    });

    const result = await response.json();

    if (result.success) {
      console.log('Lead created in Pipedrive:', result.data.id);
      return result.data.id;
    }

    return null;

  } catch (error) {
    console.error('Error creating Pipedrive lead:', error);
    return null;
  }
}
