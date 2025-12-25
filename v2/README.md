# Kandidatentekort V2 - Modular Automation Engine

## Overview

Complete rebuild van de automation backend met verbeterde architectuur, automatische analyse, en lead scoring.

## Verbeteringen t.o.v. V1

| Feature | V1 | V2 |
|---------|----|----|
| Code structuur | 2 files (3200+ regels) | 20+ modulaire files |
| Automatische analyse | Uitgeschakeld | Actief (async) |
| Lead scoring | Geen | Geimplementeerd |
| Meta Lead flow | Alleen welkom email | Direct Typeform link |
| Error handling | Basis | Retry met backoff |
| Email templates | Inline HTML | Aparte modules |

## Project Structuur

```
v2/
├── main.py                 # Flask app entry point
├── config.py              # Alle configuratie
├── handlers/
│   ├── typeform.py        # Typeform webhook
│   ├── meta_lead.py       # Meta/Facebook leads
│   └── manual.py          # Handmatige endpoints
├── services/
│   ├── claude_analyzer.py # AI analyse
│   ├── pipedrive.py       # CRM operaties
│   ├── email_sender.py    # Email verzending
│   ├── pdf_generator.py   # PDF generatie
│   └── lead_scoring.py    # Lead scoring
├── templates/
│   ├── base.py            # Basis email template
│   ├── confirmation.py    # Bevestigingsemail
│   ├── analysis_report.py # Analyse rapport
│   ├── meta_welcome.py    # Meta lead welkom
│   └── pdf_delivery.py    # PDF levering
├── nurture/
│   ├── scheduler.py       # Timing logica
│   ├── processor.py       # Email verzending
│   └── templates.py       # 8 nurture emails
└── utils/
    ├── logging_config.py  # Logging
    ├── retry.py           # Retry decorator
    └── file_extractor.py  # PDF/DOCX extractie
```

## API Endpoints

| Method | Endpoint | Beschrijving |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/health/detailed` | Detailed status |
| POST | `/webhook/typeform` | Typeform submissions |
| POST | `/webhook/meta-lead` | Meta Lead Ads |
| POST | `/update-pdf-urls` | PDF URLs toevoegen |
| POST | `/send-pdf-email` | PDF email versturen |
| POST | `/nurture/process` | Nurture emails verwerken |
| GET | `/test-email` | Email testen |

## Environment Variables

```bash
# Required
ANTHROPIC_API_KEY=       # Claude AI
PIPEDRIVE_API_TOKEN=     # Pipedrive CRM
GMAIL_USER=              # Gmail address
GMAIL_APP_PASSWORD=      # Gmail app password

# Optional
TYPEFORM_API_TOKEN=      # Voor file downloads
PDFMONKEY_API_KEY=       # Professional PDFs
META_VERIFY_TOKEN=       # Facebook webhook
```

## Lokaal Draaien

```bash
cd v2
pip install -r requirements.txt
python -m v2.main
```

## Deployment

1. Push naar Git
2. In Render.com: Update start command naar `python -m v2.main`
3. Check `/health/detailed` endpoint

## Migratie van V1

1. Test V2 endpoints met dezelfde data
2. Update Typeform webhook URL
3. Update Meta Lead Ads webhook URL
4. Verwijder oude V1 files wanneer stabiel

## Flow Diagram

```
Typeform/Meta Lead
        │
        ▼
   Parse Data
        │
        ▼
  Send Confirmation ──────► Email
        │
        ▼
 Create Pipedrive ─────► Org + Person + Deal
        │
        ▼
 Calculate Lead Score ───► Update Deal
        │
        ▼
[If enabled] Async Claude Analysis
        │
        ▼
   Generate PDF
        │
        ▼
 Send Analysis Email
        │
        ▼
 Trigger Nurture ─────► 8 emails over 30 dagen
```
