# Kandidatentekort - Deployment Guide

## 🎯 Project Structuur

Dit project heeft **twee landingspagina's**:
- **Homepage** (`/`) - Algemene vacature-analyse pagina
- **Meta Campagne** (`/meta`) - Speciaal voor Meta adverteerders

## 🚀 Deployment naar Netlify via GitHub

### Stap 1: Ga naar Netlify
1. Open [https://app.netlify.com](https://app.netlify.com)
2. Log in met je Netlify account
3. Klik op **"Add new site"** → **"Import an existing project"**

### Stap 2: Verbind met GitHub
1. Klik op **"Deploy with GitHub"**
2. Autoriseer Netlify om toegang te krijgen tot je GitHub account
3. Selecteer de repository: **`WouterArtsRecruitin/Kandidatentekortfull`**

### Stap 3: Configureer Build Settings
Kies de branch die je wilt deployen:
- **Branch:** `claude/add-footer-component-01FtQy31qvFyj9vjjLq8MoNy`

Build settings worden **automatisch gedetecteerd** vanuit `netlify.toml`:
- **Build command:** `npm run build`
- **Publish directory:** `build`
- **Redirects:** Geconfigureerd voor SPA routing

### Stap 4: Deploy!
1. Klik op **"Deploy [site-name]"**
2. Wacht 2-3 minuten voor de eerste build
3. ✅ Je site is nu live!

## 🌐 Na Deployment

### Test beide pagina's:
```
https://[your-site-name].netlify.app/        → Homepage
https://[your-site-name].netlify.app/meta    → Meta campagne pagina
```

### Custom Domain toevoegen (optioneel):
1. Ga naar **Site settings** → **Domain management**
2. Klik op **"Add custom domain"**
3. Voeg toe: `kandidatentekort.nl`
4. Configureer DNS volgens Netlify instructies

## 📱 Voor Meta Advertenties

Gebruik deze URL in je Facebook/Instagram advertenties:
```
https://kandidatentekort.nl/meta
```
(of `https://[your-site-name].netlify.app/meta` zonder custom domain)

## 🔧 Build Specificaties

- **Framework:** React 18 met Vite
- **Routing:** React Router v7
- **Styling:** Tailwind CSS
- **Bundle size:** ~440 kB (gzipped: ~140 kB)
- **Build time:** ~7 seconden

## ✅ Features

### Beide Pagina's:
- ✅ Responsive design
- ✅ VacancyAnalyzer component
- ✅ Footer met contact informatie
- ✅ Social proof notifications
- ✅ Analytics tracking

### Homepage (`/`):
- Hero met algemene messaging
- Focus op conversie-optimalisatie
- "150+ Vacatures Geanalyseerd"

### Meta Campagne (`/meta`):
- Hero geoptimaliseerd voor adverteerders
- Focus op CPH (Cost Per Hire) reductie
- "Gemiddeld 60% Lagere CPH"
- Badge: "Speciaal voor Meta Adverteerders"

## 🛠️ Lokaal Draaien

```bash
# Dependencies installeren
npm install

# Development server starten
npm run dev

# Build voor productie
npm run build
```

## 📊 Git Branch Structuur

- **Main branch:** (te configureren)
- **Feature branch:** `claude/add-footer-component-01FtQy31qvFyj9vjjLq8MoNy`

## 🔄 Continuous Deployment

Na de eerste setup deploy Netlify **automatisch** bij elke push naar de geconfigureerde branch.

## 📞 Contact

Voor vragen over de deployment:
- Email: info@recruitin.nl
- Tel: +31 313 410 507
- Website: www.recruitin.nl
