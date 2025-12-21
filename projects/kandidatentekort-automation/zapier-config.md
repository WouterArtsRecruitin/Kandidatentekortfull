# Zapier Configuratie - Kandidatentekort.nl Flow

## 📋 OVERZICHT

**Zap naam:** `Kandidatentekort - Vacature Analyse Automation`
**Trigger:** Typeform New Entry
**Stappen:** 7

---

## STEP 1: TRIGGER - Typeform

**App:** Typeform  
**Event:** New Entry  
**Account:** Je Typeform account  
**Form:** `vacature analyse (copy)` (ID: kalFRTCA)

**Test:** Haal een recente submission op om de velden te zien.

---

## STEP 2: Pipedrive - Create Person

**App:** Pipedrive  
**Event:** Create Person  
**Account:** Je Pipedrive account

**Veld mapping:**

| Pipedrive Veld | Typeform Veld |
|----------------|---------------|
| Name | `{{1. First name}} {{1. Last name}}` |
| Email | `{{1. Email}}` (field_MnmHLBESIXfh) |
| Phone | `{{1. Phone number}}` (field_1iZBbbmjqjEO) |
| Organization | `{{1. Company}}` (field_oCk4xgomQr46) |

---

## STEP 3: Pipedrive - Create Deal

**App:** Pipedrive  
**Event:** Create Deal  
**Account:** Je Pipedrive account

**Veld mapping:**

| Pipedrive Veld | Waarde |
|----------------|--------|
| Title | `Vacature Analyse - {{1. Company}}` |
| Pipeline | **vacature analyse** (SELECTEER UIT DROPDOWN!) |
| Stage | Gekwalificeerd (eerste stage) |
| Person | `{{2. Person ID}}` (van Step 2) |
| Value | 0 |

**Custom Fields (indien beschikbaar):**
- Sector: `{{1. In welke technische sector}}`
- Optimalisatiedoel: `{{1. Wat is uw optimalisatiedoel}}`
- Vacature URL: `{{1. Upload je vacaturetekst}}`

---

## STEP 4: Webhooks - GET (Download File)

**App:** Webhooks by Zapier  
**Event:** GET

**URL:** `{{1. Upload je vacaturetekst}}` (field_4RwV7AZV5PIY)

Dit is de Typeform file URL. Zapier download automatisch de content.

**Let op:** Als het een .docx is, krijg je raw text. Voor PDF heb je een extra conversie stap nodig.

---

## STEP 5: Webhooks - POST (Claude API)

**App:** Webhooks by Zapier  
**Event:** Custom Request

**Method:** POST  
**URL:** `https://api.anthropic.com/v1/messages`

**Headers:**
```
Content-Type: application/json
x-api-key: {{JE_ANTHROPIC_API_KEY}}
anthropic-version: 2023-06-01
```

**Body (JSON):**
```json
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 4096,
  "messages": [
    {
      "role": "user",
      "content": "Je bent een expert recruitment copywriter gespecialiseerd in de Nederlandse technische arbeidsmarkt.\n\n## VACATURETEKST:\n\n{{4. Response Body}}\n\n## CONTEXT:\n- Bedrijf: {{1. Company}}\n- Sector: {{1. In welke technische sector}}\n- Doel: {{1. Wat is uw optimalisatiedoel}}\n\n## OPDRACHT:\n\n1. SCORE (1-10) met onderbouwing\n2. TOP 3 VERBETERPUNTEN\n3. VERBETERDE VACATURETEKST (400-600 woorden)\n4. BONUS TIPS (2-3 tips)\n\nSchrijf in het Nederlands."
    }
  ]
}
```

**Response handling:**
- Data: `content[0].text`

---

## STEP 6: Pipedrive - Update Deal

**App:** Pipedrive  
**Event:** Update Deal

**Deal:** `{{3. Deal ID}}` (van Step 3)

**Custom Field (maak aan als niet bestaat):**
- Field naam: `Vacature Analyse Resultaat` (long text)
- Waarde: `{{5. content[0].text}}`

---

## STEP 7: Gmail - Send Email

**App:** Gmail  
**Event:** Send Email

**Veld mapping:**

| Gmail Veld | Waarde |
|------------|--------|
| To | `{{1. Email}}` |
| From | wouter@recruitin.nl |
| Subject | `🎯 Jouw verbeterde vacaturetekst voor {{1. Company}} is klaar!` |
| Body Type | HTML |
| Body | [Plak inhoud van gmail-template.html] |

**Vervang in de HTML template:**
- `{{FIRST_NAME}}` → `{{1. First name}}`
- `{{COMPANY_NAME}}` → `{{1. Company}}`
- `{{SCORE_SECTION}}` → Parse uit `{{5. content[0].text}}`
- `{{IMPROVEMENT_POINTS}}` → Parse uit `{{5. content[0].text}}`
- `{{IMPROVED_TEXT}}` → Parse uit `{{5. content[0].text}}`
- `{{BONUS_TIPS}}` → Parse uit `{{5. content[0].text}}`

**TIP:** Gebruik Formatter by Zapier (Text → Split) om de Claude output te parsen op de headers.

---

## STEP 8: Pipedrive - Update Deal (Stage)

**App:** Pipedrive  
**Event:** Update Deal

**Deal:** `{{3. Deal ID}}`  
**Stage:** `Verstuurd` (of tweede stage in pipeline)

---

## 🔧 EXTRA: Formatter Steps (Optioneel)

Tussen Step 5 en Step 7, voeg Formatter steps toe:

**Formatter 5a: Extract SCORE**
- Transform: Text → Extract Pattern
- Input: `{{5. content[0].text}}`
- Pattern: `SCORE.*?(\d+\/10.*?)(?=TOP 3|$)`

**Formatter 5b: Extract VERBETERPUNTEN**
- Transform: Text → Extract Pattern  
- Input: `{{5. content[0].text}}`
- Pattern: `TOP 3 VERBETERPUNTEN(.*?)(?=VERBETERDE|$)`

**Formatter 5c: Extract VERBETERDE TEKST**
- Transform: Text → Extract Pattern
- Input: `{{5. content[0].text}}`
- Pattern: `VERBETERDE VACATURETEKST(.*?)(?=BONUS|$)`

**Formatter 5d: Extract BONUS TIPS**
- Transform: Text → Extract Pattern
- Input: `{{5. content[0].text}}`
- Pattern: `BONUS TIPS(.*)$`

---

## ✅ TEST CHECKLIST

- [ ] Typeform trigger test gelukt
- [ ] Person aangemaakt in Pipedrive
- [ ] Deal aangemaakt in juiste pipeline (vacature analyse)
- [ ] File content opgehaald
- [ ] Claude API response ontvangen
- [ ] Deal updated met analyse resultaat
- [ ] Email verzonden naar test adres
- [ ] Deal stage updated naar "Verstuurd"

---

## 🚨 TROUBLESHOOTING

**Problem:** Deal komt in verkeerde pipeline
**Fix:** Selecteer pipeline uit dropdown, typ niet handmatig

**Problem:** File content is leeg/onleesbaar
**Fix:** Voeg een "Formatter" step toe om text te cleanen

**Problem:** Claude API error 401
**Fix:** Check API key in header (x-api-key)

**Problem:** Gmail HTML niet correct
**Fix:** Zet Body Type op "HTML", niet "Plain"

---

## 💰 KOSTEN

| Component | Kosten/maand (100 leads) |
|-----------|--------------------------|
| Zapier | Gratis (< 100 tasks) of €19 |
| Claude API | ~€5 (€0.05 × 100) |
| Gmail | Gratis |
| **Totaal** | **€5-24/maand** |

---

## 📞 SUPPORT

Vragen? 
- WhatsApp: https://wa.me/31614314593
- Email: wouter@recruitin.nl
