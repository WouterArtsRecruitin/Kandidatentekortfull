# Pipedrive Setup - Custom Fields

## 📋 BENODIGDE CUSTOM FIELDS VOOR DEALS

Maak deze custom fields aan in Pipedrive > Settings > Data fields > Deal:

### 1. Vacature Analyse Resultaat
- **Naam:** Vacature Analyse Resultaat
- **Type:** Large text
- **Pipeline:** vacature analyse
- **Gebruik:** Opslaan van volledige Claude output

### 2. Vacature Score
- **Naam:** Vacature Score
- **Type:** Numerical (1-10)
- **Pipeline:** vacature analyse
- **Gebruik:** Score uit analyse

### 3. Vacature File URL
- **Naam:** Vacature File URL
- **Type:** Text (single line)
- **Pipeline:** vacature analyse
- **Gebruik:** Link naar originele vacature

### 4. Sector
- **Naam:** Sector
- **Type:** Single option
- **Opties:**
  - High-tech & Elektronica
  - Machinebouw & Metaal
  - Elektrotechniek & Installatie
  - Bouw & Infrastructuur
  - Procestechniek & Chemie
  - Agri & Food
  - Automotive
  - Productie & Manufacturing
  - Energie & Duurzaamheid

### 5. Optimalisatiedoel
- **Naam:** Optimalisatiedoel
- **Type:** Single option
- **Opties:**
  - Meer gekwalificeerde sollicitanten
  - Betere employer branding
  - Snellere time-to-hire
  - Lagere cost-per-hire

### 6. Email Verzonden
- **Naam:** Email Verzonden
- **Type:** Date
- **Pipeline:** vacature analyse
- **Gebruik:** Timestamp wanneer analyse email is verstuurd

---

## 📊 PIPELINE STAGES

Pipeline: **vacature analyse** (ID: 4)

Zorg dat deze stages bestaan:

| # | Stage Naam | Beschrijving |
|---|------------|--------------|
| 1 | 📥 Nieuw Binnen | Typeform submission ontvangen |
| 2 | 🔍 In Analyse | Claude analyseert vacature |
| 3 | ✍️ Klaar | Analyse compleet |
| 4 | 📧 Verstuurd | Email met resultaat verzonden |
| 5 | 🔥 Interesse | Lead reageert/plant gesprek |
| 6 | 💬 In Gesprek | Sales call gepland/gedaan |
| 7 | 🏆 Klant | Opdracht gewonnen |
| 8 | ❌ Geen interesse | Lead niet verder |

---

## 🔧 HOE CUSTOM FIELDS AANMAKEN

1. Ga naar **Pipedrive** → **Settings** (tandwiel)
2. Klik op **Data fields** in left menu
3. Selecteer **Deal** tab
4. Klik **+ Add custom field**
5. Vul in:
   - Field name: [naam]
   - Field type: [type]
   - Pipelines: vacature analyse
6. **Save**

---

## 📝 FIELD API KEYS

Na aanmaken, vind de field API keys:
1. Ga naar **Settings** → **Data fields** → **Deal**
2. Klik op een custom field
3. Kopieer de **API key** (bijv. `abc123def456...`)

Deze keys heb je nodig in Zapier voor mapping.

---

## ✅ CHECKLIST

- [ ] Custom field "Vacature Analyse Resultaat" aangemaakt
- [ ] Custom field "Vacature Score" aangemaakt
- [ ] Custom field "Vacature File URL" aangemaakt
- [ ] Custom field "Sector" aangemaakt met opties
- [ ] Custom field "Optimalisatiedoel" aangemaakt met opties
- [ ] Custom field "Email Verzonden" aangemaakt
- [ ] Pipeline stages gecheckt/aangemaakt
- [ ] Field API keys genoteerd voor Zapier
