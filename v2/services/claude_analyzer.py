"""
Claude AI Vacancy Analyzer - V8 Enhanced with 5-Expert Panel.
"""

import json
import requests
from typing import Dict, Any, Optional
from dataclasses import dataclass
from ..config import ANTHROPIC_API_KEY, CLAUDE_MODEL, CLAUDE_MAX_TOKENS, CLAUDE_TIMEOUT
from ..utils import get_logger, retry_with_backoff

logger = get_logger("claude_analyzer")


@dataclass
class AnalysisResult:
    """Structured analysis result."""
    success: bool
    score: float
    score_section: str
    top_3_improvements: list
    improved_text: str
    bonus_tips: list
    executive_summary: str
    quick_wins: list
    full_analysis: str
    error: Optional[str] = None


# V8 Enhanced Prompt - 5 Expert Panel
V8_ANALYSIS_PROMPT = '''Je bent een ELITE PANEL van 5 recruitment experts die gezamenlijk vacatureteksten analyseren voor de Nederlandse technische arbeidsmarkt.

## EXPERT PANEL:

1. **RECRUITMENT PSYCHOLOOG** - Analyseert kandidaat-motivatie en beslissingsprocessen
2. **EMPLOYER BRANDING SPECIALIST** - Beoordeelt bedrijfspresentatie en EVP
3. **CONVERSION COPYWRITER** - Optimaliseert tekst voor actie en engagement
4. **ARBEIDSMARKT ANALIST** - Kent salaristrends en schaarste per sector
5. **DIVERSITY & INCLUSION EXPERT** - Identificeert bias en verbetert inclusiviteit

## ANALYSEER DEZE VACATURE:

{vacature_text}

## CONTEXT:
- Bedrijf: {bedrijf}
- Sector: {sector}

## EVALUATIE-CRITERIA (Score elk 1-10):

1. **OPENINGSZIN** - Pakt deze direct de aandacht? Spreekt het de kandidaat persoonlijk aan?
2. **BEDRIJF AANTREKKINGSKRACHT** - Is duidelijk waarom dit een geweldige werkgever is?
3. **ROLKLARHEID** - Snap je binnen 30 sec wat je gaat doen?
4. **VEREISTEN REALISME** - Zijn de eisen realistisch of is het een "purple squirrel"?
5. **GROEI-NARRATIEF** - Is er een duidelijk carrière/ontwikkelperspectief?
6. **INCLUSIE & BIAS** - Is de tekst vrij van uitsluitende formuleringen?
7. **CIALDINI TRIGGERS** - Worden overtuigingsprincipes effectief ingezet?
8. **SALARISBENCHMARK** - Is compensatie transparant en competitief?
9. **CALL-TO-ACTION** - Is het helder wat de kandidaat moet doen?

## LEVER EXACT DIT JSON FORMAT:

{{
    "overall_score": 7.2,
    "score_section": "Openingszin: 6/10 | Bedrijf: 7/10 | Rolklarheid: 8/10 | Vereisten: 5/10 | Groei: 6/10 | Inclusie: 7/10 | Cialdini: 4/10 | Salaris: 3/10 | CTA: 7/10",
    "executive_summary": "Kernboodschap in 2-3 zinnen over de belangrijkste bevindingen.",
    "top_3_improvements": [
        "Eerste concrete, direct implementeerbare verbetering",
        "Tweede concrete verbetering met specifiek voorbeeld",
        "Derde concrete verbetering"
    ],
    "quick_wins": [
        {{"title": "Quick Win 1", "description": "Wat te doen", "impact": "Verwacht effect"}},
        {{"title": "Quick Win 2", "description": "Wat te doen", "impact": "Verwacht effect"}},
        {{"title": "Quick Win 3", "description": "Wat te doen", "impact": "Verwacht effect"}}
    ],
    "improved_text": "De VOLLEDIG herschreven vacaturetekst (400-600 woorden). Start met pakkende opening die de kandidaat direct aanspreekt. Gebruik 'jij' perspectief. Concrete functie-inhoud. Duidelijke arbeidsvoorwaarden met salarisindicatie. Sterke employer branding. Overtuigende call-to-action.",
    "bonus_tips": [
        "Eerste strategische tip voor de recruiter",
        "Tweede tip over distributie of timing",
        "Derde tip over opvolging"
    ],
    "cialdini_analysis": "Korte analyse van welke overtuigingsprincipes worden/kunnen worden ingezet"
}}

BELANGRIJK:
- Antwoord ALLEEN met valid JSON
- De improved_text moet een COMPLETE, direct bruikbare vacaturetekst zijn
- Schrijf in een menselijke, warme toon (niet corporate-speak)
- Gebruik concrete getallen en voorbeelden waar mogelijk
'''


class ClaudeAnalyzer:
    """Claude AI Analyzer with retry logic."""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or ANTHROPIC_API_KEY
        self.api_url = "https://api.anthropic.com/v1/messages"

    @retry_with_backoff(max_attempts=2, initial_delay=2.0, exceptions=(requests.RequestException,))
    def _call_api(self, prompt: str) -> Dict[str, Any]:
        """Make API call to Claude."""
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }

        payload = {
            "model": CLAUDE_MODEL,
            "max_tokens": CLAUDE_MAX_TOKENS,
            "messages": [{"role": "user", "content": prompt}]
        }

        response = requests.post(
            self.api_url,
            headers=headers,
            json=payload,
            timeout=CLAUDE_TIMEOUT
        )

        response.raise_for_status()
        return response.json()

    def analyze(self, vacancy_text: str, bedrijf: str = "", sector: str = "") -> AnalysisResult:
        """
        Analyze vacancy text using Claude AI.

        Returns:
            AnalysisResult with structured analysis data
        """
        if not self.api_key:
            logger.error("ANTHROPIC_API_KEY not configured")
            return AnalysisResult(
                success=False,
                score=0,
                score_section="",
                top_3_improvements=[],
                improved_text="",
                bonus_tips=[],
                executive_summary="",
                quick_wins=[],
                full_analysis="",
                error="API key not configured"
            )

        try:
            logger.info(f"Starting Claude analysis for {bedrijf or 'unknown company'}")

            # Build prompt
            prompt = V8_ANALYSIS_PROMPT.format(
                vacature_text=vacancy_text,
                bedrijf=bedrijf or "Niet opgegeven",
                sector=sector or "Niet opgegeven"
            )

            # Call API
            response = self._call_api(prompt)

            # Extract text from response
            response_text = response['content'][0]['text']

            # Parse JSON from response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1

            if json_start < 0 or json_end <= json_start:
                logger.error("No JSON found in Claude response")
                return self._error_result("No valid JSON in response")

            analysis = json.loads(response_text[json_start:json_end])

            logger.info(f"Analysis complete: score={analysis.get('overall_score')}")

            return AnalysisResult(
                success=True,
                score=float(analysis.get('overall_score', 0)),
                score_section=analysis.get('score_section', ''),
                top_3_improvements=analysis.get('top_3_improvements', []),
                improved_text=analysis.get('improved_text', ''),
                bonus_tips=analysis.get('bonus_tips', []),
                executive_summary=analysis.get('executive_summary', ''),
                quick_wins=analysis.get('quick_wins', []),
                full_analysis=response_text,
                error=None
            )

        except json.JSONDecodeError as e:
            logger.error(f"JSON parse error: {e}")
            return self._error_result(f"JSON parse error: {e}")
        except requests.RequestException as e:
            logger.error(f"API request failed: {e}")
            return self._error_result(f"API error: {e}")
        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            return self._error_result(str(e))

    def _error_result(self, error: str) -> AnalysisResult:
        """Return error result."""
        return AnalysisResult(
            success=False,
            score=0,
            score_section="",
            top_3_improvements=[],
            improved_text="",
            bonus_tips=[],
            executive_summary="",
            quick_wins=[],
            full_analysis="",
            error=error
        )


# Convenience function
def analyze_vacancy(vacancy_text: str, bedrijf: str = "", sector: str = "") -> AnalysisResult:
    """Analyze vacancy text using Claude AI."""
    analyzer = ClaudeAnalyzer()
    return analyzer.analyze(vacancy_text, bedrijf, sector)
