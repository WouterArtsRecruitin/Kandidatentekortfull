# Lokaal Testen - Nederlandse Vacature Optimizer

## 🚀 Quick Start

```bash
# 1. Ga naar project directory
cd /Users/wouterarts/nederlandse-vacature-optimizer

# 2. Zet je API key (vervang door echte key)
export CLAUDE_API_KEY="sk-ant-api03-jouw-echte-key-hier"

# 3. Start ontwikkelserver
netlify dev
```

## 🌐 Verwachte Output

```
◐ Starting Netlify Dev with static server
┌─────────────────────────────────────────────────┐
│                                                 │
│   ◈ Server now ready on http://localhost:8888  │
│                                                 │
└─────────────────────────────────────────────────┘
```

**Open browser:** http://localhost:8888

## ✅ Functionaliteit Testen

### 1. Basic Interface
- [ ] Website laadt correct
- [ ] Header en styling werkt
- [ ] Demo buttons klikken (Slechte/Goede/Excellente Vacature)

### 2. API Connectie
- [ ] Voer eigen vacaturetekst in
- [ ] Klik "Analyseer Vacature"  
- [ ] Wacht op echte AI response (30-60 seconden)
- [ ] Controleer of scores realistisch zijn (niet altijd dezelfde)

### 3. Functions Testing
- [ ] Open browser console (F12)
- [ ] Check Network tab bij analyse
- [ ] Zie POST naar `/.netlify/functions/claude-analyze`
- [ ] Status 200 = success

## 🐛 Troubleshooting

### "Functions not found" Error
```bash
# Check functions directory
ls -la netlify/functions/
# Moet claude-analyze.js bevatten
```

### "API Key not found" Error  
```bash
# Controleer environment variable
echo $CLAUDE_API_KEY
# Moet beginnen met: sk-ant-api03-
```

### "CORS" Errors
```bash
# Herstart server met:
netlify dev --port=8888
```

### Port 8888 Bezet
```bash
# Gebruik andere port:
netlify dev --port=3000
```

## 📊 Live API Testing

### Test Vacature (Goed voor Testing):
```
Functie: Senior PHP Developer
Locatie: Amsterdam

Wij zoeken een ervaren PHP developer voor ons team.

Vereisten:
- 5+ jaar PHP ervaring
- Laravel framework kennis
- MySQL database skills

Wij bieden:
- Competitief salaris
- Goede werk-privé balans
- Leuk team
```

### Verwachte AI Response:
- **Score**: 5.5-7.5/10 (variabel)
- **Feedback**: Nederlandse recruitment tips
- **Categorieën**: 5 scores (Aantrekkelijkheid, Duidelijkheid, etc.)
- **Verbeterpunten**: Concrete suggesties

## 🚀 Production Deploy

Als lokaal testen goed werkt:

```bash
# Deploy naar Netlify
netlify deploy --prod

# Of drag & drop naar app.netlify.com
```

**Vergeet niet**: API key ook in Netlify Dashboard environment variables te zetten!

## 🎯 Success Criteria

✅ **Lokaal werkend**: API calls slagen, realistische AI responses
✅ **Geen errors**: Console clean, functions werken  
✅ **Performance**: Analyse binnen 60 seconden
✅ **Nederlandse output**: AI geeft Nederlandse feedback

Nu kun je de tool volledig testen met echte Claude AI! 🇳🇱