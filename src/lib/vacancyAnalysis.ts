// ===============================================
// Vacancy Analysis Service - Claude AI Integration
// Real-time AI-powered vacancy optimization
// ===============================================

export interface AnalysisResult {
  score: number;
  sector: string;
  sectorDisplay: string;
  findings: Finding[];
  quickWins: QuickWin[];
  rewrittenIntro?: string;
  fullAnalysis: string;
  error?: string;
}

export interface Finding {
  title: string;
  description: string;
  type: 'success' | 'warning' | 'error';
  impactPercentage?: number;
}

export interface QuickWin {
  action: string;
  expectedImprovement: number;
  implementation: string;
}

// Analysis prompt based on the Python TECHNICAL_MASTER_PROMPT
const ANALYSIS_PROMPT = `
# NEDERLANDSE TECHNISCHE & INDUSTRIELE VACATURE ANALYSE EXPERT

Je bent een senior vacature-analyse specialist. Analyseer de onderstaande vacature en geef een gestructureerde beoordeling.

## ANALYSE CRITERIA

1. **FUNCTIETITEL** - Is de titel SEO-geoptimaliseerd en herkenbaar?
2. **SALARIS TRANSPARANTIE** - Concrete salary range vermeld?
3. **TECHNISCHE CHALLENGE** - Concrete projecten en technologieën genoemd?
4. **CANDIDATE FOCUS** - Wordt de kandidaat aangesproken (jij vs wij)?
5. **SCANBAARHEID** - Bullet points en structuur?
6. **UNIQUE SELLING POINTS** - Wat maakt deze rol uniek?

## VEREIST JSON OUTPUT FORMAT

Geef ALLEEN valid JSON terug, geen andere tekst:

{
  "score": 7.5,
  "sector": "manufacturing",
  "sectorDisplay": "Manufacturing / Productie",
  "findings": [
    {
      "title": "Geen salarisindicatie",
      "description": "63% van kandidaten skipt vacatures zonder duidelijk salaris. Voeg toe: EUR 45.000 - 55.000",
      "type": "error",
      "impactPercentage": 35
    },
    {
      "title": "Goede candidate focus",
      "description": "Je spreekt de kandidaat direct aan met 'jij'. Dit verhoogt betrokkenheid.",
      "type": "success"
    },
    {
      "title": "Vage functievereisten",
      "description": "Specificeer concrete tools/systemen in plaats van 'relevante ervaring'.",
      "type": "warning",
      "impactPercentage": 15
    }
  ],
  "quickWins": [
    {
      "action": "Voeg concrete salarisindicatie toe",
      "expectedImprovement": 35,
      "implementation": "Salaris: EUR 45.000 - 55.000 bruto per jaar, afhankelijk van ervaring"
    },
    {
      "action": "Specificeer technische tools",
      "expectedImprovement": 15,
      "implementation": "Ervaring met SAP, AutoCAD, of vergelijkbare systemen"
    }
  ],
  "rewrittenIntro": "Als [Functie] bij [Bedrijf] werk je aan [concrete projecten]. Je verdient EUR XX.XXX - XX.XXX en krijgt [benefits].",
  "fullAnalysis": "Samenvatting van de analyse..."
}

## TE ANALYSEREN VACATURE:
`;

/**
 * Analyze a vacancy using Claude AI via Netlify Function
 */
export async function analyzeVacancy(vacancyText: string): Promise<AnalysisResult> {
  try {
    const prompt = ANALYSIS_PROMPT + vacancyText;

    const response = await fetch('/.netlify/functions/claude-analyze', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        prompt,
        max_tokens: 2000,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      console.error('Analysis API error:', errorData);

      // Return fallback analysis on error
      return getFallbackAnalysis(vacancyText, errorData.message || 'API niet beschikbaar');
    }

    const data = await response.json();

    if (!data.content || !data.content[0] || !data.content[0].text) {
      console.error('Invalid API response format');
      return getFallbackAnalysis(vacancyText, 'Ongeldig API response');
    }

    // Parse the JSON response from Claude
    const analysisText = data.content[0].text;

    try {
      // Extract JSON from response (Claude might add some text around it)
      const jsonMatch = analysisText.match(/\{[\s\S]*\}/);
      if (!jsonMatch) {
        console.error('No JSON found in response:', analysisText);
        return getFallbackAnalysis(vacancyText, 'Geen JSON in response');
      }

      const analysis = JSON.parse(jsonMatch[0]);

      // Validate and normalize the response
      return {
        score: Math.min(10, Math.max(0, Number(analysis.score) || 5)),
        sector: analysis.sector || 'general',
        sectorDisplay: analysis.sectorDisplay || 'Algemeen',
        findings: (analysis.findings || []).map((f: any) => ({
          title: f.title || 'Bevinding',
          description: f.description || f.desc || '',
          type: validateFindingType(f.type),
          impactPercentage: f.impactPercentage || f.impact_percentage,
        })),
        quickWins: (analysis.quickWins || analysis.week1_quick_wins || []).map((w: any) => ({
          action: w.action || '',
          expectedImprovement: w.expectedImprovement || w.expected_improvement || 0,
          implementation: w.implementation || '',
        })),
        rewrittenIntro: analysis.rewrittenIntro || analysis.rewritten_intro,
        fullAnalysis: analysis.fullAnalysis || analysis.full_analysis || '',
      };
    } catch (parseError) {
      console.error('Failed to parse Claude response:', parseError);
      return getFallbackAnalysis(vacancyText, 'Parse error');
    }
  } catch (error) {
    console.error('Analysis request failed:', error);
    return getFallbackAnalysis(vacancyText, 'Netwerk fout');
  }
}

function validateFindingType(type: string): 'success' | 'warning' | 'error' {
  if (type === 'success' || type === 'warning' || type === 'error') {
    return type;
  }
  return 'warning';
}

/**
 * Fallback analysis when API is unavailable
 * Uses basic heuristics similar to original implementation
 */
function getFallbackAnalysis(text: string, errorReason: string): AnalysisResult {
  const lowerText = text.toLowerCase();
  const findings: Finding[] = [];

  // Salary check
  if (text.includes('€') || lowerText.includes('salaris') || lowerText.includes('bruto')) {
    findings.push({
      title: '✅ Salarisindicatie gevonden',
      description: 'Vacatures met een concreet salaris krijgen tot 40% meer reacties.',
      type: 'success',
    });
  } else {
    findings.push({
      title: '❌ Geen salarisindicatie',
      description: '63% van kandidaten skipt vacatures zonder duidelijk salaris.',
      type: 'error',
      impactPercentage: 35,
    });
  }

  // Wij vs Jij check
  const weCount = (lowerText.match(/\b(wij|ons|onze)\b/g) || []).length;
  const youCount = (lowerText.match(/\b(jij|je|jouw)\b/g) || []).length;

  if (youCount > weCount) {
    findings.push({
      title: '✅ Kandidaat-gericht geschreven',
      description: 'Je spreekt de kandidaat direct aan. Dit verhoogt betrokkenheid.',
      type: 'success',
    });
  } else {
    findings.push({
      title: '⚠️ Te veel "Wij" focus',
      description: `${weCount}x 'wij' vs ${youCount}x 'jij'. Draai dit om naar kandidaat voordelen.`,
      type: 'warning',
      impactPercentage: 20,
    });
  }

  // Bullet points check
  const bulletCount = (text.match(/[-•*]\s/g) || []).length;
  if (bulletCount > 5) {
    findings.push({
      title: '✅ Goede scanbaarheid',
      description: 'Bullet points maken je vacature goed leesbaar op mobiel.',
      type: 'success',
    });
  } else {
    findings.push({
      title: '⚠️ Weinig structuur',
      description: 'Gebruik meer opsommingstekens voor betere leesbaarheid.',
      type: 'warning',
      impactPercentage: 15,
    });
  }

  // Calculate score
  let score = 5.0;
  findings.forEach(f => {
    if (f.type === 'success') score += 1.2;
    if (f.type === 'warning') score += 0.3;
    if (f.type === 'error') score -= 0.5;
  });
  score = Math.min(8.5, Math.max(3.0, score));

  return {
    score: Number(score.toFixed(1)),
    sector: 'general',
    sectorDisplay: 'Technisch',
    findings: findings.slice(0, 3),
    quickWins: [
      {
        action: 'Voeg salaris range toe',
        expectedImprovement: 35,
        implementation: 'Bijvoorbeeld: EUR 45.000 - 60.000 bruto per jaar',
      },
      {
        action: 'Meer "jij" gebruiken',
        expectedImprovement: 20,
        implementation: 'Begin zinnen met "Jij..." in plaats van "Wij zoeken..."',
      },
    ],
    fullAnalysis: `Basisanalyse uitgevoerd (${errorReason}). Voor een volledige AI-analyse, probeer het later opnieuw.`,
    error: errorReason,
  };
}
