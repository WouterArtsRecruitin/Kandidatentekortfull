#!/usr/bin/env python3
"""
Kandidatentekort.nl - Vacature Analyse Test Script
Test de Claude API integratie lokaal voordat je in Zapier implementeert.

Gebruik:
    python test-claude-api.py

Vereisten:
    pip install anthropic
"""

import os
from anthropic import Anthropic

# ⚠️ VUL IN: Je API key (of zet als environment variable)
API_KEY = os.getenv("ANTHROPIC_API_KEY", "YOUR_API_KEY_HERE")

# Test data
TEST_VACATURE = """
Wij zoeken een Software Developer.

Functie:
- Ontwikkelen van software
- Werken in team
- Bugs fixen

Vereisten:
- HBO/WO
- Ervaring met programmeren
- Goede communicatie

Wij bieden:
- Goed salaris
- Leuke collega's
- Groeimogelijkheden

Interesse? Stuur je CV naar hr@bedrijf.nl
"""

TEST_CONTEXT = {
    "company": "Test BV",
    "sector": "High-tech & Elektronica",
    "goal": "Meer gekwalificeerde sollicitanten"
}

PROMPT_TEMPLATE = """Je bent een expert recruitment copywriter gespecialiseerd in de Nederlandse technische arbeidsmarkt. Je analyseert vacatureteksten en verbetert ze voor maximale kandidaat-conversie.

## VACATURETEKST OM TE ANALYSEREN:

{vacature}

## CONTEXT:
- Bedrijf: {company}
- Sector: {sector}
- Optimalisatiedoel: {goal}

## JOUW OPDRACHT:

Analyseer deze vacaturetekst en lever het volgende:

### 1. SCORE (1-10)
Geef een score met korte onderbouwing op deze criteria:
- Aantrekkelijkheid (trekt kandidaten aan?)
- Duidelijkheid (snap je wat de rol inhoudt?)
- USP's (waarom hier werken?)
- Call-to-action (makkelijk solliciteren?)

### 2. TOP 3 VERBETERPUNTEN
Identificeer de 3 belangrijkste verbeteringen, concreet en actionable.

### 3. VERBETERDE VACATURETEKST
Herschrijf de volledige vacaturetekst met:
- Pakkende opening (hook binnen 3 seconden)
- Duidelijke functie-inhoud
- Concrete arbeidsvoorwaarden
- Sterke employer branding
- Overtuigende call-to-action
- Lengte: 400-600 woorden (ideaal voor online)

### 4. BONUS TIPS
2-3 extra tips voor de recruiter/HR manager om meer kandidaten aan te trekken.

Schrijf in het Nederlands, professioneel maar toegankelijk."""


def analyze_vacature(vacature: str, company: str, sector: str, goal: str) -> str:
    """Analyseer een vacaturetekst met Claude API."""
    
    client = Anthropic(api_key=API_KEY)
    
    prompt = PROMPT_TEMPLATE.format(
        vacature=vacature,
        company=company,
        sector=sector,
        goal=goal
    )
    
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return message.content[0].text


def parse_sections(response: str) -> dict:
    """Parse de Claude response in secties."""
    sections = {
        "score": "",
        "verbeterpunten": "",
        "verbeterde_tekst": "",
        "bonus_tips": ""
    }
    
    # Simple parsing - kan verbeterd worden
    if "SCORE" in response:
        parts = response.split("TOP 3 VERBETERPUNTEN")
        sections["score"] = parts[0].replace("### 1. SCORE", "").replace("SCORE", "").strip()
        
        if len(parts) > 1:
            parts2 = parts[1].split("VERBETERDE VACATURETEKST")
            sections["verbeterpunten"] = parts2[0].replace("### 2.", "").strip()
            
            if len(parts2) > 1:
                parts3 = parts2[1].split("BONUS TIPS")
                sections["verbeterde_tekst"] = parts3[0].replace("### 3.", "").strip()
                
                if len(parts3) > 1:
                    sections["bonus_tips"] = parts3[1].replace("### 4.", "").strip()
    
    return sections


def main():
    print("=" * 60)
    print("🎯 KANDIDATENTEKORT.NL - Vacature Analyse Test")
    print("=" * 60)
    print()
    
    print("📝 Test vacature:")
    print(TEST_VACATURE[:100] + "...")
    print()
    
    print("⏳ Analyseren met Claude API...")
    print()
    
    try:
        response = analyze_vacature(
            vacature=TEST_VACATURE,
            company=TEST_CONTEXT["company"],
            sector=TEST_CONTEXT["sector"],
            goal=TEST_CONTEXT["goal"]
        )
        
        print("✅ ANALYSE RESULTAAT:")
        print("=" * 60)
        print(response)
        print("=" * 60)
        
        # Parse en toon secties
        sections = parse_sections(response)
        
        print()
        print("📊 GEPARSDE SECTIES:")
        print("-" * 40)
        for key, value in sections.items():
            preview = value[:100] + "..." if len(value) > 100 else value
            print(f"{key}: {preview}")
        
        print()
        print("✅ Test geslaagd! Ready voor Zapier implementatie.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print()
        print("Troubleshooting:")
        print("1. Check je API key")
        print("2. pip install anthropic")
        print("3. Check je internet connectie")


if __name__ == "__main__":
    main()
