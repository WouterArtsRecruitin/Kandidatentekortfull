# Facebook Business Suite - Campagne Configuratie
## Kandidatentekort.nl - Complete Setup Guide

---

## 🔧 STAP 1: ACCOUNT SETUP

### 1.1 Business Manager Instellingen
```
URL: business.facebook.com

Business Account Naam: Kandidatentekort.nl
Business ID: [JE BUSINESS ID]
Tijdzone: Europe/Amsterdam (GMT+1)
Valuta: EUR (€)
```

### 1.2 Pagina's Koppelen
- [ ] Facebook Pagina: Kandidatentekort.nl
- [ ] Instagram Account: @kandidatentekort

### 1.3 Betalingsmethode
- [ ] Creditcard of iDEAL koppelen
- [ ] Factuuradres instellen
- [ ] Bestedingslimiet: €1.500/maand (start)

---

## 📊 STAP 2: META PIXEL INSTALLATIE

### 2.1 Pixel Aanmaken
```
Ga naar: Events Manager > Data Sources > Add > Web

Pixel Naam: Kandidatentekort.nl Pixel
Pixel ID: [WORDT GEGENEREERD]
```

### 2.2 Pixel Code voor Website
```html
<!-- Meta Pixel Code - Plaats in <head> van kandidatentekort.nl -->
<script>
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '[JOUW_PIXEL_ID]');
fbq('track', 'PageView');
</script>
<noscript><img height="1" width="1" style="display:none"
src="https://www.facebook.com/tr?id=[JOUW_PIXEL_ID]&ev=PageView&noscript=1"
/></noscript>
<!-- End Meta Pixel Code -->
```

### 2.3 Conversie Events Instellen
```javascript
// Vacature Analyse Gestart
fbq('track', 'InitiateCheckout', {
  content_name: 'Vacature Analyse',
  content_category: 'Tool Usage'
});

// Vacature Analyse Voltooid
fbq('track', 'Lead', {
  content_name: 'Analyse Completed',
  value: 15.00,
  currency: 'EUR'
});

// Contact Formulier Verzonden
fbq('track', 'Contact', {
  content_name: 'Contact Request'
});

// PDF Rapport Download
fbq('track', 'Purchase', {
  content_name: 'Report Download',
  value: 0.00,
  currency: 'EUR'
});
```

---

## 👥 STAP 3: AUDIENCES CONFIGURATIE

### 3.1 Custom Audience: Website Bezoekers
```
Naam: WEB - Alle Bezoekers 30d
Type: Website Traffic
Bron: Kandidatentekort.nl Pixel

Configuratie:
- Include: All website visitors
- Retention: 30 dagen
- Exclude: People who completed Lead event
```

### 3.2 Custom Audience: Video Viewers
```
Naam: VIDEO - 50% Viewers 14d
Type: Video Engagement
Bron: Facebook/Instagram Videos

Configuratie:
- Include: People who viewed 50% of video
- Videos: [Selecteer alle campagne videos]
- Retention: 14 dagen
```

### 3.3 Custom Audience: Engaged Users
```
Naam: ENGAGED - FB/IG 30d
Type: Page/Profile Engagement
Bron: Facebook Page + Instagram

Configuratie:
- Include: Everyone who engaged
- Actions: Likes, comments, shares, saves, clicks
- Retention: 30 dagen
```

### 3.4 Custom Audience: Leads (Exclude)
```
Naam: CONVERTED - Leads
Type: Website Traffic
Bron: Pixel Events

Configuratie:
- Include: People who completed Lead event
- Retention: 180 dagen
- Gebruik: EXCLUSIE in alle campagnes
```

### 3.5 Lookalike Audiences
```
Lookalike 1:
- Naam: LAL - Website Bezoekers 1%
- Bron: WEB - Alle Bezoekers 30d
- Locatie: Nederland
- Grootte: 1%

Lookalike 2:
- Naam: LAL - Video Viewers 1%
- Bron: VIDEO - 50% Viewers 14d
- Locatie: Nederland
- Grootte: 1%

Lookalike 3:
- Naam: LAL - Leads 1%
- Bron: CONVERTED - Leads
- Locatie: Nederland
- Grootte: 1%
```

### 3.6 Interest-Based Audience (Cold)
```
Naam: INTEREST - HR Professionals NL
Locatie: Nederland
Leeftijd: 25-55
Geslacht: Alle

Interesses (OR):
- Human resources
- Recruitment
- Talent acquisition
- Talent management
- HR management
- LinkedIn Recruiter
- Indeed
- Monsterboard
- Werkenbij

Job Titles (OR):
- HR Manager
- Human Resources Manager
- Recruiter
- Corporate Recruiter
- Talent Acquisition Specialist
- Talent Acquisition Manager
- HR Director
- HR Business Partner
- Personnel Manager
- Recruitment Consultant

Gedrag:
- Small business owners
- Business decision makers

Exclusies:
- CONVERTED - Leads
```

---

## 📢 STAP 4: CAMPAGNE 1 - AWARENESS

### 4.1 Campagne Level
```
Campagne Naam: KT_AWARENESS_COLD_[DATUM]
Objective: Awareness > Reach
Special Ad Categories: None

Budget Type: Daily Budget
Budget: €30/dag

Campaign Budget Optimization: ON
Bid Strategy: Lowest cost
```

### 4.2 Ad Set 1: Interest Targeting
```
Ad Set Naam: AS1_Interest_HR_Professionals

Audience:
- Custom Audience: INTEREST - HR Professionals NL
- Exclusions: CONVERTED - Leads

Placements: Manual
- Facebook Feed ✓
- Instagram Feed ✓
- Instagram Stories ✓
- Instagram Reels ✓
- Facebook Stories ✓

Devices: All
Schedule: Run continuously
Optimization: Reach
```

### 4.3 Ad Set 2: Lookalike
```
Ad Set Naam: AS2_LAL_Website_1pct

Audience:
- Lookalike: LAL - Website Bezoekers 1%
- Exclusions: CONVERTED - Leads, WEB - Alle Bezoekers 30d

Placements: Advantage+ (automatisch)
Optimization: Reach
```

### 4.4 Ads - Awareness Campagne
```
AD 1: Statistiek Stopper
━━━━━━━━━━━━━━━━━━━━━━━
Format: Single Image (1080x1080)
Primary Text:
"83% van alle vacatures scoort onvoldoende op leesbaarheid en aantrekkelijkheid.

Daarom krijg je te weinig (goede) sollicitaties.

✅ Ontdek in 30 seconden hoe jouw vacature scoort
✅ Ontvang direct verbeterpunten
✅ 100% gratis, geen registratie nodig

👉 Scan je vacature nu"

Headline: Gratis Vacature Scan
Description: Ontdek waarom kandidaten afhaken
CTA Button: Learn More
URL: https://kandidatentekort.nl?utm_source=meta&utm_medium=paid&utm_campaign=awareness&utm_content=statistiek

━━━━━━━━━━━━━━━━━━━━━━━

AD 2: Pain Point - Empty Inbox
━━━━━━━━━━━━━━━━━━━━━━━
Format: Single Image (1080x1080)
Primary Text:
"Weer 0 reacties op je vacature? 😩

Je bent niet alleen. De meeste vacatures missen cruciale elementen die kandidaten willen zien.

Wij analyseren je vacature op:
📊 Aantrekkelijkheid
📊 Duidelijkheid
📊 Salaristransparantie
📊 Sollicitatieproces

Binnen 30 seconden weet je wat er mist.

👉 Probeer het gratis"

Headline: Waarom Solliciteert Niemand?
Description: Gratis vacature analyse
CTA Button: Learn More
URL: https://kandidatentekort.nl?utm_source=meta&utm_medium=paid&utm_campaign=awareness&utm_content=painpoint

━━━━━━━━━━━━━━━━━━━━━━━

AD 3: Video - Statistiek
━━━━━━━━━━━━━━━━━━━━━━━
Format: Video (1080x1080 of 9:16)
Video: [InVideo AI generated]
Primary Text:
"Wist je dat 67% van de kandidaten afhaakt bij een onduidelijke vacature?

🎯 Scan je vacature gratis
🎯 Krijg direct verbeterpunten
🎯 Verhoog je response rate

Meer dan 500 HR professionals gingen je voor."

Headline: Gratis Vacature Check
CTA Button: Learn More
Thumbnail: Custom (eerste frame met tekst)
```

---

## 📢 STAP 5: CAMPAGNE 2 - CONSIDERATION

### 5.1 Campagne Level
```
Campagne Naam: KT_CONSIDERATION_WARM_[DATUM]
Objective: Traffic > Link Clicks
Special Ad Categories: None

Budget Type: Daily Budget
Budget: €40/dag

Campaign Budget Optimization: ON
Bid Strategy: Lowest cost per click
```

### 5.2 Ad Set 1: Retargeting Video Viewers
```
Ad Set Naam: AS1_Retarget_VideoViewers

Audience:
- Custom Audience: VIDEO - 50% Viewers 14d
- Exclusions: CONVERTED - Leads

Placements: Manual
- Facebook Feed ✓
- Instagram Feed ✓

Optimization: Link Clicks
```

### 5.3 Ad Set 2: Retargeting Website
```
Ad Set Naam: AS2_Retarget_Website

Audience:
- Custom Audience: WEB - Alle Bezoekers 30d
- Exclusions: CONVERTED - Leads

Placements: Manual
- Facebook Feed ✓
- Instagram Feed ✓

Optimization: Landing Page Views
```

### 5.4 Ads - Consideration Campagne
```
AD 1: Voor/Na Transformatie
━━━━━━━━━━━━━━━━━━━━━━━
Format: Single Image (1080x1080) - Split Screen
Primary Text:
"Van 3 naar 47 sollicitaties.

Dat is wat gebeurt als je vacature wél de juiste informatie bevat.

Links: Een typische vacature ❌
Rechts: Een geoptimaliseerde vacature ✅

Het verschil?
→ Concrete salarisrange
→ Duidelijke doorgroeimogelijkheden
→ Authentieke bedrijfscultuur

Ontdek wat jouw vacature mist 👇"

Headline: Van 3 naar 47 Sollicitaties
Description: Gratis analyse in 30 seconden
CTA Button: Learn More
URL: https://kandidatentekort.nl?utm_source=meta&utm_medium=paid&utm_campaign=consideration&utm_content=voorna

━━━━━━━━━━━━━━━━━━━━━━━

AD 2: Product Demo
━━━━━━━━━━━━━━━━━━━━━━━
Format: Single Image (1080x1080) - Interface Shot
Primary Text:
"Zo werkt onze gratis vacature scanner:

1️⃣ Plak je vacaturetekst
2️⃣ Onze AI analyseert op 5 criteria
3️⃣ Ontvang direct je score + verbeterpunten

✅ Geen registratie nodig
✅ Resultaat binnen 30 seconden
✅ Inclusief geoptimaliseerde versie

Probeer het nu 👇"

Headline: Scan Je Vacature Gratis
Description: Direct resultaat, geen registratie
CTA Button: Try Now
URL: https://kandidatentekort.nl?utm_source=meta&utm_medium=paid&utm_campaign=consideration&utm_content=demo

━━━━━━━━━━━━━━━━━━━━━━━

AD 3: Social Proof / Testimonial
━━━━━━━━━━━━━━━━━━━━━━━
Format: Single Image (1200x628) - Success
Primary Text:
""Van 12 naar 89 sollicitaties in 2 weken. De tool liet precies zien wat er miste: een duidelijke salarisrange en concrete doorgroeimogelijkheden."

- Marieke, HR Manager bij TechBedrijf

🎯 Ontdek wat jouw vacature mist
🎯 Krijg direct actionable feedback
🎯 100% gratis

👉 Start je gratis scan"

Headline: +640% Meer Sollicitaties
Description: Zie hoe Marieke het deed
CTA Button: Learn More
URL: https://kandidatentekort.nl?utm_source=meta&utm_medium=paid&utm_campaign=consideration&utm_content=testimonial
```

---

## 📢 STAP 6: CAMPAGNE 3 - CONVERSION

### 6.1 Campagne Level
```
Campagne Naam: KT_CONVERSION_HOT_[DATUM]
Objective: Leads > Conversions
Conversion Event: Lead (Pixel)

Budget Type: Daily Budget
Budget: €50/dag

Campaign Budget Optimization: ON
Bid Strategy: Cost per result goal
Cost Goal: €15 per lead
```

### 6.2 Ad Set 1: High Intent Visitors
```
Ad Set Naam: AS1_HighIntent_Engaged

Audience:
- Custom Audience: ENGAGED - FB/IG 30d
- AND Custom Audience: WEB - Alle Bezoekers 30d
- Exclusions: CONVERTED - Leads

Placements: Advantage+
Optimization: Conversions (Lead event)
```

### 6.3 Ad Set 2: Lookalike Leads
```
Ad Set Naam: AS2_LAL_Leads

Audience:
- Lookalike: LAL - Leads 1%
- Exclusions: CONVERTED - Leads, WEB - Alle Bezoekers 30d

Placements: Advantage+
Optimization: Conversions (Lead event)
```

### 6.4 Ads - Conversion Campagne
```
AD 1: Urgency / Limited Offer
━━━━━━━━━━━━━━━━━━━━━━━
Format: Single Image (1080x1080)
Primary Text:
"🎁 GRATIS: Complete Vacature Optimalisatie Bundle

Deze week ontvang je bij elke scan:
✅ Uitgebreide analyse op 5 criteria
✅ Geoptimaliseerde vacaturetekst
✅ Nederlandse markt benchmark
✅ Salarisindicatie voor jouw functie

Normaal €97 → Nu GRATIS

Meer dan 500 HR professionals gebruikten deze tool al.

👉 Claim je gratis analyse"

Headline: Gratis Vacature Bundle (t.w.v. €97)
Description: Alleen deze week beschikbaar
CTA Button: Get Offer
URL: https://kandidatentekort.nl?utm_source=meta&utm_medium=paid&utm_campaign=conversion&utm_content=bundle

━━━━━━━━━━━━━━━━━━━━━━━

AD 2: ROI Focus
━━━━━━━━━━━━━━━━━━━━━━━
Format: Single Image (1080x1080)
Primary Text:
"Een verkeerde hire kost gemiddeld €27.500 💸

Dat is:
• 6 maanden salaris
• Onboarding kosten
• Productiviteitsverlies
• Opnieuw werven

De oplossing? Betere vacatures = betere kandidaten.

Onze gratis tool analyseert je vacature en toont exact wat je moet verbeteren om de juiste mensen aan te trekken.

👉 Bespaar duizenden euro's - start gratis"

Headline: Bespaar €27.500 per Hire
Description: Gratis vacature optimalisatie
CTA Button: Learn More
URL: https://kandidatentekort.nl?utm_source=meta&utm_medium=paid&utm_campaign=conversion&utm_content=roi
```

---

## 📋 STAP 7: UTM PARAMETERS

### Standaard UTM Structuur
```
utm_source=meta
utm_medium=paid
utm_campaign=[awareness|consideration|conversion]
utm_content=[ad_naam]
utm_term=[audience_naam]
```

### Volledige URL Voorbeelden
```
Awareness - Statistiek:
https://kandidatentekort.nl?utm_source=meta&utm_medium=paid&utm_campaign=awareness&utm_content=statistiek&utm_term=interest_hr

Consideration - Voor/Na:
https://kandidatentekort.nl?utm_source=meta&utm_medium=paid&utm_campaign=consideration&utm_content=voorna&utm_term=retarget_video

Conversion - Bundle:
https://kandidatentekort.nl?utm_source=meta&utm_medium=paid&utm_campaign=conversion&utm_content=bundle&utm_term=high_intent
```

---

## 📊 STAP 8: REPORTING SETUP

### Custom Columns - Ads Manager
```
Kolommen instellen:
1. Delivery: Reach, Impressions, Frequency
2. Engagement: Link Clicks, CTR (link), CPC
3. Conversions: Leads, Cost per Lead, Lead Rate
4. Video: ThruPlays, Video Views (50%), Video View Rate

Opslaan als: "Kandidatentekort Standard View"
```

### Automated Rules
```
Rule 1: Pause Low Performers
━━━━━━━━━━━━━━━━━━━━━━━
Condition: CTR < 0.5% AND Impressions > 1000
Action: Turn off ad
Check: Every 24 hours

Rule 2: Budget Alert
━━━━━━━━━━━━━━━━━━━━━━━
Condition: Amount Spent > €100 (daily)
Action: Send notification
Check: Every 6 hours

Rule 3: Scale Winners
━━━━━━━━━━━━━━━━━━━━━━━
Condition: Cost per Lead < €10 AND Leads > 5
Action: Increase daily budget by 25%
Max budget: €100/dag
Check: Every 24 hours
```

---

## ✅ LAUNCH CHECKLIST

### Pre-Launch
- [ ] Business Manager account verified
- [ ] Facebook Page gekoppeld
- [ ] Instagram account gekoppeld
- [ ] Betalingsmethode actief
- [ ] Pixel geïnstalleerd en geverifieerd
- [ ] Conversie events testen (Pixel Helper)
- [ ] Alle Custom Audiences aangemaakt
- [ ] Lookalike Audiences aangemaakt
- [ ] Alle afbeeldingen geüpload (1080x1080)
- [ ] Alle video's geüpload
- [ ] Ad copy gecontroleerd op spelling
- [ ] UTM parameters correct
- [ ] Landing page live en snel

### Launch Day
- [ ] Campagne 1 (Awareness) → Active
- [ ] Campagne 2 (Consideration) → Active (of 3 dagen later)
- [ ] Campagne 3 (Conversion) → Active (of 7 dagen later)
- [ ] Spend monitoring ingesteld
- [ ] Team genotificeerd

### Week 1 Monitoring
- [ ] Dagelijkse spend check
- [ ] CTR monitoring (target: >1.5%)
- [ ] CPM monitoring (target: <€8)
- [ ] Frequency check (target: <2.0)
- [ ] Low performers pauzeren
- [ ] Winners identificeren

---

## 💰 BUDGET SAMENVATTING

| Campagne | Dagbudget | Weekbudget | 4-Weken |
|----------|-----------|------------|---------|
| Awareness | €30 | €210 | €840 |
| Consideration | €40 | €280 | €560* |
| Conversion | €50 | €350 | €350* |
| **Totaal** | **€120** | **€840** | **€1.750** |

*Consideration start week 2, Conversion start week 3

---

## 🎯 KPI TARGETS

| Fase | Metric | Target |
|------|--------|--------|
| Awareness | Reach | 30.000+ |
| Awareness | CPM | < €8 |
| Awareness | Video Views 50% | 5.000+ |
| Consideration | Clicks | 1.500+ |
| Consideration | CTR | > 2% |
| Consideration | CPC | < €0.80 |
| Conversion | Leads | 50+ |
| Conversion | CPL | < €15 |
| Conversion | Conv. Rate | > 5% |

---

*Kandidatentekort.nl - Facebook Business Suite Configuratie v1.0*
