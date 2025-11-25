# Claude API Key Setup Guide
**Nederlandse Vacature Optimizer - API Configuration**

## 🔑 Anthropic Claude API Key Krijgen

### Stap 1: Account Aanmaken
1. Ga naar **https://console.anthropic.com**
2. Klik **"Sign Up"** of **"Log In"**
3. Gebruik je email + wachtwoord of Google/GitHub login
4. Verifieer je email adres

### Stap 2: API Key Genereren
1. In de console, ga naar **"API Keys"** (linkermenu)
2. Klik **"Create Key"**
3. Geef een naam: `Nederlandse Vacature Optimizer`
4. Selecteer permissions: **Full access** (voor testing)
5. Klik **"Create Key"**
6. **KOPIEER de key meteen** (je kunt hem niet meer zien!)

### Stap 3: Credits Controleren
- **Gratis credits**: $5 bij nieuwe accounts
- **Voldoende voor**: 500+ analyses (zeer goedkoop!)
- **Toevoegen credits**: Klik "Billing" om meer toe te voegen

## 🌐 API Key in Netlify Zetten

### Optie A: Via Netlify Dashboard
1. Ga naar **app.netlify.com**
2. Selecteer je **Nederlandse Vacature Optimizer** site
3. Ga naar **Site settings** → **Environment variables**
4. Klik **"Add variable"**
5. Vul in:
   - **Key**: `CLAUDE_API_KEY`
   - **Value**: `sk-ant-api03-...` (je gekopieerde key)
6. Klik **"Create variable"**
7. Site wordt automatisch opnieuw gedeployed

### Optie B: Via Netlify CLI (Advanced)
```bash
# Als je Netlify CLI gebruikt
netlify env:set CLAUDE_API_KEY "sk-ant-api03-your-key-here"
```

## ✅ Testen of het Werkt

### Verwachte Gedrag MET API Key:
- ✅ Echte AI analyse van vacatureteksten
- ✅ Nederlandse recruitment expertise
- ✅ Persoonlijke feedback en tips
- ✅ Variërende scores per analyse

### Gedrag ZONDER API Key:
- ✅ Demo blijft werken met mock data
- ✅ Interface en alle features beschikbaar
- ✅ Vaste demo scores en tips
- ⚠️ Geen echte AI analyse

## 🔐 Veiligheid & Best Practices

### API Key Veiligheid
- ❌ **NOOIT** in code committen
- ❌ **NOOIT** in frontend JavaScript zetten
- ✅ **ALLEEN** in Netlify environment variables
- ✅ Gebruik alleen in backend functions

### Kosten Monitoring
- **Typische kosten**: €0.008 per analyse
- **Daily limit instellen**: Ga naar Anthropic console → Usage limits
- **Alerts**: Stel notificaties in bij bepaald gebruik

## 🚨 Troubleshooting

### "API Key niet gevonden" Error
```javascript
// Check in browser console:
// Functions logs tonen: "CLAUDE_API_KEY not found"
```
**Oplossing**: Controleer environment variable in Netlify

### "Invalid API Key" Error
```javascript
// API response: 401 Unauthorized
```
**Oplossing**: Genereer nieuwe key in Anthropic console

### "Rate Limit Exceeded"
```javascript
// API response: 429 Too Many Requests  
```
**Oplossing**: Wacht even of upgrade plan in Anthropic console

### "Insufficient Credits"
```javascript
// API response: Payment required
```
**Oplossing**: Voeg credits toe in Anthropic billing

## 💰 Kosten Schatting

### Gratis Tier ($5 credits):
- **~625 analyses** mogelijk
- **Perfect voor MVP testing**
- **Geen credit card vereist**

### Pay-as-you-go:
- **Input**: ~$0.003 per 1K tokens
- **Output**: ~$0.015 per 1K tokens  
- **Gemiddelde analyse**: ~€0.008
- **100 analyses/dag**: ~€24/maand

## 🔄 API Key Delen (Veilig)

### Voor Development Team:
1. **Maak separate keys** per developer
2. **Gebruik .env files** lokaal (niet committen!)
3. **Roteer keys** regelmatig
4. **Monitor usage** per key

### Voor Production:
1. **Dedicated production key**
2. **Rate limiting** instellen
3. **Usage monitoring** & alerts
4. **Backup key** voor emergencies

## 🎯 Next Steps Na Setup

1. **Deploy & test** → Controleer of analyses werken
2. **Monitor usage** → Check daily API calls
3. **Set limits** → Voorkom onverwachte kosten  
4. **Scale up** → Upgrade plan bij groei

De Nederlandse Vacature Optimizer is nu klaar voor echte AI-powered analyses! 🚀