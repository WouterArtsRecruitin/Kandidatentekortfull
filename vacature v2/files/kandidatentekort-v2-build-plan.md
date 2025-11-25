# 🚀 KANDIDATENTEKORT.NL V2 - COMPLETE BUILD PLAN

**Strategie:** Build NIEUWE versie parallel (v2.kandidatentekort.nl)  
**Tech Stack:** Next.js 15 + Cloudflare + Claude API + All tracking  
**Timeline:** 2-3 dagen voor MVP  
**Domain:** v2.kandidatentekort.nl → test → switch to main

---

## 🎯 WAAROM V2 (NIET UPDATE V1)?

✅ **V1 blijft live** (geen downtime, geen stress)  
✅ **Clean slate** (alle nieuwe features from scratch)  
✅ **A/B testing** (v1 vs v2 vergelijken)  
✅ **Gradual rollout** (test eerst, dan switch)  
✅ **Rollback ready** (v1 als backup)

**Nadelen van V1 updaten:**
❌ Downtime tijdens rebuild  
❌ Breaking changes risico  
❌ Moeilijk terug te draaien  
❌ Bezoekers verstoren

---

## 📦 V2 TECH STACK (COMPLETE)

```
┌─────────────────────────────────────────────────────┐
│              KANDIDATENTEKORT.NL V2                  │
│           v2.kandidatentekort.nl                     │
└─────────────────────────────────────────────────────┘

FRONTEND (Next.js 15):
├─ React 18 + TypeScript
├─ Tailwind CSS 4.0
├─ shadcn/ui components
├─ Streaming UI (real-time analysis)
└─ Google Analytics 4 (G-W6G1NY28BD) ✅

TRACKING & PIXELS:
├─ GA4 events (pageview, submit, complete)
├─ Facebook Pixel (retargeting)
├─ LinkedIn Insight Tag (B2B ads)
└─ Custom events (demo clicks, etc)

BACKEND (Serverless):
├─ Next.js API Routes (/api/analyze)
├─ Cloudflare Workers (queue processing)
├─ Claude API (Anthropic SDK)
└─ Multi-pass analysis (quality control)

INTEGRATIONS:
├─ Jotform (form submission)
├─ Zapier (automation flows)
├─ Resend (email delivery)
├─ Notion (database/CRM)
├─ Pipedrive (sales CRM)
└─ Google Drive (storage)

MCP SERVERS (Optional Phase 2):
├─ Brave Search (salary data)
├─ Labour Market Intelligence (kandidatenschaarste)
└─ Custom MCP (internal tool)

DEPLOYMENT:
├─ Netlify (primary hosting)
├─ Cloudflare DNS (v2 subdomain)
├─ GitHub (version control)
└─ Environment variables (secrets)
```

---

## 🏗️ V2 PROJECT STRUCTURE

```
kandidatentekort-v2/
├─ app/
│   ├─ layout.tsx              # Root layout + Analytics + Pixels
│   ├─ page.tsx                # Homepage + Hero + Form
│   ├─ api/
│   │   ├─ analyze/route.ts    # Main analysis endpoint
│   │   └─ webhooks/
│   │       └─ zapier/route.ts # Zapier webhook receiver
│   ├─ components/
│   │   ├─ Analytics.tsx       # GA4 + FB Pixel + LinkedIn
│   │   ├─ VacatureForm.tsx    # Main form with demo
│   │   ├─ DemoTemplate.tsx    # Tech demo selector
│   │   ├─ StreamingAnalysis.tsx # Real-time results
│   │   └─ ui/                 # shadcn components
│   └─ lib/
│       ├─ claude.ts           # Claude API client
│       ├─ prompts/
│       │   ├─ master-prompt.ts      # Main analysis prompt
│       │   └─ quality-check.ts      # Quality control prompt
│       ├─ templates/
│       │   └─ tech-vacatures.ts     # 15 tech templates
│       └─ integrations/
│           ├─ zapier.ts       # Zapier webhook handler
│           └─ resend.ts       # Email sender
│
├─ workers/                    # Cloudflare Workers
│   └─ analyze-queue.ts        # Background job processing
│
├─ public/
│   ├─ demo-vacatures/         # Demo files
│   └─ assets/
│
├─ .env.local                  # Secrets (gitignored)
├─ .env.example                # Template for secrets
├─ next.config.mjs
├─ tailwind.config.ts
├─ package.json
└─ README.md
```

---

## 🎯 PHASE 1: MVP (DAG 1-2) - CORE FEATURES

### **Features in MVP:**
✅ Homepage + Hero section  
✅ Vacature form (with validation)  
✅ 5 Tech demo templates  
✅ Claude API integration (streaming)  
✅ Real-time analysis results  
✅ Google Analytics 4 (G-W6G1NY28BD)  
✅ Facebook Pixel (retargeting)  
✅ LinkedIn Insight Tag  
✅ Responsive design (mobile-first)  
✅ SEO optimization  

### **NOT in MVP (Phase 2):**
❌ Multi-MCP integration (later)  
❌ Payment system (€29) (later)  
❌ User accounts (later)  
❌ Email automation (Zapier - later)  
❌ PDF generation (later)  

---

## 🚀 IMPLEMENTATION STAPPEN

### **STAP 1: PROJECT SETUP (30 MIN)**

```bash
# Create nieuwe Next.js 15 app
npx create-next-app@latest kandidatentekort-v2

# Opties:
✅ TypeScript? Yes
✅ ESLint? Yes
✅ Tailwind CSS? Yes
✅ src/ directory? No
✅ App Router? Yes
✅ Turbopack? Yes
✅ Import alias (@/*)? Yes

cd kandidatentekort-v2

# Install dependencies
npm install @anthropic-ai/sdk
npm install @next/third-parties  # Voor GA4
npm install zod                  # Form validation
npm install react-hook-form      # Forms
npm install lucide-react         # Icons
npm install class-variance-authority clsx tailwind-merge  # Utils

# Install shadcn/ui
npx shadcn@latest init

# Add components
npx shadcn@latest add button
npx shadcn@latest add textarea
npx shadcn@latest add card
npx shadcn@latest add badge
npx shadcn@latest add select
npx shadcn@latest add tabs
```

### **STAP 2: ENVIRONMENT VARIABLES (5 MIN)**

```bash
# .env.local (create this file, gitignore it)
ANTHROPIC_API_KEY=sk-ant-xxx...xxx
NEXT_PUBLIC_GA_ID=G-W6G1NY28BD
NEXT_PUBLIC_FB_PIXEL_ID=123456789012345  # Jouw FB Pixel ID
NEXT_PUBLIC_LINKEDIN_PARTNER_ID=xxxxxxx  # LinkedIn ID
```

```bash
# .env.example (commit this to git)
ANTHROPIC_API_KEY=sk-ant-your-api-key-here
NEXT_PUBLIC_GA_ID=G-XXXXXXXXXX
NEXT_PUBLIC_FB_PIXEL_ID=your-pixel-id
NEXT_PUBLIC_LINKEDIN_PARTNER_ID=your-partner-id
```

### **STAP 3: ANALYTICS COMPONENT (15 MIN)**

```typescript
// app/components/Analytics.tsx
'use client';

import { GoogleAnalytics } from '@next/third-parties/google';
import Script from 'next/script';

export function Analytics() {
  const gaId = process.env.NEXT_PUBLIC_GA_ID;
  const fbPixelId = process.env.NEXT_PUBLIC_FB_PIXEL_ID;
  const linkedInId = process.env.NEXT_PUBLIC_LINKEDIN_PARTNER_ID;

  return (
    <>
      {/* Google Analytics 4 */}
      {gaId && <GoogleAnalytics gaId={gaId} />}

      {/* Facebook Pixel */}
      {fbPixelId && (
        <>
          <Script
            id="facebook-pixel"
            strategy="afterInteractive"
            dangerouslySetInnerHTML={{
              __html: `
                !function(f,b,e,v,n,t,s)
                {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
                n.callMethod.apply(n,arguments):n.queue.push(arguments)};
                if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
                n.queue=[];t=b.createElement(e);t.async=!0;
                t.src=v;s=b.getElementsByTagName(e)[0];
                s.parentNode.insertBefore(t,s)}(window, document,'script',
                'https://connect.facebook.net/en_US/fbevents.js');
                fbq('init', '${fbPixelId}');
                fbq('track', 'PageView');
              `,
            }}
          />
          <noscript>
            <img
              height="1"
              width="1"
              style={{ display: 'none' }}
              src={`https://www.facebook.com/tr?id=${fbPixelId}&ev=PageView&noscript=1`}
            />
          </noscript>
        </>
      )}

      {/* LinkedIn Insight Tag */}
      {linkedInId && (
        <Script
          id="linkedin-insight"
          strategy="afterInteractive"
          dangerouslySetInnerHTML={{
            __html: `
              _linkedin_partner_id = "${linkedInId}";
              window._linkedin_data_partner_ids = window._linkedin_data_partner_ids || [];
              window._linkedin_data_partner_ids.push(_linkedin_partner_id);
              (function(l) {
                if (!l){window.lintrk = function(a,b){window.lintrk.q.push([a,b])};
                window.lintrk.q=[]}
                var s = document.getElementsByTagName("script")[0];
                var b = document.createElement("script");
                b.type = "text/javascript";b.async = true;
                b.src = "https://snap.licdn.com/li.lms-analytics/insight.min.js";
                s.parentNode.insertBefore(b, s);})(window.lintrk);
            `,
          }}
        />
      )}
    </>
  );
}

// Track events helper
export const trackEvent = (eventName: string, params?: Record<string, any>) => {
  // Google Analytics
  if (typeof window !== 'undefined' && window.gtag) {
    window.gtag('event', eventName, params);
  }

  // Facebook Pixel
  if (typeof window !== 'undefined' && window.fbq) {
    window.fbq('track', eventName, params);
  }
};

// TypeScript declarations
declare global {
  interface Window {
    gtag: (...args: any[]) => void;
    fbq: (...args: any[]) => void;
    lintrk: (...args: any[]) => void;
  }
}
```

### **STAP 4: ROOT LAYOUT (10 MIN)**

```typescript
// app/layout.tsx
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import { Analytics } from './components/Analytics';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Kandidatentekort.nl - Vacature Optimalisatie in 24 Uur',
  description: 'Analyseer je vacaturetekst op inclusiviteit, SEO, ATS compatibility en conversie. Krijg 5 concrete verbeterpunten binnen 24 uur.',
  keywords: 'vacature optimalisatie, recruitment, inclusiviteit, SEO, ATS',
  openGraph: {
    title: 'Kandidatentekort.nl - Vacature Optimalisatie',
    description: 'Analyseer je vacature en krijg 5 verbeterpunten binnen 24 uur',
    type: 'website',
    locale: 'nl_NL',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="nl">
      <body className={inter.className}>
        {children}
        <Analytics />
      </body>
    </html>
  );
}
```

### **STAP 5: DEMO TEMPLATES (30 MIN)**

```typescript
// lib/templates/tech-vacatures.ts

export interface VacatureTemplate {
  id: string;
  title: string;
  sector: string;
  company: string;
  text: string;
  expectedScore: number;
  topIssues: string[];
}

export const TECH_TEMPLATES: Record<string, VacatureTemplate> = {
  'backend-developer': {
    id: 'backend-developer',
    title: 'Senior Backend Developer Python',
    sector: 'Technology',
    company: 'FinTech Scale-up Amsterdam',
    expectedScore: 4.2,
    topIssues: [
      'Gender bias: "hij moet kunnen"',
      'Geen salarisbereik vermeld',
      'Te veel eisen (5 jaar + HBO)',
    ],
    text: `Senior Backend Developer Python - FinTech Amsterdam

Wij zoeken een ervaren Backend Developer die ons team komt versterken.

Over de functie:
Als Senior Backend Developer ben je verantwoordelijk voor de ontwikkeling van onze fintech platform backend. Hij moet kunnen werken in een snel groeiende scale-up omgeving en heeft ervaring met high-traffic systemen.

Jouw profiel:
- Minimaal 5 jaar ervaring met Python
- Hij moet kunnen werken met Django of Flask
- Ervaring met PostgreSQL en Redis
- Kennis van Docker en Kubernetes is een pre
- Je bent een teamplayer
- HBO werk- en denkniveau
- Goede communicatieve vaardigheden in Nederlands en Engels

Wat wij bieden:
- Een uitdagende rol in een innovatief bedrijf
- Marktconform salaris
- Leuke collega's
- Moderne werkplek in Amsterdam
- Gratis koffie en fruit
- 25 vakantiedagen

Ben jij de developer die wij zoeken? Solliciteer nu via ons online formulier!`,
  },

  'devops-engineer': {
    id: 'devops-engineer',
    title: 'DevOps Engineer (Kubernetes)',
    sector: 'Technology',
    company: 'Cloud Native Consultancy',
    expectedScore: 5.9,
    topIssues: [
      'CKA certificaat vereist (te streng)',
      'On-call niet gecompenseerd',
      'Multi-cloud unrealistic',
    ],
    text: `DevOps Engineer gezocht voor scale-up!

Jouw rol:
Als DevOps Engineer ben je verantwoordelijk voor onze cloud infrastructure en CI/CD pipelines.

Requirements:
- 4+ jaar DevOps ervaring
- Kubernetes (CKA certificaat vereist)
- Terraform, Ansible, Helm
- AWS/Azure/GCP (multi-cloud)
- Python en/of Go scripting
- GitOps (ArgoCD/Flux)
- Monitoring (Prometheus, Grafana, ELK)
- Security best practices
- On-call beschikbaarheid
- BSc Computer Science

Wij bieden:
- €70.000 - €90.000 per jaar
- 30 vakantiedagen
- Remote work
- Conference budget €2000/jaar
- Pensioenregeling

Solliciteer via ons portal.`,
  },

  'frontend-developer': {
    id: 'frontend-developer',
    title: 'Medior Frontend Developer React',
    sector: 'Technology',
    company: 'E-commerce Platform Rotterdam',
    expectedScore: 5.1,
    topIssues: [
      'Te informeel ("wizard", "buttery-smooth")',
      'On-site only in 2025',
      'Free lunch als benefit = zwak',
    ],
    text: `Ben jij de React wizard die wij zoeken?

De functie:
Word jij enthousiast van pixel-perfect UI's en buttery-smooth animations? Dan ben jij de developer die wij zoeken!

Wat vragen wij:
- 3+ jaar React experience
- TypeScript master
- Je kent CSS als je broekzak
- Next.js, Redux, Testing Library
- Agile/Scrum mindset
- Goede communicatieve vaardigheden

Wat bieden wij:
- Een competitive salary
- Gezellig team
- Free lunch on Fridays!
- Latest MacBook Pro

Interesse? Stuur je CV!`,
  },

  'data-engineer': {
    id: 'data-engineer',
    title: 'Senior Data Engineer',
    sector: 'Data & Analytics',
    company: 'Data Platform Schiphol',
    expectedScore: 5.7,
    topIssues: [
      '5 jaar vereist (3 is genoeg)',
      'Te veel tools (Snowflake + BigQuery + Redshift)',
      '3 days office = ouderwets',
    ],
    text: `Senior Data Engineer voor data platform

Jouw verantwoordelijkheden:
Je bouwt en onderhoudt onze data pipelines die dagelijks TB's aan data verwerken.

Wij zoeken:
- 5+ jaar data engineering ervaring
- Strong SQL skills (complex queries, optimization)
- Python (pandas, PySpark)
- Airflow or Dagster
- Snowflake, BigQuery, of Redshift
- DBT for data transformations
- Data modeling (Kimball, Data Vault)
- Understanding of data governance
- Experience with real-time streaming (Kafka)
- Bachelor degree in CS/Engineering

Wij bieden:
- Competitive compensation package
- Hybrid working model (3 days office)
- Travel allowance
- Pension plan
- Professional development opportunities

Send your application to hr@company.nl`,
  },

  'full-stack-developer': {
    id: 'full-stack-developer',
    title: 'Full-Stack Developer (React + Node.js)',
    sector: 'Technology',
    company: 'SaaS Start-up Utrecht',
    expectedScore: 4.8,
    topIssues: [
      'Startup jargon ("rockstar", "rocketship")',
      'Equity zonder context',
      '"Break things" = chaos culture',
    ],
    text: `🚀 Join our rocketship!

We're building the future of SaaS. 10x growth last year. Series A funded. Now hiring rockstar full-stack devs!

The Role:
You'll own features end-to-end. From database to pixel. Ship fast, break things, iterate. True startup mentality!

You:
- React (hooks, context, etc.)
- Node.js + Express
- MongoDB or PostgreSQL
- AWS/GCP/Azure
- CI/CD pipelines
- Microservices architecture
- Event-driven systems
- GraphQL nice-to-have

We offer:
- Equity (0.1-0.5%)
- Unlimited vacation
- Work from anywhere
- Latest tech stack
- Beer fridge 🍺

Ready to change the world? Apply now!`,
  },
};

export const getTemplateById = (id: string): VacatureTemplate | null => {
  return TECH_TEMPLATES[id] || null;
};

export const getAllTemplates = (): VacatureTemplate[] => {
  return Object.values(TECH_TEMPLATES);
};
```

---

## 📋 NEXT STEPS

**WAT MOET IK NU DOEN?**

### **OPTIE A: IK BUILD V2 ZELF** (DIY)
```
Timeline: 2-3 dagen
Cost: €0 (jouw tijd)
I provide: Complete code voor elke stap

Say: "Start V2 build"
→ Ik geef je stap-voor-stap alle code
```

### **OPTIE B: CLAUDE BOUWT V2** (Full Service)
```
Timeline: 2 dagen
Cost: €1,200 (16 uur × €75)
Deliverables:
✅ Complete Next.js 15 app
✅ All tracking (GA4 + FB + LinkedIn)
✅ 5 tech demo templates
✅ Claude API integration (streaming)
✅ Responsive design
✅ Deploy to v2.kandidatentekort.nl
✅ Documentation + handover

Say: "Build V2 for me"
→ Ik bouw alles, jij test
```

### **OPTIE C: HYBRID** (Pair Programming)
```
Timeline: 3 dagen
Cost: €600 (8 uur × €75)
Setup:
- Ik build core (API, Claude, templates)
- Jij doet UI/design (frontend)
- Daily sync calls (30 min)

Say: "Hybrid approach"
→ We bouwen samen
```

---

## 💰 COST COMPARISON

**V2 Build Costs:**
```
Development:
├─ DIY (Option A): €0 (jouw tijd)
├─ Hybrid (Option C): €600 (8 uur)
└─ Full service (Option B): €1,200 (16 uur)

Monthly Tools:
├─ Claude API: €20-50/maand
├─ Netlify: €0 (free tier sufficient for start)
├─ Domain: €12/jaar
└─ Total: €20-50/maand
```

**Revenue Projection:**
```
Month 1: 30 vacatures × €29 = €870
Month 3: 100 vacatures × €29 = €2,900
Month 6: 300 vacatures × €29 = €8,700

ROI (Option B):
Investment: €1,200
Month 1 revenue: €870
Break-even: Month 2
Year 1 profit: €33,600 - €1,200 = €32,400
```

---

## 🎯 MIJN ADVIES

**Start with Option C (Hybrid):**
- Ik bouw de complexe delen (API, Claude, MCP)
- Jij doet de creative delen (design, copy, branding)
- Cost: €600 vs €1,200 (50% besparing)
- Timeline: 3 dagen (iets langer maar je leert)
- Result: Production-ready V2 + je snapt de code

**Wat wordt het?**

Type:
- **"Start V2 build"** → DIY, ik guide je
- **"Build V2 for me"** → Full service, ik doe alles
- **"Hybrid approach"** → We bouwen samen

Laten we kandidatentekort.nl V2 launch-ready maken! 🚀
