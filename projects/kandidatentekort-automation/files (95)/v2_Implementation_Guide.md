# kandidatentekort.nl - Premium Templates v2
## Implementation Guide

---

## 🎨 WAT IS NIEUW IN V2?

### Design Upgrades
- **Recruitment APK Styling**: Dezelfde premium look als je bestaande APK rapporten
- **Data Journalism Infographics**: Visuele storytelling met conic gradients, benchmark charts
- **Narrative Approach**: Niet opsommen maar verhalen vertellen
- **Hover Effects & Shadows**: Premium feel met subtiele interacties

### Visuele Elementen
- Conic gradient score circles (voor/na vergelijking)
- Benchmark comparison bars met industry averages
- ROI impact cards met dark gradient backgrounds
- Progress trackers met real-time updates
- Color-coded impact badges (High/Medium/Quick Win)
- Trust signals en credibility badges

---

## 📦 TEMPLATE OVERVIEW

| Template | Pagina's | Doel | Key Features |
|----------|----------|------|--------------|
| **Executive Summary** | 1 | Eerste indruk | Score transformatie, top 3 verbeteringen, benchmark chart |
| **Before & After Vergelijking** | 2 | Onderbouwing | Side-by-side tekst, uitleg per verbetering, echte bronnen |
| **Verbeterde Vacature** | 2 | Het product | Premium job posting met salary banner, benefits grid |
| **Tips Checklist** | 2 | Self-service | 15 actionable tips, progress tracker, timeline |
| **Email Delivery** | - | Automation | Mobile responsive, success banner, CTA |

---

## 🚀 QUICK START

### Stap 1: PDFMonkey Account
1. Ga naar [pdfmonkey.io](https://pdfmonkey.io)
2. Maak account aan (Starter €15/mo = 500 docs)
3. Noteer je **API Key** (Settings → API)

### Stap 2: Templates Uploaden
1. **Dashboard → Templates → New Template**
2. Upload HTML file
3. Selecteer **A4** als paper size
4. Zet **Page breaks** op `CSS-based`
5. Klik **Create Template**
6. Noteer de **Template ID**

### Stap 3: Test met JSON Data
```javascript
// In PDFMonkey Preview
{
  "bedrijfsnaam": "TechFlow B.V.",
  "functie_titel": "Senior Software Developer",
  "score_voor": 54,
  "score_na": 87,
  "score_verbetering": 33
  // ... rest van test data
}
```

### Stap 4: Zapier Integratie
Zie workflow diagram hieronder.

---

## 🔄 ZAPIER WORKFLOW

```
┌─────────────────────────────────────────────────────────────────┐
│                        TRIGGER                                   │
├─────────────────────────────────────────────────────────────────┤
│  Typeform → New Entry                                           │
│  • Bedrijfsnaam, functie, email, vacaturetekst                  │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      ACTION 1: CRM                               │
├─────────────────────────────────────────────────────────────────┤
│  Pipedrive → Create Deal                                        │
│  • Title: "[Bedrijf] - [Functie]"                              │
│  • Stage: "Analyse Gestart"                                     │
│  • Value: €29                                                   │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ACTION 2: AI ANALYSE                          │
├─────────────────────────────────────────────────────────────────┤
│  Webhooks by Zapier → POST to Claude API                        │
│  • Input: Originele vacaturetekst                               │
│  • Output: JSON met scores, verbeteringen, nieuwe tekst         │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                 ACTION 3-5: PDF GENERATION (PARALLEL)            │
├─────────────────────────────────────────────────────────────────┤
│  3a. PDFMonkey → Generate Executive Summary                     │
│  3b. PDFMonkey → Generate Verbeterde Vacature                   │
│  3c. PDFMonkey → Generate Tips Checklist                        │
│  • Wait for all 3 to complete                                   │
│  • Collect download URLs                                        │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      ACTION 6: EMAIL                             │
├─────────────────────────────────────────────────────────────────┤
│  Resend / Gmail → Send Email                                    │
│  • To: Klant email                                              │
│  • Template: v2_Email_Delivery_Template                         │
│  • Attachments: 3x PDF download links                           │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ACTION 7: CRM UPDATE                          │
├─────────────────────────────────────────────────────────────────┤
│  Pipedrive → Update Deal                                        │
│  • Stage: "Rapport Verzonden"                                   │
│  • Note: Add PDF links + delivery timestamp                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎨 BRAND COLORS

```css
:root {
    /* Primary */
    --primary-orange: #FF6B35;
    --primary-orange-light: #FF8A5E;
    --primary-orange-dark: #E55A2B;
    --primary-blue: #2C3E50;
    --primary-blue-light: #34495E;
    
    /* Status */
    --success-green: #10B981;
    --success-green-light: #D1FAE5;
    --warning-amber: #F59E0B;
    --danger-red: #EF4444;
    
    /* Accent */
    --purple: #7C3AED;
    --purple-light: #EDE9FE;
    --cyan: #06B6D4;
    --cyan-light: #CFFAFE;
    
    /* Neutral */
    --gray-50: #F9FAFB;
    --gray-100: #F3F4F6;
    --gray-500: #6B7280;
    --gray-800: #1F2937;
    
    /* Gradients */
    --orange-gradient: linear-gradient(135deg, #FF6B35, #E55A2B);
    --blue-gradient: linear-gradient(135deg, #2C3E50, #1E3A5F);
    --success-gradient: linear-gradient(135deg, #10B981, #059669);
}
```

---

## 📊 HANDLEBARS CHEATSHEET

### Basis
```handlebars
{{variabele}}                     <!-- Simpele waarde -->
{{bedrijfsnaam}}                  <!-- "TechFlow B.V." -->
```

### Loops
```handlebars
{{#each werkzaamheden}}
    <li>{{this}}</li>
{{/each}}

{{#each top_verbeteringen}}
    <div>
        <h4>{{this.titel}}</h4>
        <p>{{this.beschrijving}}</p>
    </div>
{{/each}}
```

### Index in Loop
```handlebars
{{#each items}}
    <span>{{@index}}</span>       <!-- 0, 1, 2, ... -->
{{/each}}
```

### Conditionals
```handlebars
{{#if hybride_mogelijk}}
    <span>Hybride werken mogelijk</span>
{{else}}
    <span>Op locatie</span>
{{/if}}
```

### Score Circle (CSS calc)
```css
/* Conic gradient based on score */
background: conic-gradient(
    var(--success-green) 0deg calc({{score_na}} * 3.6deg),
    var(--gray-200) calc({{score_na}} * 3.6deg) 360deg
);
```

---

## ✅ GO-LIVE CHECKLIST

### PDFMonkey Setup
- [ ] Account aangemaakt
- [ ] API Key genoteerd
- [ ] 3 templates geüpload
- [ ] Template IDs genoteerd
- [ ] Test met JSON data succesvol

### Zapier Configuration
- [ ] Typeform trigger geconfigureerd
- [ ] Pipedrive Create Deal actie
- [ ] Claude API webhook
- [ ] PDFMonkey acties (3x)
- [ ] Email actie (Resend/Gmail)
- [ ] Pipedrive Update actie
- [ ] End-to-end test gedaan

### Quality Check
- [ ] PDF renders correct in browser
- [ ] Print preview toont correcte pagina-breaks
- [ ] Alle variabelen worden ingevuld
- [ ] Email komt aan in inbox (niet spam)
- [ ] Mobile email rendering OK
- [ ] Links in email werken

---

## 💰 KOSTEN BREAKDOWN

| Component | Plan | Kosten | Docs/maand |
|-----------|------|--------|------------|
| PDFMonkey | Starter | €15/mo | 500 docs |
| PDFMonkey | Growth | €49/mo | 2,500 docs |
| Zapier | Professional | €49/mo | 2,000 tasks |
| Resend | Pro | €20/mo | 50k emails |
| **TOTAAL** | - | **€84-118/mo** | - |

### Break-even
- Bij €29/klant: **4-5 klanten/maand** = break-even
- Bij 30 klanten/maand: **€870 revenue** vs **€118 kosten** = **€752 winst**

---

## 📁 BESTANDEN

```
v2_templates/
├── v2_Executive_Summary_Rapport.html    # 1-page score rapport
├── v2_Before_After_Vergelijking.html    # 2-page before/after + bronnen
├── v2_Verbeterde_Vacature_Template.html # 2-page vacature
├── v2_Praktische_Tips_Checklist.html    # 2-page checklist
├── v2_Email_Delivery_Template.html      # Email template
├── v2_PDFMonkey_Test_Data.json          # Complete test data
└── v2_Implementation_Guide.md           # Deze guide
```

---

## 🆘 SUPPORT

Vragen? 
- **Email**: wouter@recruitin.nl
- **Call**: [Calendly](https://calendly.com/wouter-arts-/vacature-analyse-advies)

---

*kandidatentekort.nl • Powered by Recruitin*
