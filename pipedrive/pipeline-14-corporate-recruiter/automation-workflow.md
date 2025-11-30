# Pipeline 14: Corporate Recruiter Vacatures - Automation Workflow

## Overview

**Pipeline ID:** 14
**Campagne:** Corporate Recruiter Vacatures (JobDigger leads)
**Doelgroep:** HR Directors / Hiring Managers met openstaande recruiter vacature
**Doel:** Gesprek plannen over invulling recruiter positie

---

## Email Sequence Flow

```
JobDigger Lead Import
        ↓
   Pipedrive Deal Created (Pipeline 14)
        ↓
   ┌─────────────────────────────────┐
   │      EMAIL 1: THE OPENER        │
   │  Dinsdag/Woensdag 09:30        │
   │  Subject A/B test               │
   └─────────────────────────────────┘
        ↓
   Wait 4 days (skip weekends)
        ↓
   ┌─────────────────────────────────┐
   │    Check: Reply received?       │
   └─────────────────────────────────┘
        ↓                    ↓
      [YES]                 [NO]
        ↓                    ↓
   Move to "Replied"    ┌─────────────────────────────────┐
   Stage               │     EMAIL 2: THE FOLLOW-UP      │
                       │  Als REPLY op Email 1           │
                       │  Maandag 09:30                  │
                       └─────────────────────────────────┘
                              ↓
                       Wait 3 weeks
                              ↓
                       [No reply = Email 3*]

* Email 3+ templates not yet defined
```

---

## Pipedrive Variables Mapping

| Template Variable | Pipedrive Field | Description |
|-------------------|-----------------|-------------|
| `{{first_name}}` | `person.first_name` | Voornaam contactpersoon |
| `{{company}}` | `organization.name` | Bedrijfsnaam |
| `{{days_open}}` | `deal.custom_field_days_open` | Dagen vacature open |
| `{{region}}` | `organization.address_region` | Regio (fallback: "Nederland") |
| `{{industry}}` | `organization.custom_field_sector` | Sector/branche |
| `{{days_open_plus_4}}` | Calculated | `days_open + 4` |

---

## Zapier/Make Workflow Configuration

### Zap 1: Lead Import + Email 1

**Trigger:** JobDigger webhook / CSV import

**Actions:**
1. Create Pipedrive Deal
   - Pipeline: 14
   - Stage: "New Lead"
   - Title: `{{company}} - Recruiter Vacature`
   - Custom Fields: days_open, region, industry

2. Create/Update Person
   - Name: `{{first_name}} {{last_name}}`
   - Email: `{{email}}`
   - Organization: Link to deal

3. Delay until optimal send time
   - Next Tuesday/Wednesday 09:30 CET

4. Send Email 1
   - Template: `email-1-opener.html`
   - Subject: A/B test variants

5. Update Deal
   - Custom field: `email_1_sent = true`
   - Custom field: `email_1_date = now()`

### Zap 2: Email 2 Follow-up

**Trigger:** Schedule (Daily at 09:30)

**Filter:**
- `email_1_sent = true`
- `email_1_date <= now() - 4 days`
- `reply_received = false`
- Day is Monday, Tuesday, Wednesday, or Thursday

**Actions:**
1. Send Email 2
   - As REPLY to Email 1 thread
   - Template: `email-2-followup.html`

2. Update Deal
   - Custom field: `email_2_sent = true`
   - Custom field: `email_2_date = now()`

### Zap 3: Reply Detection

**Trigger:** Pipedrive Email Reply webhook

**Actions:**
1. Update Deal
   - `reply_received = true`
   - Move to "Replied" stage

2. Create Activity
   - Type: Follow-up call
   - Due: Next business day

---

## Email Subject Line A/B Test Setup

### Variant Distribution (50 leads minimum per variant)

| Variant | Subject Line | Target |
|---------|--------------|--------|
| A | `{{first_name}}, snelle vraag over jullie recruiter vacature` | 33% |
| B | `Recruiter vacature {{company}} - mag ik iets checken?` | 33% |
| C | `Die 45 dagen...` | 33% |

### Winning Criteria
- Minimum sample: 50 sends per variant
- Primary metric: Reply rate
- Secondary metric: Open rate
- Test duration: 2 weeks

---

## Required Pipedrive Custom Fields

Create these custom fields in Pipedrive for Pipeline 14:

### Deal Custom Fields
| Field Name | API Key | Type | Description |
|------------|---------|------|-------------|
| Days Open | `days_open` | Number | Dagen sinds JobDigger posting |
| Email 1 Sent | `email_1_sent` | Boolean | Email 1 verzonden |
| Email 1 Date | `email_1_date` | Date | Datum Email 1 |
| Email 2 Sent | `email_2_sent` | Boolean | Email 2 verzonden |
| Email 2 Date | `email_2_date` | Date | Datum Email 2 |
| Reply Received | `reply_received` | Boolean | Reactie ontvangen |
| Subject Variant | `subject_variant` | Enum (A/B/C) | A/B test variant |

### Organization Custom Fields
| Field Name | API Key | Type | Description |
|------------|---------|------|-------------|
| Sector | `sector` | Text/Enum | Branche/industrie |
| Region | `address_region` | Text | Regio Nederland |

---

## Pipeline Stages

| Stage | API Name | Description |
|-------|----------|-------------|
| 1 | `new_lead` | Nieuwe lead uit JobDigger |
| 2 | `email_1_sent` | Email 1 verzonden |
| 3 | `email_2_sent` | Email 2 verzonden |
| 4 | `replied` | Reactie ontvangen |
| 5 | `meeting_scheduled` | Gesprek gepland |
| 6 | `won` | Klant gewonnen |
| 7 | `lost` | Lead verloren |

---

## Domain Warmup Checklist

Before sending at scale:

- [ ] SPF record configured
- [ ] DKIM signing enabled
- [ ] DMARC policy set
- [ ] Domain age: minimum 2 weeks
- [ ] Warmup schedule: 20-50 emails/day buildup
- [ ] Sender reputation monitoring enabled

---

## Expected Results

| Metric | Benchmark | Expected |
|--------|-----------|----------|
| Email 1 Open Rate | 27-39% | 45%+ |
| Email 1 Reply Rate | 5.1% | 8-12% |
| Email 2 Open Rate | +15% boost | 50%+ |
| Email 2 Reply Rate | +49% vs E1 | 15%+ |
| Combined Reply Rate | - | 20%+ |

---

## Files in this Configuration

```
pipedrive/pipeline-14-corporate-recruiter/
├── pipeline-config.json      # Main pipeline configuration
├── email-1-opener.html       # Email 1 HTML template
├── email-1-config.json       # Email 1 metadata & settings
├── email-2-followup.html     # Email 2 HTML template
├── email-2-config.json       # Email 2 metadata & settings
└── automation-workflow.md    # This documentation
```

---

## Pro Tips

1. **Test eerst op 50 leads** voordat je opschaalt naar 500+
2. **Track opens met pixel** maar vertrouw er niet blind op (Apple Privacy)
3. **Positive reply ≠ sales ready** - kwalificeer in gesprek
4. **Negatieve reply = data** - vraag waarom, leer ervan
5. **No reply na E2** - wacht 3 weken, dan Email 3 (nieuwe waarde)

---

*Gebaseerd op 16.5M cold emails research (Belkins, Reply.io, Lemlist, SalesBread)*
