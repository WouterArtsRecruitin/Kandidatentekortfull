#!/usr/bin/env python3
"""
Kandidatentekort Automatische Vacature Analyse
===============================================
Nederlandse Technische & Industriele Vacature Optimizer
Met sector-specifieke analyse voor maximale sollicitatie conversie.

Sectoren: Oil & Gas, Manufacturing, Automation, Renewable Energy, Construction
"""

import os
import re
import json
import time
import logging
from datetime import datetime
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

# Third-party imports (install via: pip install anthropic flask requests)
try:
    import anthropic
except ImportError:
    anthropic = None
    print("Warning: anthropic package not installed. Run: pip install anthropic")

try:
    from flask import Flask, request, jsonify
except ImportError:
    Flask = None
    print("Warning: flask package not installed. Run: pip install flask")

try:
    import requests
except ImportError:
    requests = None
    print("Warning: requests package not installed. Run: pip install requests")

# ===============================================
# CONFIGURATION
# ===============================================

# Logging setup - StreamHandler only for cloud compatibility (Render, Heroku, etc.)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Environment variables
CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY', '')
PIPEDRIVE_API_KEY = os.getenv('PIPEDRIVE_API_KEY', '')
SMTP_HOST = os.getenv('SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
SMTP_USER = os.getenv('SMTP_USER', '')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')


# ===============================================
# SECTOR DEFINITIONS
# ===============================================

class TechnicalSector(Enum):
    OIL_GAS = "oil_gas"
    MANUFACTURING = "manufacturing"
    AUTOMATION = "automation"
    RENEWABLE = "renewable"
    CONSTRUCTION = "construction"
    GENERAL = "general"


@dataclass
class SectorBenchmark:
    """Benchmark scores per sector based on market research"""
    name: str
    display_name: str
    avg_score_range: Tuple[int, int]
    key_focus: str
    keywords: list


SECTOR_BENCHMARKS = {
    TechnicalSector.OIL_GAS: SectorBenchmark(
        name="oil_gas",
        display_name="Oil & Gas",
        avg_score_range=(28, 38),
        key_focus="safety & compliance",
        keywords=['oil', 'gas', 'petrochemical', 'refinery', 'offshore', 'pipeline',
                  'drilling', 'lpg', 'lng', 'chemical plant', 'hsse', 'ppe']
    ),
    TechnicalSector.MANUFACTURING: SectorBenchmark(
        name="manufacturing",
        display_name="Manufacturing",
        avg_score_range=(35, 45),
        key_focus="process optimization",
        keywords=['manufacturing', 'productie', 'quality', 'process', 'lean',
                  'six sigma', 'production', 'assembly', 'oem', 'fabriek']
    ),
    TechnicalSector.AUTOMATION: SectorBenchmark(
        name="automation",
        display_name="Automation",
        avg_score_range=(32, 42),
        key_focus="technology advancement",
        keywords=['automation', 'plc', 'scada', 'control', 'robotics', 'dcs',
                  'instrumentation', 'hmi', 'siemens', 'allen bradley', 'abb']
    ),
    TechnicalSector.RENEWABLE: SectorBenchmark(
        name="renewable",
        display_name="Renewable Energy",
        avg_score_range=(30, 40),
        key_focus="sustainability & impact",
        keywords=['renewable', 'wind', 'solar', 'energy', 'duurzaam', 'sustainable',
                  'green', 'turbine', 'biomass', 'hydrogen', 'battery storage']
    ),
    TechnicalSector.CONSTRUCTION: SectorBenchmark(
        name="construction",
        display_name="Construction",
        avg_score_range=(25, 35),
        key_focus="project delivery",
        keywords=['construction', 'civil', 'project', 'infrastructure', 'building',
                  'architect', 'structural', 'bouw', 'civiel', 'grondwerk']
    )
}


# ===============================================
# TECHNICAL MASTER PROMPT v2.0
# ===============================================

TECHNICAL_MASTER_PROMPT = """
# NEDERLANDSE TECHNISCHE & INDUSTRIELE VACATURE ANALYSE EXPERT

## EXPERTISE & CONTEXT
Je bent een senior vacature-analyse specialist gespecialiseerd in TECHNISCHE EN INDUSTRIELE SECTOREN.
Je combineert Intelligence Group's VacatureVerbeteraar expertise met 15+ jaar ervaring in Oil & Gas,
Manufacturing, Automation, Renewable Energy en Construction recruitment.

ALLEEN technische en industriele rollen voor bedrijven met 50-800 medewerkers in Gelderland,
Overijssel, Noord-Brabant.

## NEDERLANDSE RECRUITMENT INTELLIGENCE (2025)

### Sector Benchmarks:
- Oil & Gas: 28-38/100 - Hoge salarisverwachtingen, safety focus, internationale projecten
- Manufacturing: 35-45/100 - Proces optimalisatie, kwaliteit driven, lean cultuur
- Automation: 32-42/100 - Technology advancement, innovation driven, cutting-edge tech
- Renewable Energy: 30-40/100 - Sustainability motivated, growth sector, purpose-driven
- Construction: 25-35/100 - Project mentality, result oriented, team dynamics

**Minimaal 45+ punten nodig voor decent results, 60+ voor moeilijke functies**

## ANALYSE FRAMEWORK

### 1. FUNCTIETITEL KRACHT (SEO + herkenbaarheid)
- Is de titel SEO-geoptimaliseerd voor technische zoekopdrachten?
- Herkenbaar voor technici in de sector?
- Vermijd vage titels zoals "Specialist" of "Medewerker"

### 2. SALARIS TRANSPARANTIE (Nederlandse wet 2025 compliance)
- Concrete salary range vermeld?
- Marktconform voor de sector en regio?
- Secundaire arbeidsvoorwaarden specifiek benoemd?

### 3. TECHNISCHE CHALLENGE
- Concrete projecten en projectschaal genoemd?
- Specifieke technologieen/systemen/tools?
- Team samenstelling en senioriteit?
- Equipment / software / tech stack?

### 4. PROCES & KWALITEIT FOCUS (voor manufacturing/process engineers)
- Lean/Six Sigma cultuur aanwezig?
- Continuous improvement opportunities?
- Kwaliteitssystemen en certificeringen?

### 5. CAREER DEVELOPMENT
- Groeipad en doorgroeimogelijkheden?
- Training en certificeringen aangeboden?
- Internationale exposure mogelijk?
- Mentorship en kennisdeling?

### 6. COMPANY CREDIBILITY
- Financiele gezondheid van het bedrijf?
- Referentie projecten en klanten?
- Innovatie-mindset zichtbaar?

## OUTPUT FORMAT (STRICT JSON):

{
    "vacature_score": 7.5,
    "sector": "manufacturing",
    "sector_display": "Manufacturing",
    "confidence": 0.85,

    "critical_blockers": [
        {
            "issue": "Geen salarisindicatie",
            "impact_percentage": 35,
            "fix": "Voeg salary range toe: EUR 55.000 - 70.000 bruto per jaar"
        },
        {
            "issue": "Vage functievereisten",
            "impact_percentage": 25,
            "fix": "Specificeer: 'Ervaring met SAP Quality Module' ipv 'ERP ervaring'"
        },
        {
            "issue": "Geen projectvoorbeelden",
            "impact_percentage": 20,
            "fix": "Voeg toe: 'Je werkt aan de nieuwe productielijn van EUR 5M'"
        }
    ],

    "week1_quick_wins": [
        {
            "action": "Voeg concrete salarisindicatie toe",
            "expected_improvement": 35,
            "implementation": "Tussen EUR 55.000 - 70.000 bruto, afhankelijk van ervaring"
        },
        {
            "action": "Specificeer de technische tools",
            "expected_improvement": 15,
            "implementation": "Lijst specifieke systemen: SAP QM, Minitab, SPC tools"
        }
    ],

    "roi_impact": {
        "expected_application_increase": 45,
        "expected_time_to_hire_reduction_days": 12,
        "quality_improvement_score": 3.5
    },

    "sector_specific_advice": "Voor Manufacturing vacatures is het cruciaal om de productieomgeving te beschrijven. Kandidaten willen weten: moderne of legacy faciliteiten? Batch of continuous production? Lean/Six Sigma cultuur?",

    "rewritten_intro": "Als Quality Manager bij [Bedrijf] leid je een team van 5 QA Engineers in onze state-of-the-art productieomgeving (Industry 4.0). Je bent verantwoordelijk voor EUR 25M aan jaarlijkse output en werkt direct samen met R&D aan nieuwe productontwikkeling. Salaris: EUR 65.000-75.000 + auto + bonus.",

    "full_analysis": "Uitgebreide analyse tekst hier..."
}

## BELANGRIJKE RICHTLIJNEN:
1. Wees SPECIFIEK - geen vage adviezen zoals "verbeter de tekst"
2. Geef CONCRETE cijfers en percentages
3. Focus op wat TECHNISCHE professionals belangrijk vinden
4. Vergelijk met marktstandaarden in de sector
5. Geef KOPIEERBARE verbeteringen die direct implementeerbaar zijn
6. Maak elke aanbeveling DIRECT implementeerbaar voor Nederlandse technische recruitment

## GEWENST OUTPUT FORMAT (naast JSON):

**VACATURE SCORE: X.X/10**
**SECTOR: [Oil&Gas/Manufacturing/Automation/Renewable/Construction]**
**DOELGROEP: [Process Engineer/Project Manager/Maintenance/etc]**

**TOP 3 CRITICAL BLOCKERS:**
1. [Specifieke blocker] - kost [%] sollicitaties
2. [Specifieke blocker] - kost [%] sollicitaties
3. [Specifieke blocker] - kost [%] sollicitaties

**WEEK 1 QUICK WINS (implementatie <2 uur):**
- [Concrete tekstwijziging met rationale]
- [Concrete verbetering met expected impact]
- [Specifieke optimalisatie met % verbetering]

**STRATEGISCHE VERBETERINGEN:**
- [Sector-specifieke optimalisatie]
- [Doelgroep-gerichte aanpassing]
- [Competitive advantage enhancement]

**ROI IMPACT:**
- Expected: +[X]% meer sollicitaties
- Expected: +[X]% betere kwalificatie rate
- Expected: -[X] dagen snellere time-to-hire

Analyseer nu de volgende vacature en geef je expert oordeel:
"""


# ===============================================
# SECTOR DETECTION
# ===============================================

def detect_technical_sector(vacature_text: str) -> Tuple[TechnicalSector, float]:
    """
    Detect the technical sector of a vacancy based on keyword matching.

    Returns:
        Tuple of (sector, confidence_score)
    """
    text_lower = vacature_text.lower()

    sector_scores = {}

    for sector, benchmark in SECTOR_BENCHMARKS.items():
        # Count keyword matches
        matches = sum(1 for keyword in benchmark.keywords if keyword in text_lower)

        # Weight by keyword specificity (longer keywords = more specific = higher weight)
        weighted_score = sum(
            len(keyword) / 5 for keyword in benchmark.keywords if keyword in text_lower
        )

        sector_scores[sector] = {
            'matches': matches,
            'weighted': weighted_score
        }

    # Find best matching sector
    if not sector_scores:
        return TechnicalSector.GENERAL, 0.5

    best_sector = max(sector_scores, key=lambda s: sector_scores[s]['weighted'])
    best_score = sector_scores[best_sector]

    # Calculate confidence (0.5 - 1.0 range)
    max_possible = len(SECTOR_BENCHMARKS[best_sector].keywords) * 2
    confidence = min(0.5 + (best_score['weighted'] / max_possible) * 0.5, 1.0)

    # If no clear winner, default to manufacturing (most common)
    if best_score['matches'] == 0:
        return TechnicalSector.MANUFACTURING, 0.5

    return best_sector, confidence


# ===============================================
# CLAUDE API INTEGRATION
# ===============================================

def call_claude_api(prompt: str, max_tokens: int = 4000) -> Optional[str]:
    """
    Call the Claude API with the given prompt.

    Returns:
        Response text or None if failed
    """
    if not CLAUDE_API_KEY:
        logger.error("CLAUDE_API_KEY not configured")
        return None

    if anthropic is None:
        logger.error("anthropic package not installed")
        return None

    try:
        client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=max_tokens,
            temperature=0.3,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        if message.content and len(message.content) > 0:
            return message.content[0].text

        return None

    except Exception as e:
        logger.error(f"Claude API error: {str(e)}")
        return None


# ===============================================
# MAIN ANALYSIS FUNCTION
# ===============================================

def analyze_vacature_technical(
    vacature_text: str,
    bedrijf_naam: str = "",
    functie_titel: str = ""
) -> Dict[str, Any]:
    """
    Analyze a technical vacancy and provide sector-specific recommendations.

    Args:
        vacature_text: The full vacancy text
        bedrijf_naam: Company name (optional)
        functie_titel: Job title (optional)

    Returns:
        Dictionary with analysis results
    """
    start_time = time.time()

    # Step 1: Detect sector
    sector, sector_confidence = detect_technical_sector(vacature_text)
    benchmark = SECTOR_BENCHMARKS.get(sector)

    logger.info(f"Detected sector: {sector.value} (confidence: {sector_confidence:.2f})")

    # Step 2: Build analysis prompt
    sector_info = f"""
## GEDETECTEERDE SECTOR: {benchmark.display_name if benchmark else 'Algemeen'}
- Benchmark score range: {benchmark.avg_score_range if benchmark else 'N/A'}
- Key focus: {benchmark.key_focus if benchmark else 'N/A'}
- Sector confidence: {sector_confidence:.0%}
"""

    analysis_prompt = f"""{TECHNICAL_MASTER_PROMPT}

{sector_info}

## TE ANALYSEREN VACATURE:
**Bedrijf:** {bedrijf_naam or 'Niet gespecificeerd'}
**Functie:** {functie_titel or 'Niet gespecificeerd'}

**Vacaturetekst:**
{vacature_text}

---

Geef je complete analyse in het opgegeven JSON format. Wees specifiek en actionable.
"""

    # Step 3: Call Claude API
    response_text = call_claude_api(analysis_prompt)

    if not response_text:
        logger.error("Failed to get Claude API response")
        return {
            'success': False,
            'error': 'API call failed',
            'sector': sector.value,
            'sector_display': benchmark.display_name if benchmark else 'Algemeen'
        }

    # Step 4: Parse response
    try:
        # Try to extract JSON from response
        json_match = re.search(r'\{[\s\S]*\}', response_text)
        if json_match:
            analysis_data = json.loads(json_match.group())
        else:
            analysis_data = {'raw_analysis': response_text}
    except json.JSONDecodeError:
        analysis_data = {'raw_analysis': response_text}

    # Step 5: Extract score
    score = analysis_data.get('vacature_score', 7.5)
    if isinstance(score, str):
        score_match = re.search(r'(\d+\.?\d*)', score)
        score = float(score_match.group(1)) if score_match else 7.5

    # Ensure score is in valid range
    score = max(0, min(10, float(score)))

    # Step 6: Build result
    elapsed_time = time.time() - start_time

    result = {
        'success': True,
        'analysis': analysis_data,
        'score': score,
        'sector': sector.value,
        'sector_display': benchmark.display_name if benchmark else 'Algemeen',
        'sector_confidence': sector_confidence,
        'benchmark_range': benchmark.avg_score_range if benchmark else None,
        'processing_time': round(elapsed_time, 2),
        'timestamp': datetime.now().isoformat()
    }

    logger.info(f"Success! Score: {score}/10 | Sector: {sector.value} | Time: {elapsed_time:.2f}s")

    return result


# ===============================================
# EMAIL FUNCTIONS
# ===============================================

def generate_email_subject(result: Dict[str, Any]) -> str:
    """Generate a compelling email subject based on analysis results."""
    sector_display = result.get('sector_display', 'Technische')
    score = result.get('score', 7.5)

    # Calculate potential improvement percentage
    improvement_pct = int((10 - score) * 20)

    subjects = {
        'oil_gas': f"Je Oil & Gas vacature: {improvement_pct}% meer gekwalificeerde sollicitaties mogelijk",
        'manufacturing': f"Je Manufacturing vacature: {improvement_pct}% meer sollicitaties mogelijk",
        'automation': f"Je Automation vacature: {improvement_pct}% meer technische kandidaten mogelijk",
        'renewable': f"Je Renewable Energy vacature: {improvement_pct}% meer impact-gedreven sollicitaties",
        'construction': f"Je Construction vacature: {improvement_pct}% meer projectprofessionals mogelijk",
        'general': f"Je technische vacature: {improvement_pct}% meer sollicitaties mogelijk"
    }

    sector = result.get('sector', 'general')
    return subjects.get(sector, subjects['general'])


def generate_email_body(result: Dict[str, Any], bedrijf_naam: str = "") -> str:
    """Generate the email body with analysis results."""
    score = result.get('score', 7.5)
    sector_display = result.get('sector_display', 'Technische')
    analysis = result.get('analysis', {})

    # Extract critical blockers
    blockers = analysis.get('critical_blockers', [])
    blockers_text = ""
    for i, blocker in enumerate(blockers[:3], 1):
        if isinstance(blocker, dict):
            blockers_text += f"\n{i}. {blocker.get('issue', 'N/A')} - kost {blocker.get('impact_percentage', '?')}% sollicitaties"
            blockers_text += f"\n   Fix: {blocker.get('fix', 'N/A')}"

    # Extract quick wins
    quick_wins = analysis.get('week1_quick_wins', [])
    quick_wins_text = ""
    for win in quick_wins[:2]:
        if isinstance(win, dict):
            quick_wins_text += f"\n- {win.get('action', 'N/A')} (+{win.get('expected_improvement', '?')}% verwacht)"

    # ROI impact
    roi = analysis.get('roi_impact', {})
    roi_text = ""
    if roi:
        roi_text = f"""
VERWACHTE ROI:
- +{roi.get('expected_application_increase', '?')}% meer sollicitaties
- -{roi.get('expected_time_to_hire_reduction_days', '?')} dagen snellere time-to-hire
"""

    email_body = f"""
Beste {bedrijf_naam or 'Hiring Manager'},

Bedankt voor het indienen van je {sector_display} vacature bij Kandidatentekort.nl!

VACATURE SCORE: {score}/10

Op basis van onze analyse van 50.000+ technische vacatures in Nederland hebben we de volgende verbeterpunten geidentificeerd:

TOP 3 KRITIEKE BLOCKERS:
{blockers_text or 'Geen kritieke blockers gevonden'}

WEEK 1 QUICK WINS:
{quick_wins_text or 'Zie volledige analyse'}

{roi_text}

SECTOR-SPECIFIEK ADVIES ({sector_display}):
{analysis.get('sector_specific_advice', 'Neem contact op voor gepersonaliseerd advies.')}

---

Wil je dat wij je vacaturetekst herschrijven voor maximale conversie?
Reply op deze email of bel direct: 020-XXX XXXX

Met vriendelijke groet,
Het Kandidatentekort Team

P.S. Vacatures met een score boven 8.0 krijgen gemiddeld 156% meer sollicitaties!
"""

    return email_body


def send_analysis_email(
    to_email: str,
    result: Dict[str, Any],
    bedrijf_naam: str = ""
) -> bool:
    """
    Send analysis results via email.

    Returns:
        True if email was sent successfully
    """
    try:
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
    except ImportError:
        logger.error("Email libraries not available")
        return False

    if not all([SMTP_HOST, SMTP_USER, SMTP_PASSWORD]):
        logger.warning("SMTP not configured, skipping email")
        return False

    try:
        subject = generate_email_subject(result)
        body = generate_email_body(result, bedrijf_naam)

        msg = MIMEMultipart()
        msg['From'] = SMTP_USER
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)

        logger.info(f"Email sent to {to_email}")
        return True

    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        return False


# ===============================================
# ENHANCED EMAIL FUNCTIONS v2.0
# ===============================================

def get_sector_specific_email_subject(score: float, sector: str, improvement_percentage: int) -> str:
    """
    Generate sector-specific email subjects voor betere open rates.
    Variatie op basis van score niveau.
    """
    sector_names = {
        'oil_gas': 'Oil & Gas',
        'manufacturing': 'Manufacturing',
        'automation': 'Automation',
        'renewable': 'Renewable Energy',
        'construction': 'Construction'
    }

    sector_name = sector_names.get(sector, 'Technische')

    if score >= 7.0:
        return f"Je {sector_name} vacature scoort {score}/10 - Professioneel niveau!"
    elif score >= 5.0:
        return f"Je {sector_name} vacature: {improvement_percentage}% meer sollicitaties mogelijk"
    else:
        return f"Je {sector_name} vacature scoort {score}/10 - Directe verbetering nodig"


def enhance_email_content(analysis_result: Dict[str, Any]) -> str:
    """Add sector-specific insights to email content."""
    sector = analysis_result.get('sector', 'manufacturing')
    score = analysis_result.get('score', 0.0)

    sector_insights = {
        'oil_gas': "Oil & Gas professionals verwachten transparante salarisinformatie en duidelijke safety focus in vacatureteksten.",
        'manufacturing': "Manufacturing engineers zoeken naar proces optimalisatie kansen en kwaliteitssysteem ownership.",
        'automation': "Automation specialisten willen concrete technologie stacks en innovatie projecten zien.",
        'renewable': "Renewable Energy professionals zijn gemotiveerd door sustainability impact en groei sector kansen.",
        'construction': "Construction engineers zoeken project variëteit en tangible results in grote infrastructuur projecten."
    }

    insight = sector_insights.get(sector, "Technische professionals waarderen specifieke, concrete vacature informatie.")

    return f"""
Sector Insight: {insight}

Recruitin B.V. specialiseert in technische recruitment voor de {sector.replace('_', ' & ')} sector
in Gelderland, Overijssel en Noord-Brabant.

Interesse in een gesprek over optimalisatie?
Direct contact: wouter@recruitin.nl
    """


# ===============================================
# TYPEFORM INTEGRATION
# ===============================================

def process_technical_vacature(typeform_data: Dict[str, Any]) -> bool:
    """
    Main function voor Typeform webhook integratie.
    Enhanced voor technische sectoren.

    Args:
        typeform_data: Dictionary met Typeform submission data

    Returns:
        True als succesvol verwerkt
    """
    try:
        # Extract data from Typeform
        vacature_text = typeform_data.get('vacature_tekst', '')
        bedrijf_naam = typeform_data.get('bedrijf_naam', '')
        functie_titel = typeform_data.get('functie_titel', '')
        email = typeform_data.get('email', '')
        naam = typeform_data.get('naam', '')

        logger.info(f"Processing {functie_titel} at {bedrijf_naam}")

        # Step 1: Technical Analysis met nieuwe prompt
        analysis_result = analyze_vacature_technical(
            vacature_text=vacature_text,
            bedrijf_naam=bedrijf_naam,
            functie_titel=functie_titel
        )

        if not analysis_result.get('success'):
            logger.error(f"Analysis failed: {analysis_result.get('error')}")
            return False

        # Step 2: Enhanced Email Creation
        score = analysis_result.get('score', 0.0)
        sector = analysis_result.get('sector', 'manufacturing')
        improvement_pct = min(int((10 - score) * 20), 200)

        subject = get_sector_specific_email_subject(score, sector, improvement_pct)
        enhanced_content = enhance_email_content(analysis_result)

        # Step 3: Send Email
        email_sent = False
        if email:
            email_sent = send_analysis_email(
                to_email=email,
                result=analysis_result,
                bedrijf_naam=bedrijf_naam
            )

        # Step 4: Pipedrive Lead Creation met sector info
        pipedrive_lead = None
        if PIPEDRIVE_API_KEY:
            pipedrive_lead = create_pipedrive_lead(
                result=analysis_result,
                bedrijf_naam=bedrijf_naam,
                contact_email=email,
                functie_titel=functie_titel
            )

        # Step 5: Track performance
        track_performance_improvement(analysis_result)

        logger.info(f"Success! Score: {score}/10 | Sector: {sector} | Email: {email_sent}")
        return True

    except Exception as e:
        logger.error(f"Process Error: {str(e)}")
        return False


# ===============================================
# PERFORMANCE TRACKING
# ===============================================

def track_performance_improvement(analysis_result: Dict[str, Any]) -> None:
    """Track before/after performance voor ROI measurement."""
    performance_log = {
        'timestamp': datetime.now().isoformat(),
        'version': 'technical_master_prompt_v2.0',
        'score': analysis_result.get('score', 0),
        'sector': analysis_result.get('sector', 'unknown'),
        'sector_confidence': analysis_result.get('sector_confidence', 0),
        'processing_time': analysis_result.get('processing_time', 0),
        'avg_score_before': 4.2,  # Baseline
        'expected_improvement': '+150% more qualified leads',
        'sectors_active': ['oil_gas', 'manufacturing', 'automation', 'renewable', 'construction']
    }

    # Log naar file voor tracking
    log_file = os.getenv('PERFORMANCE_LOG_FILE', 'performance_tracking.json')
    try:
        with open(log_file, 'a') as f:
            f.write(json.dumps(performance_log) + '\n')
    except Exception as e:
        logger.warning(f"Could not write performance log: {str(e)}")


# ===============================================
# PIPEDRIVE INTEGRATION
# ===============================================

def create_pipedrive_lead(
    result: Dict[str, Any],
    bedrijf_naam: str,
    contact_email: str,
    functie_titel: str = ""
) -> Optional[str]:
    """
    Create a lead in Pipedrive with sector tags.

    Returns:
        Lead ID if successful, None otherwise
    """
    if not PIPEDRIVE_API_KEY:
        logger.warning("PIPEDRIVE_API_KEY not configured")
        return None

    if requests is None:
        logger.error("requests package not installed")
        return None

    try:
        score = result.get('score', 0)
        sector = result.get('sector_display', 'Technisch')

        # Determine lead value based on score (lower score = higher potential value)
        lead_value = int((10 - score) * 500)  # EUR 0 - 5000

        lead_data = {
            'title': f"{bedrijf_naam} - {functie_titel or 'Vacature Optimalisatie'}",
            'value': lead_value,
            'currency': 'EUR',
            'person_id': None,  # Will be created if needed
            'organization_id': None,
            'expected_close_date': None,
            'visible_to': 1,
            'label_ids': []  # Add sector labels here
        }

        # Add note with analysis
        note_content = f"""
Sector: {sector}
Score: {score}/10
Potential Improvement: {int((10-score)*20)}%

Quick Wins:
{json.dumps(result.get('analysis', {}).get('week1_quick_wins', []), indent=2, ensure_ascii=False)}
"""

        # Create lead via API
        api_url = f"https://api.pipedrive.com/v1/leads?api_token={PIPEDRIVE_API_KEY}"

        response = requests.post(api_url, json=lead_data)

        if response.status_code == 201:
            lead_id = response.json().get('data', {}).get('id')
            logger.info(f"Pipedrive lead created: {lead_id}")
            return lead_id
        else:
            logger.error(f"Pipedrive API error: {response.status_code}")
            return None

    except Exception as e:
        logger.error(f"Pipedrive error: {str(e)}")
        return None


# ===============================================
# FLASK WEBHOOK SERVER
# ===============================================

def create_app() -> Optional[Any]:
    """Create Flask application with webhook endpoints."""
    if Flask is None:
        logger.error("Flask not installed")
        return None

    app = Flask(__name__)

    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'service': 'kandidatentekort-auto',
            'timestamp': datetime.now().isoformat(),
            'has_api_key': bool(CLAUDE_API_KEY)
        })

    @app.route('/webhook/analyze', methods=['POST'])
    def webhook_analyze():
        """Main webhook endpoint for vacancy analysis."""
        try:
            data = request.get_json()

            if not data:
                return jsonify({'error': 'No data provided'}), 400

            vacature_text = data.get('vacature_text', '')
            bedrijf_naam = data.get('bedrijf_naam', '')
            functie_titel = data.get('functie_titel', '')
            contact_email = data.get('email', '')

            if not vacature_text:
                return jsonify({'error': 'vacature_text is required'}), 400

            # Perform analysis
            result = analyze_vacature_technical(
                vacature_text,
                bedrijf_naam,
                functie_titel
            )

            # Send email if configured
            email_sent = False
            if contact_email and result.get('success'):
                email_sent = send_analysis_email(
                    contact_email,
                    result,
                    bedrijf_naam
                )

            # Create Pipedrive lead if configured
            pipedrive_lead = None
            if result.get('success') and PIPEDRIVE_API_KEY:
                pipedrive_lead = create_pipedrive_lead(
                    result,
                    bedrijf_naam,
                    contact_email,
                    functie_titel
                )

            result['email_sent'] = email_sent
            result['pipedrive_lead_id'] = pipedrive_lead

            return jsonify(result)

        except Exception as e:
            logger.error(f"Webhook error: {str(e)}")
            return jsonify({'error': str(e)}), 500

    @app.route('/api/sector-detect', methods=['POST'])
    def api_sector_detect():
        """Quick sector detection endpoint."""
        try:
            data = request.get_json()
            text = data.get('text', '')

            if not text:
                return jsonify({'error': 'text is required'}), 400

            sector, confidence = detect_technical_sector(text)
            benchmark = SECTOR_BENCHMARKS.get(sector)

            return jsonify({
                'sector': sector.value,
                'sector_display': benchmark.display_name if benchmark else 'Algemeen',
                'confidence': confidence,
                'benchmark_range': benchmark.avg_score_range if benchmark else None,
                'key_focus': benchmark.key_focus if benchmark else None
            })

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/webhook/typeform', methods=['POST'])
    def webhook_typeform():
        """
        Typeform webhook endpoint voor automatische vacature verwerking.
        Verwacht Typeform webhook payload format.
        """
        try:
            data = request.get_json()

            if not data:
                return jsonify({'error': 'No data provided'}), 400

            # Extract from Typeform format
            form_response = data.get('form_response', {})
            answers = form_response.get('answers', [])

            # Map Typeform answers to our format
            typeform_data = {}
            for answer in answers:
                field_type = answer.get('type', '')
                field_ref = answer.get('field', {}).get('ref', '')

                if field_type == 'text':
                    value = answer.get('text', '')
                elif field_type == 'email':
                    value = answer.get('email', '')
                elif field_type == 'long_text':
                    value = answer.get('text', '')
                else:
                    value = str(answer.get('text', answer.get('email', '')))

                # Map common field refs
                if 'vacature' in field_ref.lower() or 'tekst' in field_ref.lower():
                    typeform_data['vacature_tekst'] = value
                elif 'bedrijf' in field_ref.lower() or 'company' in field_ref.lower():
                    typeform_data['bedrijf_naam'] = value
                elif 'functie' in field_ref.lower() or 'title' in field_ref.lower():
                    typeform_data['functie_titel'] = value
                elif 'email' in field_ref.lower():
                    typeform_data['email'] = value
                elif 'naam' in field_ref.lower() or 'name' in field_ref.lower():
                    typeform_data['naam'] = value

            # Process the vacancy
            success = process_technical_vacature(typeform_data)

            return jsonify({
                'success': success,
                'message': 'Vacature processed' if success else 'Processing failed'
            })

        except Exception as e:
            logger.error(f"Typeform webhook error: {str(e)}")
            return jsonify({'error': str(e)}), 500

    return app


# ===============================================
# CLI TESTING
# ===============================================

def test_analysis():
    """Run a quick test analysis."""
    test_vacancy = """
    Quality Manager - Manufacturing

    Wij zoeken een ervaren Quality Manager voor ons productie bedrijf in Rotterdam.

    Wat ga je doen:
    - Aansturen van het QA team
    - Implementeren van kwaliteitssystemen
    - Rapporteren aan directie

    Wat vragen wij:
    - HBO opleiding
    - 5+ jaar ervaring
    - Kennis van ISO 9001

    Wat bieden wij:
    - Marktconform salaris
    - Lease auto
    - 25 vakantiedagen
    """

    print("\n" + "="*60)
    print("KANDIDATENTEKORT TEST ANALYSIS")
    print("="*60 + "\n")

    # Test sector detection
    sector, confidence = detect_technical_sector(test_vacancy)
    print(f"Detected Sector: {sector.value} (confidence: {confidence:.0%})")

    # Test full analysis (requires API key)
    if CLAUDE_API_KEY:
        result = analyze_vacature_technical(
            test_vacancy,
            "Test Company BV",
            "Quality Manager"
        )

        print(f"\nTest Score: {result.get('score', 'N/A')}/10")
        print(f"Sector: {result.get('sector_display', 'N/A')}")
        print(f"Success: {result.get('success', False)}")
        print(f"Processing Time: {result.get('processing_time', 'N/A')}s")

        # Show email subject
        print(f"\nEmail Subject: {generate_email_subject(result)}")
    else:
        print("\nNote: Set CLAUDE_API_KEY to test full analysis")

    print("\n" + "="*60)
    print("TEST COMPLETE")
    print("="*60 + "\n")


# ===============================================
# MAIN ENTRY POINT
# ===============================================

if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == 'test':
            test_analysis()
        elif sys.argv[1] == 'server':
            app = create_app()
            if app:
                port = int(os.getenv('PORT', '5000'))
                print("\n" + "="*60)
                print("KANDIDATENTEKORT AUTO v2.0 - TECHNICAL MASTER PROMPT")
                print("="*60)
                print(f"\nStarting server on port {port}...")
                print(f"\nEndpoints:")
                print(f"  Health:    http://localhost:{port}/health")
                print(f"  Analyze:   http://localhost:{port}/webhook/analyze")
                print(f"  Typeform:  http://localhost:{port}/webhook/typeform")
                print(f"  Sector:    http://localhost:{port}/api/sector-detect")
                print("\nExpected: +150% better lead quality")
                print("ROI: EUR 28k+ besparing per successful placement")
                print("="*60 + "\n")
                app.run(host='0.0.0.0', port=port, debug=False)
            else:
                print("Failed to create app. Install Flask: pip install flask")
        else:
            print("Usage: python kandidatentekort_auto.py [test|server]")
    else:
        print("""
============================================================
KANDIDATENTEKORT AUTO v2.0 - TECHNICAL MASTER PROMPT
============================================================

Nederlandse Technische & Industriele Vacature Optimizer
Met sector-specifieke analyse voor Oil & Gas, Manufacturing,
Automation, Renewable Energy en Construction.

Usage:
  python kandidatentekort_auto.py test     - Run test analysis
  python kandidatentekort_auto.py server   - Start webhook server

Endpoints (when running server):
  /health              - Health check
  /webhook/analyze     - Direct vacancy analysis
  /webhook/typeform    - Typeform webhook integration
  /api/sector-detect   - Quick sector detection

Environment Variables:
  CLAUDE_API_KEY       - Required for analysis
  PIPEDRIVE_API_KEY    - Optional for CRM integration
  SMTP_HOST            - Email server host
  SMTP_PORT            - Email server port (default: 587)
  SMTP_USER            - Email username
  SMTP_PASSWORD        - Email password
  PERFORMANCE_LOG_FILE - Performance tracking log file

Install Dependencies:
  pip install anthropic flask requests

Expected Results:
  - Scores: 4.2/10 -> 7.8/10
  - Lead Quality: +150% improvement
  - ROI: EUR 28k+ per successful placement
============================================================
        """)
