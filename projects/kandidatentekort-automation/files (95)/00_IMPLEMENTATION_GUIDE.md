# 🎯 KANDIDATENTEKORT.NL - TEMPLATES IMPLEMENTATION GUIDE

**Versie:** 1.0  
**Datum:** November 2024  
**Auteur:** Claude AI voor Recruitin B.V.

---

## 📦 WHAT YOU GOT

Je hebt nu **4 production-ready templates** voor kandidatentekort.nl:

1. **01_Verbeterde_Vacature_Template** (Markdown + HTML)
2. **02_Executive_Summary_Rapport** (HTML)
3. **03_Praktische_Tips_Checklist** (HTML + Interactive)
4. **04_Email_Delivery_Template** (HTML)

Totaal: **~2,500 regels code** + **42 praktische tips** + **15+ secties**

---

## 🏗️ ARCHITECTURE OVERVIEW

```
USER SUBMITS VACATURE (Typeform/Website)
         ↓
  Zapier catches submission
         ↓
  Creates Pipedrive Deal
         ↓
  Triggers Claude API Analysis
         ↓
  Claude analyzes + fills templates
         ↓
  Generates 3 files (HTML/PDF/MD)
         ↓
  Stores in Google Drive
         ↓
  Sends Email (Resend) with attachments
         ↓
  Updates Pipedrive Deal status
```

---

## 🔧 INTEGRATION ROADMAP

### **PHASE 1: Template Setup** (Day 1) ✅ DONE

- [x] Vacature template (Markdown + HTML)
- [x] Executive summary rapport (HTML)
- [x] Tips checklist (HTML)
- [x] Email delivery template (HTML)

### **PHASE 2: Claude API Integration** (Day 2-3)

#### 2.1 Create Claude Analysis Function

```javascript
// Cloudflare Worker or Netlify Function
import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY
});

async function analyzeVacature(vacatureText, metadata) {
  const prompt = `
Je bent een expert recruitment copywriter. Analyseer deze vacaturetekst en vul de template variabelen in.

ORIGINELE VACATURE:
${vacatureText}

METADATA:
- Bedrijfsnaam: ${metadata.bedrijfsnaam}
- Functie: ${metadata.functie}
- Locatie: ${metadata.locatie}
- Sector: ${metadata.sector}

INSTRUCTIES:
1. Analyseer de vacature op:
   - Aantrekkelijkheid (score 0-100)
   - Inclusiviteit (score 0-100)
   - SEO kwaliteit
   - Conversie-potentieel
   
2. Identificeer top 3 verbeteringen
3. Schrijf verbeterde versie (inclusief, SEO-proof, GDPR-compliant)
4. Vul ALLE template variabelen in (JSON output)

OUTPUT FORMAT:
Return een JSON object met:
{
  "analysis": {
    "score_voor": 65,
    "score_na": 87,
    "response_voor": 30,
    "response_na": 42,
    "inclusie_voor": 55,
    "inclusie_na": 85,
    "verbetering_1_titel": "...",
    "verbetering_1_desc": "...",
    ...
  },
  "template_variables": {
    "functie_titel": "...",
    "bedrijfsnaam": "...",
    "intro_paragraaf": "...",
    "taken_en_verantwoordelijkheden": "...",
    ...
  },
  "seo": {
    "title": "...",
    "description": "...",
    "keywords": "..."
  }
}
`;

  const response = await anthropic.messages.create({
    model: 'claude-sonnet-4-20250514',
    max_tokens: 8000,
    temperature: 0.7,
    messages: [{
      role: 'user',
      content: prompt
    }]
  });

  // Parse JSON from Claude's response
  const jsonMatch = response.content[0].text.match(/\{[\s\S]*\}/);
  return JSON.parse(jsonMatch[0]);
}
```

#### 2.2 Template Filling Function

```javascript
function fillTemplate(template, variables) {
  let filled = template;
  
  // Replace all {{variable}} placeholders
  for (const [key, value] of Object.entries(variables)) {
    const regex = new RegExp(`{{${key}}}`, 'g');
    filled = filled.replace(regex, value);
  }
  
  return filled;
}

// Usage
const vacatureHTML = fillTemplate(
  vacatureTemplateHTML,
  claudeResponse.template_variables
);

const rapportHTML = fillTemplate(
  rapportTemplateHTML,
  claudeResponse.analysis
);

const emailHTML = fillTemplate(
  emailTemplateHTML,
  {
    voornaam: metadata.voornaam,
    ...claudeResponse.analysis,
    dashboard_url: `https://kandidatentekort.nl/dashboard/${dealId}`,
    rapport_url: `https://kandidatentekort.nl/rapporten/${dealId}`,
    contact_email: 'support@kandidatentekort.nl',
    contact_telefoon: '+31 6 12345678'
  }
);
```

### **PHASE 3: File Generation** (Day 4)

#### 3.1 HTML to PDF Conversion

```javascript
// Option A: Puppeteer (Cloudflare Workers doesn't support)
import puppeteer from 'puppeteer';

async function htmlToPDF(html) {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.setContent(html, { waitUntil: 'networkidle0' });
  const pdf = await page.pdf({
    format: 'A4',
    printBackground: true,
    margin: { top: '10mm', bottom: '10mm', left: '10mm', right: '10mm' }
  });
  await browser.close();
  return pdf;
}

// Option B: HTML2PDF.js (client-side)
// Render HTML in browser, let user print to PDF

// Option C: Gotenberg (Docker service)
// POST HTML to https://your-gotenberg.com/forms/chromium/convert/html
```

#### 3.2 Store in Google Drive

```javascript
import { google } from 'googleapis';

async function uploadToGoogleDrive(fileName, fileContent, mimeType) {
  const auth = new google.auth.GoogleAuth({
    credentials: JSON.parse(process.env.GOOGLE_CREDENTIALS),
    scopes: ['https://www.googleapis.com/auth/drive.file']
  });

  const drive = google.drive({ version: 'v3', auth });

  const fileMetadata = {
    name: fileName,
    parents: [process.env.GOOGLE_DRIVE_FOLDER_ID] // kandidatentekort folder
  };

  const media = {
    mimeType: mimeType,
    body: Buffer.from(fileContent)
  };

  const file = await drive.files.create({
    requestBody: fileMetadata,
    media: media,
    fields: 'id, webViewLink'
  });

  return {
    id: file.data.id,
    url: file.data.webViewLink
  };
}

// Usage
const files = {
  vacature_html: await uploadToGoogleDrive(
    `${dealId}_Vacature.html`,
    vacatureHTML,
    'text/html'
  ),
  vacature_md: await uploadToGoogleDrive(
    `${dealId}_Vacature.md`,
    vacatureMarkdown,
    'text/markdown'
  ),
  rapport_pdf: await uploadToGoogleDrive(
    `${dealId}_Rapport.pdf`,
    await htmlToPDF(rapportHTML),
    'application/pdf'
  ),
  tips_html: await uploadToGoogleDrive(
    `${dealId}_Tips_Checklist.html`,
    tipsHTML,
    'text/html'
  )
};
```

### **PHASE 4: Email Delivery** (Day 5)

#### 4.1 Send via Resend

```javascript
import { Resend } from 'resend';

const resend = new Resend(process.env.RESEND_API_KEY);

async function sendDeliveryEmail(toEmail, variables, attachmentUrls) {
  const emailHTML = fillTemplate(emailTemplateHTML, variables);

  const { data, error } = await resend.emails.send({
    from: 'Kandidatentekort.nl <delivery@kandidatentekort.nl>',
    to: toEmail,
    subject: `✅ Je Vacature "${variables.functie_titel}" is Geoptimaliseerd!`,
    html: emailHTML,
    attachments: [
      {
        filename: 'Vacature_Verbeterd.html',
        path: attachmentUrls.vacature_html
      },
      {
        filename: 'Analyse_Rapport.pdf',
        path: attachmentUrls.rapport_pdf
      },
      {
        filename: 'Tips_Checklist.html',
        path: attachmentUrls.tips_html
      }
    ],
    tags: [
      { name: 'category', value: 'delivery' },
      { name: 'deal_id', value: variables.deal_id }
    ]
  });

  if (error) {
    throw new Error(`Email failed: ${error.message}`);
  }

  return data;
}
```

#### 4.2 Alternative: Gmail via Google Workspace

```javascript
import { google } from 'googleapis';

async function sendViaGmail(to, subject, htmlBody, attachments) {
  const auth = new google.auth.GoogleAuth({
    credentials: JSON.parse(process.env.GOOGLE_CREDENTIALS),
    scopes: ['https://www.googleapis.com/auth/gmail.send']
  });

  const gmail = google.gmail({ version: 'v1', auth });

  // Create MIME message
  const message = [
    `To: ${to}`,
    `Subject: ${subject}`,
    'Content-Type: text/html; charset=utf-8',
    '',
    htmlBody
  ].join('\n');

  const encodedMessage = Buffer.from(message)
    .toString('base64')
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=+$/, '');

  await gmail.users.messages.send({
    userId: 'me',
    requestBody: {
      raw: encodedMessage
    }
  });
}
```

### **PHASE 5: Pipedrive Integration** (Day 6)

#### 5.1 Update Deal Status

```javascript
import axios from 'axios';

async function updatePipedriveDeal(dealId, updates) {
  const response = await axios.put(
    `https://api.pipedrive.com/v1/deals/${dealId}`,
    updates,
    {
      params: {
        api_token: process.env.PIPEDRIVE_API_TOKEN
      }
    }
  );

  return response.data;
}

// Usage
await updatePipedriveDeal(dealId, {
  status: 'won', // or keep 'open' if not closing deal
  stage_id: 5, // "Delivered" stage
  custom_fields: {
    analyse_score: claudeResponse.analysis.score_na,
    verwachte_verbetering: `+${claudeResponse.analysis.response_verbetering}%`,
    google_drive_folder: files.folder_url,
    email_verzonden: new Date().toISOString()
  }
});
```

#### 5.2 Add Note to Deal

```javascript
async function addPipedriveDealNote(dealId, content) {
  const response = await axios.post(
    'https://api.pipedrive.com/v1/notes',
    {
      deal_id: dealId,
      content: content,
      pinned_to_deal_flag: 1
    },
    {
      params: {
        api_token: process.env.PIPEDRIVE_API_TOKEN
      }
    }
  );

  return response.data;
}

// Usage
await addPipedriveDealNote(dealId, `
📊 Analyse Compleet

**Scores:**
- Voor: ${claudeResponse.analysis.score_voor}/100
- Na: ${claudeResponse.analysis.score_na}/100
- Verbetering: +${claudeResponse.analysis.score_verbetering} punten

**Top 3 Verbeteringen:**
1. ${claudeResponse.analysis.verbetering_1_titel}
2. ${claudeResponse.analysis.verbetering_2_titel}
3. ${claudeResponse.analysis.verbetering_3_titel}

**Deliverables:**
- [Vacature HTML](${files.vacature_html.url})
- [Rapport PDF](${files.rapport_pdf.url})
- [Tips Checklist](${files.tips_html.url})

✅ Email verzonden naar ${metadata.email}
`);
```

---

## 🔄 COMPLETE WORKFLOW

### Zapier Setup (Option A: No-Code)

```
TRIGGER: Typeform - New Entry
  ↓
ACTION: Pipedrive - Create Deal
  - Title: {{functie}} bij {{bedrijfsnaam}}
  - Person: {{email}} (create if not exists)
  - Custom fields: vacature_text, sector, locatie
  ↓
ACTION: Webhooks - POST to Cloudflare Worker
  - URL: https://kandidatentekort-api.yourworker.workers.dev/analyze
  - Payload: {
      deal_id: {{pipedrive_deal_id}},
      vacature_text: {{typeform_vacature}},
      metadata: {...}
    }
  ↓
  [Worker processes async - 30-60 seconds]
  ↓
ACTION: Delay - 2 minutes
  ↓
ACTION: Pipedrive - Update Deal
  - Status: Check if worker completed
  ↓
ACTION: Gmail/Resend - Send Email
  - Template: 04_Email_Delivery_Template.html
  - Attachments: Links from Google Drive
```

### Custom Code Setup (Option B: Full Control)

```javascript
// main.js - Netlify/Cloudflare Function

export async function handler(event) {
  const { deal_id, vacature_text, metadata } = JSON.parse(event.body);

  try {
    // 1. Analyze with Claude
    console.log('Step 1: Analyzing vacature...');
    const analysis = await analyzeVacature(vacature_text, metadata);

    // 2. Fill templates
    console.log('Step 2: Filling templates...');
    const vacatureHTML = fillTemplate(vacatureTemplateHTML, analysis.template_variables);
    const vacatureMD = fillTemplate(vacatureTemplateMD, analysis.template_variables);
    const rapportHTML = fillTemplate(rapportTemplateHTML, analysis.analysis);
    const tipsHTML = tipsTemplateHTML; // Static, no variables needed
    const emailHTML = fillTemplate(emailTemplateHTML, {
      ...metadata,
      ...analysis.analysis
    });

    // 3. Convert to PDF
    console.log('Step 3: Generating PDF...');
    const rapportPDF = await htmlToPDF(rapportHTML);

    // 4. Upload to Google Drive
    console.log('Step 4: Uploading files...');
    const files = {
      vacature_html: await uploadToGoogleDrive(`${deal_id}_Vacature.html`, vacatureHTML, 'text/html'),
      vacature_md: await uploadToGoogleDrive(`${deal_id}_Vacature.md`, vacatureMD, 'text/markdown'),
      rapport_pdf: await uploadToGoogleDrive(`${deal_id}_Rapport.pdf`, rapportPDF, 'application/pdf'),
      tips_html: await uploadToGoogleDrive(`${deal_id}_Tips.html`, tipsHTML, 'text/html')
    };

    // 5. Send email
    console.log('Step 5: Sending email...');
    await sendDeliveryEmail(metadata.email, {
      ...metadata,
      ...analysis.analysis,
      dashboard_url: `https://kandidatentekort.nl/dashboard/${deal_id}`,
      rapport_url: files.rapport_pdf.url
    }, files);

    // 6. Update Pipedrive
    console.log('Step 6: Updating Pipedrive...');
    await updatePipedriveDeal(deal_id, {
      stage_id: 5, // Delivered
      custom_fields: {
        analyse_score: analysis.analysis.score_na,
        google_drive_folder: files.vacature_html.url.split('/').slice(0, -1).join('/')
      }
    });

    await addPipedriveDealNote(deal_id, `
✅ Analyse compleet
📊 Score: ${analysis.analysis.score_voor} → ${analysis.analysis.score_na}
📧 Email verzonden
    `);

    return {
      statusCode: 200,
      body: JSON.stringify({
        success: true,
        deal_id,
        files
      })
    };

  } catch (error) {
    console.error('Error:', error);

    // Update Pipedrive with error
    await addPipedriveDealNote(deal_id, `
❌ Error tijdens verwerking: ${error.message}
    `);

    return {
      statusCode: 500,
      body: JSON.stringify({
        success: false,
        error: error.message
      })
    };
  }
}
```

---

## 📊 TEMPLATE VARIABLES REFERENCE

### Vacature Template Variables

```javascript
{
  // Header
  "functie_titel": "Senior Java Developer",
  "bedrijfsnaam": "TechCorp B.V.",
  "locatie": "Amsterdam",
  "uren_per_week": "32-40",
  "dienstverband": "Onbeperkt contract",
  "salaris_range": "€5.000 - €7.000 bruto/maand",

  // Content
  "intro_paragraaf": "...",
  "impact_bullets": "...",
  "taken_en_verantwoordelijkheden": "...",
  "dagelijks_beeld": "...",
  
  // Requirements
  "harde_eisen": "...",
  "wensen": "...",
  "persoonlijkheid_fit": "...",
  
  // Benefits
  "contract_type": "Onbeperkt",
  "vakantiedagen": "27 dagen + 5 ADV",
  "pensioen": "70% werkgever betaald",
  "bonus": "8% jaarlijks",
  "ontwikkel_mogelijkheden": "...",
  "work_life_balance": "...",
  "secundaire_arbeidsvoorwaarden": "...",
  
  // Company
  "bedrijfs_beschrijving": "...",
  "why_join_bullets": "...",
  "team_beschrijving": "...",
  "bereikbaarheid": "...",
  "hybride_beleid": "...",
  
  // Application
  "sollicitatie_call_to_action": "...",
  "contactpersoon": "Sarah van der Berg",
  "contact_email": "sarah@techcorp.nl",
  "contact_telefoon": "+31 20 123 4567",
  "procedure_stappen": "<li>...</li><li>...</li>",
  "verwachte_doorlooptijd": "3 weken",
  
  // Meta
  "publicatie_datum": "2024-11-25",
  "sluitings_datum": "2024-12-25",
  "vacature_id": "TC-2024-089",
  "seo_title": "...",
  "seo_description": "...",
  "seo_keywords": "..."
}
```

### Rapport Template Variables

```javascript
{
  "rapport_datum": "25 november 2024",
  "functie_titel": "Senior Java Developer",
  "bedrijfsnaam": "TechCorp B.V.",
  "vacature_id": "TC-2024-089",
  "sector": "IT/Software",
  "locatie": "Amsterdam",
  "woorden_voor": 450,
  "woorden_na": 850,
  
  // Metrics
  "score_voor": 65,
  "score_na": 87,
  "score_verbetering": 22,
  "response_voor": 30,
  "response_na": 42,
  "response_verbetering": 40,
  "inclusie_voor": 55,
  "inclusie_na": 85,
  "inclusie_verbetering": 30,
  
  // Top 3 Improvements
  "verbetering_1_titel": "Salaris transparantie toegevoegd",
  "verbetering_1_desc": "Concrete salary range vermeld (€5-7k) verhoogt sollicitaties met 35%",
  "verbetering_2_titel": "Gender-neutrale taal",
  "verbetering_2_desc": "Woorden zoals 'rockstar' vervangen door inclusieve alternatieven",
  "verbetering_3_titel": "SEO geoptimaliseerd",
  "verbetering_3_desc": "Functietitel + locatie 3x herhaald voor Google vindbaarheid",
  
  // Impact
  "impact_kandidaten": 40,
  "impact_tijd": 18,
  "impact_besparing": "6.500"
}
```

### Email Template Variables

```javascript
{
  "voornaam": "Wouter",
  "functie_titel": "Senior Java Developer",
  "verbetering_percentage": 40,
  "seo_verbetering": 60,
  "score_verbetering": 22,
  "response_verbetering": 40,
  "inclusie_score": 85,
  
  // URLs
  "dashboard_url": "https://kandidatentekort.nl/dashboard/abc123",
  "rapport_url": "https://drive.google.com/file/...",
  "upgrade_url": "https://kandidatentekort.nl/prijzen",
  "whatsapp_url": "https://wa.me/31612345678",
  "unsubscribe_url": "https://kandidatentekort.nl/unsubscribe/...",
  "linkedin_url": "https://linkedin.com/company/kandidatentekort",
  "facebook_url": "https://facebook.com/kandidatentekort",
  "instagram_url": "https://instagram.com/kandidatentekort",
  
  // Contact
  "contact_email": "support@kandidatentekort.nl",
  "contact_telefoon": "+31 6 12345678",
  "kvk_nummer": "12345678",
  "bedrijfsadres": "Straatnaam 123, 1234 AB Amsterdam"
}
```

---

## ⚙️ ENVIRONMENT VARIABLES

Create `.env` file:

```bash
# Anthropic Claude API
ANTHROPIC_API_KEY=sk-ant-api03-...

# Google APIs
GOOGLE_CREDENTIALS={"type":"service_account",...}
GOOGLE_DRIVE_FOLDER_ID=1abc...

# Pipedrive
PIPEDRIVE_API_TOKEN=abc123...

# Resend Email
RESEND_API_KEY=re_...

# Application
SITE_URL=https://kandidatentekort.nl
NODE_ENV=production
```

---

## 🚀 DEPLOYMENT CHECKLIST

### Pre-Launch

- [ ] Test Claude API with real vacature
- [ ] Verify template variable replacement
- [ ] Test PDF generation
- [ ] Test Google Drive upload + permissions
- [ ] Test email delivery (Resend)
- [ ] Test Pipedrive integration
- [ ] Setup monitoring (Sentry/Cloudflare Analytics)
- [ ] Configure error notifications (Slack/email)

### Launch Day

- [ ] Deploy to production (Cloudflare/Netlify)
- [ ] Update Zapier webhooks (point to prod URL)
- [ ] Test end-to-end with real submission
- [ ] Monitor logs for errors
- [ ] Check Pipedrive deal creation
- [ ] Verify email delivery
- [ ] Confirm files in Google Drive

### Post-Launch

- [ ] Collect first 10 customer feedback
- [ ] Iterate on template copy
- [ ] Optimize Claude prompt
- [ ] A/B test email subject lines
- [ ] Track metrics: open rate, click rate, satisfaction

---

## 📈 MONITORING & METRICS

### Track These KPIs

```javascript
// Log to Google Analytics or Mixpanel
analytics.track('Vacature Analyzed', {
  deal_id: dealId,
  score_improvement: analysis.score_verbetering,
  processing_time: endTime - startTime,
  word_count_before: analysis.woorden_voor,
  word_count_after: analysis.woorden_na,
  sector: metadata.sector
});

analytics.track('Email Delivered', {
  deal_id: dealId,
  recipient: metadata.email,
  delivery_time: new Date() - submissionTime
});
```

### Alert on Failures

```javascript
if (error) {
  // Send to Slack
  await fetch(process.env.SLACK_WEBHOOK_URL, {
    method: 'POST',
    body: JSON.stringify({
      text: `🚨 Kandidatentekort Error: ${error.message}`,
      blocks: [{
        type: 'section',
        text: {
          type: 'mrkdwn',
          text: `*Deal ID:* ${deal_id}\n*Error:* ${error.message}\n*Stack:* \`\`\`${error.stack}\`\`\``
        }
      }]
    })
  });
  
  // Send to Sentry
  Sentry.captureException(error, {
    tags: {
      deal_id: deal_id,
      component: 'vacature_analysis'
    }
  });
}
```

---

## 🎨 CUSTOMIZATION TIPS

### Modify Templates

```javascript
// Change colors
// In HTML templates, replace:
#ff6b35 → #YOUR_PRIMARY_COLOR
#2c3e50 → #YOUR_SECONDARY_COLOR

// Change fonts
font-family: 'Inter', ... → font-family: 'YourFont', ...

// Add logo
<img src="https://your-cdn.com/logo.png" alt="Logo" style="height: 40px;">
```

### Add Variables

```javascript
// 1. Add to template HTML
<div>{{new_variable}}</div>

// 2. Update Claude prompt
"Output moet ook bevatten: new_variable (beschrijving)"

// 3. Test with mock data
const testData = {
  ...existingVariables,
  new_variable: "Test value"
};
```

### Multilingual Support

```javascript
// Create separate templates per language
const templates = {
  nl: vacatureTemplateNL,
  en: vacatureTemplateEN,
  de: vacatureTemplateDE
};

const template = templates[metadata.language || 'nl'];
```

---

## 🐛 TROUBLESHOOTING

### Issue: Claude returns invalid JSON

```javascript
try {
  const parsed = JSON.parse(claudeResponse);
} catch (e) {
  // Retry with stricter prompt
  const retryPrompt = `${originalPrompt}

CRITICAL: Return ONLY valid JSON. No markdown, no text before/after.
Start with { and end with }. Validate JSON before returning.`;
  
  const retry = await analyzeVacature(vacatureText, metadata, retryPrompt);
}
```

### Issue: PDF generation fails

```javascript
// Fallback: Send HTML instead of PDF
const fallbackAttachment = {
  filename: 'Rapport.html',
  content: rapportHTML,
  contentType: 'text/html'
};

// Or: Use external service
const pdfEndpoint = 'https://gotenberg.yourdomain.com/forms/chromium/convert/html';
const pdfResponse = await fetch(pdfEndpoint, {
  method: 'POST',
  body: rapportHTML,
  headers: { 'Content-Type': 'text/html' }
});
const pdfBuffer = await pdfResponse.arrayBuffer();
```

### Issue: Email not delivered

```javascript
// Check Resend dashboard for errors
// Common issues:
// 1. Domain not verified → Verify in Resend settings
// 2. Recipient bounced → Check email validity
// 3. Rate limit hit → Upgrade Resend plan

// Fallback: Use Gmail
if (resendError) {
  await sendViaGmail(metadata.email, subject, emailHTML, attachments);
}
```

---

## 💰 COST BREAKDOWN

### Per Delivery (Single Vacature)

```
Claude API (8K tokens output):     €0.12
Google Drive (storage):            €0.00 (free tier)
Resend (1 email + 3 attachments):  €0.00 (free tier)
Pipedrive API (2 calls):           €0.00 (included)
Cloudflare Worker (1 execution):   €0.00 (free tier)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL PER DELIVERY:                €0.12

Your pricing: €29 → Margin: €28.88 (99.6% gross margin!)
```

### At Scale (100 deliveries/month)

```
Claude API:              €12
Resend (>free tier):     €20
Google Drive (>15GB):    €2
Cloudflare (>free):      €5
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL COST:              €39/month
Revenue (100 x €29):     €2,900
NET PROFIT:              €2,861

Profit margin: 98.7% 🚀
```

---

## 🎯 SUCCESS METRICS

Track these to measure template effectiveness:

1. **Customer Satisfaction**
   - NPS score
   - Feedback ratings
   - Repeat usage rate

2. **Template Quality**
   - Average score improvement
   - Time to delivery
   - Error rate

3. **Business Impact**
   - Conversion rate (visitor → customer)
   - Upsell rate (€29 → €99 plan)
   - Churn rate

4. **Technical Performance**
   - Claude API latency
   - Email delivery rate
   - PDF generation success rate

---

## 📞 SUPPORT & QUESTIONS

Voor vragen over deze implementation:

- **Email:** wouter@recruitin.nl
- **GitHub Issues:** [your-repo]/issues
- **Slack:** #kandidatentekort (internal)

---

**READY TO LAUNCH! 🚀**

Je hebt nu alles wat je nodig hebt voor een volledig geautomatiseerde kandidatentekort.nl pipeline. Start met Zapier setup voor quick MVP, dan migrate naar custom code voor meer controle.

Succes!

---
*Generated by Claude Sonnet 4.5 | Kandidatentekort.nl Template System v1.0*
