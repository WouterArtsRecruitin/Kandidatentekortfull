# Kandidatentekort.nl - Automation Review & Lead Generation Verbeterplan

## DEEL 1: HUIDIGE AUTOMATION FLOW REVIEW

### Overzicht Huidige Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         LEAD ENTRY POINTS                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│  1. Quick Analyzer (React Frontend)                                          │
│     └─> Claude AI analyse → Results modal → Typeform redirect                │
│                                                                              │
│  2. vacature-insturen.html (Typeform Direct)                                 │
│     └─> Typeform embed → Webhook → Pipedrive                                 │
│                                                                              │
│  3. Meta/Facebook Lead Ads                                                   │
│     └─> Webhook → Welcome email → Pipedrive                                  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         PROCESSING PIPELINE                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│  Typeform Webhook (kandidatentekort_auto.py)                                │
│  ├─> Parse form data (email, bedrijf, functie, vacature)                    │
│  ├─> Extract PDF/DOCX file content                                          │
│  ├─> Send confirmation email                                                │
│  ├─> Create Pipedrive: Organization → Person → Deal                         │
│  └─> Store vacancy text in notes                                            │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    HANDMATIGE VERWERKING (Huidige situatie)                 │
├─────────────────────────────────────────────────────────────────────────────┤
│  1. Wouter analyseert vacature handmatig                                    │
│  2. Upload PDFs naar externe storage                                        │
│  3. POST /update-pdf-urls met deal_id + PDF URLs                           │
│  4. 24 uur reminder taak wordt aangemaakt                                   │
│  5. POST /send-pdf-email om rapport te versturen                           │
│  6. Nurture sequence wordt automatisch getriggerd                          │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    NURTURE SEQUENCE (8 emails over 30 dagen)                │
├─────────────────────────────────────────────────────────────────────────────┤
│  Day 1:  Check-in                                                           │
│  Day 3:  Is het gelukt?                                                     │
│  Day 5:  Resultaten                                                         │
│  Day 8:  Tip Functietitel                                                   │
│  Day 11: Tip Salaris                                                        │
│  Day 14: Tip Opening                                                        │
│  Day 21: Gesprek Aanbod                                                     │
│  Day 30: Final Check-in                                                     │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## DEEL 2: GEIDENTIFICEERDE PROBLEMEN & VERBETERPUNTEN

### KRITIEKE ISSUES

#### 1. Handmatige Bottleneck in Analyse Flow
**Probleem:** Na recente wijzigingen (commit `1ade881`) is de automatische Claude analyse uitgeschakeld. Nu moet Wouter handmatig:
- Vacatures analyseren met webhook_v6.py
- PDFs uploaden
- URLs plakken
- Email versturen

**Impact:** Vertraagt response tijd van "instant" naar "tot 24 uur"

**Oplossing:** Hybride aanpak implementeren:
```python
# Nieuwe flow:
1. Typeform → Automatische Claude analyse (binnen minuten)
2. PDFs worden automatisch gegenereerd (PDFMonkey of ReportLab fallback)
3. Email wordt in draft gezet voor snelle review
4. One-click approve om te versturen
```

#### 2. Meta Lead Ads Flow is Incompleet
**Probleem:** Meta leads krijgen alleen een "welkom" email met instructie om vacature te mailen. Ze moeten nog:
- Handmatig email sturen
- Wachten op response

**Impact:** Hoog dropout percentage - leads "koelen af"

**Oplossing:** Direct in-app flow voor Meta leads:
```
Meta Lead → Landing page met one-click Typeform → Instant analyse
```

#### 3. Geen Automatische Lead Scoring
**Probleem:** Alle leads worden gelijk behandeld in Pipedrive Stage 21

**Impact:** Geen prioritering voor "hot" leads

**Oplossing:** Lead scoring implementeren:
```python
LEAD_SCORE_FACTORS = {
    'source': {'typeform_direct': 10, 'meta_lead': 5, 'organic': 8},
    'company_size': {'enterprise': 10, 'sme': 7, 'startup': 5},
    'urgency': {'now': 10, 'week': 7, 'month': 3},
    'email_opens': {'per_open': 2}
}
```

#### 4. Tracking Gaps
**Probleem:**
- Facebook Pixel ID inconsistent (2 verschillende IDs gevonden)
- Server-side tracking geeft niet altijd correcte IP door
- UTM parameters gaan verloren bij cross-domain redirect naar Typeform

**Impact:** Incomplete attributie data

---

### TECHNISCHE VERBETERINGEN

#### 1. Code Duplicatie
- `kandidatentekort_auto.py` (1800+ lines) en `webhook_v6.py` (1400+ lines) hebben overlappende functionaliteit
- Email templates herhaald in meerdere functies

**Oplossing:** Refactor naar modules:
```
/backend
├── handlers/
│   ├── typeform.py
│   ├── meta_lead.py
│   └── analysis.py
├── services/
│   ├── email.py
│   ├── pipedrive.py
│   ├── claude.py
│   └── pdf.py
├── templates/
│   └── emails/
└── main.py
```

#### 2. Error Handling
**Probleem:** Veel bare `except Exception as e:` zonder recovery

**Oplossing:** Retry logic met exponential backoff:
```python
@retry(max_attempts=3, backoff=2)
def send_email_with_retry(to, subject, body):
    ...
```

#### 3. Missing Health Checks
**Oplossing:** Monitoring endpoints toevoegen:
```python
@app.route("/health/detailed")
def health_detailed():
    return {
        "pipedrive": check_pipedrive(),
        "email": check_smtp(),
        "claude": check_anthropic(),
        "pdfmonkey": check_pdfmonkey()
    }
```

---

## DEEL 3: LEAD GENERATION VERBETERPLAN

### QUICK WINS (< 1 week implementatie)

#### 1. Exit Intent Popup Activeren
**Huidige status:** ExitIntentPopup.tsx bestaat maar is niet actief

**Actie:** Activeren met A/B test:
```tsx
// In App.tsx
<ExitIntentPopup
  delay={5000}
  showOnlyOnce={true}
  offer="Gratis Vacature Quick-Check"
/>
```

**Verwachte impact:** +10-15% lead capture

#### 2. Social Proof Notifications
**Huidige status:** SocialProofNotification.tsx bestaat maar niet actief

**Actie:** Implementeren met echte data uit Pipedrive:
```tsx
// "John van TechBedrijf ontving zojuist zijn analyse"
<SocialProofNotification
  fetchFromAPI={true}
  interval={15000}
/>
```

**Verwachte impact:** +5-8% conversie

#### 3. WhatsApp Click-to-Chat Optimaliseren
**Huidige status:** WhatsAppButton.tsx met vaste tekst

**Actie:** Contextual messaging:
```tsx
// Na analyse: "Vragen over je score van 6.5?"
// Op homepage: "Direct advies nodig?"
```

**Verwachte impact:** +20% engagement

#### 4. Typeform Pre-fill Verbeteren
**Huidige actie:** Alleen vacature_text wordt doorgegeven

**Verbetering:**
```javascript
const typeformUrl = `https://form.typeform.com/to/${TYPEFORM_ID}#` +
  `vacature_text=${encodedText}` +
  `&score=${analysisResult.score}` +
  `&sector=${analysisResult.sector}` +
  `&utm_source=${utmParams.utm_source}`;
```

---

### MEDIUM TERM (2-4 weken)

#### 5. LinkedIn Lead Ads Integratie
**Waarom:** Hogere kwaliteit B2B leads dan Facebook

**Implementatie:**
```python
@app.route("/webhook/linkedin-lead", methods=["POST"])
def linkedin_lead_webhook():
    # Vergelijkbare flow als Meta webhook
    ...
```

#### 6. Chatbot/Live Chat Toevoegen
**Optie 1:** Tidio (gratis tier beschikbaar)
**Optie 2:** Intercom (meer features)
**Optie 3:** Custom met OpenAI API

**Implementation:**
```html
<script src="//code.tidio.co/YOUR_KEY.js" async></script>
```

**Verwachte impact:** +15-20% lead capture

#### 7. Content Upgrades per Sector
**Concept:** Sector-specifieke lead magnets

| Sector | Lead Magnet |
|--------|-------------|
| IT | "Salarisgids IT 2025" |
| Bouw | "Checklist Vacature Bouw" |
| Techniek | "5 Fouten bij Werving Technici" |
| Productie | "Template Productiemedewerker" |

**Flow:**
```
Blog post over sector → CTA voor download → Email capture → Nurture
```

#### 8. Referral Programma
**Concept:** Klanten die anderen doorverwijzen

**Implementatie:**
```
- Unieke referral link per klant
- €25 korting voor doorverwijzer
- €25 korting voor nieuwe klant
- Tracking via UTM: ?ref=customer123
```

---

### LONG TERM (1-3 maanden)

#### 9. SEO Content Strategie
**Keyword opportunities:**

| Keyword | Zoekvolume/maand | Moeilijkheid |
|---------|------------------|--------------|
| vacature schrijven | 1,200 | Medium |
| vacaturetekst voorbeeld | 800 | Low |
| werknemers werven | 500 | Medium |
| personeel vinden | 400 | Medium |
| goede vacature maken | 300 | Low |

**Content plan:**
1. Blog: "Zo schrijf je een vacature die wél werkt"
2. Blog: "10 voorbeelden van vacatureteksten [per sector]"
3. Tool: "Vacature Checklist Generator"
4. Guide: "Werven in krappe arbeidsmarkt 2025"

#### 10. Webinar Funnel
**Concept:** Gratis webinar over vacancy copywriting

**Flow:**
```
Landing page → Registratie → Email reminders →
Live webinar → Q&A → Offer → Follow-up sequence
```

**Topics:**
- "3 Geheimen voor 2x meer sollicitaties"
- "Waarom je vacature niet werkt (en hoe je het fixt)"

#### 11. Partnership Channel
**Potentiële partners:**
- ATS leveranciers (Recruitee, Homerun, Carerix)
- HR software (Personio, HiBob)
- Uitzendbureaus (white-label analyse tool)
- Brancheverenigingen

**Model:**
```
Partner embed onze tool → Revenue share 20-30%
```

#### 12. Retargeting Campagnes
**Audiences:**

| Audience | Trigger | Ad Creative |
|----------|---------|-------------|
| Analyzer users | Bezocht, niet gesubmit | "Je analyse staat klaar!" |
| Form abandoners | Typeform 50% | "Nog 2 velden..." |
| Report viewers | PDF geopend | "Hulp nodig met implementatie?" |

---

## DEEL 4: PRIORITERING & ROADMAP

### WEEK 1-2: Foundation
- [ ] Fix Facebook Pixel consistency
- [ ] Activeer ExitIntentPopup
- [ ] Activeer SocialProofNotification
- [ ] Test en deploy automatic Claude analyse

### WEEK 3-4: Optimization
- [ ] Implement lead scoring in Pipedrive
- [ ] LinkedIn Lead Ads webhook
- [ ] Chatbot integratie
- [ ] A/B test landing page

### MAAND 2: Content & Channels
- [ ] Launch 3 SEO blog posts
- [ ] Sector lead magnets creëren
- [ ] Referral programma opzetten
- [ ] Retargeting campagnes starten

### MAAND 3: Scale
- [ ] Eerste webinar organiseren
- [ ] Partnership outreach starten
- [ ] Automatiseer lead scoring
- [ ] Geavanceerde nurture branching

---

## DEEL 5: KPIs & METRICS

### Huidige Baseline (schatten)
- Website bezoekers: ?/maand
- Quick analyzer gebruikt: ?/maand
- Typeform submits: ?/maand
- Meta leads: ?/maand
- Conversie naar klant: ?%

### Targets na implementatie
| Metric | Huidig | Target (+90 dagen) | Verbetering |
|--------|--------|-------------------|-------------|
| Lead capture rate | ~3% | 6% | +100% |
| Typeform completion | ~40% | 60% | +50% |
| Email open rate | ~25% | 35% | +40% |
| Response time | 24u | <2u | -91% |
| Hot lead ratio | ~10% | 25% | +150% |

---

## DEEL 6: TECHNISCHE IMPLEMENTATIE DETAILS

### Automatische Analyse Reactiveren (Prioriteit 1)

```python
# In kandidatentekort_auto.py, update typeform_webhook():

@app.route("/webhook/typeform", methods=["POST"])
def typeform_webhook():
    # ... existing parsing code ...

    # REACTIVEER: Automatische analyse
    if vacancy_text and len(vacancy_text) > 100:
        # Start async analyse
        thread = threading.Thread(
            target=process_analysis_async,
            args=(deal_id, vacancy_text, p['email'], p['voornaam'], p['bedrijf'])
        )
        thread.start()

    return jsonify({"success": True, "analysis": "started"}), 200

def process_analysis_async(deal_id, vacancy_text, email, voornaam, bedrijf):
    """Background processing voor analyse"""
    try:
        # 1. Claude analyse
        analysis = analyze_with_claude(vacancy_text, bedrijf)

        # 2. Generate PDFs
        if USE_PDFMONKEY:
            rapport_pdf = generate_pdf_with_pdfmonkey(...)
            vacature_pdf = generate_pdf_with_pdfmonkey(...)
        else:
            rapport_pdf = generate_reportlab_pdf(...)

        # 3. Upload to storage (Cloudinary/S3)
        rapport_url = upload_pdf(rapport_pdf, f"rapport_{deal_id}.pdf")
        vacature_url = upload_pdf(vacature_pdf, f"vacature_{deal_id}.pdf")

        # 4. Update Pipedrive
        update_deal_with_analysis(deal_id, analysis, rapport_url, vacature_url)

        # 5. Send email
        send_analysis_email(email, voornaam, bedrijf, analysis, rapport_url, vacature_url)

        # 6. Start nurture
        trigger_nurture_sequence(deal_id)

    except Exception as e:
        logger.error(f"Async analysis failed: {e}")
        # Fallback: mark for manual processing
        add_pipedrive_note(deal_id, f"⚠️ Automatische analyse mislukt: {e}")
```

### Meta Lead Flow Verbeteren (Prioriteit 2)

```python
# Nieuwe Meta lead email met directe Typeform link

def get_meta_lead_email_html_v2(voornaam, bedrijf, typeform_url):
    return f'''
    ...
    <a href="{typeform_url}" style="...">
        📝 Upload je vacature direct (1 minuut)
    </a>
    ...
    '''

# In meta_lead_webhook():
typeform_url = f"https://form.typeform.com/to/{TYPEFORM_ID}#" + \
    f"email={lead['email']}&bedrijf={lead['bedrijf']}&source=meta"
```

---

## APPENDIX: Checklist voor Developer

### Vereiste Environment Variables
```bash
# Core
ANTHROPIC_API_KEY=
PIPEDRIVE_API_TOKEN=
GMAIL_USER=
GMAIL_APP_PASSWORD=

# Optional (for enhanced features)
PDFMONKEY_API_KEY=
PDFMONKEY_TEMPLATE_ANALYSE=
PDFMONKEY_TEMPLATE_VACATURE=
FB_ACCESS_TOKEN=
FB_PIXEL_ID=
GA4_API_SECRET=
GA4_MEASUREMENT_ID=
CLOUDINARY_URL=  # Voor PDF storage
```

### API Endpoints Referentie
```
GET  /                      - Health check
POST /webhook/typeform      - Typeform webhook
POST /webhook/meta-lead     - Meta Lead Ads webhook
POST /send-pdf-email        - Verstuur PDF email
POST /update-pdf-urls       - Update deal met PDF URLs
POST /nurture/process       - Process pending nurture emails
GET  /health/detailed       - Detailed health check (toe te voegen)
```

---

*Document versie: 1.0*
*Laatst bijgewerkt: 2025-12-25*
*Auteur: Claude Code Analysis*
