# Pipeline 14: Corporate Recruiter Vacatures - Complete Automation Workflow

## Overview

| Field | Value |
|-------|-------|
| **Pipeline ID** | 14 |
| **Campagne** | Corporate Recruiter Vacatures (JobDigger leads) |
| **Doelgroep** | HR Directors / Hiring Managers met openstaande recruiter vacature |
| **Doel** | Gesprek → Deal → Plaatsing (€7,990 fee) |
| **Sequence Duration** | 90 dagen |
| **Total Emails** | 7 |
| **Target Reply Rate** | 35% |

---

## Email Sequence Flow

```
DAG 0   ──► EMAIL 1: The Opener (pattern interrupt + vraag)
            │
            ├── REPLY? → Sales handoff → Calendly
            │
DAG 4   ──► EMAIL 2: The Follow-up (case study + methode)
            │
            ├── REPLY? → Sales handoff → Calendly
            │
DAG 11  ──► EMAIL 3: The Value Drop (gratis resource)
            │
            ├── REPLY "JA"? → Stuur checklist → Sales handoff
            │
DAG 18  ──► EMAIL 4: The Social Proof (testimonial)
            │
            ├── REPLY? → Sales handoff → Calendly
            │
DAG 28  ──► EMAIL 5: The Reality Check (kosten berekening)
            │
            ├── REPLY "BELLEN"? → Schedule call
            │
DAG 42  ──► EMAIL 6: The Breakup (laatste kans)
            │
            ├── REPLY "LATER"? → Re-engage dag 90
            │
DAG 90  ──► EMAIL 7: The Resurrection (nieuwe trigger)
            │
            └── REPLY? → Sales handoff → Terug naar begin
```

---

## Expected Metrics

| Email | Open Rate | Reply Rate | Cumulative Replies |
|-------|-----------|------------|-------------------|
| E1 - The Opener | 45% | 8% | 8% |
| E2 - The Follow-up | 50% | 7% | 15% |
| E3 - The Value Drop | 40% | 5% | 20% |
| E4 - The Social Proof | 38% | 4% | 24% |
| E5 - The Reality Check | 35% | 3% | 27% |
| E6 - The Breakup | 45% | 5% | 32% |
| E7 - The Resurrection | 30% | 3% | 35% |

**Target:** 35% reply rate over volledige sequence
**Bij 100 leads:** 35 gesprekken → 10 deals → €79,900 revenue

---

## Pipedrive Pipeline Stages

```
Pipeline: "Recruiter Vacature Outreach" (ID: 14)

Stages:
1.  📥 New Lead (import JobDigger)
2.  📧 Email 1 Sent
3.  📧 Email 2 Sent
4.  📧 Email 3 Sent
5.  📧 Email 4 Sent
6.  📧 Email 5 Sent
7.  📧 Email 6 Sent (Breakup)
8.  💬 Replied - Positive
9.  💬 Replied - Negative
10. 📞 Call Scheduled
11. 🤝 Meeting Done
12. 📝 Proposal Sent
13. ✅ Won
14. ❌ Lost
```

---

## Pipedrive Custom Fields

### Deal Custom Fields

| Field Name | API Key | Type | Options/Format |
|------------|---------|------|----------------|
| Email Sequence Stage | `email_sequence_stage` | Enum | E1, E2, E3, E4, E5, E6, E7, Replied, Stopped |
| Days Open | `days_open` | Number | Auto-calculated |
| Import Date | `import_date` | Date | JobDigger import datum |
| Region | `region` | Enum | Gelderland, Overijssel, Noord-Brabant, Other |
| Last Email Sent | `last_email_sent` | Date | Timestamp |
| Reply Sentiment | `reply_sentiment` | Enum | Positive, Negative, Neutral, None |
| Vacature URL | `vacature_url` | Text | Indeed/LinkedIn link |
| Subject Variant | `subject_variant` | Enum | A, B, C |

### Organization Custom Fields

| Field Name | API Key | Type | Options |
|------------|---------|------|---------|
| Sector | `sector` | Text/Enum | Branche/industrie |
| Region | `address_region` | Text | Regio Nederland |

---

## Pipedrive Variables Mapping

| Template Variable | Pipedrive Field | Description |
|-------------------|-----------------|-------------|
| `{{first_name}}` | `person.first_name` | Voornaam contactpersoon |
| `{{company}}` | `organization.name` | Bedrijfsnaam |
| `{{days_open}}` | `deal.days_open` | Dagen vacature open |
| `{{days_open_updated}}` | Calculated | `days_open + sequence_day` |
| `{{region}}` | `organization.address_region` | Regio (fallback: "Nederland") |
| `{{industry}}` | `organization.sector` | Sector/branche |
| `{{calculated_cost}}` | Calculated | `days_open_updated × 218.67` |

---

## Zapier Automation Flows

### ZAP 1: JobDigger → Pipedrive Import

```yaml
TRIGGER: Webhook (JobDigger nieuwe vacature)
    ↓
ACTION 1: Pipedrive - Create Organization
    - Name: {{company_name}}
    - Address: {{location}}
    - Custom: Region = {{region}}
    ↓
ACTION 2: Pipedrive - Create Person
    - Name: {{contact_name}}
    - Email: {{contact_email}}
    - Organization: {{org_id}}
    ↓
ACTION 3: Pipedrive - Create Deal
    - Title: "Recruiter - {{company_name}}"
    - Value: €7,990
    - Pipeline: 14
    - Stage: "New Lead"
    - Custom Fields:
        - Days Open: {{days_open_from_jobdigger}}
        - Email Sequence Stage: "Pending"
        - Import Date: {{today}}
        - Vacature URL: {{job_url}}
```

### ZAP 2: Email 1 Sender (Daily 9:30 AM)

```yaml
TRIGGER: Schedule - Every day at 9:30 AM (Tue/Wed only)
    ↓
ACTION 1: Pipedrive - Find Deals
    - Filter: Email Sequence Stage = "Pending"
    - Filter: Import Date <= today
    - Limit: 20 per dag (warmup)
    ↓
LOOP: For each deal
    ↓
ACTION 2: Formatter - A/B Test Assignment
    - Random: A (50%) or B (50%)
    ↓
ACTION 3: Gmail - Send Email
    - To: {{person.email}}
    - Subject (A): "{{first_name}}, snelle vraag over jullie recruiter vacature"
    - Subject (B): "Die 45 dagen..."
    - Body: [EMAIL 1 TEMPLATE]
    - From: wouter@recruitin.nl
    ↓
ACTION 4: Pipedrive - Update Deal
    - Email Sequence Stage: "E1"
    - Subject Variant: {{ab_variant}}
    - Last Email Sent: {{now}}
    - Move to Stage: "Email 1 Sent"
```

### ZAP 3: Email 2 Sender (4 dagen na E1)

```yaml
TRIGGER: Schedule - Every day at 9:30 AM (Mon/Tue only)
    ↓
ACTION 1: Pipedrive - Find Deals
    - Filter: Email Sequence Stage = "E1"
    - Filter: Last Email Sent <= today - 4 days
    - Filter: Reply Sentiment = "None"
    ↓
LOOP: For each deal
    ↓
ACTION 2: Gmail - Send Email (as Reply)
    - To: {{person.email}}
    - Subject: Re: {{E1_subject}}
    - Body: [EMAIL 2 TEMPLATE]
    - Thread ID: {{gmail_thread_id}}
    ↓
ACTION 3: Pipedrive - Update Deal
    - Email Sequence Stage: "E2"
    - Last Email Sent: {{now}}
    - Move to Stage: "Email 2 Sent"
```

### ZAP 4: Email 3 Sender (11 dagen na E1)

```yaml
TRIGGER: Schedule - Every day at 9:30 AM (Tue/Wed only)
    ↓
ACTION 1: Pipedrive - Find Deals
    - Filter: Email Sequence Stage = "E2"
    - Filter: Last Email Sent <= today - 7 days
    - Filter: Reply Sentiment = "None"
    ↓
LOOP: For each deal
    ↓
ACTION 2: Gmail - Send Email (as Reply to E1 thread)
    - To: {{person.email}}
    - Subject: Re: {{E1_subject}}
    - Body: [EMAIL 3 TEMPLATE - VALUE DROP]
    - Thread ID: {{gmail_thread_id_E1}}
    ↓
ACTION 3: Pipedrive - Update Deal
    - Email Sequence Stage: "E3"
    - Last Email Sent: {{now}}
    - Move to Stage: "Email 3 Sent"
```

### ZAP 5: Email 4 Sender (18 dagen na E1)

```yaml
TRIGGER: Schedule - Every day at 9:30 AM (Tue/Wed only)
    ↓
ACTION 1: Pipedrive - Find Deals
    - Filter: Email Sequence Stage = "E3"
    - Filter: Last Email Sent <= today - 7 days
    - Filter: Reply Sentiment = "None"
    ↓
LOOP: For each deal
    ↓
ACTION 2: Gmail - Send Email (as Reply to E1 thread)
    - To: {{person.email}}
    - Subject: Re: {{E1_subject}}
    - Body: [EMAIL 4 TEMPLATE - SOCIAL PROOF]
    ↓
ACTION 3: Pipedrive - Update Deal
    - Email Sequence Stage: "E4"
    - Last Email Sent: {{now}}
    - Move to Stage: "Email 4 Sent"
```

### ZAP 6: Email 5 Sender (28 dagen na E1) - NEW THREAD

```yaml
TRIGGER: Schedule - Every day at 9:30 AM (Tue/Wed only)
    ↓
ACTION 1: Pipedrive - Find Deals
    - Filter: Email Sequence Stage = "E4"
    - Filter: Last Email Sent <= today - 10 days
    - Filter: Reply Sentiment = "None"
    ↓
LOOP: For each deal
    ↓
ACTION 2: Formatter - Calculate Cost
    - days_open_updated = days_open + 28
    - calculated_cost = days_open_updated × 218.67
    ↓
ACTION 3: Gmail - Send Email (NEW THREAD)
    - To: {{person.email}}
    - Subject: "{{first_name}}, wat kost jullie lege recruiter stoel?"
    - Body: [EMAIL 5 TEMPLATE - REALITY CHECK]
    ↓
ACTION 4: Pipedrive - Update Deal
    - Email Sequence Stage: "E5"
    - Last Email Sent: {{now}}
    - Move to Stage: "Email 5 Sent"
```

### ZAP 7: Email 6 Sender (42 dagen na E1) - BREAKUP

```yaml
TRIGGER: Schedule - Every day at 9:30 AM (Any weekday)
    ↓
ACTION 1: Pipedrive - Find Deals
    - Filter: Email Sequence Stage = "E5"
    - Filter: Last Email Sent <= today - 14 days
    - Filter: Reply Sentiment = "None"
    ↓
LOOP: For each deal
    ↓
ACTION 2: Gmail - Send Email (Reply to E5 thread)
    - To: {{person.email}}
    - Subject: Re: {{E5_subject}}
    - Body: [EMAIL 6 TEMPLATE - BREAKUP]
    ↓
ACTION 3: Pipedrive - Update Deal
    - Email Sequence Stage: "E6"
    - Last Email Sent: {{now}}
    - Move to Stage: "Email 6 Sent (Breakup)"
```

### ZAP 8: Email 7 Sender (90 dagen na E1) - RESURRECTION

```yaml
TRIGGER: Schedule - Every Monday at 9:30 AM
    ↓
ACTION 1: Pipedrive - Find Deals
    - Filter: Email Sequence Stage = "E6"
    - Filter: Last Email Sent <= today - 48 days
    - Filter: Status != "Won" AND Status != "Lost"
    ↓
LOOP: For each deal
    ↓
ACTION 2: Gmail - Send Email (NEW THREAD)
    - To: {{person.email}}
    - Subject: "{{first_name}}, nog steeds aan het zoeken?"
    - Body: [EMAIL 7 TEMPLATE - RESURRECTION]
    ↓
ACTION 3: Pipedrive - Update Deal
    - Email Sequence Stage: "E7"
    - Last Email Sent: {{now}}
```

### ZAP 9: Reply Handler

```yaml
TRIGGER: Gmail - New Email Matching Search
    - Search: from:(-@recruitin.nl) to:wouter@recruitin.nl subject:(recruiter OR vacature)
    ↓
ACTION 1: Formatter - Extract sender email
    ↓
ACTION 2: Pipedrive - Find Person by Email
    ↓
ACTION 3: Pipedrive - Find Deal by Person
    ↓
ACTION 4: Filter - Check if deal exists
    ↓
ACTION 5: Formatter - Detect trigger words
    - Contains "JA" → Action: Send checklist
    - Contains "BELLEN" → Action: Schedule call
    - Contains "LATER" → Action: Re-engage in 90 days
    - Contains "STOP" → Action: Unsubscribe
    ↓
ACTION 6: Pipedrive - Update Deal
    - Reply Sentiment: "Positive" / "Negative" / "Neutral"
    - Email Sequence Stage: "Replied"
    - Move to Stage: "Replied - Positive" or "Replied - Negative"
    ↓
ACTION 7: Slack - Send Alert
    - Channel: #sales-alerts
    - Message: "Reply van {{person.name}} ({{company}}): {{reply_preview}}"
```

### ZAP 10: Trigger Word Actions

```yaml
TRIGGER: ZAP 9 Output (Trigger word detected)

IF trigger_word = "JA":
    → Send checklist email (prepared PDF)
    → Create Pipedrive activity: "Checklist verzonden"

IF trigger_word = "BELLEN":
    → Send Calendly link
    → Create Pipedrive activity: "Call requested"

IF trigger_word = "LATER":
    → Update deal: Re-engage date = today + 90 days
    → Move to stage: "Replied - Positive"
```

---

## Timing Schedule

| Email | Dag | Wachttijd | Verzenddag | Tijd | Send As |
|-------|-----|-----------|------------|------|---------|
| E1 - Opener | 0 | - | Tue/Wed | 09:30 | New thread |
| E2 - Follow-up | 4 | 4d | Mon/Tue | 09:30 | Reply to E1 |
| E3 - Value Drop | 11 | 7d | Tue/Wed | 09:30 | Reply to E1 |
| E4 - Social Proof | 18 | 7d | Tue/Wed | 09:30 | Reply to E1 |
| E5 - Reality Check | 28 | 10d | Tue/Wed | 09:30 | **New thread** |
| E6 - Breakup | 42 | 14d | Any weekday | 09:30 | Reply to E5 |
| E7 - Resurrection | 90 | 48d | Monday | 09:30 | **New thread** |

**Regel:** Nooit op vrijdag/weekend versturen

---

## Stop Conditions

Stop de sequence automatisch als:

1. **Reply ontvangen** (positive, negative, of neutral)
2. **Bounce** (email niet bezorgd)
3. **Unsubscribe** (reply "stop" of "uitschrijven")
4. **Deal status = Won of Lost**
5. **Manual override** (sales zet "Stopped")

---

## Trigger Words

| Email | Word | Action |
|-------|------|--------|
| E3 | "JA" | Stuur vacature checklist (PDF) |
| E5 | "BELLEN" | Stuur Calendly link |
| E6 | "LATER" | Re-engage na 3 maanden |

---

## Email Warmup Protocol

| Week | Emails/dag |
|------|------------|
| Week 1 | 10 |
| Week 2 | 20 |
| Week 3 | 35 |
| Week 4+ | 50 max |

---

## Domain Health Checklist

- [ ] SPF: `v=spf1 include:_spf.google.com ~all`
- [ ] DKIM: Enabled via Google Workspace
- [ ] DMARC: `v=DMARC1; p=none; rua=mailto:dmarc@recruitin.nl`
- [ ] Custom tracking domain: `track.recruitin.nl`

### Anti-Spam Checklist

- [ ] Geen ALL CAPS in subject
- [ ] Geen excessive punctuation (!!!)
- [ ] Geen spam trigger words (FREE, URGENT, ACT NOW)
- [ ] Text-only emails (geen images in cold outreach)
- [ ] Unsubscribe optie in elke email (PS: reply STOP)
- [ ] Max 2 links per email

---

## Weekly Dashboard Metrics

| Metric | Formula | Target |
|--------|---------|--------|
| Emails sent this week | COUNT(Last Email Sent = this week) | 100 |
| Open rate | Opens / Sent | 45% |
| Reply rate | Replies / Sent | 8% |
| Positive replies | Positive / Total replies | 60% |
| Calls scheduled | Stage = "Call Scheduled" | 10/week |
| Pipeline value | SUM(Deal value in active stages) | €79,900 |

---

## Launch Checklist

### Before Go-Live

- [ ] Pipedrive pipeline 14 created
- [ ] All 14 stages configured
- [ ] Custom fields added (deal + organization)
- [ ] All 10 Zapier zaps built & tested
- [ ] Gmail warmup completed (2+ weeks)
- [ ] SPF/DKIM/DMARC verified
- [ ] Test sequence doorlopen (intern)
- [ ] All 7 email templates in Zapier
- [ ] Slack alerts configured
- [ ] Tracking dashboard ready

### Go-Live (Soft Launch)

- [ ] Import 50 JobDigger leads
- [ ] Start Email 1 op dinsdag
- [ ] Monitor deliverability eerste 48u
- [ ] Check replies dagelijks
- [ ] Adjust subject lines na 50 sends

### Scale-Up (na 1 week)

- [ ] Verhoog naar 100 leads
- [ ] Implement Email 2-7 triggers
- [ ] Weekly reporting starten
- [ ] A/B test resultaten analyseren

---

## Files in this Configuration

```
pipedrive/pipeline-14-corporate-recruiter/
├── pipeline-config.json         # Main pipeline configuration
├── automation-workflow.md       # This documentation
│
├── email-1-opener.html          # Email 1 HTML template
├── email-1-config.json          # Email 1 metadata
│
├── email-2-followup.html        # Email 2 HTML template
├── email-2-config.json          # Email 2 metadata
│
├── email-3-value-drop.html      # Email 3 HTML template
├── email-3-config.json          # Email 3 metadata
│
├── email-4-social-proof.html    # Email 4 HTML template
├── email-4-config.json          # Email 4 metadata
│
├── email-5-reality-check.html   # Email 5 HTML template
├── email-5-config.json          # Email 5 metadata
│
├── email-6-breakup.html         # Email 6 HTML template
├── email-6-config.json          # Email 6 metadata
│
├── email-7-resurrection.html    # Email 7 HTML template
└── email-7-config.json          # Email 7 metadata
```

---

## Quick Reference Card

```
EMAIL 1 (Dag 0)   = Pattern interrupt + vraag         [New thread]
EMAIL 2 (Dag 4)   = Case study + methode              [Reply E1]
EMAIL 3 (Dag 11)  = Value drop (gratis resource)      [Reply E1]
EMAIL 4 (Dag 18)  = Social proof (testimonial)        [Reply E1]
EMAIL 5 (Dag 28)  = Reality check (kosten)            [New thread]
EMAIL 6 (Dag 42)  = Breakup (laatste kans)            [Reply E5]
EMAIL 7 (Dag 90)  = Resurrection (nieuwe trigger)     [New thread]
```

**Golden Rules:**

1. E2/E3/E4 als REPLY op E1 versturen
2. E5 start NIEUWE thread (frisse start na stille periode)
3. E6 als REPLY op E5
4. E7 NIEUWE thread (3 maanden later)
5. Nooit op vrijdag/weekend
6. Stop bij elke reply
7. Max 50 emails/dag
8. Track alles in Pipedrive

---

*Document versie 2.0 | Laatste update: 30 november 2025*
*Gebaseerd op 16.5M cold emails research (Belkins, Reply.io, Lemlist, SalesBread)*
