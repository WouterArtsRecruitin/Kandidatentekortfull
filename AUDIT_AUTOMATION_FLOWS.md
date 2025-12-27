# AUTOMATION FLOW AUDIT - Kandidatentekort.nl

**Audit Datum:** 2025-12-25
**Versies:** V1 (kandidatentekort_auto.py) vs V2 (v2/)

---

## FLOW 1: META LEAD ADS → PIPEDRIVE → EMAIL

### V1 Huidige Implementatie

```
Facebook Lead Ad
       │
       ▼
POST /webhook/meta-lead
       │
       ├─► Parse lead data (email, naam, bedrijf, telefoon)
       │
       ├─► Validate email ──► 400 error if invalid
       │
       ├─► Send welcome email
       │   └─► "Stuur je vacature naar info@..."
       │       ⚠️ HANDMATIGE ACTIE VEREIST
       │
       ├─► Create Pipedrive Organization
       │
       ├─► Create Pipedrive Person
       │
       └─► Create Pipedrive Deal
           └─► Stage 21 (Gekwalificeerd)
           └─► Note: "Wacht op vacaturetekst"
```

#### V1 Gaps Geïdentificeerd

| Issue | Impact | Severity |
|-------|--------|----------|
| Welkom email vraagt handmatige actie | Lead moet zelf vacature mailen | 🔴 HIGH |
| Geen directe Typeform link | Extra friction, lager conversie | 🔴 HIGH |
| Geen lead scoring | Geen prioritering | 🟡 MEDIUM |
| Geen tracking van bron in Pipedrive | Attributie onduidelijk | 🟡 MEDIUM |
| Geen follow-up als lead niet reageert | Lead gaat verloren | 🔴 HIGH |

### V2 Verbeterde Implementatie

```
Facebook Lead Ad
       │
       ▼
POST /webhook/meta-lead
       │
       ├─► Parse lead data
       │
       ├─► Calculate lead score ──► Hot/Warm/Cold
       │
       ├─► Send welcome email
       │   └─► DIRECT TYPEFORM LINK met pre-fill
       │       ✅ ONE-CLICK naar vacature upload
       │
       ├─► Create Pipedrive Organization
       │
       ├─► Create Pipedrive Person
       │
       └─► Create Pipedrive Deal
           ├─► Lead score in notes
           └─► Bron tracking
```

#### V2 Verbeteringen

- ✅ Direct Typeform link in email
- ✅ Pre-filled data (email, bedrijf)
- ✅ Lead scoring
- ✅ Bron tracking in notes

---

## FLOW 2: TYPEFORM → PIPEDRIVE → EMAIL AUTOMATION

### V1 Huidige Implementatie

```
Typeform Submit
       │
       ▼
POST /webhook/typeform
       │
       ├─► Parse form data
       │   ├─► Email, naam, bedrijf
       │   ├─► Functie, sector
       │   └─► File upload (PDF/DOCX)
       │
       ├─► Extract text from file
       │
       ├─► Send confirmation email ──► Immediate
       │
       ├─► Create Pipedrive Organization
       │
       ├─► Create Pipedrive Person
       │
       └─► Create Pipedrive Deal
           ├─► Vacancy text in notes
           └─► "PDF URLs hier plakken" placeholder

           ⚠️ STOP - HANDMATIGE VERWERKING NODIG:

           1. Wouter analyseert vacature handmatig
           2. Maakt PDFs aan
           3. POST /update-pdf-urls
           4. POST /send-pdf-email (binnen 24u)
           5. Nurture sequence start
```

#### Nurture Sequence (als handmatig getriggerd)

```
Rapport verzonden
       │
       ├─► Day 1:  Email 1 - Check-in
       ├─► Day 3:  Email 2 - Is het gelukt?
       ├─► Day 5:  Email 3 - Resultaten
       ├─► Day 8:  Email 4 - Tip Functietitel
       ├─► Day 11: Email 5 - Tip Salaris
       ├─► Day 14: Email 6 - Tip Opening
       ├─► Day 21: Email 7 - Gesprek Aanbod
       └─► Day 30: Email 8 - Final Check-in

Trigger: POST /nurture/process (moet periodiek worden aangeroepen)
Filter: Alleen deals in Stage 21 (Gekwalificeerd)
Stop: Stage wijziging of unsubscribe
```

#### V1 Gaps Geïdentificeerd

| Issue | Impact | Severity |
|-------|--------|----------|
| Claude analyse is UITGESCHAKELD | Geen automatische analyse | 🔴 CRITICAL |
| Handmatige PDF creatie | Vertraging 24-48u | 🔴 HIGH |
| Handmatige email versturen | Risico op vergeten | 🔴 HIGH |
| Nurture moet handmatig getriggerd | POST /nurture/process nodig | 🟡 MEDIUM |
| Geen lead scoring | Geen prioritering | 🟡 MEDIUM |
| Geen fallback bij errors | Lead kan verloren gaan | 🟡 MEDIUM |

### V2 Verbeterde Implementatie

```
Typeform Submit
       │
       ▼
POST /webhook/typeform
       │
       ├─► Parse form data
       │
       ├─► Calculate lead score ──► Hot/Warm/Cold
       │
       ├─► Extract text from file
       │
       ├─► Send confirmation email ──► Immediate
       │
       ├─► Create Pipedrive records
       │
       └─► IF vacancy text > 100 chars:
           │
           └─► START ASYNC THREAD:
               │
               ├─► Claude AI analyse (V8 Enhanced)
               │
               ├─► Generate PDF (PDFMonkey/ReportLab)
               │
               ├─► Add analysis to Pipedrive
               │
               ├─► Send analysis email with PDF
               │
               └─► Trigger nurture sequence
                   └─► FIELD_RAPPORT_VERZONDEN = today
```

#### V2 Verbeteringen

- ✅ Automatische Claude analyse (async)
- ✅ Automatische PDF generatie
- ✅ Automatische email versturen
- ✅ Automatische nurture trigger
- ✅ Lead scoring
- ✅ Retry logic met exponential backoff
- ✅ Error logging met context

---

## PIPEDRIVE CUSTOM FIELDS

### Vereiste Fields (check in Pipedrive)

| Field Key | Doel | Gebruikt in |
|-----------|------|-------------|
| `337f9ccca15334e6e4f937ca5ef0055f13ed0c63` | Rapport Verzonden (datum) | Nurture trigger |
| `22d33c7f119119e178f391a272739c571cf2e29b` | Email Sequence Status | Nurture tracking |
| `753f37a1abc8e161c7982c1379a306b21fae1bab` | Laatste Email | Nurture progress |

### Pipedrive Stage Flow

```
Stage 21: Gekwalificeerd
    │     └─► Actieve nurture emails
    │
    ▼
Stage 22+: Actief Contact
          └─► Nurture gestopt (handmatige opvolging)
```

---

## KRITIEKE GAPS SAMENVATTING

### V1 → V2 Fixes

| Gap | V1 Status | V2 Fix |
|-----|-----------|--------|
| Claude analyse | ❌ Uitgeschakeld | ✅ Async processing |
| PDF generatie | ❌ Handmatig | ✅ Automatisch |
| Email versturen | ❌ Handmatig | ✅ Automatisch |
| Meta lead flow | ❌ Handmatige actie | ✅ Direct Typeform link |
| Lead scoring | ❌ Geen | ✅ Hot/Warm/Cold |
| Error recovery | ❌ Basis | ✅ Retry + fallback |

### Nog Niet Opgelost (TODO)

| Item | Beschrijving | Priority |
|------|-------------|----------|
| Cron job voor nurture | `/nurture/process` moet periodiek draaien | HIGH |
| Email open tracking | Geen engagement data | MEDIUM |
| Unsubscribe handling | Niet geïmplementeerd | MEDIUM |
| A/B testing emails | Niet geïmplementeerd | LOW |

---

## AANBEVELINGEN

### Immediate (voor deployment)

1. **Cron job instellen** voor `/nurture/process`
   - Render.com: Cron Job feature
   - Of: externe service (EasyCron, Pipedream)
   - Frequentie: Dagelijks om 09:00

2. **Test met echte data**
   - Verstuur test Typeform
   - Check Pipedrive record
   - Verify email ontvangst

3. **Monitor eerste week**
   - Check `/health/detailed` dagelijks
   - Review error logs

### Later (na validatie)

1. Email open/click tracking (via SendGrid of Mailgun)
2. Unsubscribe link toevoegen
3. Engagement-based nurture branching

---

## FLOW DIAGRAMS

### Complete V2 Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           LEAD SOURCES                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   ┌──────────────┐      ┌──────────────┐      ┌──────────────┐          │
│   │ Quick        │      │ Typeform     │      │ Meta Lead    │          │
│   │ Analyzer     │      │ Direct       │      │ Ads          │          │
│   │ (Frontend)   │      │              │      │              │          │
│   └──────┬───────┘      └──────┬───────┘      └──────┬───────┘          │
│          │                     │                      │                  │
│          │ Redirect            │ Webhook              │ Webhook          │
│          ▼                     ▼                      ▼                  │
│   ┌──────────────────────────────────────────────────────────────┐      │
│   │                      V2 AUTOMATION ENGINE                      │      │
│   ├──────────────────────────────────────────────────────────────┤      │
│   │                                                                │      │
│   │   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐         │      │
│   │   │ Lead        │   │ Claude      │   │ PDF         │         │      │
│   │   │ Scoring     │   │ Analyzer    │   │ Generator   │         │      │
│   │   └──────┬──────┘   └──────┬──────┘   └──────┬──────┘         │      │
│   │          │                  │                 │                │      │
│   │          ▼                  ▼                 ▼                │      │
│   │   ┌─────────────────────────────────────────────────────┐     │      │
│   │   │              PIPEDRIVE CRM                           │     │      │
│   │   │  Organization → Person → Deal → Notes → Activities   │     │      │
│   │   └─────────────────────────────────────────────────────┘     │      │
│   │                           │                                    │      │
│   │                           ▼                                    │      │
│   │   ┌─────────────────────────────────────────────────────┐     │      │
│   │   │              EMAIL SERVICE                           │     │      │
│   │   │  Confirmation → Analysis → Nurture (8 emails)        │     │      │
│   │   └─────────────────────────────────────────────────────┘     │      │
│   │                                                                │      │
│   └────────────────────────────────────────────────────────────────┘      │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

*Audit voltooid: 2025-12-25*
*Auditor: Claude Code Analysis*
