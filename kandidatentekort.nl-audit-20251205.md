# Website Audit: kandidatentekort.nl
**Datum:** 2025-12-05
**URL:** https://kandidatentekort.nl

---

## Samenvatting

| Categorie | Score | Status |
|-----------|-------|--------|
| Tracking | 5/10 | :yellow_circle: |
| Performance | 8/10 | :green_circle: |
| SEO | 9/10 | :green_circle: |
| Mobile | 9/10 | :green_circle: |
| Security | 4/10 | :red_circle: |

---

## Tracking Status

| Pixel | Gevonden | ID/Details | Actie Nodig |
|-------|----------|------------|-------------|
| Meta Pixel (index.html) | :white_check_mark: | `517991158551582` | :x: **CONFLICTEREND** |
| Meta Pixel (analytics.ts) | :white_check_mark: | `1735907367288442` | :x: **ANDER ID!** |
| Google Analytics 4 | :white_check_mark: | `G-67PJ02SXVN` | Geen |
| Google Tag Manager | :x: | - | Optioneel |
| LinkedIn Insight | :x: | - | Toevoegen voor B2B |
| Hotjar | :x: | - | Optioneel |
| HubSpot | :x: | - | - |
| Cookiebot | :warning: | `YOUR_COOKIEBOT_CBID` | **NIET GECONFIGUREERD!** |

### KRITIEKE TRACKING ISSUES

#### 1. Dubbele/Conflicterende Meta Pixel IDs
```
index.html:157    → fbq('init', '517991158551582');
analytics.ts:185  → fbq('init', '1735907367288442');
```
**Impact:** Dubbele PageView events, verkeerde attributie, vervuilde data.

#### 2. Cookiebot Niet Geconfigureerd
```html
<!-- index.html:111 -->
data-cbid="YOUR_COOKIEBOT_CBID"
```
**Impact:** Cookie consent werkt NIET. GDPR compliance risico!

---

## Forms & Embeds

| Type | ID | Status |
|------|-----|--------|
| Typeform | `kalFRTCA` | :white_check_mark: Correct geconfigureerd |
| Calendly | `wouter-arts-/vacature-analyse-advies` | :white_check_mark: Aanwezig |

**UTM Tracking:** :white_check_mark: Volledig geïmplementeerd in `analytics.ts`
- Opslaat in localStorage
- Wordt meegegeven aan events
- Server-side tracking via Netlify function

---

## SEO Status

| Element | Waarde | OK? |
|---------|--------|-----|
| Title | "Gratis Vacature Analyse - 40-60% Meer Sollicitaties \| KandidatenTekort.nl" | :white_check_mark: |
| Meta Description | "Upload je vacature en ontvang direct een AI-powered analyse..." (156 chars) | :white_check_mark: |
| Canonical | `https://kandidatentekort.nl/` | :white_check_mark: |
| Robots | `index, follow` | :white_check_mark: |
| Viewport | `width=device-width, initial-scale=1.0` | :white_check_mark: |
| Lang | `nl` | :white_check_mark: |
| OG:Title | :white_check_mark: Aanwezig | :white_check_mark: |
| OG:Description | :white_check_mark: Aanwezig | :white_check_mark: |
| OG:Image | Google Photos CDN (1200x630) | :white_check_mark: |
| Twitter Card | `summary_large_image` | :white_check_mark: |
| Schema.org | Organization + SoftwareApplication | :white_check_mark: |

---

## Security Check

| Check | Status |
|-------|--------|
| HTTPS | :white_check_mark: Geforceerd via canonical |
| Google Consent Mode v2 | :white_check_mark: Correct geïmplementeerd |
| Cookie Consent (Cookiebot) | :red_circle: **NIET ACTIEF** (placeholder ID) |
| SameSite Cookies | :white_check_mark: `SameSite=None;Secure` |
| IP Anonymization | :white_check_mark: `anonymize_ip: true` |
| External Scripts | :warning: 4 externe domains |

### Externe Script Sources
1. `consent.cookiebot.com` - Cookie consent
2. `www.googletagmanager.com` - GA4
3. `connect.facebook.net` - Meta Pixel
4. `embed.typeform.com` - Formulier

---

## Performance

| Aspect | Status | Details |
|--------|--------|---------|
| Preconnect | :white_check_mark: | 4 domains voorgeladen |
| Consent Mode | :white_check_mark: | Blocking tot consent |
| Async Scripts | :white_check_mark: | GA4 + FB async geladen |
| Images | :white_check_mark: | Alleen 1 SVG in public |
| OG Image | :warning: | Externe CDN (Google Photos) |
| Bundle | Vite + React | Modern, tree-shaking |

### Render-Blocking Resources
- Cookiebot (blocking mode) - intentioneel voor consent
- Consent Mode v2 inline script - noodzakelijk

---

## Mobile

| Check | Status |
|-------|--------|
| Viewport Meta | :white_check_mark: |
| Responsive CSS | :white_check_mark: Tailwind CSS |
| iOS Typeform Fix | :white_check_mark: Speciale handling in code |
| Touch Targets | :white_check_mark: Grote buttons (py-4 px-8) |

---

## Top 5 Prioriteiten

### 1. [KRITIEK] Cookiebot Configureren
**File:** `index.html:111`
```html
<!-- VERANDER DIT: -->
data-cbid="YOUR_COOKIEBOT_CBID"
<!-- NAAR JE ECHTE COOKIEBOT ID -->
```
**Risico:** GDPR boetes, consent werkt niet, tracking onbetrouwbaar.

### 2. [KRITIEK] Meta Pixel ID Conflict Oplossen
**Files:** `index.html:157` en `src/lib/analytics.ts:185`
```
index.html:     517991158551582
analytics.ts:   1735907367288442
```
**Actie:** Kies 1 ID en gebruik overal hetzelfde. Verwijder dubbele initialisatie.

### 3. [HOOG] LinkedIn Insight Tag Toevoegen
**Reden:** B2B recruitment doelgroep → LinkedIn ads tracking is essentieel.
```html
<script>
_linkedin_partner_id = "YOUR_PARTNER_ID";
</script>
```

### 4. [MED] Server-side FB CAPI Valideren
**File:** `src/lib/analytics.ts:106`
De Netlify function `track-conversion` wordt aangeroepen maar check of deze correct werkt.

### 5. [LAAG] OG Image naar Eigen Server
**Huidige:** `https://lh3.googleusercontent.com/d/...`
**Risico:** Google kan link breken, langzamere load.
**Fix:** Host op eigen domain of CDN.

---

## Quick Wins (< 30 min)

- [ ] Cookiebot account aanmaken en CBID invullen
- [ ] Meta Pixel ID kiezen en consistent maken
- [ ] Netlify function `track-conversion` testen in logs
- [ ] OG Image Facebook Debugger checken: https://developers.facebook.com/tools/debug/

---

## Development Nodig

- [ ] LinkedIn Insight Tag implementeren (met consent)
- [ ] Google Tag Manager overwegen voor centrale tracking
- [ ] A/B test tracking toevoegen (voor CTA optimalisatie)
- [ ] Server-side CAPI voor alle events (niet alleen conversies)

---

## Ruwe Data

### index.html - Head Section (Tracking)
```html
<!-- Cookiebot - NIET GECONFIGUREERD -->
<script id="Cookiebot" src="https://consent.cookiebot.com/uc.js"
        data-cbid="YOUR_COOKIEBOT_CBID"
        data-blockingmode="auto"
        data-culture="nl"></script>

<!-- GA4 -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-67PJ02SXVN"></script>

<!-- Meta Pixel -->
fbq('init', '517991158551582');
```

### analytics.ts - Dubbele Initialisatie
```typescript
// Lijn 185 - ANDER PIXEL ID!
fbq('init', '1735907367288442');
```

### VacancyAnalyzer.tsx - Typeform
```typescript
const TYPEFORM_ID = "kalFRTCA";  // Correct
```

---

## Conclusie

De website heeft een **sterke SEO en mobile setup**, maar de **tracking is niet betrouwbaar** door:
1. Cookiebot placeholder (geen consent actief)
2. Conflicterende Meta Pixel IDs

**Prioriteit 1:** Fix tracking VOORDAT je geld uitgeeft aan ads. Anders zijn alle data en attributie onbetrouwbaar.
