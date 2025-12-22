#!/usr/bin/env python3
"""
Test script voor de nieuwe professionele PDF generatie
"""

import sys
import os

# Add the current directory to path
sys.path.insert(0, '/private/tmp/Kandidatentekortfull')

# Set environment variables for testing
os.environ['PIPEDRIVE_API_TOKEN'] = 'test_token'
os.environ['ANTHROPIC_API_KEY'] = 'test_key'

# Now import the functions
from webhook_v6 import generate_pdf_analysis_report, generate_pdf_vacancy_text, parse_analysis_sections

# Test data
test_company = "Demo Tech Solutions"
test_vacancy = "Full Stack Developer"

# Simulated Claude analysis response
test_analysis = """
**OVERALL SCORE: 6.2/10**

## VACATURETEKST SCORES

| Criterium | Score | Toelichting |
|-----------|-------|-------------|
| Openingszin | 4/10 | De opening is te generiek en mist impact |
| Bedrijfsprofiel | 5/10 | Beperkte informatie over bedrijfscultuur |
| Rolklarheid | 7/10 | Taken zijn redelijk duidelijk beschreven |
| Vereisten Realisme | 6/10 | Eisen zijn realistisch maar kunnen specifieker |
| Groei-narratief | 3/10 | Geen doorgroeimogelijkheden vermeld |
| Inclusie & Bias | 8/10 | Tekst is overwegend neutraal |
| Cialdini Triggers | 4/10 | Weinig overtuigingsprincipes toegepast |
| Salarisbenchmark | 5/10 | Marktconform is te vaag |
| Call-to-Action | 6/10 | Basis CTA aanwezig maar niet pakkend |
| Competitieve Delta | 4/10 | USPs ontbreken grotendeels |
| Confidence Score | 6/10 | Gemiddelde professionaliteit |
| Implementatie | 8/10 | Verbeteringen zijn snel door te voeren |

## EXECUTIVE SUMMARY

De vacaturetekst voor Full Stack Developer heeft een score van 6.2/10. De tekst is functioneel maar mist de wervingskracht die nodig is in de huidige arbeidsmarkt. De grootste verbeterpunten liggen bij de opening, het bedrijfsprofiel en het groei-narratief.

## QUICK WINS

1. **Versterk de openingszin** - Begin met een prikkelende vraag of statement die direct de aandacht grijpt
2. **Voeg salarisindicatie toe** - Kandidaten willen transparantie, noem een bandbreedte
3. **Beschrijf doorgroeimogelijkheden** - Dit is een top-3 factor voor developers bij het kiezen van een werkgever

## CIALDINI POWER-UPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. "Voeg toe hoeveel developers er al werken en hoe lang ze gemiddeld bij jullie blijven"
2. "Benoem dat dit een zeldzame kans is bij een snelgroeiend team dat verdubbeld is in 2 jaar"
3. "Vermeld awards, certificeringen of technische achievements van het bedrijf"

## VERBETERDE VACATURETEKST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Bouw mee aan de toekomst van Tech - Senior Full Stack Developer gezocht!**

Stel je voor: je code draait straks bij honderden bedrijven. Als Full Stack Developer bij Demo Tech Solutions werk je niet aan zomaar een project - je bouwt de tools die de Nederlandse tech-industrie veranderen.

**Wat ga je doen?**
- Architectuur ontwerpen en implementeren voor schaalbare applicaties
- Werken met moderne stack: React, Node.js, PostgreSQL en AWS
- Bijdragen aan technische beslissingen in een team van 8 ervaren developers
- Code reviews uitvoeren en kennis delen met collega's

**Wat bieden wij?**
- Salaris: €55.000 - €75.000 afhankelijk van ervaring
- 30 vakantiedagen + flexibel werken (3 dagen kantoor Utrecht)
- Persoonlijk ontwikkelbudget van €3.000 per jaar
- Groeipad naar Tech Lead binnen 2-3 jaar

**Wie zoeken wij?**
- 3+ jaar ervaring met full-stack development
- HBO/WO werk- en denkniveau
- Passie voor clean code en best practices
- Teamspeler die ook zelfstandig kan werken

*Solliciteer vandaag nog - we reageren binnen 48 uur!*

**Over Demo Tech Solutions**
Wij zijn een snelgroeiende scale-up in Utrecht met 45 medewerkers. Onze software helpt bedrijven hun processen te optimaliseren. In 3 jaar zijn we gegroeid van 10 naar 45 mensen, en we zoeken developers die mee willen groeien.

## BONUS TIP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Gebruik deze geoptimaliseerde tekst direct op je vacaturesite!
"""

test_contact = "Wouter Arts"

print("=" * 60)
print("TEST: Professionele PDF Generatie")
print("=" * 60)

# Test 1: Parse analysis sections
print("\n📋 Test 1: Parse analysis sections...")
sections = parse_analysis_sections(test_analysis)
print(f"   - Available keys: {list(sections.keys())}")
print(f"   - Number of individual scores: {len(sections.get('scores', {}))}")
print(f"   - Executive summary: {len(sections.get('executive_summary', ''))} chars")
print(f"   - Quick wins: {len(sections.get('quick_wins', []))} items")
print(f"   - Improved text: {len(sections.get('improved_text', ''))} chars")
print(f"   - Cialdini tips: {len(sections.get('cialdini_tips', []))} items")

# Test 2: Generate Bijlage 1
print("\n📄 Test 2: Generate Bijlage 1 (Analysis Report)...")
try:
    pdf1 = generate_pdf_analysis_report(
        company_name=test_company,
        contact_name=test_contact,
        vacancy_title=test_vacancy,
        analysis_result=test_analysis,
        original_vacancy_text="Originele vacaturetekst hier..."
    )
    if pdf1:
        print(f"   ✅ SUCCESS! Bijlage 1 generated: {len(pdf1):,} bytes")
        # Save to file for inspection
        with open('/tmp/test_bijlage1.pdf', 'wb') as f:
            f.write(pdf1)
        print(f"   📁 Saved to: /tmp/test_bijlage1.pdf")
    else:
        print("   ❌ FAILED: PDF is None")
except Exception as e:
    print(f"   ❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Generate Bijlage 2
print("\n📄 Test 3: Generate Bijlage 2 (Vacancy Text)...")
try:
    pdf2 = generate_pdf_vacancy_text(
        company_name=test_company,
        vacancy_title=test_vacancy,
        analysis_result=test_analysis
    )
    if pdf2:
        print(f"   ✅ SUCCESS! Bijlage 2 generated: {len(pdf2):,} bytes")
        # Save to file for inspection
        with open('/tmp/test_bijlage2.pdf', 'wb') as f:
            f.write(pdf2)
        print(f"   📁 Saved to: /tmp/test_bijlage2.pdf")
    else:
        print("   ❌ FAILED: PDF is None")
except Exception as e:
    print(f"   ❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("TEST COMPLETED")
print("=" * 60)
