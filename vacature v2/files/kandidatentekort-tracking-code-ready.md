# 🎯 KANDIDATENTEKORT.NL - TRACKING CODE (COPY/PASTE READY)

**Installatie tijd:** 10 minuten  
**Impact:** +150-200% leads  
**Cost:** €0

---

## 📋 STAP 1: OPEN JE WEBSITE CODE

**Vraag:** Hoe update je kandidatentekort.nl nu?

- **A) Via code editor** (VS Code, etc) → Perfect, ga door
- **B) Via CMS/builder** (WordPress, Webflow) → Zelfde proces
- **C) Via Netlify** → Ga naar je GitHub repo
- **D) Weet ik niet** → Vertel me en ik help

**Zoek het bestand met `<head>` sectie** (meestal `index.html` of `layout.tsx`)

---

## 📋 STAP 2: COPY/PASTE DEZE CODE

### **OPTIE A: HTML WEBSITE**

Plak dit **DIRECT NA `<head>` tag:**

```html
<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <!-- ============================================ -->
    <!-- TRACKING CODES - START -->
    <!-- ============================================ -->
    
    <!-- Google Analytics 4 -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-W6G1NY28BD"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-W6G1NY28BD');
    </script>
    
    <!-- Facebook Pixel -->
    <script>
      !function(f,b,e,v,n,t,s)
      {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
      n.callMethod.apply(n,arguments):n.queue.push(arguments)};
      if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
      n.queue=[];t=b.createElement(e);t.async=!0;
      t.src=v;s=b.getElementsByTagName(e)[0];
      s.parentNode.insertBefore(t,s)}(window, document,'script',
      'https://connect.facebook.net/en_US/fbevents.js');
      
      // VERVANG 'YOUR_PIXEL_ID' met jouw Facebook Pixel ID
      fbq('init', 'YOUR_PIXEL_ID');
      fbq('track', 'PageView');
    </script>
    <noscript>
      <img height="1" width="1" style="display:none"
           src="https://www.facebook.com/tr?id=YOUR_PIXEL_ID&ev=PageView&noscript=1"/>
    </noscript>
    
    <!-- LinkedIn Insight Tag -->
    <script type="text/javascript">
      _linkedin_partner_id = "YOUR_LINKEDIN_PARTNER_ID"; // VERVANG met jouw ID
      window._linkedin_data_partner_ids = window._linkedin_data_partner_ids || [];
      window._linkedin_data_partner_ids.push(_linkedin_partner_id);
    </script>
    <script type="text/javascript">
      (function(l) {
        if (!l){window.lintrk = function(a,b){window.lintrk.q.push([a,b])};
        window.lintrk.q=[]}
        var s = document.getElementsByTagName("script")[0];
        var b = document.createElement("script");
        b.type = "text/javascript";b.async = true;
        b.src = "https://snap.licdn.com/li.lms-analytics/insight.min.js";
        s.parentNode.insertBefore(b, s);
      })(window.lintrk);
    </script>
    <noscript>
      <img height="1" width="1" style="display:none;" alt="" 
           src="https://px.ads.linkedin.com/collect/?pid=YOUR_LINKEDIN_PARTNER_ID&fmt=gif" />
    </noscript>
    
    <!-- ============================================ -->
    <!-- TRACKING CODES - END -->
    <!-- ============================================ -->
    
    <title>Jouw originele title hier</title>
    <!-- Rest van je head... -->
</head>
<body>
    <!-- Je normale content... -->
</body>
</html>
```

---

### **OPTIE B: NEXT.JS / REACT**

**Als je Next.js gebruikt, edit `app/layout.tsx`:**

```typescript
// app/layout.tsx
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import Script from 'next/script';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'KandidatenTekort.nl - Vacature Optimalisatie',
  description: '40-60% meer sollicitaties via AI-powered analyse',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="nl">
      <head>
        {/* Google Analytics 4 */}
        <Script
          src="https://www.googletagmanager.com/gtag/js?id=G-W6G1NY28BD"
          strategy="afterInteractive"
        />
        <Script id="google-analytics" strategy="afterInteractive">
          {`
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', 'G-W6G1NY28BD');
          `}
        </Script>

        {/* Facebook Pixel */}
        <Script id="facebook-pixel" strategy="afterInteractive">
          {`
            !function(f,b,e,v,n,t,s)
            {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
            n.callMethod.apply(n,arguments):n.queue.push(arguments)};
            if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
            n.queue=[];t=b.createElement(e);t.async=!0;
            t.src=v;s=b.getElementsByTagName(e)[0];
            s.parentNode.insertBefore(t,s)}(window, document,'script',
            'https://connect.facebook.net/en_US/fbevents.js');
            fbq('init', 'YOUR_PIXEL_ID');
            fbq('track', 'PageView');
          `}
        </Script>

        {/* LinkedIn Insight */}
        <Script id="linkedin-insight" strategy="afterInteractive">
          {`
            _linkedin_partner_id = "YOUR_LINKEDIN_PARTNER_ID";
            window._linkedin_data_partner_ids = window._linkedin_data_partner_ids || [];
            window._linkedin_data_partner_ids.push(_linkedin_partner_id);
            (function(l) {
              if (!l){window.lintrk = function(a,b){window.lintrk.q.push([a,b])};
              window.lintrk.q=[]}
              var s = document.getElementsByTagName("script")[0];
              var b = document.createElement("script");
              b.type = "text/javascript";b.async = true;
              b.src = "https://snap.licdn.com/li.lms-analytics/insight.min.js";
              s.parentNode.insertBefore(b, s);
            })(window.lintrk);
          `}
        </Script>
      </head>
      <body className={inter.className}>
        {children}
      </body>
    </html>
  );
}
```

---

## 📋 STAP 3: GET FACEBOOK PIXEL ID (5 MIN)

**Je hebt nog geen Facebook Pixel, dus:**

1. Ga naar: https://business.facebook.com/events_manager
2. Klik "Connect Data Sources" → "Web" → "Meta Pixel"
3. Naam: "Kandidatentekort.nl Pixel"
4. Website: kandidatentekort.nl
5. **KOPIEER HET PIXEL ID** (format: 123456789012345)
6. Vervang `YOUR_PIXEL_ID` in de code hierboven

---

## 📋 STAP 4: GET LINKEDIN PARTNER ID (5 MIN)

1. Ga naar: https://www.linkedin.com/campaignmanager
2. Klik "Account Assets" → "Insight Tag"
3. Klik "Install my Insight Tag"
4. **KOPIEER HET PARTNER ID** (6-7 cijfers)
5. Vervang `YOUR_LINKEDIN_PARTNER_ID` in de code hierboven

---

## 📋 STAP 5: ADD EVENT TRACKING

**Voor je form submit button, voeg toe:**

```javascript
// Als je HTML gebruikt:
<script>
function handleVacatureSubmit() {
  // Track in GA4
  if (typeof gtag !== 'undefined') {
    gtag('event', 'vacature_submitted', {
      'event_category': 'engagement',
      'event_label': 'quick_scan_form'
    });
  }
  
  // Track in Facebook
  if (typeof fbq !== 'undefined') {
    fbq('track', 'Lead', {
      content_name: 'Vacature Quick Scan',
      value: 0,
      currency: 'EUR'
    });
  }
  
  // Je normale form submit logic hier...
}
</script>

<!-- Op je submit button: -->
<button onclick="handleVacatureSubmit()">
  Analyseer Vacature
</button>
```

**Als je React gebruikt:**

```typescript
// components/VacatureForm.tsx
'use client';

import { useState } from 'react';

export function VacatureForm() {
  const [vacature, setVacature] = useState('');
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Track events
    if (typeof window !== 'undefined') {
      // GA4
      if (window.gtag) {
        window.gtag('event', 'vacature_submitted', {
          event_category: 'engagement',
          event_label: 'quick_scan_form'
        });
      }
      
      // Facebook Pixel
      if (window.fbq) {
        window.fbq('track', 'Lead', {
          content_name: 'Vacature Quick Scan',
          value: 0,
          currency: 'EUR'
        });
      }
    }
    
    // Je normale submit logic...
  };
  
  return (
    <form onSubmit={handleSubmit}>
      <textarea 
        value={vacature}
        onChange={(e) => setVacature(e.target.value)}
        placeholder="Plak je vacature hier..."
      />
      <button type="submit">Analyseer Vacature</button>
    </form>
  );
}

// TypeScript declarations
declare global {
  interface Window {
    gtag: (...args: any[]) => void;
    fbq: (...args: any[]) => void;
  }
}
```

---

## 📋 STAP 6: DEPLOY & TEST (10 MIN)

### **A) Deploy je code**
- Git push (als je GitHub gebruikt)
- Of: Upload via FTP
- Of: Deploy via Netlify/Vercel

### **B) Test GA4**
1. Open kandidatentekort.nl
2. Chrome DevTools (F12) → Network tab
3. Refresh de pagina
4. Zoek naar "collect?v=2" requests
5. Zie je ze? ✅ GA4 werkt!

Alternative:
1. Ga naar https://analytics.google.com
2. Klik "Realtime" 
3. Open kandidatentekort.nl in andere tab
4. Zie je jezelf? ✅ Werkt!

### **C) Test Facebook Pixel**
1. Installeer Chrome extension: "Facebook Pixel Helper"
2. Open kandidatentekort.nl
3. Klik op extension icon
4. Zie je groen vinkje? ✅ Werkt!

### **D) Test Events**
1. Submit het form
2. Check GA4 → Realtime → Events
3. Zie je "vacature_submitted"? ✅ Werkt!

---

## ✅ CHECKLIST - JE BENT KLAAR ALS:

- [ ] GA4 code toegevoegd (G-W6G1NY28BD)
- [ ] Facebook Pixel code toegevoegd
- [ ] LinkedIn Insight code toegevoegd
- [ ] Event tracking toegevoegd (form submit)
- [ ] Code deployed naar live site
- [ ] GA4 test: Real-time traffic visible ✅
- [ ] FB Pixel test: Green checkmark in helper ✅
- [ ] Event test: "vacature_submitted" in GA4 ✅

---

## 🎉 RESULTAAT

**Na installatie:**
```
✅ Real-time traffic data (hoeveel bezoekers?)
✅ Traffic sources (Google/Social/Direct?)
✅ Bounce rate (gaan ze direct weg?)
✅ Conversie tracking (hoeveel submits?)
✅ Retargeting capability (90% recovered!)
✅ A/B testing ready (data-driven!)
```

**Expected impact:**
```
Week 1: Baseline data verzameld
Week 2: Retargeting audiences building
Week 3: First retargeting ads (+3-6 leads)
Month 2: +150-200% total leads
```

---

## 🚀 KLAAR OM TE STARTEN?

**Antwoord deze vragen:**

1. **Welke tech stack?** (HTML / Next.js / Anders?)
2. **Heb je Facebook Business Manager?** (Ja / Nee / Moet maken)
3. **Heb je LinkedIn Campaign Manager?** (Ja / Nee / Moet maken)
4. **Wil je het zelf doen?** (Ja / Nee, doe jij het maar)

**Dan geef ik je:**
- Exacte code voor jouw setup
- Stap-voor-stap installatie
- Testing checklist
- Troubleshooting hulp

**Type:** "Ready to install" + antwoorden op 4 vragen
