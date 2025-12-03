# KandidatenTekort.nl - Project Backup & Documentation

**Laatste update:** December 2025
**Eigenaar:** Recruitin B.V.

---

## 1. UTM Links voor Marketing

### Facebook
```
# Facebook Ads
https://kandidatentekort.nl/?utm_source=facebook&utm_medium=cpc&utm_campaign=vacature_analyse

# Facebook Organic Post
https://kandidatentekort.nl/?utm_source=facebook&utm_medium=organic&utm_campaign=social_post
```

### LinkedIn
```
# LinkedIn Ads
https://kandidatentekort.nl/?utm_source=linkedin&utm_medium=cpc&utm_campaign=vacature_analyse

# LinkedIn Organic Post
https://kandidatentekort.nl/?utm_source=linkedin&utm_medium=organic&utm_campaign=social_post
```

### Email
```
# Newsletter
https://kandidatentekort.nl/?utm_source=email&utm_medium=newsletter&utm_campaign=weekly

# Direct Outreach
https://kandidatentekort.nl/?utm_source=email&utm_medium=direct&utm_campaign=outreach
```

### Other Channels
```
# WhatsApp Share
https://kandidatentekort.nl/?utm_source=whatsapp&utm_medium=referral&utm_campaign=share

# Google Ads
https://kandidatentekort.nl/?utm_source=google&utm_medium=cpc&utm_campaign=vacature_analyse
```

---

## 2. Tracking IDs & Configuratie

### Google Analytics 4
- **Measurement ID:** `G-67PJ02SXVN`
- **Status:** Actief
- **Events tracked:**
  - `demo_clicked`
  - `initiate_checkout`
  - `complete_registration`
  - `calendly_click`
  - `whatsapp_click`
  - `exit_intent_shown`
  - `exit_intent_cta_clicked`

### Facebook
- **Pixel ID:** `1735907367288442`
- **App ID:** `757606233848402`
- **App Secret:** `9ee40f5aa3ba931320ac3c3e61233401`
- **Access Token:** `EAASX9Iy8fL8BP...` (zie environment variables)

### Typeform
- **Form ID:** `01KARQKA6091587B0YQE19KZB5`

### Calendly
- **URL:** `https://calendly.com/wouter-arts-/vacature-analyse-advies`

### WhatsApp Business
- **Nummer:** `31614314593`

---

## 3. Environment Variables

### Netlify (Frontend + Functions)
```bash
FB_ACCESS_TOKEN=<Facebook Access Token>
GA4_API_SECRET=<GA4 Measurement Protocol Secret>
```

### Render (Python API)
```bash
CLAUDE_API_KEY=<Anthropic API Key>
PIPEDRIVE_API_KEY=<Pipedrive API Key>
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=<email>
SMTP_PASSWORD=<app password>
```

---

## 4. Automation Flows

### Typeform → Analyse → Email Flow
1. Gebruiker vult Typeform in
2. Typeform webhook → `POST /webhook/typeform`
3. Python API analyseert met TECHNICAL_MASTER_PROMPT v2.0
4. Email met analyse wordt verstuurd
5. Lead wordt aangemaakt in Pipedrive

### API Endpoints (Render)
```
GET  /                      - API info
GET  /health               - Health check
POST /webhook/analyze      - Direct vacancy analysis
POST /webhook/typeform     - Typeform webhook
POST /api/sector-detect    - Quick sector detection
```

### Netlify Functions
```
POST /.netlify/functions/track-conversion  - FB CAPI + GA4 MP
POST /.netlify/functions/claude-analyze    - Claude API wrapper
```

---

## 5. GitHub Repository

- **Repo:** `WouterArtsRecruitin/Kandidatentekortfull`
- **Main Branch:** `main`
- **Frontend URL:** https://kandidatentekort.nl
- **Netlify:** Auto-deploy from main

### Key Files
```
index.html                          - Main HTML with meta tags
kandidatentekort_auto.py            - Python API with master prompt
netlify/functions/track-conversion.js - Server-side tracking
netlify/functions/claude-analyze.js   - Claude API wrapper
src/lib/analytics.ts                  - Frontend analytics + UTM
render.yaml                           - Render deployment config
netlify.toml                          - Netlify config
```

---

## 6. Backup Commando's

### Clone Repository
```bash
git clone https://github.com/WouterArtsRecruitin/Kandidatentekortfull.git
cd Kandidatentekortfull
```

### Export All Files
```bash
zip -r kandidatentekort_backup_$(date +%Y%m%d).zip . -x "node_modules/*" -x ".git/*"
```

### Netlify Export
```bash
# Via Netlify CLI
netlify sites:list
netlify env:list
```

---

## 7. Contacts & Support

- **Wouter Arts** - wouter@recruitin.nl
- **Website:** https://www.recruitin.nl
- **Phone:** +31 313 410 507

---

## 8. Open Graph Preview

```html
<meta property="fb:app_id" content="757606233848402">
<meta property="og:title" content="Gratis Vacature Analyse - 40-60% Meer Sollicitaties">
<meta property="og:description" content="Upload je vacature en ontvang direct een AI-powered analyse.">
<meta property="og:image" content="https://lh3.googleusercontent.com/d/1cBokXlFmTFYgxlaALdnGvbcXbhtvuLjT=w1200">
<meta property="og:url" content="https://kandidatentekort.nl">
```

Test URL: https://developers.facebook.com/tools/debug/?q=https://kandidatentekort.nl

---

*Dit document is automatisch gegenereerd. Bewaar een kopie op een veilige locatie.*
