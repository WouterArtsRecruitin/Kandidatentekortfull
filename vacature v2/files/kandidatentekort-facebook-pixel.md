# FACEBOOK PIXEL SETUP - KANDIDATENTEKORT.NL

## ✅ STAP 3: FACEBOOK PIXEL (30 MIN) - €0.50 CPA! ⭐

**Waarom dit GOUD is:**
- Bezoeker komt, vult niet in, vertrekt
- Zonder pixel = VERLOREN (90% doet dit!)
- Met pixel = RETARGETING ads (€0.50-2 per lead!)

**ROI Example:**
```
100 bezoekers → 2 conversies (2% zonder pixel)
100 bezoekers → 5-8 conversies (5-8% MET retargeting!)

Cost: €50 ad spend
Result: 3-6 extra leads × €29 = €87-174
Profit: €37-124 (74-148% ROI!)
```

---

## STAP 1: MAAK FACEBOOK PIXEL (10 MIN)

### A) Ga naar Meta Events Manager
```
1. Open: https://business.facebook.com/events_manager
2. Klik "Connect Data Sources" → "Web"
3. Kies "Meta Pixel"
4. Geef naam: "Kandidatentekort.nl Pixel"
5. Voer in: kandidatentekort.nl
6. Klik "Continue"
```

### B) Kopieer Pixel ID
```
Je ziet nu: "Pixel ID: 123456789012345"
↑ KOPIEER DIT NUMMER!
```

---

## STAP 2: INSTALLEER PIXEL (10 MIN)

### Optie A: HTML Website

```html
<!-- Plak dit VOOR </head> op ELKE pagina -->
<script>
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', 'JOUW_PIXEL_ID_HIER'); // VERVANG!
fbq('track', 'PageView');
</script>
<noscript>
  <img height="1" width="1" style="display:none"
       src="https://www.facebook.com/tr?id=JOUW_PIXEL_ID_HIER&ev=PageView&noscript=1"/>
</noscript>
```

### Optie B: Next.js

```tsx
// app/components/FacebookPixel.tsx
'use client';

import Script from 'next/script';

export function FacebookPixel() {
  return (
    <>
      <Script 
        id="facebook-pixel"
        strategy="afterInteractive"
        dangerouslySetInnerHTML={{
          __html: `
            !function(f,b,e,v,n,t,s)
            {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
            n.callMethod.apply(n,arguments):n.queue.push(arguments)};
            if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
            n.queue=[];t=b.createElement(e);t.async=!0;
            t.src=v;s=b.getElementsByTagName(e)[0];
            s.parentNode.insertBefore(t,s)}(window, document,'script',
            'https://connect.facebook.net/en_US/fbevents.js');
            fbq('init', 'JOUW_PIXEL_ID_HIER');
            fbq('track', 'PageView');
          `
        }}
      />
      <noscript>
        <img 
          height="1" 
          width="1" 
          style={{ display: 'none' }}
          src="https://www.facebook.com/tr?id=JOUW_PIXEL_ID_HIER&ev=PageView&noscript=1"
        />
      </noscript>
    </>
  );
}

// app/layout.tsx
import { FacebookPixel } from '@/components/FacebookPixel';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <FacebookPixel />
      </body>
    </html>
  );
}
```

---

## STAP 3: TRACK EVENTS (10 MIN)

### Track form submission:

```javascript
// Wanneer iemand formulier indient
function handleFormSubmit() {
  // Track als Lead event
  fbq('track', 'Lead', {
    content_name: 'Vacature Quick Scan',
    value: 29.00,
    currency: 'EUR'
  });
  
  // Jouw normale submit logic
  submitForm();
}
```

### Track als iemand betaalt (€29):

```javascript
// Na succesvolle betaling
function handlePaymentSuccess() {
  fbq('track', 'Purchase', {
    content_name: 'Vacature Analyse Premium',
    value: 29.00,
    currency: 'EUR',
    content_type: 'product'
  });
}
```

---

## STAP 4: VERIFICATIE (5 MIN)

### A) Test met Facebook Pixel Helper

```
1. Installeer Chrome extensie: "Facebook Pixel Helper"
2. Open kandidatentekort.nl
3. Klik op extension icon
4. Zie je groene vinkje + jouw Pixel ID? ✅ WERKT!
```

### B) Check in Events Manager

```
1. Ga terug naar: https://business.facebook.com/events_manager
2. Klik op jouw pixel
3. Zie je "Activity" / events komen binnen? ✅ WERKT!
```

---

## STAP 5: SETUP RETARGETING AD (Bonus - 15 min later)

**Nadat je 50+ bezoekers hebt:**

```
1. Ga naar Meta Ads Manager
2. Create Campaign → "Traffic"
3. Audience → "Custom Audience"
4. Source → "Website"
5. Events:
   - Include: "Page View" (kandidatentekort.nl)
   - Exclude: "Lead" (wie al converted)
   - Time window: Last 30 days
6. Create ad:
   - Headline: "Vergeet je niet iets? 🤔"
   - Text: "Je was bijna klaar met je vacature-analyse. 
           Kom terug en ontdek 5 verbeterpunten in 24 uur!"
   - CTA: "Analyseer Vacature"
7. Budget: €5/dag (test)
8. Run for 7 days
```

**Expected Results:**
```
€35 spend (7 days × €5)
3-7 conversions
CPA: €5-12 per lead
ROI: 140-480% (€29 value)
```

---

## WAT JE NU HEBT:

✅ Facebook Pixel tracking (retargeting capability)
✅ Event tracking (leads + sales)
✅ Audience building (voor ads later)
✅ €0.50-2 CPA via retargeting (vs €20-40 cold traffic!)

**Impact: 90% bezoekers NIET verloren, maar retargetable!** 🎯
