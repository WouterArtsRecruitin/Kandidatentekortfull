# GOOGLE ANALYTICS 4 SETUP - KANDIDATENTEKORT.NL

## STAP 1: INSTALLATIE (15 MIN)

### Als je Next.js gebruikt:

```bash
# Installeer package
npm install @next/third-parties
```

```typescript
// app/layout.tsx
import { GoogleAnalytics } from '@next/third-parties/google'

export default function RootLayout({ children }) {
  return (
    <html>
      <head>
        {/* Andere head content */}
      </head>
      <body>
        {children}
        <GoogleAnalytics gaId="G-XXXXXXXXXX" /> {/* VERVANG met jouw ID */}
      </body>
    </html>
  )
}
```

### Als je HTML website hebt:

```html
<!-- Plak VOOR </head> in ELKE pagina -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

---

## STAP 2: EVENT TRACKING (5 MIN)

### Track form submission:

```javascript
// Wanneer iemand het formulier indient
function handleFormSubmit() {
  // Jouw normale form logic hier
  
  // Track event
  gtag('event', 'vacature_submitted', {
    'event_category': 'engagement',
    'event_label': 'quick_scan_form'
  });
}
```

### Voeg toe aan je submit button:

```html
<button onclick="handleFormSubmit()">
  Analyseer Mijn Vacature
</button>
```

---

## STAP 3: VERIFICATIE (5 MIN)

1. Upload/deploy je website
2. Open kandidatentekort.nl in browser
3. Open Chrome DevTools (F12)
4. Ga naar "Network" tab
5. Refresh pagina
6. Zoek naar "collect?v=2" requests
7. Zie je ze? ✅ GA4 werkt!

Alternative check:
1. Ga naar https://analytics.google.com
2. Klik "Realtime" in left menu
3. Open kandidatentekort.nl in andere tab
4. Zie je jezelf in Realtime? ✅ Werkt!

---

## WAT JE NU HEBT:

✅ Traffic data (hoeveel bezoekers?)
✅ Bounce rate (gaan ze direct weg?)
✅ Form submissions (hoeveel conversies?)
✅ User flow (welke pagina's bezoeken ze?)

**Dit is GOUD voor optimalisatie!** 🏆
