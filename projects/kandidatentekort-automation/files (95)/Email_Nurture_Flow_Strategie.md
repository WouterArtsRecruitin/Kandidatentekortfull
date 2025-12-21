# kandidatentekort.nl - Complete Email Nurture Flow
## Van Eenmalige Klant naar Terugkerende Subscriber

---

## 📧 OVERZICHT EMAIL FLOW

```
DAG 0: Delivery Email (rapport + documenten)
   │
   ├─► DAG 1: Tip #1 - Quick Wins Implementatie
   │
   ├─► DAG 3: Tip #2 - Doelgroep Targeting + Dashboard Teaser
   │
   ├─► DAG 5: Consult Reminder + Recruitment APK Gratis Aanbod
   │
   ├─► DAG 8: Tip #3 - Labour Market Intelligence Preview
   │
   ├─► DAG 14: Case Study + Begeleiding Pakket Intro
   │
   ├─► DAG 21: Consult LAATSTE KANS (verloopt over 7 dagen)
   │
   └─► DAG 30: Final Value Email + Abonnement Aanbod
```

---

## 📬 DETAIL PER EMAIL

### EMAIL 0: DELIVERY (Dag 0) ✅ [BESTAAND]
**Onderwerp:** Je vacature analyse is klaar! Score: {{score_voor}} → {{score_na}} 🎉
**Doel:** Levering + eerste waarde
**CTA:** Download documenten + Plan gratis consult

---

### EMAIL 1: QUICK WINS (Dag 1)
**Onderwerp:** 3 verbeteringen die je vandaag nog kunt doorvoeren
**Doel:** Directe waarde + engagement

**Inhoud:**
```
Hoi {{voornaam}},

Gisteren ontvingen je je geoptimaliseerde vacature voor {{functie_titel}}.

Om je op weg te helpen, hier de 3 snelste wins die je vandaag nog kunt implementeren:

⚡ QUICK WIN 1: Functietitel aanpassen
Je huidige titel scoorde {{seo_voor}}/10 op vindbaarheid.
→ Wijzig naar: "{{nieuw_functietitel}}"
→ Verwachte impact: +40% meer views

⚡ QUICK WIN 2: Salaris toevoegen
{{#if geen_salaris}}
Je vacature bevat nog geen salarisvermelding.
→ Voeg toe: "€X.XXX - €X.XXX bruto per maand"
→ Verwachte impact: +35% meer sollicitaties
{{else}}
Je salarisindicatie is nu zichtbaar - goed bezig!
{{/if}}

⚡ QUICK WIN 3: Opening aanscherpen
→ Vervang "Wij zoeken..." door een vraag of statement
→ Verwachte impact: +18% click-through rate

📅 Wil je deze tips samen doorlopen?
[PLAN JE GRATIS 15-MIN CONSULT]
(Geldig tot {{consult_vervaldatum}})

Succes!
Team kandidatentekort.nl
```

---

### EMAIL 2: DOELGROEP TARGETING (Dag 3)
**Onderwerp:** Weet jij waar je ideale kandidaat zich bevindt?
**Doel:** Introduce Labour Market Intelligence dashboard

**Inhoud:**
```
Hoi {{voornaam}},

Je vacature voor {{functie_titel}} is geoptimaliseerd. 
Maar weet je ook WIE je probeert te bereiken?

🎯 DOELGROEP INZICHT

Voor {{functie_titel}} in regio {{locatie}} zijn dit de feiten:

• Actief zoekend: ~{{geschatte_kandidaten_actief}} kandidaten
• Passief beschikbaar: ~{{geschatte_kandidaten_passief}} kandidaten  
• Gemiddeld salaris markt: €{{markt_salaris_gem}}
• Meest gebruikte kanalen: {{top_kanalen}}
• Beste dag om te posten: {{beste_dag}}

📊 BINNENKORT: LABOUR MARKET INTELLIGENCE DASHBOARD

Wij werken aan een real-time dashboard waarmee je:
✅ Kandidatenaanbod per regio kunt zien
✅ Salaristrends kunt volgen
✅ Concurrentie-analyse kunt doen
✅ Optimale posting-tijden ontdekt

🔔 Wil je als eerste toegang?
[ZET ME OP DE EARLY ACCESS LIJST]

Of plan eerst je gratis consult:
[PLAN 15-MIN GESPREK]
(Nog {{dagen_tot_verval}} dagen geldig)

Groeten,
Team kandidatentekort.nl
```

---

### EMAIL 3: RECRUITMENT APK AANBOD (Dag 5)
**Onderwerp:** Gratis: Complete check-up van je recruitment proces
**Doel:** Lead generatie voor Recruitment APK

**Inhoud:**
```
Hoi {{voornaam}},

Je vacaturetekst is verbeterd. Maar hoe staat het met de rest van je recruitment proces?

🔧 GRATIS RECRUITMENT APK

Wij bieden nu tijdelijk een gratis "APK-keuring" aan voor je complete recruitment:

Wat we checken:
├─ 📝 Vacatureteksten (✅ al gedaan!)
├─ 🎯 Candidate Journey
├─ ⏱️ Time-to-Hire benchmark
├─ 💰 Cost-per-Hire analyse
├─ 🌐 Employer Branding
└─ 📊 Channel Effectiveness

Resultaat: Een compleet rapport met concrete verbeterpunten en prioritering.

💡 Normaal €299 - Nu GRATIS voor bestaande klanten

[VRAAG JE GRATIS RECRUITMENT APK AAN]

Dit aanbod is geldig tot {{apk_vervaldatum}}.

PS: Nog geen consult gepland? Je hebt nog {{dagen_tot_verval}} dagen:
[PLAN 15-MIN GESPREK]

Team kandidatentekort.nl
```

---

### EMAIL 4: LABOUR MARKET INTELLIGENCE (Dag 8)
**Onderwerp:** 📊 Nieuw: Real-time arbeidsmarkt data voor {{locatie}}
**Doel:** Preview dashboard + waitlist

**Inhoud:**
```
Hoi {{voornaam}},

Wat als je precies kon zien hoeveel kandidaten er beschikbaar zijn voor {{functie_titel}}?

📊 SNEAK PEEK: LABOUR MARKET INTELLIGENCE

[SCREENSHOT/GIF VAN DASHBOARD]

Features die we bouwen:

🔴 LIVE Kandidatentekort Index
Zie per functie en regio hoeveel vraag vs aanbod er is.
→ "{{functie_titel}} in {{locatie}}: 3.2 vacatures per kandidaat"

📈 Salaris Benchmark Tool  
Vergelijk je aanbod met de markt.
→ "Jouw range: {{jouw_salaris}} | Markt mediaan: €{{markt_mediaan}}"

🗺️ Regionale Heatmap
Waar zitten de kandidaten?
→ Visualisatie van talent hotspots

⏰ Timing Optimizer
Wanneer is de beste tijd om te posten?
→ "Voor {{functie_titel}}: Dinsdag 9:00"

🎯 Concurrentie Radar
Hoeveel vergelijkbare vacatures staan er live?
→ "Nu live: 47 vergelijkbare vacatures"

---

🚀 Early Access Pricing (Founding Members)

Normale prijs: €149/maand
Early Access: €79/maand LOCKED IN FOREVER

[CLAIM EARLY ACCESS - BEPERKT BESCHIKBAAR]

Groeten,
Wouter Arts
kandidatentekort.nl
```

---

### EMAIL 5: CASE STUDY + BEGELEIDING (Dag 14)
**Onderwerp:** Hoe [Bedrijf X] 40% sneller aannam met onze begeleiding
**Doel:** Social proof + introduce coaching pakketten

**Inhoud:**
```
Hoi {{voornaam}},

Twee weken geleden optimaliseerden we je vacature. 
Hoe gaat het met de resultaten?

📖 CASE STUDY: [KLANT BEDRIJFSNAAM]

Situatie:
"We zochten al 4 maanden naar een {{vergelijkbare_functie}}. 
Nauwelijks reacties, verkeerde kandidaten..."

Aanpak:
├─ Week 1: Vacature optimalisatie + targeting advies
├─ Week 2: Channel strategie + sourcing ondersteuning  
├─ Week 3-4: Screening support + interview coaching

Resultaat:
├─ 📈 Van 2 naar 23 sollicitaties per week
├─ ⏱️ Time-to-hire: van 16 naar 6 weken
├─ 💰 Bespaard: €8.000 aan bureau fees
└─ ✅ Perfecte match gevonden

---

🎯 NIEUW: RECRUITMENT BEGELEIDING PAKKETTEN

**14-DAGEN SPRINT** - €499
├─ Dagelijkse check-ins
├─ Vacature optimalisatie (onbeperkt)
├─ Sourcing strategie
├─ Kandidaat screening support
└─ Interview vragenlijsten

**30-DAGEN PROGRAMMA** - €899  
Alles uit 14-dagen PLUS:
├─ Employer branding advies
├─ Salary benchmarking
├─ Offer negotiation support
├─ 2x live coaching calls
└─ Templates & tools library

**RETAINER** - €1.499/maand
├─ Onbeperkte support
├─ Dedicated recruitment partner
├─ Alle tools & dashboards
├─ Wekelijkse strategy calls
└─ Priority response (<2 uur)

[BEKIJK ALLE PAKKETTEN]

Of laten we eerst even bellen?
[PLAN GRATIS CONSULT] 
⚠️ Let op: Nog {{dagen_tot_verval}} dagen geldig!

Groeten,
Wouter
```

---

### EMAIL 6: CONSULT URGENCY (Dag 21)
**Onderwerp:** ⏰ Laatste week: Je gratis consult verloopt over 7 dagen
**Doel:** Urgentie creëren voor consult booking

**Inhoud:**
```
Hoi {{voornaam}},

Quick reminder: je gratis 15-minuten consult verloopt over 7 dagen.

📅 Wat we kunnen bespreken:

✅ De resultaten van je {{functie_titel}} vacature tot nu toe
✅ Eventuele obstakels bij het werven
✅ Concrete next steps voor jouw situatie
✅ Of onze begeleiding iets voor je zou zijn

🎁 BONUS als je deze week plant:
Ik stuur je ons "Recruitment Playbook 2025" (normaal €49) 
met 50+ templates, scripts en checklists.

[PLAN NU - LAATSTE PLEKKEN DEZE WEEK]

Na {{consult_vervaldatum}} vervalt dit aanbod automatisch.

Groeten,
Wouter Arts
kandidatentekort.nl

PS: Geen tijd voor een call? Reply op deze email met je 
belangrijkste recruitment uitdaging - ik stuur je gericht advies.
```

---

### EMAIL 7: FINAL VALUE + ABONNEMENT (Dag 30)
**Onderwerp:** 30 dagen later: Hoe nu verder? + Exclusief aanbod
**Doel:** Conversie naar abonnement

**Inhoud:**
```
Hoi {{voornaam}},

Een maand geleden optimaliseerden we je vacature voor {{functie_titel}}.

📊 TERUGBLIK

Je startte met een score van {{score_voor}}/100.
Na onze optimalisatie: {{score_na}}/100 (+{{score_verbetering}} punten)

Ik ben benieuwd: hoe zijn de resultaten tot nu toe?
(Reply gerust met een update!)

---

🚀 KLAAR VOOR DE VOLGENDE STAP?

We hebben 3 manieren om je recruitment naar het volgende niveau te tillen:

**OPTIE 1: LOS BLIJVEN WERKEN**
€29 per vacature optimalisatie
→ Ideaal voor incidenteel werven
[NIEUWE VACATURE AANMELDEN]

**OPTIE 2: RECRUITER ABONNEMENT** ⭐ Populair
€99/maand (of €990/jaar = 2 maanden gratis)
├─ 5 vacatures per maand (€19.80 ipv €29)
├─ 12-uur express levering
├─ Template library (50+ templates)
├─ Priority support
├─ Labour Market Dashboard access
└─ Onbeperkte revisies

[START RECRUITER PLAN]

**OPTIE 3: FULL SERVICE BEGELEIDING**
Vanaf €499 voor 14 dagen
├─ Hands-on recruitment support
├─ Sourcing & screening hulp  
├─ Alle tools & dashboards
├─ Direct contact met Wouter
└─ Garantie op resultaten

[BEKIJK BEGELEIDING OPTIES]

---

🎓 GRATIS BLIJVEN LEREN?

We organiseren maandelijks:
• 📚 Webinars over recruitment trends
• 💬 Q&A sessions met experts
• 📖 Nieuwe templates en guides

[SCHRIJF JE IN VOOR ONZE COMMUNITY]

---

Bedankt voor je vertrouwen in kandidatentekort.nl!

Groeten,
Wouter Arts
Founder, kandidatentekort.nl
Powered by Recruitin

PS: Vragen? Bel me direct: +31 6 XX XXX XXX
of mail naar wouter@recruitin.nl
```

---

## 💰 PRICING MODEL (DEFINITIEF)

### LOSSE DIENSTEN

| Dienst | Prijs | Inclusief |
|--------|-------|-----------|
| Vacature Optimalisatie | €29 | Rapport + verbeterde tekst + tips |
| Rush Delivery (6 uur) | +€15 | Express verwerking |
| Recruitment APK | €299 | Complete proces audit |
| Extra revisieronde | €10 | 1 aanpassing na oplevering |

### ABONNEMENTEN

| Plan | Prijs | Vacatures | Extra's |
|------|-------|-----------|---------|
| **Starter** | €49/maand | 2 | Templates, 24h delivery |
| **Recruiter** ⭐ | €99/maand | 5 | + Dashboard, 12h delivery, priority |
| **Agency** | €299/maand | 15 | + White-label, API, team accounts |
| **Enterprise** | €499/maand | 30 | + Dedicated manager, SLA |

### BEGELEIDING PAKKETTEN

| Pakket | Prijs | Duur | Inclusief |
|--------|-------|------|-----------|
| **Sprint** | €499 | 14 dagen | Optimalisatie + sourcing support |
| **Programma** | €899 | 30 dagen | + Coaching calls + employer branding |
| **Retainer** | €1.499/maand | Doorlopend | Full service recruitment partner |

### ADD-ONS (bij abonnement)

| Add-on | Prijs |
|--------|-------|
| Labour Market Dashboard | €49/maand |
| Doelgroep Analyse | €79/rapport |
| Salary Benchmark Report | €29/functie |
| Webinar/Workshop Seat | €49/sessie |
| Extra vacatures (5-pack) | €79 |

---

## 🎯 COMMUNITY & CONTENT STRATEGIE

### MAANDELIJKSE WEBINARS
- **Week 1:** "Recruitment Trends Update" (gratis)
- **Week 2:** "Deep Dive Workshop" (€49 of gratis voor subscribers)
- **Week 3:** "Q&A met Wouter" (alleen subscribers)
- **Week 4:** "Case Study Sessie" (community)

### COMMUNITY PLATFORM (Toekomst)
- Slack/Discord workspace
- Template sharing
- Peer support
- Job board voor recruiters
- Exclusive early access

---

## 📅 CONSULT GELDIGHEID

**Regel:** Gratis 15-min consult is **maximaal 30 dagen** geldig na aankoop.

**Tracking velden:**
- `aankoop_datum`: Datum van vacature optimalisatie
- `consult_vervaldatum`: aankoop_datum + 30 dagen
- `dagen_tot_verval`: Berekend per email
- `consult_gepland`: Boolean (true/false)
- `consult_verlopen`: Boolean (auto-set na 30 dagen)

**Logica:**
```javascript
if (dagen_tot_verval <= 7 && !consult_gepland) {
  stuur_urgentie_email(); // Email 6
}

if (dagen_tot_verval <= 0 && !consult_gepland) {
  consult_verlopen = true;
  // Geen reminder emails meer
}
```

---

## 🔄 PIPEDRIVE NATIVE AUTOMATION

### WAAROM PIPEDRIVE NATIVE?
- ✅ Geen extra kosten (zit in je Pipedrive plan)
- ✅ Geen Zapier limiet issues
- ✅ Alles in 1 platform
- ✅ Betere tracking (open rates, clicks in Pipedrive)
- ✅ Email templates direct in Pipedrive

---

### SETUP STAPPEN

#### STAP 1: Custom Fields Aanmaken

**Deal Custom Fields:**
```
Veld Naam                | Type        | Opties
-------------------------|-------------|------------------
Rapport Verzonden Op     | Date        | -
Consult Gepland          | Single Option | Ja / Nee / Verlopen
Consult Vervaldatum      | Date        | (auto: +30 dagen)
Email Sequence Status    | Single Option | Actief / Gepauzeerd / Voltooid
Laatste Email Verzonden  | Single Option | Email 0-7
APK Aangevraagd          | Single Option | Ja / Nee
Abonnement Type          | Single Option | Geen / Starter / Recruiter / Agency
```

#### STAP 2: Deal Stages Configureren

```
Pipeline: Kandidatentekort Klanten
├─► Stage 1: Nieuwe Aanvraag
├─► Stage 2: In Analyse
├─► Stage 3: Rapport Verzonden ← TRIGGER VOOR EMAILS
├─► Stage 4: Consult Gepland
├─► Stage 5: APK Aangevraagd
├─► Stage 6: Begeleiding Actief
├─► Stage 7: Abonnement Actief
└─► Stage 8: Afgesloten (Won/Lost)
```

#### STAP 3: Email Templates in Pipedrive

**Settings → Email Templates → Nieuw Template**

Maak templates voor elke email (0-7) met merge fields:
- `{deal.title}` → Functietitel
- `{person.first_name}` → Voornaam
- `{organization.name}` → Bedrijfsnaam
- `{deal.Consult Vervaldatum}` → Custom field
- `{deal.Score Voor}` → Custom field
- `{deal.Score Na}` → Custom field

#### STAP 4: Automations Instellen

**Automation 1: Start Sequence**
```
TRIGGER: Deal moves to "Rapport Verzonden"
ACTIONS:
├─► Set "Rapport Verzonden Op" = Today
├─► Set "Consult Vervaldatum" = Today + 30 days
├─► Set "Email Sequence Status" = "Actief"
├─► Set "Consult Gepland" = "Nee"
├─► Send Email: Template "Email 0 - Delivery"
└─► Set "Laatste Email Verzonden" = "Email 0"
```

**Automation 2: Email 1 - Quick Wins (Dag 1)**
```
TRIGGER: Deal updated
CONDITIONS:
├─► "Email Sequence Status" = "Actief"
├─► "Laatste Email Verzonden" = "Email 0"
├─► "Rapport Verzonden Op" = 1 day ago
ACTIONS:
├─► Send Email: Template "Email 1 - Quick Wins"
└─► Set "Laatste Email Verzonden" = "Email 1"
```

**Automation 3: Email 2 - Doelgroep (Dag 3)**
```
TRIGGER: Deal updated
CONDITIONS:
├─► "Email Sequence Status" = "Actief"
├─► "Laatste Email Verzonden" = "Email 1"
├─► "Rapport Verzonden Op" = 3 days ago
ACTIONS:
├─► Send Email: Template "Email 2 - Doelgroep"
└─► Set "Laatste Email Verzonden" = "Email 2"
```

**Automation 4: Email 3 - APK (Dag 5)**
```
TRIGGER: Deal updated
CONDITIONS:
├─► "Email Sequence Status" = "Actief"
├─► "Laatste Email Verzonden" = "Email 2"
├─► "Rapport Verzonden Op" = 5 days ago
ACTIONS:
├─► Send Email: Template "Email 3 - APK"
└─► Set "Laatste Email Verzonden" = "Email 3"
```

**Automation 5: Email 4 - Dashboard (Dag 8)**
```
TRIGGER: Deal updated
CONDITIONS:
├─► "Email Sequence Status" = "Actief"
├─► "Laatste Email Verzonden" = "Email 3"
├─► "Rapport Verzonden Op" = 8 days ago
ACTIONS:
├─► Send Email: Template "Email 4 - Dashboard"
└─► Set "Laatste Email Verzonden" = "Email 4"
```

**Automation 6: Email 5 - Case Study (Dag 14)**
```
TRIGGER: Deal updated
CONDITIONS:
├─► "Email Sequence Status" = "Actief"
├─► "Laatste Email Verzonden" = "Email 4"
├─► "Rapport Verzonden Op" = 14 days ago
ACTIONS:
├─► Send Email: Template "Email 5 - Case Study"
└─► Set "Laatste Email Verzonden" = "Email 5"
```

**Automation 7: Email 6 - Urgency (Dag 21)**
```
TRIGGER: Deal updated
CONDITIONS:
├─► "Email Sequence Status" = "Actief"
├─► "Laatste Email Verzonden" = "Email 5"
├─► "Rapport Verzonden Op" = 21 days ago
├─► "Consult Gepland" = "Nee" ← BELANGRIJK!
ACTIONS:
├─► Send Email: Template "Email 6 - Urgency"
└─► Set "Laatste Email Verzonden" = "Email 6"
```

**Automation 8: Email 7 - Final (Dag 30)**
```
TRIGGER: Deal updated
CONDITIONS:
├─► "Email Sequence Status" = "Actief"
├─► "Laatste Email Verzonden" = "Email 6" OR "Email 5"
├─► "Rapport Verzonden Op" = 30 days ago
ACTIONS:
├─► Send Email: Template "Email 7 - Final"
├─► Set "Laatste Email Verzonden" = "Email 7"
├─► Set "Email Sequence Status" = "Voltooid"
└─► IF "Consult Gepland" = "Nee" THEN Set = "Verlopen"
```

**Automation 9: Stop bij Consult**
```
TRIGGER: Deal moves to "Consult Gepland"
ACTIONS:
├─► Set "Consult Gepland" = "Ja"
└─► (Sequence gaat door, maar Email 6 wordt geskipt)
```

**Automation 10: Stop bij Abonnement**
```
TRIGGER: "Abonnement Type" changed (not "Geen")
ACTIONS:
├─► Set "Email Sequence Status" = "Voltooid"
└─► Move Deal to "Abonnement Actief"
```

---

### WORKFLOW DIAGRAM (Pipedrive Native)

```
[Typeform] 
    ↓
[Pipedrive Webhook/Zapier 1x] → Create Deal in "Nieuwe Aanvraag"
    ↓
[Manual/Claude API] → Analyse + Rapport genereren
    ↓
[Move to "Rapport Verzonden"] ← TRIGGER
    ↓
┌─────────────────────────────────────────────────┐
│           PIPEDRIVE NATIVE AUTOMATIONS          │
├─────────────────────────────────────────────────┤
│  Dag 0:  Email 0 (Delivery)         ✉️          │
│  Dag 1:  Email 1 (Quick Wins)       ✉️          │
│  Dag 3:  Email 2 (Doelgroep)        ✉️          │
│  Dag 5:  Email 3 (APK)              ✉️          │
│  Dag 8:  Email 4 (Dashboard)        ✉️          │
│  Dag 14: Email 5 (Case Study)       ✉️          │
│  Dag 21: Email 6 (Urgency) *        ✉️          │
│  Dag 30: Email 7 (Final)            ✉️          │
│                                                 │
│  * Alleen als Consult Gepland = Nee             │
└─────────────────────────────────────────────────┘
    ↓
[Deal Stage Updates op basis van acties]
```

---

### TIPS VOOR PIPEDRIVE AUTOMATIONS

**Trigger Type:**
- Gebruik "Deal updated" i.p.v. "Time-based" (Pipedrive heeft geen native delay)
- Check op "dagen geleden" in conditions

**Workaround voor Delays:**
Pipedrive automation checkt elke keer als deal updated wordt.
- Maak een scheduled workflow (via Pipedrive Scheduler add-on)
- Of: gebruik 1 simpele Zapier "Schedule" trigger die dagelijks alle deals checkt

**Alternatief: Pipedrive Campaigns (Email Marketing)**
Als je Pipedrive Campaigns hebt:
- Maak een drip campaign met echte delays
- Koppel aan segment "Stage = Rapport Verzonden"
- Voordeel: Echte email marketing features (open tracking, A/B test)

---

### KOSTEN VERGELIJKING

| Oplossing | Kosten/maand | Emails/maand | Opmerkingen |
|-----------|--------------|--------------|-------------|
| Zapier Pro + Resend | €49 + €20 = €69 | 2000 tasks | Complex, meerdere tools |
| **Pipedrive Native** | €0 (incl.) | Onbeperkt | Simpel, alles in 1 |
| Pipedrive Campaigns | +€13/user | 1000 tracked | Beste tracking |
| Pipedrive + Outfunnel | +€29 | Onbeperkt | Geavanceerde sequences |

---

## ✅ NEXT STEPS

1. [ ] Email templates bouwen in HTML (responsive)
2. [ ] Zapier flow configureren
3. [ ] Pipedrive custom fields toevoegen
4. [ ] Resend templates uploaden
5. [ ] Calendly reminder voor consult verval
6. [ ] Tracking/analytics opzetten
7. [ ] A/B test subject lines

---

*kandidatentekort.nl - Email Nurture Flow v1.0*
*Laatst bijgewerkt: 25 november 2024*
