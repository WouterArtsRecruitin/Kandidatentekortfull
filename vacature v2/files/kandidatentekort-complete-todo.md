# 🎯 KANDIDATENTEKORT.NL - COMPLETE TODO LIJST

**Status:** Production-Ready Checklist  
**Priority:** CRITICAL → HIGH → MEDIUM → NICE-TO-HAVE  
**Timeline:** Week 1-4

---

## 🚨 CRITICAL (Week 1 - MUST HAVE)

### **1. GOOGLE ANALYTICS 4 SETUP** ⭐ PRIORITY 1
**Why:** Je weet NIETS zonder tracking. Blind vliegen is gevaarlijk.

**Implementation:**
```bash
# Step 1: Create GA4 Property
# 1. Go to: https://analytics.google.com
# 2. Admin → Create Property → "Kandidatentekort.nl"
# 3. Copy Measurement ID (format: G-XXXXXXXXXX)

# Step 2: Install in Next.js
npm install @next/third-parties

# Step 3: Add to app/layout.tsx
import { GoogleAnalytics } from '@next/third-parties/google'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <GoogleAnalytics gaId="G-XXXXXXXXXX" />
      </body>
    </html>
  )
}

# Step 4: Setup Events
// app/components/AnalyzeButton.tsx
const handleSubmit = () => {
  // Track submission
  window.gtag('event', 'vacature_submitted', {
    'event_category': 'engagement',
    'event_label': 'quick_scan_form'
  });
  
  // Your submit logic
}
```

**Custom Events to Track:**
```typescript
// Critical Events
1. 'page_view' - Auto-tracked
2. 'vacature_submitted' - Form submit
3. 'analysis_completed' - Streaming done
4. 'copy_result' - Copy-to-clipboard clicked
5. 'pricing_viewed' - Pricing page visit
6. 'upgrade_clicked' - Premium CTA clicked
7. 'email_opened' - Nurture email tracking
8. 'consultation_booked' - Calendly booking

// Implementation:
export const trackEvent = (eventName: string, params?: object) => {
  if (typeof window !== 'undefined' && window.gtag) {
    window.gtag('event', eventName, params);
  }
};
```

**Enhanced Ecommerce (For €29 Payments):**
```typescript
// Track purchase
gtag('event', 'purchase', {
  transaction_id: 'T_12345',
  value: 29.00,
  currency: 'EUR',
  items: [{
    item_id: 'vacature_analysis',
    item_name: 'Vacature Optimalisatie',
    price: 29.00,
    quantity: 1
  }]
});
```

**Time:** 1 hour  
**Cost:** €0  
**Impact:** CRITICAL - Data-driven decisions

---

### **2. VACATURE ANALYSE PROMPT VERBETEREN** ⭐ PRIORITY 2
**Why:** Dit is je core product. Betere prompt = betere resultaten = meer betalende klanten.

**Current Issues:**
- Te generiek (niet sector-specifiek)
- Geen output structuur (inconsistent)
- Missing key analyses (SEO, inclusiviteit, ATS compatibility)
- Geen before/after comparison

**NEW MASTER PROMPT:**
```typescript
// lib/prompts/vacature-analyse.ts

export const VACATURE_ANALYSE_PROMPT = `Je bent een expert recruitment copywriter met 15+ jaar ervaring in de Nederlandse arbeidsmarkt.

# ANALYSETAAK
Analyseer de volgende vacaturetekst en genereer een professioneel rapport met concrete verbeterpunten.

# VACATURETEKST
{vacature_tekst}

# BEDRIJFSCONTEXT (optioneel)
Bedrijfsnaam: {bedrijf_naam}
Sector: {sector}
Locatie: {locatie}

# OUTPUT STRUCTUUR

## 1. EXECUTIVE SUMMARY
- Overall score (1-10)
- Top 3 sterktes
- Top 3 zwaktes
- Urgentie niveau (laag/medium/hoog)

## 2. INCLUSIVITEIT ANALYSE
Score: X/10

**Problematische taal gevonden:**
- [Specifiek woord/zin] → Waarom problematisch → Suggestie

**Gender-bias:**
- Mannelijke taal: [voorbeelden]
- Verbeterde versie: [gender-neutrale alternatieven]

**Toegankelijkheid:**
- Educatie-barriers: [voorbeelden]
- Leeftijd-bias: [voorbeelden]
- Fysieke vereisten: [zijn deze echt nodig?]

## 3. SEO OPTIMALISATIE
Score: X/10

**Keyword analyse:**
- Primaire keyword: [keyword]
- Zoekvolume: [aantal/maand]
- Huidige gebruik: [X keer in tekst]
- Optimaal: [Y keer]

**Meta data:**
- Titel optimalisatie: [suggestie max 60 chars]
- Meta description: [suggestie max 160 chars]

**Google for Jobs compatibiliteit:**
✅/❌ Salarisbereik vermeld
✅/❌ Werklocatie duidelijk
✅/❌ Werktype (fulltime/parttime)
✅/❌ Startdatum

## 4. ATS COMPATIBILITY
Score: X/10

**Formatting issues:**
- Tabellen: [gevonden/niet gevonden]
- Afbeeldingen: [problematisch voor ATS]
- Speciale karakters: [voorbeelden]

**Keyword matching:**
- Skills gevonden: [lijst]
- Ontbrekende standaard skills: [lijst]

## 5. CONVERSION OPTIMIZATION
Score: X/10

**Call-to-Action analyse:**
- Aantal CTAs: [X]
- Placement: [begin/midden/einde]
- Kracht: [zwak/medium/sterk]
- Verbeterd: [concrete suggestie]

**Urgentie & Scarcity:**
- Deadline: [gevonden/ontbreekt]
- Aantal posities: [vermeld/ontbreekt]
- Start datum: [duidelijk/vaag]

**Sociale bewijskracht:**
- Bedrijfsgrootte: [vermeld/ontbreekt]
- Teamsamenstelling: [beschreven/vaag]
- Groei indicators: [aanwezig/ontbreekt]

## 6. CONTENT KWALITEIT
Score: X/10

**Leesbaarheid:**
- Flesch Reading Ease: [score]
- Gemiddelde zinslengte: [X woorden]
- Passieve zinnen: [X%]

**Structuur:**
- Kopjes: [effectief/zwak]
- Bullets: [goed gebruik/kan beter]
- Witruimte: [voldoende/te druk]

**Tone of Voice:**
- Gevonden toon: [formeel/informeel/professioneel]
- Aanbevolen: [advies voor sector]

## 7. SALARIS & VOORWAARDEN
Score: X/10

**Salarisvermelding:**
Status: [Vermeld/Niet vermeld/Vaag]
Marktconformiteit: [Check via externe data]
Aanbeveling: [Concreet bereik voor functie]

**Secundaire voorwaarden:**
✅/❌ Vakantiedagen
✅/❌ Reiskostenvergoeding
✅/❌ Thuiswerkmogelijkheden
✅/❌ Opleidingsbudget
✅/❌ Pensioenregeling

## 8. VERBETERDE VERSIE (SNIPPET)

**VOOR:**
[Originele eerste 3 alinea's]

**NA:**
[Geoptimaliseerde eerste 3 alinea's met alle verbeteringen toegepast]

**Belangrijkste wijzigingen:**
1. [Wijziging 1]
2. [Wijziging 2]
3. [Wijziging 3]

## 9. QUICK WINS (Top 5)
Prioriteit 1: [Concrete actie] → Impact: [Hoog/Medium]
Prioriteit 2: [Concrete actie] → Impact: [Hoog/Medium]
Prioriteit 3: [Concrete actie] → Impact: [Hoog/Medium]
Prioriteit 4: [Concrete actie] → Impact: [Medium]
Prioriteit 5: [Concrete actie] → Impact: [Medium]

## 10. IMPLEMENTATION CHECKLIST
- [ ] Vervang problematische taal (15 min)
- [ ] Voeg salarisbereik toe (5 min)
- [ ] Optimaliseer meta tags (10 min)
- [ ] Verbeter CTA (5 min)
- [ ] Update job posting op Indeed/LinkedIn (20 min)

**Totale implementatietijd: ~1 uur**
**Verwachte impact: +30-50% sollicitaties**

# TONE & STYLE
- Professioneel maar toegankelijk
- Concrete voorbeelden (niet vaag)
- Data-gedreven waar mogelijk
- Actiegericht (implementeerbare tips)
- Nederlands (formele aanspreking)

# CONSTRAINTS
- Geen juridisch advies
- Focus op NL arbeidsmarkt
- Respecteer sector-specifieke normen
- Geen garanties op resultaat`;

// Usage:
const prompt = VACATURE_ANALYSE_PROMPT
  .replace('{vacature_tekst}', userInput)
  .replace('{bedrijf_naam}', company || 'Niet opgegeven')
  .replace('{sector}', sector || 'Algemeen')
  .replace('{locatie}', location || 'Nederland');
```

**Multi-Pass Quality (Voor 24-uur model):**
```typescript
// Voor premium 24-uur service
export const QUALITY_CONTROL_PROMPT = `Je bent een senior reviewer.

Beoordeel de volgende vacature-analyse op:
1. Accuraatheid (zijn claims correct?)
2. Compleetheid (alle secties?)
3. Bruikbaarheid (concrete tips?)
4. Tone (professioneel?)

Geef score 1-10 en leg uit waarom.
Als <8: suggest improvements.`;

// Multi-pass workflow:
async function generatePremiumAnalysis(vacature: string) {
  // Pass 1: Initial analysis
  const analysis1 = await claude.messages.create({
    model: 'claude-sonnet-4-20250514',
    messages: [{ role: 'user', content: VACATURE_ANALYSE_PROMPT }]
  });
  
  // Pass 2: Quality check
  const qualityCheck = await claude.messages.create({
    model: 'claude-sonnet-4-20250514',
    messages: [{ 
      role: 'user', 
      content: QUALITY_CONTROL_PROMPT + '\n\n' + analysis1.content 
    }]
  });
  
  // Pass 3: Final polish (if needed)
  if (qualityScore < 8) {
    const finalAnalysis = await claude.messages.create({
      // Improvement pass
    });
    return finalAnalysis;
  }
  
  return analysis1;
}
```

**Time:** 2 hours (implementation + testing)  
**Cost:** €0  
**Impact:** CRITICAL - Product quality

---

### **3. TEMPLATE VACATURETEKSTEN** ⭐ PRIORITY 3
**Why:** Users willen instant resultaat zien (trust building). Demo data helpt conversie.

**Implementation:**
```typescript
// lib/templates/vacatures.ts

export const VACATURE_TEMPLATES = {
  'software-developer': {
    title: 'Senior Software Developer',
    sector: 'Technology',
    company: 'TechCorp B.V.',
    text: `Wij zoeken een ervaren Software Developer...

[Complete realistic vacature met bekende issues:
- Gender bias ("hij moet kunnen")
- Geen salaris
- Zwakke CTA
- Missing SEO
- Te veel vereisten]`,
    
    // Expected analysis results (pre-generated)
    expectedScore: 4.5,
    topIssues: ['Gender bias', 'Geen salaris', 'Zwakke CTA']
  },
  
  'werkvoorbereider': {
    title: 'Allround Werkvoorbereider',
    sector: 'Engineering',
    company: 'Bouwbedrijf Nederland',
    text: `Voor onze vestiging in Gelderland zoeken wij...`,
    expectedScore: 5.2,
    topIssues: ['Onduidelijke vereisten', 'Geen thuiswerk vermeld']
  },
  
  'recruiter': {
    title: 'Corporate Recruiter',
    sector: 'HR',
    company: 'HR Solutions Group',
    text: `Ben jij de recruitment specialist die wij zoeken?`,
    expectedScore: 6.8,
    topIssues: ['Te informeel', 'Vaag functieprofiel']
  }
};

// Component usage:
<select onChange={(e) => loadTemplate(e.target.value)}>
  <option value="">-- Of probeer een voorbeeld --</option>
  <option value="software-developer">Software Developer</option>
  <option value="werkvoorbereider">Werkvoorbereider</option>
  <option value="recruiter">Corporate Recruiter</option>
</select>
```

**Homepage Implementation:**
```tsx
// app/page.tsx

export default function HomePage() {
  return (
    <section className="hero">
      <h1>Optimaliseer Je Vacaturetekst in 24 Uur</h1>
      
      {/* Template selector */}
      <div className="template-demo">
        <p className="text-sm text-gray-600 mb-2">
          Geen vacature bij de hand? Probeer een voorbeeld:
        </p>
        <TemplateSelector onSelect={handleTemplateSelect} />
      </div>
      
      {/* Main form */}
      <QuickScanForm initialText={selectedTemplate} />
      
      {/* Live demo results */}
      {selectedTemplate && (
        <div className="demo-results">
          <h3>Verwachte analyse-preview:</h3>
          <div className="score-badge">
            Score: {template.expectedScore}/10
          </div>
          <ul>
            {template.topIssues.map(issue => (
              <li key={issue}>⚠️ {issue}</li>
            ))}
          </ul>
          <button onClick={runFullAnalysis}>
            Zie Volledige Analyse →
          </button>
        </div>
      )}
    </section>
  );
}
```

**Time:** 3 hours (5 templates + UI)  
**Cost:** €0  
**Impact:** HIGH - Trust building + conversie

---

### **4. FACEBOOK PIXEL + LINKEDIN INSIGHT TAG** ⭐ PRIORITY 4
**Why:** Retargeting = goedkoopste traffic. €0.50-2 CPA via ads.

**Implementation:**
```typescript
// app/components/Analytics.tsx

'use client';

import Script from 'next/script';

export function FacebookPixel() {
  return (
    <>
      <Script id="facebook-pixel" strategy="afterInteractive">
        {`
          !function(f,b,e,v,n,t,s)
          {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
          n.callMethod.apply(n,arguments):n.queue.push(arguments)};
          if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
          n.queue=[];t=b.createElement(e);t.async=!0;
          t.src=v;s=b.getElementsByTagName(e)[0];
          s.parentNode.insertBefore(t,s)}(window, document,'script',
          'https://connect.facebook.net/en_US/fbevents.js');
          fbq('init', 'YOUR_PIXEL_ID');
          fbq('track', 'PageView');
        `}
      </Script>
      <noscript>
        <img 
          height="1" 
          width="1" 
          style={{ display: 'none' }}
          src="https://www.facebook.com/tr?id=YOUR_PIXEL_ID&ev=PageView&noscript=1"
        />
      </noscript>
    </>
  );
}

export function LinkedInInsightTag() {
  return (
    <Script id="linkedin-insight" strategy="afterInteractive">
      {`
        _linkedin_partner_id = "YOUR_PARTNER_ID";
        window._linkedin_data_partner_ids = window._linkedin_data_partner_ids || [];
        window._linkedin_data_partner_ids.push(_linkedin_partner_id);
        (function(l) {
          if (!l){window.lintrk = function(a,b){window.lintrk.q.push([a,b])};
          window.lintrk.q=[]}
          var s = document.getElementsByTagName("script")[0];
          var b = document.createElement("script");
          b.type = "text/javascript";b.async = true;
          b.src = "https://snap.licdn.com/li.lms-analytics/insight.min.js";
          s.parentNode.insertBefore(b, s);})(window.lintrk);
      `}
    </Script>
  );
}

// Event tracking:
export const trackConversion = (eventName: string, value?: number) => {
  // Facebook
  if (typeof window !== 'undefined' && window.fbq) {
    window.fbq('track', eventName, { value, currency: 'EUR' });
  }
  
  // LinkedIn
  if (typeof window !== 'undefined' && window.lintrk) {
    window.lintrk('track', { conversion_id: YOUR_CONVERSION_ID });
  }
};

// Usage in components:
const handlePurchase = () => {
  trackConversion('Purchase', 29); // €29 payment
};

const handleLead = () => {
  trackConversion('Lead'); // Form submission
};
```

**Setup Steps:**
```bash
# 1. Facebook Business Manager
# - Go to: https://business.facebook.com
# - Events Manager → Create Pixel
# - Copy Pixel ID

# 2. LinkedIn Campaign Manager
# - Go to: https://www.linkedin.com/campaignmanager
# - Account Assets → Insight Tag
# - Install Tag → Copy Partner ID

# 3. Verify Installation
# - Facebook Pixel Helper extension
# - LinkedIn Insight Tag Helper extension
```

**Time:** 1 hour  
**Cost:** €0  
**Impact:** HIGH - Retargeting capability

---

### **5. AUTOMATION FLOW VERBETEREN** ⭐ PRIORITY 5
**Why:** Handmatige processen = bottleneck. Automation = scale.

**Current Flow (Manual):**
```
User submits form
  ↓
Email to you (manual)
  ↓
You run analysis (manual)
  ↓
You email results (manual)
  ↓
Follow-up??? (forgotten)
```

**NEW AUTOMATED FLOW:**
```
User submits form
  ↓
Zapier: Trigger "New Jotform Submission"
  ↓
┌─────────────────────────────────────┐
│ PARALLEL ACTIONS:                   │
├─────────────────────────────────────┤
│ 1. Add to Notion database           │
│ 2. Add to Pipedrive (CRM)           │
│ 3. Backup to Google Drive           │
│ 4. Send instant confirmation email  │
│ 5. Queue analysis job               │
└─────────────────────────────────────┘
  ↓
Cloudflare Workers: Process Queue
  ↓
Claude API: Generate analysis (24h)
  ↓
┌─────────────────────────────────────┐
│ PARALLEL ACTIONS:                   │
├─────────────────────────────────────┤
│ 1. Email results to user            │
│ 2. Update Notion (status: Complete) │
│ 3. Update Pipedrive (activity log)  │
│ 4. Save PDF to Google Drive         │
│ 5. Start email sequence (Day 3)     │
└─────────────────────────────────────┘
  ↓
Email Sequence (Automated):
  ├─ Day 0: Results + Upsell €29
  ├─ Day 3: Check-in + Bonus tip
  ├─ Day 7: Whitepaper download
  └─ Day 15: Free consultation offer
```

**Zapier Workflow Configuration:**
```yaml
# Zap 1: Form Submission → Database Sync
Trigger: Jotform "New Submission"
Actions:
  1. Create Notion Page
     - Database: "Kandidatentekort Leads"
     - Properties:
       - Naam: {{jotform.naam}}
       - Email: {{jotform.email}}
       - Bedrijf: {{jotform.bedrijf}}
       - Vacaturetekst: {{jotform.vacature}}
       - Status: "Pending Analysis"
       - Submitted: {{jotform.created_at}}
  
  2. Create Pipedrive Deal
     - Pipeline: "Kandidatentekort"
     - Stage: "New Lead"
     - Title: "{{jotform.bedrijf}} - Vacature Analyse"
     - Value: €29
     - Custom Fields:
       - Vacature Titel: {{jotform.vacature_titel}}
       - Lead Source: "Website Form"
  
  3. Upload to Google Drive
     - Folder: "Kandidatentekort/Submissions/{{format_date}}"
     - Filename: "{{jotform.bedrijf}}_{{timestamp}}.txt"
     - Content: {{jotform.vacature}}
  
  4. Send Email (Resend)
     - To: {{jotform.email}}
     - Template: "confirmation"
     - Subject: "✅ Je Vacature Analyse is Onderweg!"
     - Body: [Confirmation template]

# Zap 2: Analysis Complete → Delivery
Trigger: Webhook "Analysis Complete"
Actions:
  1. Update Notion
     - Find page: {{webhook.email}}
     - Update: Status = "Complete"
     - Add: Analysis URL
  
  2. Send Email (Resend)
     - To: {{webhook.email}}
     - Template: "results"
     - Attachment: {{webhook.pdf_url}}
  
  3. Delay: 3 days
  
  4. Send Email (Follow-up)
     - Template: "check-in"

# Zap 3: Email Sequence Manager
Trigger: Tag "Email Sequence Start"
Actions:
  1. Delay: 3 days → Email 2
  2. Delay: 7 days → Email 3
  3. Delay: 15 days → Email 4
```

**Cloudflare Workers (Analysis Queue):**
```typescript
// workers/analysis-queue.ts

export default {
  async scheduled(event, env, ctx) {
    // Run every hour
    const pendingJobs = await env.DB.prepare(
      'SELECT * FROM analysis_queue WHERE status = "pending" LIMIT 10'
    ).all();
    
    for (const job of pendingJobs.results) {
      try {
        // Run analysis
        const result = await runAnalysis(job.vacature_text);
        
        // Update database
        await env.DB.prepare(
          'UPDATE analysis_queue SET status = "complete", result = ? WHERE id = ?'
        ).bind(JSON.stringify(result), job.id).run();
        
        // Trigger Zapier webhook
        await fetch('https://hooks.zapier.com/YOUR_WEBHOOK', {
          method: 'POST',
          body: JSON.stringify({
            email: job.email,
            result: result,
            pdf_url: await generatePDF(result)
          })
        });
      } catch (error) {
        // Error handling
        await logError(job.id, error);
      }
    }
  }
};
```

**Time:** 4 hours (setup + testing)  
**Cost:** €0-5/maand (Zapier free tier initially)  
**Impact:** CRITICAL - Scale from 10 → 100 vacatures/maand

---

## 🔥 HIGH PRIORITY (Week 2)

### **6. MCP SERVER VOOR KANDIDATENTEKORT**
**Why:** Integreer kandidatentekort.nl direct in Claude workflow.

**Use Case:**
```
User (in Claude chat): 
"Analyse deze vacature: [paste text]"

Claude (via MCP):
→ Call kandidatentekort.nl API
→ Get real-time analysis
→ Return structured results
```

**MCP Server Implementation:**
```typescript
// mcp-servers/kandidatentekort/index.ts

import { McpServer } from '@modelcontextprotocol/sdk';

const server = new McpServer({
  name: 'kandidatentekort',
  version: '1.0.0'
});

server.addTool({
  name: 'analyze_vacature',
  description: 'Analyseer een Nederlandse vacaturetekst op inclusiviteit, SEO, ATS compatibility en conversion optimization',
  parameters: {
    type: 'object',
    properties: {
      vacature_tekst: {
        type: 'string',
        description: 'De volledige vacaturetekst om te analyseren'
      },
      bedrijf: {
        type: 'string',
        description: 'Optioneel: bedrijfsnaam voor context'
      },
      sector: {
        type: 'string',
        description: 'Optioneel: sector (technology, engineering, HR, etc)'
      }
    },
    required: ['vacature_tekst']
  },
  async handler(params) {
    const response = await fetch('https://kandidatentekort.nl/api/analyze', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${process.env.KANDIDATENTEKORT_API_KEY}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        vacature: params.vacature_tekst,
        bedrijf: params.bedrijf,
        sector: params.sector
      })
    });
    
    const result = await response.json();
    
    return {
      content: [{
        type: 'text',
        text: `# Vacature Analyse Resultaat

Overall Score: ${result.score}/10

## Top Issues:
${result.issues.map((issue, i) => `${i+1}. ${issue}`).join('\n')}

## Quick Wins:
${result.quickWins.map((win, i) => `${i+1}. ${win}`).join('\n')}

Volledige rapport: ${result.report_url}
`
      }]
    };
  }
});

export default server;
```

**Installation:**
```json
// claude_desktop_config.json (Mac)
// %APPDATA%/Claude/claude_desktop_config.json (Windows)

{
  "mcpServers": {
    "kandidatentekort": {
      "command": "node",
      "args": ["/path/to/mcp-servers/kandidatentekort/build/index.js"],
      "env": {
        "KANDIDATENTEKORT_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

**Time:** 6 hours (build + test)  
**Cost:** €0  
**Impact:** MEDIUM - Power user feature

---

### **7. EMAIL TEMPLATES (RESEND)**
**Why:** Professional emails = trust. Automated = scale.

**Templates Needed:**
```
1. confirmation.html - Instant confirmation
2. results.html - Analysis delivery
3. follow-up-day3.html - Check-in
4. follow-up-day7.html - Whitepaper
5. follow-up-day15.html - Consultation offer
6. premium-upsell.html - €29 upgrade
```

**Implementation:**
```typescript
// lib/email/templates.ts

export const CONFIRMATION_EMAIL = `
<!DOCTYPE html>
<html>
<head>
  <style>
    body { font-family: 'Inter', sans-serif; }
    .container { max-width: 600px; margin: 0 auto; }
    .header { background: #4A4A4A; color: white; padding: 20px; }
    .content { padding: 30px; }
    .cta { background: #FF9933; color: white; padding: 15px 30px; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <img src="https://kandidatentekort.nl/logo.png" alt="Recruitin" />
      <h1>✅ Je Vacature Analyse is Onderweg!</h1>
    </div>
    
    <div class="content">
      <p>Beste {{naam}},</p>
      
      <p>Bedankt voor je aanmelding! We gaan direct aan de slag met de analyse van je vacature.</p>
      
      <h3>Wat krijg je?</h3>
      <ul>
        <li>✅ Inclusiviteit Score (gender-bias detectie)</li>
        <li>✅ SEO Optimalisatie (Google for Jobs)</li>
        <li>✅ ATS Compatibility Check</li>
        <li>✅ 5 Concrete Verbeterpunten</li>
        <li>✅ Voor/Na Vergelijking</li>
      </ul>
      
      <p><strong>Levertijd:</strong> Binnen 24 uur in je inbox</p>
      
      <p>Kan je niet wachten? <a href="https://kandidatentekort.nl/premium" class="cta">Upgrade naar Express (6 uur) →</a></p>
      
      <p>Tot snel!</p>
      <p>Wouter van der Linden<br>Recruitin B.V.</p>
    </div>
  </div>
</body>
</html>
`;

// Send email:
import { Resend } from 'resend';
const resend = new Resend(process.env.RESEND_API_KEY);

await resend.emails.send({
  from: 'Recruitin <noreply@recruitin.nl>',
  to: user.email,
  subject: '✅ Je Vacature Analyse is Onderweg!',
  html: CONFIRMATION_EMAIL.replace('{{naam}}', user.naam)
});
```

**Time:** 3 hours (all templates)  
**Cost:** €0-20/maand (Resend)  
**Impact:** HIGH - Professional communication

---

## 🎯 MEDIUM PRIORITY (Week 3)

### **8. PRICING PAGE + PAYMENT (STRIPE/MOLLIE)**
### **9. CASE STUDIES PAGE**
### **10. BLOG SETUP (SEO Content)**
### **11. PRIVACY POLICY + AVG**
### **12. SITEMAP + ROBOTS.TXT**

---

## 🎁 NICE-TO-HAVE (Week 4+)

### **13. DASHBOARD (USER LOGIN)**
### **14. API ACCESS (ENTERPRISE)**
### **15. SLACK/TEAMS INTEGRATION**
### **16. MULTI-LANGUAGE (EN/DE)**

---

## 📊 IMPLEMENTATION PRIORITY MATRIX

```
┌─────────────────────────────────────────────┐
│ CRITICAL (Week 1)                           │
├─────────────────────────────────────────────┤
│ 1. Google Analytics         │ 1 hour        │
│ 2. Vacature Prompt          │ 2 hours       │
│ 3. Template Vacatures       │ 3 hours       │
│ 4. Facebook/LinkedIn Pixel  │ 1 hour        │
│ 5. Automation Flow (Zapier) │ 4 hours       │
├─────────────────────────────────────────────┤
│ TOTAL Week 1: 11 hours                      │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ HIGH (Week 2)                               │
├─────────────────────────────────────────────┤
│ 6. MCP Server               │ 6 hours       │
│ 7. Email Templates          │ 3 hours       │
├─────────────────────────────────────────────┤
│ TOTAL Week 2: 9 hours                       │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ MEDIUM (Week 3)                             │
├─────────────────────────────────────────────┤
│ 8-12. Pages + Legal         │ 12 hours      │
├─────────────────────────────────────────────┤
│ TOTAL Week 3: 12 hours                      │
└─────────────────────────────────────────────┘
```

---

## 🚀 EXECUTION PLAN

### **WEEK 1 SPRINT (11 hours)**
```
Monday:
├─ 09:00-10:00: Google Analytics setup
├─ 10:00-12:00: Vacature prompt verbeteren
└─ 13:00-16:00: Template vacatures + UI

Tuesday:
├─ 09:00-10:00: Facebook/LinkedIn Pixel
└─ 10:00-14:00: Automation flow (Zapier + CF Workers)

Wednesday:
└─ Testing & refinement
```

### **SUCCESS CRITERIA**
```
Week 1 Complete When:
✅ GA4 tracking all events
✅ Improved prompt live (score +2 points)
✅ 5 template vacatures working
✅ Retargeting pixels firing
✅ Automation flow tested (form → email → sequence)
```

---

## 💰 COST BREAKDOWN

```
Week 1 (Critical):
├─ Development: 11 hours × €75 = €825
├─ Tools: €0 (all free tier)
└─ Total: €825

Week 2 (High):
├─ Development: 9 hours × €75 = €675
├─ Tools: Resend €0-20/maand
└─ Total: €675-695

Week 3 (Medium):
├─ Development: 12 hours × €75 = €900
├─ Tools: €0
└─ Total: €900

GRAND TOTAL: €2,400-2,420 (one-time)
Monthly Recurring: €50-100 (tools)
```

---

## 🎯 WHAT TO DO NEXT

**Kies een optie:**

**A) START WEEK 1 SPRINT** (Recommended)
- Ik implementeer alle 5 critical items
- Timeline: 3 dagen (Monday-Wednesday)
- Cost: €825
- Impact: Production-ready kandidatentekort.nl

**B) QUICK WINS ONLY** (2 hours)
- Google Analytics
- Facebook Pixel
- Template demo
- Cost: €150
- Impact: Immediate tracking + trust

**C) FULL MONTH BUILD** (Week 1-4)
- Alle 16 items
- Timeline: 4 weken
- Cost: €2,400
- Impact: Complete platform

**Wat wordt het? A, B of C?** 🎯

Laten we bouwen! 🚀
