# ACTIEPLAN - Direct Aan Te Pakken

**Datum:** 27 december 2024
**Status:** V2 gebouwd, klaar voor deployment
**Branch:** `claude/improve-automation-leads-JEUsn`

---

## 🚨 FASE 1: VANDAAG (Kritieke fixes)

### Actie 1.1: Test V2 met echte data
**Tijd:** 30 minuten
**Prioriteit:** KRITIEK

```bash
# Start V2 lokaal
cd /home/user/Kandidatentekortfull/v2
python main.py
```

**Test stappen:**
1. [ ] Stuur test Typeform submission naar `/webhook/typeform`
2. [ ] Controleer Pipedrive: Deal aangemaakt?
3. [ ] Controleer email: Bevestiging ontvangen?
4. [ ] Controleer Claude analyse: Draait async?
5. [ ] Controleer PDF: Wordt gegenereerd?

---

### Actie 1.2: Environment variables controleren
**Tijd:** 15 minuten
**Prioriteit:** KRITIEK

Controleer dat alle keys aanwezig zijn:

| Variable | Status | Waar te vinden |
|----------|--------|----------------|
| `ANTHROPIC_API_KEY` | [ ] Check | Anthropic Console |
| `PIPEDRIVE_API_KEY` | [ ] Check | Pipedrive Settings |
| `GMAIL_USER` | [ ] Check | .env bestand |
| `GMAIL_APP_PASSWORD` | [ ] Check | Google Account |
| `PDFMONKEY_API_KEY` | [ ] Check | PDFMonkey Dashboard |

```bash
# Controleer huidige .env
cat .env | grep -E "API_KEY|GMAIL|PDF"
```

---

### Actie 1.3: V2 deployen naar productie
**Tijd:** 20 minuten
**Prioriteit:** HOOG

**Optie A: Render/Railway (aanbevolen)**
```bash
# Push naar main voor auto-deploy
git checkout main
git merge claude/improve-automation-leads-JEUsn
git push origin main
```

**Optie B: Handmatig op server**
```bash
# Upload v2/ folder naar server
# Update webhook URLs in Typeform & Meta
```

---

## ⚡ FASE 2: DEZE WEEK

### Actie 2.1: Webhook URLs updaten
**Tijd:** 10 minuten per platform

| Platform | Huidige URL | Nieuwe URL |
|----------|-------------|------------|
| Typeform | `/webhook` (V1) | `/webhook/typeform` (V2) |
| Meta Lead Ads | `/meta-webhook` (V1) | `/webhook/meta` (V2) |

**Typeform:**
1. [ ] Login op Typeform.com
2. [ ] Ga naar form "Kandidaten Tekort"
3. [ ] Connect → Webhooks
4. [ ] Update URL naar V2 endpoint

**Meta Lead Ads:**
1. [ ] Login op Facebook Business Manager
2. [ ] Events Manager → Lead Ads
3. [ ] Update webhook URL

---

### Actie 2.2: Cron job instellen voor nurture emails
**Tijd:** 10 minuten
**Prioriteit:** HOOG

```bash
# Crontab bewerken
crontab -e

# Voeg toe (dagelijks 09:00):
0 9 * * * curl -X POST https://jouw-domain.com/nurture/process
```

Of via externe service:
- [ ] cron-job.org account aanmaken
- [ ] Nieuwe job: POST naar `/nurture/process`
- [ ] Schedule: Dagelijks 09:00 CET

---

### Actie 2.3: Claude analyse opnieuw activeren
**Tijd:** 5 minuten
**Prioriteit:** KRITIEK

Dit is al gedaan in V2! Controleer alleen:

```python
# v2/config.py
ENABLE_AUTO_ANALYSIS = True  # ✅ Staat aan
```

---

## 📈 FASE 3: VOLGENDE WEEK

### Actie 3.1: Meta Lead flow verbeteren
**Status:** Al gedaan in V2

V2 stuurt nu:
- Directe Typeform link in welcome email
- Pre-filled email en bedrijfsnaam
- Betere call-to-action

**Te doen:**
1. [ ] Monitor conversie Meta Lead → Typeform invulling
2. [ ] A/B test verschillende email onderwerpen

---

### Actie 3.2: Lead scoring dashboard
**Tijd:** 2 uur

Maak simpel dashboard om te zien:
- Hoeveel HOT leads (>30 punten)
- Hoeveel WARM leads (15-30 punten)
- Hoeveel COLD leads (<15 punten)

---

### Actie 3.3: Tracking implementeren
**Tijd:** 1 uur

1. [ ] UTM parameters toevoegen aan alle links
2. [ ] Facebook Pixel events voor conversies
3. [ ] Google Analytics goals instellen

---

## ✅ CHECKLIST VOOR GO-LIVE

```
VOOR DEPLOYMENT:
[ ] V2 lokaal getest met echte Typeform data
[ ] V2 lokaal getest met echte Meta Lead data
[ ] Alle environment variables aanwezig
[ ] Backup V1 bevestigd (lokaal + GitHub)
[ ] Rollback plan klaar

TIJDENS DEPLOYMENT:
[ ] V2 deployen naar productie server
[ ] Webhook URLs updaten in Typeform
[ ] Webhook URLs updaten in Meta
[ ] Cron job instellen voor nurture
[ ] Health check: GET /health/detailed

NA DEPLOYMENT (eerste 24 uur):
[ ] Monitor logs voor errors
[ ] Controleer eerste lead doorloop
[ ] Bevestig emails worden verstuurd
[ ] Bevestig Pipedrive deals correct
```

---

## 🔙 ROLLBACK PLAN

Als V2 problemen geeft:

```bash
# Stap 1: Webhook URLs terugzetten naar V1
# In Typeform: /webhook
# In Meta: /meta-webhook

# Stap 2: V1 code herstellen (indien nodig)
cp -r _backup_v1_20251225_202820/* ./

# Stap 3: V1 herstarten
python kandidatentekort_auto.py
```

---

## 📞 DIRECTE ACTIE NU

**Start hier:**

1. **NU:** Test V2 lokaal met test data
2. **VANDAAG:** Controleer alle API keys
3. **MORGEN:** Deploy V2 + update webhooks
4. **DEZE WEEK:** Monitor en optimaliseer

---

*Laatste update: 27 december 2024*
