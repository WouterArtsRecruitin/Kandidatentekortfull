# Test Checklist - Nederlandse Vacature Optimizer
**✅ Complete Testing Guide voor Live Site**

## 🌐 Site URL: https://admirable-syrniki-edef2f.netlify.app/

## 1️⃣ Basic Functionality Test (2 minuten)

### Homepage Loading:
- [ ] Site laadt zonder errors
- [ ] Hero section zichtbaar met animaties
- [ ] Nederlandse teksten correct weergegeven
- [ ] Responsive op mobile (test op telefoon)

### Interface Elements:
- [ ] 3 demo buttons zichtbaar (Slecht/Goed/Excellent)
- [ ] Textarea voor vacature input werkt
- [ ] Character counter update bij typen (max 5000)
- [ ] "Analyseer Vacature" button klikbaar

---

## 2️⃣ Demo Vacatures Test (3 minuten)

### Test Elke Demo Button:

**1. Slechte Vacature (Score ~3.2/10)**
- [ ] Klik "Slechte Vacature" button
- [ ] Vacature tekst verschijnt in textarea
- [ ] Character count update

**2. Goede Vacature (Score ~6.8/10)**  
- [ ] Klik "Goede Vacature" button
- [ ] Andere tekst verschijnt
- [ ] Smooth transition

**3. Excellente Vacature (Score ~9.2/10)**
- [ ] Klik "Excellente Vacature" button
- [ ] Premium vacature tekst laadt
- [ ] Alle demo's werken smooth

---

## 3️⃣ AI Analysis Test (5 minuten)

### Test met Eigen Vacature:
```
Functie: Senior Developer
Locatie: Amsterdam

Wij zoeken een developer met ervaring.

Vereisten:
- 5 jaar ervaring
- Java kennis

Wat wij bieden:
- Salaris
- Laptop
```

### Verwacht Resultaat MET API Key:
- [ ] "Analyseren..." loading state (30-60 sec)
- [ ] **Unieke score** (niet altijd dezelfde)
- [ ] **Nederlandse feedback** specifiek voor jouw tekst
- [ ] **5 categorieën** met individuele scores
- [ ] **Concrete verbeterpunten** (variabel per analyse)

### Resultaat ZONDER API Key (Mock Mode):
- [ ] Vaste score: 7.2/10
- [ ] Standaard demo feedback
- [ ] Altijd dezelfde tips

---

## 4️⃣ Advanced Features Test (3 minuten)

### Progress Indicators:
- [ ] Loading animatie tijdens analyse
- [ ] Smooth progress bar
- [ ] Duidelijke status updates

### Results Display:
- [ ] Overall score prominent getoond
- [ ] 5 categorie scores (Aantrekkelijkheid, etc.)
- [ ] Progress bars animeren
- [ ] Improvement tips leesbaar

### Error Handling:
- [ ] Test met lege vacature → error message
- [ ] Test met 5000+ characters → limit warning
- [ ] API timeout → fallback naar mock data

---

## 5️⃣ Performance & Browser Test (2 minuten)

### Browser Compatibility:
- [ ] Chrome/Edge - volledig functioneel
- [ ] Safari - check animations
- [ ] Mobile browsers - responsive design

### Performance Checks:
- [ ] Page load < 3 seconden
- [ ] Smooth animations (60fps)
- [ ] No console errors (F12 → Console)
- [ ] API calls succesvol (F12 → Network)

---

## 🎯 API Key Verificatie

### Check of API Key Werkt:
1. Open browser console (F12)
2. Analyseer een vacature
3. Kijk in Network tab voor:
   ```
   POST /.netlify/functions/claude-analyze
   Status: 200 OK
   Response: Unique AI-generated content
   ```

### Signs API Key is Working:
- ✅ Verschillende scores per analyse
- ✅ Specifieke feedback op jouw tekst
- ✅ Nederlandse context in tips
- ✅ Analyse duurt 30-60 seconden

### Signs Using Mock Data:
- ⚠️ Altijd score 7.2/10
- ⚠️ Zelfde feedback elke keer
- ⚠️ Instant resultaat (geen delay)
- ⚠️ Generic improvement tips

---

## 🐛 Troubleshooting

### Site Laadt Niet:
- Check Netlify deploy status
- Clear browser cache (Ctrl+F5)
- Probeer incognito window

### API Errors:
- Verify environment variable in Netlify
- Check API key format (sk-ant-...)
- Monitor Anthropic usage dashboard

### Trage Performance:
- Normal: 30-60 sec voor AI analyse
- Te traag: Check network speed
- Timeout: Retry of check API status

---

## ✅ Test Geslaagd Als:

1. **Basic UI** - Alle buttons en interface werken
2. **Demo Content** - 3 demo vacatures laden correct
3. **AI Analysis** - Echte, unieke feedback per vacature
4. **Nederlandse Output** - Professionele NL recruitment tips
5. **Error Handling** - Graceful omgang met edge cases
6. **Performance** - Snelle, smooth experience

## 🚀 Volgende Stappen:

Als alles werkt:
1. **Share URL** voor feedback
2. **Monitor usage** in Anthropic console
3. **Generate design assets** met Leonardo AI
4. **Create marketing materials** in Canva
5. **Plan launch** strategie

**Test Status:** ⏳ Wachtend op "Published" status...

Laat me weten zodra de site live is! 🎉