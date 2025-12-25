// ===============================================
// Netlify Function - Typeform Webhook Handler
// Receives Typeform submissions and triggers analysis pipeline
// ===============================================

const headers = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'Content-Type',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Content-Type': 'application/json'
};

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

  console.log('📥 Typeform webhook received');

  try {
    const payload = JSON.parse(event.body || '{}');

    // Extract Typeform data
    const formResponse = payload.form_response || {};
    const answers = formResponse.answers || [];
    const definition = formResponse.definition || {};

    // Map answers to our format
    const data = {
      vacature_tekst: '',
      bedrijf_naam: '',
      functie_titel: '',
      email: '',
      naam: '',
      submitted_at: formResponse.submitted_at || new Date().toISOString()
    };

    // Process each answer
    for (const answer of answers) {
      const fieldRef = answer.field?.ref || '';
      const fieldType = answer.type || '';

      let value = '';
      if (fieldType === 'text' || fieldType === 'long_text') {
        value = answer.text || '';
      } else if (fieldType === 'email') {
        value = answer.email || '';
      } else if (fieldType === 'short_text') {
        value = answer.text || '';
      }

      // Map to our fields based on field reference
      const refLower = fieldRef.toLowerCase();
      if (refLower.includes('vacature') || refLower.includes('tekst') || refLower.includes('text')) {
        data.vacature_tekst = value;
      } else if (refLower.includes('bedrijf') || refLower.includes('company')) {
        data.bedrijf_naam = value;
      } else if (refLower.includes('functie') || refLower.includes('title') || refLower.includes('rol')) {
        data.functie_titel = value;
      } else if (refLower.includes('email') || refLower.includes('mail')) {
        data.email = value;
      } else if (refLower.includes('naam') || refLower.includes('name')) {
        data.naam = value;
      }
    }

    console.log(`📋 Extracted: ${data.bedrijf_naam} - ${data.functie_titel} (${data.email})`);

    // Validate required fields
    if (!data.vacature_tekst && !data.email) {
      console.warn('⚠️ Missing required fields');
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({
          error: 'Missing required fields',
          received: Object.keys(data).filter(k => data[k])
        })
      };
    }

    // Step 1: Analyze vacancy with Claude
    let analysisResult = null;
    if (data.vacature_tekst && process.env.CLAUDE_API_KEY) {
      console.log('🔍 Starting Claude analysis...');
      analysisResult = await analyzeVacancy(data.vacature_tekst, data.bedrijf_naam, data.functie_titel);
      console.log(`✅ Analysis complete: Score ${analysisResult.score}/10`);
    }

    // Step 2: Send email with results
    let emailSent = false;
    if (data.email && analysisResult) {
      console.log('📧 Sending analysis email...');
      emailSent = await sendAnalysisEmail(data, analysisResult);
      console.log(emailSent ? '✅ Email sent' : '❌ Email failed');
    }

    // Step 3: Create Pipedrive lead
    let pipedriveLeadId = null;
    if (process.env.PIPEDRIVE_API_KEY) {
      console.log('📊 Creating Pipedrive lead...');
      pipedriveLeadId = await createPipedriveLead(data, analysisResult);
      console.log(pipedriveLeadId ? `✅ Lead created: ${pipedriveLeadId}` : '❌ Lead creation failed');
    }

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        success: true,
        message: 'Webhook processed successfully',
        results: {
          analysis: analysisResult ? { score: analysisResult.score, sector: analysisResult.sector } : null,
          email_sent: emailSent,
          pipedrive_lead_id: pipedriveLeadId
        }
      })
    };

  } catch (error) {
    console.error('❌ Webhook error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({
        error: 'Webhook processing failed',
        message: error.message
      })
    };
  }
};

// ===============================================
// Claude AI Analysis
// ===============================================
async function analyzeVacancy(vacatureText, bedrijfNaam, functieTitel) {
  const prompt = `
# NEDERLANDSE TECHNISCHE VACATURE ANALYSE

Analyseer deze vacature en geef een gestructureerde beoordeling.

## ANALYSE CRITERIA
1. SALARIS TRANSPARANTIE - Is er een concreet salaris genoemd?
2. CANDIDATE FOCUS - Wordt de kandidaat aangesproken (jij vs wij)?
3. TECHNISCHE DETAILS - Concrete projecten en technologieën?
4. SCANBAARHEID - Bullet points en structuur?
5. UNIQUE SELLING POINTS - Wat maakt deze rol uniek?

## VACATURE
Bedrijf: ${bedrijfNaam || 'Onbekend'}
Functie: ${functieTitel || 'Onbekend'}

${vacatureText}

## GEEF JSON OUTPUT:
{
  "score": 7.5,
  "sector": "manufacturing",
  "sectorDisplay": "Manufacturing / Productie",
  "findings": [
    {"title": "...", "description": "...", "type": "success|warning|error", "impactPercentage": 20}
  ],
  "quickWins": [
    {"action": "...", "expectedImprovement": 15, "implementation": "..."}
  ],
  "rewrittenIntro": "Verbeterde opening van de vacature...",
  "fullAnalysis": "Samenvatting..."
}
`;

  try {
    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': process.env.CLAUDE_API_KEY,
        'anthropic-version': '2023-06-01'
      },
      body: JSON.stringify({
        model: 'claude-3-5-sonnet-20241022',
        max_tokens: 2000,
        temperature: 0.3,
        system: 'Je bent een Nederlandse recruitment expert. Geef altijd antwoorden in correct JSON format.',
        messages: [{ role: 'user', content: prompt }]
      })
    });

    if (!response.ok) {
      throw new Error(`Claude API error: ${response.status}`);
    }

    const data = await response.json();
    const text = data.content?.[0]?.text || '';

    // Extract JSON from response
    const jsonMatch = text.match(/\{[\s\S]*\}/);
    if (jsonMatch) {
      return JSON.parse(jsonMatch[0]);
    }

    throw new Error('No JSON in response');
  } catch (error) {
    console.error('Claude analysis error:', error);
    // Return basic fallback
    return {
      score: 5.0,
      sector: 'general',
      sectorDisplay: 'Algemeen',
      findings: [{ title: 'Analyse niet beschikbaar', description: error.message, type: 'warning' }],
      quickWins: [],
      fullAnalysis: 'Analyse kon niet worden uitgevoerd.'
    };
  }
}

// ===============================================
// Email via Resend
// ===============================================
async function sendAnalysisEmail(data, analysis) {
  const RESEND_API_KEY = process.env.RESEND_API_KEY;
  if (!RESEND_API_KEY) {
    console.warn('RESEND_API_KEY not configured');
    return false;
  }

  const score = analysis.score || 5;
  const improvement = Math.min(Math.round((10 - score) * 15), 100);

  const htmlContent = `
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #1e293b; }
    .container { max-width: 600px; margin: 0 auto; padding: 20px; }
    .header { background: linear-gradient(135deg, #f97316, #ea580c); color: white; padding: 30px; border-radius: 12px 12px 0 0; }
    .score { font-size: 48px; font-weight: 800; }
    .content { background: #f8fafc; padding: 30px; border-radius: 0 0 12px 12px; }
    .finding { padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid; }
    .finding.success { background: #ecfdf5; border-color: #10b981; }
    .finding.warning { background: #fffbeb; border-color: #f59e0b; }
    .finding.error { background: #fef2f2; border-color: #ef4444; }
    .cta { background: #1e293b; color: white; padding: 15px 30px; border-radius: 8px; text-decoration: none; display: inline-block; margin-top: 20px; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1 style="margin:0;">Jouw Vacature Analyse</h1>
      <div class="score">${score.toFixed(1)}/10</div>
      <p>Potentiële verbetering: +${improvement}% meer sollicitaties</p>
    </div>
    <div class="content">
      <h2>Hallo ${data.naam || 'daar'},</h2>
      <p>Bedankt voor het insturen van je vacature${data.functie_titel ? ` voor <strong>${data.functie_titel}</strong>` : ''}${data.bedrijf_naam ? ` bij ${data.bedrijf_naam}` : ''}.</p>

      <h3>📊 Bevindingen</h3>
      ${(analysis.findings || []).map(f => `
        <div class="finding ${f.type}">
          <strong>${f.title}</strong><br>
          ${f.description}
          ${f.impactPercentage ? `<br><small>Impact: -${f.impactPercentage}% sollicitaties</small>` : ''}
        </div>
      `).join('')}

      ${analysis.quickWins && analysis.quickWins.length > 0 ? `
        <h3>⚡ Quick Wins</h3>
        <ul>
          ${analysis.quickWins.map(w => `<li><strong>${w.action}</strong> (+${w.expectedImprovement}%)</li>`).join('')}
        </ul>
      ` : ''}

      ${analysis.rewrittenIntro ? `
        <h3>✨ Verbeterde Opening</h3>
        <div style="background: #f3e8ff; padding: 15px; border-radius: 8px; font-style: italic;">
          "${analysis.rewrittenIntro}"
        </div>
      ` : ''}

      <p style="margin-top: 30px;">
        <a href="https://calendly.com/wouter-arts-/vacature-analyse-advies" class="cta">
          📅 Plan een gratis adviesgesprek
        </a>
      </p>

      <p style="margin-top: 30px; color: #64748b; font-size: 14px;">
        Met vriendelijke groet,<br>
        <strong>Team KandidatenTekort.nl</strong><br>
        Recruitin B.V.
      </p>
    </div>
  </div>
</body>
</html>
`;

  try {
    const response = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${RESEND_API_KEY}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        from: 'KandidatenTekort.nl <analyse@kandidatentekort.nl>',
        to: [data.email],
        subject: `🎯 Je vacature scoort ${score.toFixed(1)}/10 - Hier zijn je verbeterpunten`,
        html: htmlContent
      })
    });

    if (!response.ok) {
      const error = await response.text();
      console.error('Resend error:', error);
      return false;
    }

    return true;
  } catch (error) {
    console.error('Email send error:', error);
    return false;
  }
}

// ===============================================
// Pipedrive Lead Creation
// ===============================================
async function createPipedriveLead(data, analysis) {
  const PIPEDRIVE_API_KEY = process.env.PIPEDRIVE_API_KEY;
  const PIPEDRIVE_DOMAIN = process.env.PIPEDRIVE_COMPANY_DOMAIN || 'recruitinbv.pipedrive.com';

  if (!PIPEDRIVE_API_KEY) {
    console.warn('PIPEDRIVE_API_KEY not configured');
    return null;
  }

  const score = analysis?.score || 5;
  const leadValue = Math.round((10 - score) * 500); // EUR 0-5000 based on improvement potential

  try {
    // Create person first
    let personId = null;
    if (data.email) {
      const personResponse = await fetch(`https://${PIPEDRIVE_DOMAIN}/api/v1/persons?api_token=${PIPEDRIVE_API_KEY}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: data.naam || data.email.split('@')[0],
          email: [{ value: data.email, primary: true }],
          visible_to: 3
        })
      });

      if (personResponse.ok) {
        const personData = await personResponse.json();
        personId = personData.data?.id;
      }
    }

    // Create organization
    let orgId = null;
    if (data.bedrijf_naam) {
      const orgResponse = await fetch(`https://${PIPEDRIVE_DOMAIN}/api/v1/organizations?api_token=${PIPEDRIVE_API_KEY}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: data.bedrijf_naam,
          visible_to: 3
        })
      });

      if (orgResponse.ok) {
        const orgData = await orgResponse.json();
        orgId = orgData.data?.id;
      }
    }

    // Create deal
    const dealTitle = `${data.bedrijf_naam || 'Lead'} - ${data.functie_titel || 'Vacature Optimalisatie'}`;

    const dealResponse = await fetch(`https://${PIPEDRIVE_DOMAIN}/api/v1/deals?api_token=${PIPEDRIVE_API_KEY}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        title: dealTitle,
        value: leadValue,
        currency: 'EUR',
        person_id: personId,
        org_id: orgId,
        pipeline_id: 14, // Kandidatentekort pipeline
        visible_to: 3
      })
    });

    if (!dealResponse.ok) {
      const error = await dealResponse.text();
      console.error('Pipedrive deal error:', error);
      return null;
    }

    const dealData = await dealResponse.json();
    const dealId = dealData.data?.id;

    // Add note with analysis
    if (dealId && analysis) {
      const noteContent = `
🎯 VACATURE ANALYSE
━━━━━━━━━━━━━━━━━━━━
Score: ${score}/10
Sector: ${analysis.sectorDisplay || 'Algemeen'}
Potentiële verbetering: +${Math.round((10-score)*15)}%

📊 BEVINDINGEN:
${(analysis.findings || []).map(f => `• ${f.title}: ${f.description}`).join('\n')}

⚡ QUICK WINS:
${(analysis.quickWins || []).map(w => `• ${w.action} (+${w.expectedImprovement}%)`).join('\n')}

📧 Email: ${data.email || 'Niet opgegeven'}
📅 Ingediend: ${data.submitted_at || new Date().toISOString()}
      `;

      await fetch(`https://${PIPEDRIVE_DOMAIN}/api/v1/notes?api_token=${PIPEDRIVE_API_KEY}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          deal_id: dealId,
          content: noteContent
        })
      });
    }

    return dealId;
  } catch (error) {
    console.error('Pipedrive error:', error);
    return null;
  }
}
