# RecruitmentAPK.nl - Tracking Setup Guide

## ✅ VOLLEDIG GECONFIGUREERD

### Tracking IDs
| Platform | ID | Status |
|----------|-----|--------|
| **Meta Pixel** | `238226887541404` | ✅ Geïnstalleerd |
| **LinkedIn Insight** | `1830706` | ✅ Geïnstalleerd |
| **GA4** | `G-XXXXXXXXXX` | ⚠️ Nog aan te maken |

---

## 📁 Geïmplementeerde bestanden

| Bestand | Functie |
|---------|---------|
| `index.html` | Meta Pixel + LinkedIn + GA4 scripts |
| `src/utils/tracking.ts` | Tracking functies |
| `src/components/CookieConsent.tsx` | GDPR cookie banner |
| `src/App.tsx` | Tracking integration |

---

## 🎯 Event Tracking

### Meta Pixel Events
| Actie | Event | Value |
|-------|-------|-------|
| Page load | PageView | - |
| Assessment start | InitiateCheckout | €45 |
| Assessment klaar | Lead + CompleteRegistration | €45 |
| Rapport download | Purchase | €45 |

### Hoe te gebruiken in code:
```typescript
import { trackAssessmentStart, trackAssessmentComplete } from './utils/tracking';

// Bij start assessment
trackAssessmentStart();

// Bij voltooiing
trackAssessmentComplete({
  company: 'ACME BV',
  industry: 'Manufacturing',
  employees: '50-100',
  score: 72
});
```

---

## 🔧 NOG TE DOEN

### 1. GA4 Property aanmaken
1. Ga naar [analytics.google.com](https://analytics.google.com)
2. Admin → Create Property → "RecruitmentAPK"
3. Kopieer Measurement ID (G-XXXXXXX)
4. Update `index.html` regel 29 en 34
5. Update `src/utils/tracking.ts` regel 16

### 2. Deploy naar Netlify
```bash
cd /Users/wouterarts/.claude-worktrees/Recruitment-APK/stoic-payne
git add .
git commit -m "feat: Meta Pixel 238226887541404 + LinkedIn Insight 1830706"
git push
```

### 3. Test tracking
- Installeer [Facebook Pixel Helper](https://chrome.google.com/webstore/detail/facebook-pixel-helper/)
- Bezoek recruitmentapk.nl
- Check of events correct triggeren

---

## 🔗 Related Meta Credentials

```python
CONFIG = {
    "meta": {
        "pixel_id": "238226887541404",
        "ad_account_id": "act_1443564313411457",
        "app_id": "1735907367288442"
    }
}
```

---

*Laatste update: December 2024*
