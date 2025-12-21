# 🚀 QUICK START - Kandidatentekort Automation

## ⏱️ Geschatte setup tijd: 30-45 minuten

---

## STAP 1: API Key (5 min)

1. Ga naar https://console.anthropic.com/
2. Login / Maak account
3. Ga naar **API Keys**
4. Klik **Create Key**
5. Kopieer en bewaar veilig

✅ **Check:** Je hebt een `sk-ant-...` key

---

## STAP 2: Pipedrive Custom Fields (10 min)

1. Open `pipedrive-setup.md`
2. Maak de 6 custom fields aan
3. Check dat pipeline "vacature analyse" bestaat

✅ **Check:** Custom fields zichtbaar bij deal

---

## STAP 3: Zapier Zap Bouwen (20-30 min)

1. Ga naar https://zapier.com/app/zaps
2. Klik **Create Zap**
3. Volg `zapier-config.md` stap voor stap:
   - Trigger: Typeform
   - Step 2: Pipedrive Create Person
   - Step 3: Pipedrive Create Deal
   - Step 4: Webhooks GET
   - Step 5: Webhooks POST (Claude API)
   - Step 6: Pipedrive Update Deal
   - Step 7: Gmail Send Email
   - Step 8: Pipedrive Update Deal (stage)

✅ **Check:** Alle steps groen in Zapier

---

## STAP 4: Test (5 min)

1. Ga naar https://form.typeform.com/to/kalFRTCA
2. Vul test submission in met:
   - Je eigen email
   - Een test vacature document
3. Wacht 1-2 minuten
4. Check:
   - [ ] Deal verschijnt in Pipedrive
   - [ ] Email ontvangen
   - [ ] Analyse correct

---

## 🎉 DONE!

De automation draait nu automatisch voor elke nieuwe Typeform submission.

---

## 📁 BESTANDEN OVERZICHT

```
kandidatentekort-automation/
├── README.md                    # Overzicht
├── QUICK-START.md              # Deze guide
├── zapier-config.md            # Stap-voor-stap Zapier
├── pipedrive-setup.md          # Custom fields setup
├── typeform-fields.md          # Veld mapping
├── claude-api-prompt.txt       # Prompt template
├── claude-api-webhook.json     # Webhook config
├── gmail-template.html         # HTML email
├── gmail-template-plaintext.txt # Plain text email
├── test-claude-api.py          # Python test script
└── test-claude-api.sh          # Bash test script
```

---

## 🆘 HULP NODIG?

- **WhatsApp:** https://wa.me/31614314593
- **Calendly:** https://calendly.com/wouter-arts-/vacature-analyse-advies

---

## 📊 VERWACHTE RESULTATEN

| Metric | Verwachting |
|--------|-------------|
| Response tijd | < 5 minuten (was 24 uur) |
| Analyse kwaliteit | Consistent, professioneel |
| Kosten per lead | ~€0.05 (Claude API) |
| Conversie naar gesprek | 10-15% |

---

Succes! 🎯
