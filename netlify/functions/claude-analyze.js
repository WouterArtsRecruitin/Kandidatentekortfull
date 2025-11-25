// ===============================================
// Netlify Function - Claude API Integration
// Nederlandse Vacature Optimizer Backend
// ===============================================

const headers = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Content-Type': 'application/json'
};

exports.handler = async (event, context) => {
  // Handle preflight requests
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers,
      body: ''
    };
  }

  // Only allow POST requests
  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      headers,
      body: JSON.stringify({
        error: 'Method not allowed',
        message: 'Only POST requests are supported'
      })
    };
  }

  // Validate environment variables
  if (!process.env.CLAUDE_API_KEY) {
    console.error('❌ CLAUDE_API_KEY not configured');
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({
        error: 'Configuration error',
        message: 'API key not configured. Please check environment variables.'
      })
    };
  }

  try {
    // Parse request body
    const { prompt, max_tokens = 4000 } = JSON.parse(event.body || '{}');

    if (!prompt) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({
          error: 'Bad request',
          message: 'Prompt is required'
        })
      };
    }

    // Log request (without sensitive data)
    console.log(`🔍 Claude API request - Prompt length: ${prompt.length} chars`);

    // Call Claude API
    const claudeResponse = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.CLAUDE_API_KEY}`,
        'anthropic-version': '2023-06-01'
      },
      body: JSON.stringify({
        model: 'claude-3-5-sonnet-20241022',
        max_tokens: max_tokens,
        messages: [
          {
            role: 'user',
            content: prompt
          }
        ],
        temperature: 0.3, // Lower temperature for more consistent analysis
        system: "Je bent een Nederlandse recruitment expert. Geef altijd antwoorden in correct JSON format zonder extra tekst."
      })
    });

    // Handle Claude API errors
    if (!claudeResponse.ok) {
      const errorText = await claudeResponse.text();
      console.error(`❌ Claude API error: ${claudeResponse.status} - ${errorText}`);
      
      let errorMessage = 'Claude API request failed';
      
      if (claudeResponse.status === 401) {
        errorMessage = 'Invalid API key';
      } else if (claudeResponse.status === 429) {
        errorMessage = 'Rate limit exceeded. Please try again in a moment.';
      } else if (claudeResponse.status === 400) {
        errorMessage = 'Invalid request format';
      }
      
      return {
        statusCode: claudeResponse.status,
        headers,
        body: JSON.stringify({
          error: 'Claude API error',
          message: errorMessage,
          details: errorText
        })
      };
    }

    // Parse Claude response
    const claudeData = await claudeResponse.json();
    
    if (!claudeData.content || !claudeData.content[0] || !claudeData.content[0].text) {
      console.error('❌ Invalid Claude response format:', claudeData);
      return {
        statusCode: 500,
        headers,
        body: JSON.stringify({
          error: 'Invalid response',
          message: 'Claude API returned invalid response format'
        })
      };
    }

    // Log successful response
    const responseLength = claudeData.content[0].text.length;
    console.log(`✅ Claude API success - Response length: ${responseLength} chars`);

    // Return successful response
    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        content: claudeData.content,
        usage: claudeData.usage || {},
        model: claudeData.model || 'claude-3-5-sonnet-20241022',
        timestamp: new Date().toISOString()
      })
    };

  } catch (error) {
    console.error('❌ Function error:', error);
    
    // Determine error type
    let statusCode = 500;
    let errorMessage = 'Internal server error';
    
    if (error.name === 'SyntaxError') {
      statusCode = 400;
      errorMessage = 'Invalid JSON in request body';
    } else if (error.code === 'ENOTFOUND' || error.code === 'ECONNREFUSED') {
      statusCode = 503;
      errorMessage = 'Unable to connect to Claude API';
    } else if (error.message.includes('fetch')) {
      statusCode = 503;
      errorMessage = 'Network error while contacting Claude API';
    }

    return {
      statusCode,
      headers,
      body: JSON.stringify({
        error: 'Function error',
        message: errorMessage,
        details: process.env.NODE_ENV === 'development' ? error.message : undefined,
        timestamp: new Date().toISOString()
      })
    };
  }
};

// Health check endpoint
exports.healthCheck = async (event, context) => {
  return {
    statusCode: 200,
    headers,
    body: JSON.stringify({
      status: 'healthy',
      service: 'claude-analyze',
      timestamp: new Date().toISOString(),
      environment: process.env.NODE_ENV || 'production',
      hasApiKey: !!process.env.CLAUDE_API_KEY
    })
  };
};