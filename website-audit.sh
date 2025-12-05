#!/bin/bash
# website-audit.sh - Generieke website analyse voor Claude Code
#
# GEBRUIK:
#   ./website-audit.sh <url> [pixel_id] [form_id]
#
# VOORBEELDEN:
#   ./website-audit.sh https://kandidatentekort.nl 238226887541404 kalFRTCA
#   ./website-audit.sh https://recruitmentapk.nl
#   ./website-audit.sh https://example.com

# Kleuren
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Check arguments
if [ -z "$1" ]; then
    echo -e "${RED}❌ Geen URL opgegeven${NC}"
    echo ""
    echo "Gebruik: ./website-audit.sh <url> [meta_pixel_id] [typeform_id]"
    echo ""
    echo "Voorbeelden:"
    echo "  ./website-audit.sh https://kandidatentekort.nl 238226887541404 kalFRTCA"
    echo "  ./website-audit.sh https://recruitmentapk.nl"
    echo "  ./website-audit.sh https://mijnsite.nl"
    exit 1
fi

# Parameters
URL="$1"
PIXEL_ID="${2:-niet opgegeven}"
FORM_ID="${3:-niet opgegeven}"
DATE=$(date +%Y%m%d-%H%M)
DOMAIN=$(echo "$URL" | sed -e 's|https\?://||' -e 's|/.*||')
OUTPUT="${DOMAIN}-audit-${DATE}.md"

# Header
echo ""
echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     🔍 WEBSITE AUDIT - CLAUDE CODE     ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}URL:${NC}        $URL"
echo -e "${GREEN}Domain:${NC}     $DOMAIN"
echo -e "${GREEN}Meta Pixel:${NC} $PIXEL_ID"
echo -e "${GREEN}Form ID:${NC}    $FORM_ID"
echo -e "${GREEN}Output:${NC}     $OUTPUT"
echo ""

# Build prompt
PROMPT="Voer een complete technische website audit uit voor: $URL

## ANALYSE OPDRACHT

### 1. FETCH & STRUCTURE
- Fetch de homepage HTML
- Analyseer document structure (head, body)
- Tel externe scripts en stylesheets

### 2. TRACKING PIXELS
Zoek naar deze tracking codes:
| Type | Zoekterm | Specifiek ID |
|------|----------|--------------|
| Meta Pixel | fbq, facebook.com/tr | $PIXEL_ID |
| Google Analytics | gtag, GA4, G-XXXXX | any |
| LinkedIn | linkedin.com/px, _linkedin_partner_id | any |
| Google Tag Manager | gtm.js, GTM- | any |
| Hotjar | hotjar.com | any |
| HubSpot | hs-scripts | any |

### 3. FORMS & EMBEDS
- Zoek naar form embeds (Typeform ID: $FORM_ID, Jotform, HubSpot, etc.)
- Check hidden fields (utm_source, utm_medium, utm_campaign)
- Analyseer form action URLs

### 4. PERFORMANCE
- Tel render-blocking resources
- Check image formats en lazy loading
- Identificeer grote/ongeoptimaliseerde assets
- Schat laadtijd impact

### 5. SEO & META
- Title tag
- Meta description
- Open Graph tags
- Canonical URL
- Robots directives

### 6. SECURITY
- SSL/HTTPS check
- Mixed content warnings
- External script sources

### 7. MOBILE
- Viewport meta tag
- Responsive indicators
- Touch-friendly elements

## OUTPUT FORMAT

\`\`\`markdown
# Website Audit: $DOMAIN
**Datum:** \$(date '+%Y-%m-%d %H:%M')
**URL:** $URL

## Samenvatting
| Categorie | Score | Status |
|-----------|-------|--------|
| Tracking | /10 | 🟢🟡🔴 |
| Performance | /10 | 🟢🟡🔴 |
| SEO | /10 | 🟢🟡🔴 |
| Mobile | /10 | 🟢🟡🔴 |
| Security | /10 | 🟢🟡🔴 |

## Tracking Status
| Pixel | Gevonden | ID/Details | Actie Nodig |
|-------|----------|------------|-------------|

## Performance Issues
| Issue | Impact | Fix |
|-------|--------|-----|

## SEO Status
| Element | Waarde | OK? |
|---------|--------|-----|

## Security Check
| Check | Status |
|-------|--------|

## Top 5 Prioriteiten
1. [HOOG] ...
2. [HOOG] ...
3. [MED] ...
4. [MED] ...
5. [LAAG] ...

## Quick Wins (< 30 min)
- [ ] ...

## Development Nodig
- [ ] ...

## Ruwe Data
[Relevante code snippets]
\`\`\`

Wees specifiek, actionable, geen vage adviezen."

# Run
echo -e "${YELLOW}▶ Claude Code analyse starten...${NC}"
echo ""

claude "$PROMPT" > "$OUTPUT"

# Done
echo ""
echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║           ✅ AUDIT COMPLEET            ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""
echo -e "📄 Rapport: ${BLUE}$OUTPUT${NC}"
echo ""
echo "Commands:"
echo "  cat $OUTPUT          # Bekijk rapport"
echo "  code $OUTPUT         # Open in VS Code"
echo "  open $OUTPUT         # Open in default app"
echo ""
