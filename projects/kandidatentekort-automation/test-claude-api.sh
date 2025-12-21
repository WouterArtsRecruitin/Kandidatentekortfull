#!/bin/bash
# Test script voor Claude API vacature analyse
# Run: chmod +x test-claude-api.sh && ./test-claude-api.sh

# ⚠️ VUL IN: Je Anthropic API key
API_KEY="YOUR_ANTHROPIC_API_KEY_HERE"

# Test vacaturetekst
VACATURE="Wij zoeken een Software Developer.

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

Interesse? Stuur je CV naar hr@bedrijf.nl"

# Claude API call
curl -X POST https://api.anthropic.com/v1/messages \
  -H "Content-Type: application/json" \
  -H "x-api-key: $API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d "{
    \"model\": \"claude-sonnet-4-20250514\",
    \"max_tokens\": 4096,
    \"messages\": [
      {
        \"role\": \"user\",
        \"content\": \"Je bent een expert recruitment copywriter gespecialiseerd in de Nederlandse technische arbeidsmarkt.\\n\\n## VACATURETEKST:\\n\\n$VACATURE\\n\\n## CONTEXT:\\n- Bedrijf: Test BV\\n- Sector: High-tech & Elektronica\\n- Doel: Meer gekwalificeerde sollicitanten\\n\\n## OPDRACHT:\\n\\n1. SCORE (1-10) met onderbouwing\\n2. TOP 3 VERBETERPUNTEN\\n3. VERBETERDE VACATURETEKST (400-600 woorden)\\n4. BONUS TIPS (2-3 tips)\\n\\nSchrijf in het Nederlands.\"
      }
    ]
  }" | jq '.content[0].text'
