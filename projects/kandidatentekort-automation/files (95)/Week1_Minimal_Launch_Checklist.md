# 🚀 KANDIDATENTEKORT.NL - WEEK 1 MINIMAL VIABLE LAUNCH

## A) EERSTE AD + TYPEFORM FLOW

---

### 📱 META AD (Facebook/Instagram)

**Ad Format:** Single Image of Carousel
**Objective:** Lead Generation
**Budget:** €20-50/dag (start laag, schaal op bij resultaat)

**COPY OPTIE 1 (Direct/Problem-focused):**
```
🔴 Vacature online, maar geen reacties?

Je bent niet alleen. 73% van de technische vacatures 
krijgt te weinig sollicitaties door suboptimale teksten.

✅ Wij analyseren je vacature gratis
✅ Je ontvangt concrete verbeterpunten
✅ Gemiddeld +40% meer sollicitaties

📩 Upload je vacature → Rapport binnen 24 uur

[ANALYSEER MIJN VACATURE - GRATIS]
```

**COPY OPTIE 2 (Curiosity/Score-focused):**
```
Wat scoort jouw vacaturetekst? 🤔

De meeste vacatures scoren tussen 40-60/100 
op vindbaarheid, inclusiviteit en conversie.

Ontdek jouw score + verbeterpunten:
✅ Gratis analyse
✅ Binnen 24 uur
✅ Concrete tips

[ONTDEK MIJN SCORE →]
```

**COPY OPTIE 3 (Social Proof):**
```
"Van 3 naar 23 sollicitaties per week" 💬

Dat was het resultaat na onze vacature-optimalisatie.

Benieuwd wat wij voor jouw vacature kunnen betekenen?

🎁 Gratis analyse (normaal €29)
⏰ Rapport binnen 24 uur
📈 Gemiddeld +40% meer reacties

[CLAIM JE GRATIS ANALYSE]
```

---

### 🖼️ AD VISUAL (Canva template suggestie)

**Formaat:** 1080x1080px (square) of 1080x1350px (portrait)

**Design:**
```
┌─────────────────────────────────┐
│                                 │
│   [Recruitin logo klein]        │
│                                 │
│   ╔═══════════════════════════╗ │
│   ║                           ║ │
│   ║   VACATURE SCORE:         ║ │
│   ║                           ║ │
│   ║      47 → 87              ║ │
│   ║      ──────────           ║ │
│   ║   🔴 voor   🟢 na         ║ │
│   ║                           ║ │
│   ╚═══════════════════════════╝ │
│                                 │
│   "Ontdek jouw score"           │
│                                 │
│   ✅ Gratis analyse             │
│   ✅ Binnen 24 uur              │
│                                 │
│   kandidatentekort.nl           │
│                                 │
└─────────────────────────────────┘
```

**Kleuren:**
- Background: #2C3E50 (dark blue) of wit
- Accent: #FF6B35 (Recruitin orange)
- Score voor: #DC2626 (rood)
- Score na: #10B981 (groen)

---

### 🔗 TYPEFORM FLOW

**Jouw Typeform:** https://form.typeform.com/to/z1GroMCc

**Gewenste velden (check of je deze hebt):**

| Veld | Type | Verplicht | Waarom |
|------|------|-----------|--------|
| Vacaturetekst | Long text | ✅ Ja | Core input |
| Functietitel | Short text | ✅ Ja | Voor rapport |
| Bedrijfsnaam | Short text | ❌ Nee | Nice to have |
| Voornaam | Short text | ✅ Ja | Personalisatie |
| Email | Email | ✅ Ja | Delivery |
| Telefoon | Phone | ❌ Nee | Follow-up (optioneel) |

**Typeform → Pipedrive koppeling:**
1. Typeform native Pipedrive integratie (Settings → Connect → Pipedrive)
2. Of: Zapier (1 zap: Typeform → Pipedrive Create Deal)

---

### 📊 TRACKING SETUP

**UTM Parameters voor ad:**
```
?utm_source=facebook
&utm_medium=paid
&utm_campaign=vacature-analyse-gratis
&utm_content=score-visual-v1
```

**Facebook Pixel Events:**
1. PageView (automatisch)
2. Lead (bij Typeform submit - via Typeform tracking)
3. Purchase (later, bij betaling)

**Typeform Tracking:**
- Typeform heeft native FB Pixel integratie
- Settings → Tracking → Facebook Pixel ID invoeren

---

## B) HANDMATIGE WEEK 1 CHECKLIST

### 📋 PER KLANT - HANDMATIGE FLOW

**Wanneer:** Elke keer dat een Typeform binnenkomt

---

#### STAP 1: INTAKE (5 min)
```
□ Check Pipedrive voor nieuwe deal
□ Open Typeform response
□ Kopieer vacaturetekst naar werkdocument
□ Noteer: functietitel, bedrijf, email, voornaam
```

#### STAP 2: ANALYSE (15 min)
```
□ Open Claude (chat of API)
□ Plak vacaturetekst + analyseprompt (zie onder)
□ Genereer rapport
□ Review output op kwaliteit
□ Pas aan indien nodig
```

**Analyseprompt:**
```
Analyseer deze Nederlandse vacaturetekst en geef:

1. SCORE (0-100) op:
   - Vindbaarheid/SEO
   - Inclusiviteit
   - Conversie/aantrekkelijkheid
   - Totaalscore

2. TOP 3 VERBETERPUNTEN met concrete suggesties

3. HERSCHREVEN VERSIE van de vacature

4. 3 QUICK WINS die direct te implementeren zijn

Vacaturetekst:
"""
[PLAK HIER]
"""

Functie: [FUNCTIETITEL]
Bedrijf: [BEDRIJFSNAAM]
```

#### STAP 3: RAPPORT MAKEN (10 min)
```
□ Open rapport template (v2_Executive_Summary)
□ Vul scores in
□ Vul verbeterpunten in
□ Kopieer herschreven vacature
□ Exporteer als PDF
□ Sla op in Google Drive (map per klant)
```

#### STAP 4: DELIVERY (5 min)
```
□ Open email template
□ Personaliseer (voornaam, functietitel, scores)
□ Attach PDF rapport
□ Verstuur email
□ Update Pipedrive: Stage → "Rapport Verzonden"
□ Set reminder: Follow-up over 2 dagen
```

#### STAP 5: FOLLOW-UP (dag 2-3)
```
□ Check of email geopend is (Pipedrive tracking)
□ Geen reactie? Stuur reminder:
   "Hoi [naam], heb je het rapport kunnen bekijken? 
    Eventuele vragen? Je kunt ook een gratis 
    15-min call plannen: [Calendly link]"
□ Update Pipedrive notities
```

---

### 📧 EMAIL TEMPLATES (Handmatig)

**Email 1: Delivery**
```
Onderwerp: Je vacature analyse is klaar! Score: [X] → [Y] 🎉

Hoi [voornaam],

Goed nieuws! Je vacature voor [functietitel] is geanalyseerd.

📊 Resultaat:
• Originele score: [score_voor]/100
• Na optimalisatie: [score_na]/100
• Verbetering: +[verschil] punten

📎 In de bijlage vind je:
• Executive Summary met alle scores
• Concrete verbeterpunten
• Herschreven vacaturetekst

⚡ Top 3 quick wins:
1. [tip 1]
2. [tip 2]
3. [tip 3]

📅 Wil je de resultaten samen doorlopen?
Plan een gratis 15-min call: [CALENDLY LINK]
(Geldig tot [datum +30 dagen])

Succes met werven!

Groeten,
Wouter Arts
kandidatentekort.nl
```

**Email 2: Follow-up (dag 2-3)**
```
Onderwerp: Heb je het rapport kunnen bekijken?

Hoi [voornaam],

Even een snelle check-in over je vacature analyse.

Heb je het rapport kunnen bekijken? 
Eventuele vragen of onduidelijkheden?

💡 Tip: De 3 quick wins kun je vandaag nog doorvoeren 
voor direct resultaat.

📅 Liever even sparren? Plan een gratis call:
[CALENDLY LINK]

Groeten,
Wouter
```

---

### ⏱️ TIJDSINVESTERING PER KLANT

| Stap | Tijd | Totaal |
|------|------|--------|
| Intake | 5 min | 5 min |
| Analyse | 15 min | 20 min |
| Rapport | 10 min | 30 min |
| Email | 5 min | 35 min |
| Follow-up | 5 min | 40 min |

**Per klant: ~40 minuten**

Bij 5 klanten/dag = 3-4 uur werk
Bij €29/klant = €145/dag = **€36/uur**

---

### 📈 WEEK 1 TARGETS

| Dag | Doel | Actie |
|-----|------|-------|
| Ma | Ad live | Setup Meta ad + Typeform check |
| Di | 2-3 leads | Verwerk handmatig |
| Wo | 2-3 leads | Verwerk + eerste follow-ups |
| Do | 2-3 leads | Optimaliseer ad indien nodig |
| Vr | 2-3 leads | Eerste consult calls? |
| Za-Zo | Review | Wat werkt? Wat niet? |

**Week 1 doel: 10-15 klanten handmatig**

---

### 🎯 WAT JE LEERT IN WEEK 1

Na 10+ klanten weet je:

1. **Pricing:** Is €29 te laag/hoog? Vraagt iemand om meer?
2. **Conversie:** Hoeveel % van ad clicks wordt lead?
3. **Kwaliteit:** Zijn klanten tevreden met rapport?
4. **Upsell:** Vraagt iemand om consult/APK/begeleiding?
5. **Tijd:** Hoelang duurt het echt per klant?
6. **Pijnpunten:** Wat kost de meeste tijd?

---

### ✅ VANDAAG DOEN

```
□ 1. Check Typeform (https://form.typeform.com/to/z1GroMCc)
     - Heeft alle velden?
     - Pipedrive integratie aan?
     - FB Pixel tracking aan?

□ 2. Maak Meta ad
     - Kies 1 copy variant
     - Maak visual in Canva
     - Zet ad live met €20/dag budget

□ 3. Bereid templates voor
     - Email templates in Gmail drafts
     - Rapport template ready
     - Claude prompt saved

□ 4. Test volledige flow zelf
     - Vul Typeform in als test
     - Check of Pipedrive deal aankomt
     - Maak 1 test rapport
     - Stuur test email

□ 5. Go live!
```

---

### 🆘 ALS HET NIET WERKT

**Geen leads na 2 dagen:**
- Check ad: wordt hij vertoond? (Ads Manager)
- Check targeting: te breed/smal?
- Check visual: scroll-stopping?
- Test andere copy variant

**Leads maar geen opens:**
- Check spam folder
- Onderwerpregel A/B testen
- Verzendtijd aanpassen (9:00 of 14:00)

**Veel vragen/support:**
- FAQ maken
- Rapport verduidelijken
- Video walkthrough overwegen

---

*Succes! Start simpel, leer snel, schaal daarna.* 🚀
