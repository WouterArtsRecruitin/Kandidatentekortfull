# 📄 Kandidatentekort.nl - Template Implementatie Guide

## 🎯 OVERZICHT

Dit pakket bevat **4 PDFMonkey-ready templates** voor kandidatentekort.nl:

| # | Template | Doel | Pagina's |
|---|----------|------|----------|
| 1 | Verbeterde Vacature | Het product - geoptimaliseerde vacaturetekst | 2 |
| 2 | Executive Summary | Analyse rapport met voor/na vergelijking | 1 |
| 3 | Praktische Tips | Self-service checklist met 15 tips | 2 |
| 4 | Email Delivery | Automation-ready delivery email | N/A |

---

## 🔧 PDFMONKEY SETUP

### Stap 1: Account & API Key
1. Login op [PDFMonkey.io](https://pdfmonkey.io)
2. Ga naar Settings → API Keys
3. Kopieer je API key

### Stap 2: Templates Uploaden
Voor elke template:
1. Create New Template
2. Kopieer HTML content naar template editor
3. Test met JSON data uit `05_pdfmonkey_test_data.json`
4. Noteer de Template ID

### Stap 3: Template IDs Noteren
```
TEMPLATE_VACATURE_ID = "tmpl_xxx..."
TEMPLATE_RAPPORT_ID = "tmpl_xxx..."
TEMPLATE_TIPS_ID = "tmpl_xxx..."
```

---

## 📡 API INTEGRATIE

### JavaScript/Node.js
```javascript
const generateVacaturePDF = async (vacatureData) => {
  const response = await fetch('https://api.pdfmonkey.io/api/v1/documents', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.PDFMONKEY_API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      document: {
        document_template_id: process.env.TEMPLATE_VACATURE_ID,
        payload: vacatureData,
        status: 'pending'
      }
    })
  });
  
  return response.json();
};
```

### Python
```python
import requests
import os

def generate_vacature_pdf(vacature_data):
    url = "https://api.pdfmonkey.io/api/v1/documents"
    
    headers = {
        "Authorization": f"Bearer {os.getenv('PDFMONKEY_API_KEY')}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "document": {
            "document_template_id": os.getenv('TEMPLATE_VACATURE_ID'),
            "payload": vacature_data,
            "status": "pending"
        }
    }
    
    response = requests.post(url, headers=headers, json=payload)
    return response.json()
```

---

## 🔄 ZAPIER WORKFLOW

### Trigger: Typeform Submission
```
Typeform → Zapier → Claude API → PDFMonkey → Email (Resend)
```

### Zapier Steps:

**Step 1: Typeform Trigger**
- New Entry in Typeform

**Step 2: Claude API (Webhooks)**
```json
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 4000,
  "messages": [{
    "role": "user",
    "content": "Analyseer en verbeter deze vacature: {{typeform_vacancy_text}}"
  }]
}
```

**Step 3: PDFMonkey Generate**
- Template: Verbeterde Vacature
- Payload: Claude API response (mapped)

**Step 4: PDFMonkey Generate (Rapport)**
- Template: Executive Summary
- Payload: Analysis scores

**Step 5: PDFMonkey Generate (Tips)**
- Template: Praktische Tips
- Payload: Bedrijfsnaam, functie

**Step 6: Delay**
- Wait 30 seconds (PDF generation)

**Step 7: Resend Email**
- To: {{typeform_email}}
- Template: Email Delivery
- Attachments: PDF download links

---

## 📊 HANDLEBARS VARIABELEN

### Template 1: Verbeterde Vacature
```handlebars
{{bedrijfsnaam}}
{{functie_titel}}
{{functie_subtitle}}
{{locatie}}
{{sector}}
{{dienstverband}}
{{uren_per_week}}
{{werk_locatie}}
{{#if hybride_mogelijk}}...{{/if}}
{{intro_tekst}}
{{#each werkzaamheden}}{{this}}{{/each}}
{{#each eisen}}{{this}}{{/each}}
{{#each nice_to_haves}}{{this}}{{/each}}
{{salaris_range}}
{{salaris_details}}
{{#each benefits}}
  {{this.icon}}
  {{this.titel}}
  {{this.beschrijving}}
{{/each}}
{{bedrijf_beschrijving}}
{{team_beschrijving}}
{{#each sollicitatie_proces}}Stap {{@index}}: {{this}}{{/each}}
{{inclusiviteit_statement}}
{{contact_naam}}
{{contact_email}}
{{contact_telefoon}}
{{datum}}
{{referentie_nummer}}
```

### Template 2: Executive Summary
```handlebars
{{score_voor}}
{{score_na}}
{{score_verbetering}}
{{verwachte_response}}
{{#each top_verbeteringen}}
  {{this.titel}}
  {{this.beschrijving}}
  {{this.impact}}
{{/each}}
{{#each categorie_scores}}
  {{this.naam}}
  {{this.voor}}
  {{this.na}}
{{/each}}
{{#each quick_tips}}{{this}}{{/each}}
```

### Template 3: Tips Checklist
```handlebars
{{bedrijfsnaam}}
{{functie_titel}}
{{progress_percentage}}
{{tips_completed}}
{{tips_remaining}}
{{potential_improvement}}
{{datum}}
{{contact_email}}
```

### Template 4: Email Delivery
```handlebars
{{preview_tekst}}
{{voornaam}}
{{score_voor}}
{{score_na}}
{{score_verbetering}}
{{#each top_verbeteringen}}{{this}}{{/each}}
{{download_link}}
{{calendly_link}}
{{referentie_nummer}}
```

---

## 🎨 BRAND COLORS

```css
/* Primary - Recruitin Orange */
--primary: #ff6b35;
--primary-dark: #e55a2b;

/* Secondary - Dark */
--dark: #2c3e50;
--gray-700: #4a5568;
--gray-500: #718096;
--gray-300: #e2e8f0;

/* Success */
--success: #38a169;
--success-light: #c6f6d5;

/* Warning */
--warning: #ed8936;
--warning-light: #fffbeb;

/* Error */
--error: #e53e3e;
--error-light: #fed7d7;

/* Info */
--info: #4299e1;
--info-light: #ebf8ff;
```

---

## 📁 BESTANDEN

```
templates/
├── 01_verbeterde_vacature_template.html    # Het product
├── 02_executive_summary_rapport.html       # Analyse rapport
├── 03_praktische_tips_checklist.html       # Self-service tips
├── 04_email_delivery_template.html         # Automation email
├── 05_pdfmonkey_test_data.json             # Test data
└── 06_implementation_guide.md              # Deze guide
```

---

## ✅ CHECKLIST VOOR GO-LIVE

- [ ] PDFMonkey account actief
- [ ] Alle 4 templates geüpload
- [ ] Template IDs genoteerd
- [ ] API key in environment variables
- [ ] Test PDF gegenereerd per template
- [ ] Zapier workflow geconfigureerd
- [ ] Email delivery getest
- [ ] Download links werkend
- [ ] Calendly link correct
- [ ] GDPR compliance checked

---

## 🚀 AUTOMATION FLOW

```
┌─────────────────┐
│   Typeform      │
│   Submission    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Pipedrive     │
│   Deal Created  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Claude API    │
│   Analysis      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   PDFMonkey     │
│   Generate 3x   │
│   (Parallel)    │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌───────┐ ┌───────┐
│Vacature│ │Rapport│
│  PDF   │ │  PDF  │
└───┬───┘ └───┬───┘
    │         │
    └────┬────┘
         │
         ▼
┌─────────────────┐
│   Resend/Gmail  │
│   Email + PDFs  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Pipedrive     │
│   Deal Updated  │
│   (Delivered)   │
└─────────────────┘
```

---

## 💰 KOSTEN

| Service | Plan | Kosten/maand |
|---------|------|--------------|
| PDFMonkey | Starter | €15 (500 docs) |
| PDFMonkey | Pro | €49 (2500 docs) |
| Zapier | Professional | €49 |
| Resend | Pro | €20 |
| **Totaal** | | **€84-118/maand** |

**Break-even:** ~4-5 klanten/maand @ €29 pay-per-use

---

## 📞 SUPPORT

**Technische vragen:** support@kandidatentekort.nl

**PDFMonkey docs:** https://docs.pdfmonkey.io

**Handlebars syntax:** https://handlebarsjs.com/guide/

---

*Last updated: Januari 2025*
*Version: 1.0*
