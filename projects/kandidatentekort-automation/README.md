# Kandidatentekort.nl Automation

**Twee opties beschikbaar:**

---

## 🔀 OPTIE 1: Zapier (No-Code)
📁 **Folder:** `/`

Gebruik Zapier voor de automation flow. Geen code nodig.

**Bestanden:**
- `QUICK-START.md` - Start hier
- `zapier-config.md` - Stap-voor-stap setup
- `gmail-template.html` - Email template

**Tijd:** ~30-45 min setup in Zapier UI

---

## 🤖 OPTIE 2: Autonomous Script (Code)
📁 **Folder:** `/autonomous-script/`

Python script dat direct draait zonder Zapier. Deploy op Render.

**Bestanden:**
- `kandidatentekort_auto.py` - Main script
- `CLAUDE_CODE_COMMANDS.sh` - Copy-paste commands
- `render.yaml` - Deploy config

**Tijd:** ~10 min met Claude Code

**Voordelen:**
- ✅ Geen Zapier kosten
- ✅ Sneller (geen Zapier latency)
- ✅ Volledige controle
- ✅ Makkelijk te customizen

---

## 🎯 Welke kiezen?

| Criterium | Zapier | Autonomous Script |
|-----------|--------|-------------------|
| Setup tijd | 30-45 min | 10 min |
| Code nodig | Nee | Ja (Python) |
| Kosten/maand | €0-19 | €0 (Render free) |
| Customization | Beperkt | Volledig |
| Maintenance | Zapier beheert | Zelf beheren |

**Mijn advies:** Start met **Autonomous Script** → sneller, gratis, meer controle.

---

## 📞 Links

- **Calendly:** https://calendly.com/wouter-arts-/vacature-analyse-advies
- **WhatsApp:** https://wa.me/31614314593
- **Typeform:** https://form.typeform.com/to/kalFRTCA

---

## 🚀 Quick Start - Autonomous Script

```bash
cd /Users/wouterarts/Projects/kandidatentekort-automation/autonomous-script
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env met API keys
python kandidatentekort_auto.py
```

Test: `curl http://localhost:8080/test`

---

**Gemaakt:** 25 november 2025, 04:30
