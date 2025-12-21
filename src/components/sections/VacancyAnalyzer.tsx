import React, { useState } from 'react';
import { motion, AnimatePresence } from "motion/react";
import { trackEvent } from "../../lib/analytics";
import { analyzeVacancy, type AnalysisResult, type Finding, type QuickWin } from "../../lib/vacancyAnalysis";
import { Loader2, AlertTriangle, CheckCircle2, Sparkles, FileText, BarChart2, ShieldCheck, ArrowRight, Calendar, PartyPopper, Zap, TrendingUp, Lightbulb } from "lucide-react";
import { Button } from "../ui/button";

// Updated Typeform ID from user snippet
const TYPEFORM_ID = "kalFRTCA";

// Calendly URL
const CALENDLY_URL = "https://calendly.com/wouter-arts-/vacature-analyse-advies";

// Example templates
const EXAMPLE_TEMPLATES = {
  backend: `VACATURE: WERKVOORBEREIDER BOUW

Ben jij een organisatorisch talent met een passie voor bouwprojecten? Voor onze opdrachtgever in de regio Utrecht zijn wij op zoek naar een Werkvoorbereider Bouw.

Wat ga je doen?
Als Werkvoorbereider ben je de spil in het web tijdens de voorbereidings- en uitvoeringsfase van diverse bouwprojecten. Je zorgt ervoor dat alle materialen en mensen op het juiste moment op de juiste plaats zijn. Je controleert tekeningen, vraagt offertes aan en bewaakt de planning en het budget.

Takenpakket:
- Het opstellen en bewaken van projectplanningen.
- Inkopen van materialen en diensten.
- Meer- en minderwerk signaleren en verwerken.
- Contact onderhouden met leveranciers, onderaannemers en uitvoerders.

Wat vragen wij?
- Een afgeronde MBO/HBO opleiding richting Bouwkunde.
- Minimaal 3 jaar ervaring in een soortgelijke functie.
- Kennis van bouwregelgeving en moderne bouwmethodieken.
- Goede communicatieve vaardigheden.

Wat bieden wij?
- Een uitdagende baan bij een dynamisch bouwbedrijf.
- Marktconform salaris afhankelijk van ervaring.
- Goede secundaire arbeidsvoorwaarden.
- Mogelijkheden voor persoonlijke ontwikkeling.

Interesse? Stuur je CV en motivatie naar info@bouwbedrijf-voorbeeld.nl.`,

  devops: `VACATURE: MAINTENANCE ENGINEER

Voor een hightech productiebedrijf in Eindhoven zoeken wij een gedreven Maintenance Engineer. Wil jij verantwoordelijk zijn voor de betrouwbaarheid en beschikbaarheid van geavanceerde productielijnen?

Functieomschrijving:
In deze rol analyseer je storingen en prestaties van het machinepark. Je stelt onderhoudsplannen op en initieert verbetertrajecten om de uptime te verhogen. Je werkt nauw samen met de technische dienst en productie.

Verantwoordelijkheden:
- Uitvoeren van Root Cause Analyses (RCA) bij complexe storingen.
- Optimaliseren van preventief en predictief onderhoud.
- Begeleiden van modificaties en nieuwbouwprojecten.
- Beheren van technische documentatie en reserveonderdelen.

Jouw profiel:
- HBO werk- en denkniveau (Werktuigbouwkunde, Elektrotechniek of Mechatronica).
- Ervaring met onderhoudsmanagementsystemen (bijv. SAP, Ultimo).
- Analytisch sterk en proactief.
- Beheersing van de Nederlandse en Engelse taal.

Ons aanbod:
- Een salaris tussen €3.500 en €5.000 bruto per maand.
- 27 vakantiedagen en 13 ATV dagen.
- Flexibele werktijden.
- Direct een vast contract.

Solliciteren kan via de button hieronder.`,

  frontend: `VACATURE: TECHNISCH TEKENAAR / CONSTRUCTEUR

Heb jij oog voor detail en wil je werken aan innovatieve staalconstructies? Dan is deze vacature voor Technisch Tekenaar echt iets voor jou!

Over de functie:
Je vertaalt de wensen van de klant naar concrete technische tekeningen en 3D-modellen. Je berekent constructies en zorgt dat alles voldoet aan de geldende normen. Je werkt in een team van engineers en projectleiders.

Wat ga je doen?
- Maken van ontwerp-, productie- en montagetekeningen.
- Uitwerken van details en knooppunten.
- Overleggen met constructeurs en werkvoorbereiders.
- Controleren van tekeningen van derden.

Wie ben jij?
- Afgeronde MBO/HBO opleiding Civiele Techniek of Werktuigbouwkunde.
- Ervaring met Tekla Structures en/of AutoCAD.
- Je werkt nauwkeurig en gestructureerd.
- Je bent een teamspeler maar kan ook zelfstandig werken.

Wij bieden:
- Een informele werksfeer met korte lijnen.
- Goed salaris en pensioenregeling.
- Ruimte voor eigen initiatief.
- Vrijdagmiddagborrel en leuke teamuitjes.

Ben je enthousiast geworden? Reageer dan snel!`,
};

export const VacancyAnalyzer = () => {
  const [vacancyText, setVacancyText] = useState("");
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisStep, setAnalysisStep] = useState(0);
  const [showResults, setShowResults] = useState(false);
  const [showThankYou, setShowThankYou] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [isAiPowered, setIsAiPowered] = useState(false);

  const loadDemo = (type: string) => {
    // @ts-ignore
    const fullText = EXAMPLE_TEMPLATES[type] || "";
    setVacancyText(fullText);
    trackEvent('demo_clicked', { template_type: type });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (vacancyText.trim().length < 50) {
      alert('De tekst is te kort voor een goede analyse. Plak minimaal 50 karakters.');
      return;
    }

    trackEvent('initiate_checkout', { content_name: 'Recruitment Quickscan AI' });
    setIsAnalyzing(true);
    setAnalysisStep(0);
    setIsAiPowered(false);

    // Start step animation
    const stepTimer1 = setTimeout(() => setAnalysisStep(1), 1500);
    const stepTimer2 = setTimeout(() => setAnalysisStep(2), 3000);
    const stepTimer3 = setTimeout(() => setAnalysisStep(3), 4500);

    try {
      // Call Claude AI via Netlify function
      const result = await analyzeVacancy(vacancyText);

      // Clear timers and set final step
      clearTimeout(stepTimer1);
      clearTimeout(stepTimer2);
      clearTimeout(stepTimer3);
      setAnalysisStep(4);

      setAnalysisResult(result);
      setIsAiPowered(!result.error);

      // Small delay for UX before showing results
      setTimeout(() => {
        setIsAnalyzing(false);
        setShowResults(true);
        trackEvent('analysis_complete', {
          score: result.score,
          sector: result.sector,
          ai_powered: !result.error
        });
      }, 500);

    } catch (error) {
      console.error('Analysis failed:', error);
      clearTimeout(stepTimer1);
      clearTimeout(stepTimer2);
      clearTimeout(stepTimer3);

      // Fallback to basic analysis
      const fallbackResult: AnalysisResult = {
        score: 5.5,
        sector: 'general',
        sectorDisplay: 'Algemeen',
        findings: [
          { title: 'Analyse tijdelijk niet beschikbaar', description: 'Probeer het later opnieuw.', type: 'warning' }
        ],
        quickWins: [],
        fullAnalysis: 'De AI analyse is tijdelijk niet beschikbaar.',
        error: 'API niet bereikbaar'
      };
      setAnalysisResult(fallbackResult);
      setIsAnalyzing(false);
      setShowResults(true);
    }
  };

  const openFullAnalysisForm = () => {
    const encodedText = encodeURIComponent(vacancyText.substring(0, 1500));
    const typeformUrl = `https://form.typeform.com/to/${TYPEFORM_ID}#vacature_text=${encodedText}`;

    trackEvent('typeform_redirect', { device: 'all' });

    // Always open in new tab - most reliable method
    const newWindow = window.open(typeformUrl, '_blank');

    // If popup blocked, redirect current page
    if (!newWindow) {
      window.location.href = typeformUrl;
    }

    // Show thank you after short delay (user will fill form in new tab)
    setTimeout(() => {
      setShowResults(false);
      setShowThankYou(true);
      trackEvent('complete_registration', { content_name: 'Recruitment Quickscan' });
    }, 2000);
  };

  const openCalendly = () => {
    trackEvent('calendly_click', { source: 'thank_you_screen' });
    window.open(CALENDLY_URL, '_blank');
  };

  return (
    <section className="py-24 relative overflow-hidden bg-slate-50" id="analyse-tool">
      
      {/* Static Clean Background */}
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none opacity-40">
         <div className="absolute -top-[400px] -right-[300px] w-[800px] h-[800px] bg-gradient-to-br from-orange-100/40 to-blue-50/40 rounded-full blur-3xl" />
         <div className="absolute top-1/2 -left-[200px] w-[600px] h-[600px] bg-gradient-to-tr from-blue-50/50 to-slate-100/50 rounded-full blur-3xl" />
      </div>

      <div className="container mx-auto px-4 md:px-6 relative z-10">
        
        {/* Header */}
        <div className="text-center max-w-3xl mx-auto mb-12">
          <h2 className="text-4xl md:text-5xl lg:text-6xl font-black mb-6 tracking-tight leading-[1.1] text-slate-900">
            Waarom solliciteert <span className="relative inline-block text-transparent bg-clip-text bg-gradient-to-r from-orange-500 to-red-600">niemand?</span>
          </h2>
          <p className="text-xl leading-relaxed font-medium max-w-2xl mx-auto text-slate-600">
            Plak je vacaturetekst hieronder en ontdek direct welke <strong>12 conversie-killers</strong> jouw kandidaten wegjagen.
          </p>
        </div>

        {/* Main Analysis Card */}
        <div className="p-1 md:p-2 max-w-5xl mx-auto relative transition-all duration-500 bg-white shadow-[0_20px_50px_-12px_rgba(0,0,0,0.1)] border border-slate-200 rounded-3xl">
          <div className="p-6 md:p-10 lg:p-12 rounded-2xl">
            
            <form onSubmit={handleSubmit} className="relative">
              <div className="relative group">
                <textarea
                  value={vacancyText}
                  onChange={(e) => setVacancyText(e.target.value)}
                  placeholder="Plak hier je vacaturetekst (of URL)..."
                  maxLength={8000}
                  className="relative w-full min-h-[280px] p-6 md:p-8 font-sans text-base md:text-lg leading-relaxed resize-y transition-all outline-none shadow-inner bg-white border-slate-200 focus:border-orange-500 focus:ring-4 focus:ring-orange-500/10 text-slate-900 placeholder:text-slate-400 rounded-2xl"
                  required
                />
                
                {vacancyText.length === 0 && (
                  <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 pointer-events-none opacity-60 flex flex-col items-center gap-3">
                    <div className="w-12 h-12 rounded-xl flex items-center justify-center border bg-white border-slate-200 text-slate-400">
                      <FileText className="w-6 h-6" />
                    </div>
                    <span className="text-sm font-semibold text-slate-400">Plak je tekst hier</span>
                  </div>
                )}
              </div>

              <div className="flex flex-col md:flex-row justify-between items-center mt-6 gap-6">
                {/* Examples */}
                <div className="flex items-center gap-3 w-full md:w-auto overflow-x-auto pb-2 md:pb-0">
                  <span className="text-xs font-bold uppercase tracking-wider whitespace-nowrap text-slate-400">Probeer een demo:</span>
                  <div className="flex gap-2">
                    {['backend', 'devops', 'frontend'].map((type) => (
                      <button 
                        key={type}
                        type="button" 
                        onClick={() => loadDemo(type as any)} 
                        className="whitespace-nowrap px-3 py-1.5 text-xs font-semibold transition-all shadow-sm bg-white border border-slate-200 hover:border-orange-300 text-slate-600"
                      >
                        {type === 'backend' ? 'Bouw' : type === 'devops' ? 'Techniek' : 'Engineering'}
                      </button>
                    ))}
                  </div>
                </div>

                <div className="flex flex-col sm:flex-row items-center gap-4 w-full md:w-auto">
                   <span className={`text-xs font-bold transition-colors ${vacancyText.length > 50 ? "text-emerald-600" : "text-slate-400"}`}>
                    {vacancyText.length} tekens
                   </span>
                   <Button 
                    type="submit"
                    disabled={isAnalyzing || vacancyText.length < 10}
                    className="w-full sm:w-auto h-auto py-4 px-8 text-lg font-bold transition-all bg-slate-900 hover:bg-slate-800 text-white shadow-xl shadow-slate-900/20 rounded-xl border-0"
                  >
                    {isAnalyzing ? (
                      <span className="flex items-center gap-3"><Loader2 className="animate-spin" /> Analyseren...</span>
                    ) : (
                      <span className="flex items-center gap-3">Start Analyse <ArrowRight className="w-5 h-5" /></span>
                    )}
                  </Button>
                </div>
              </div>
            </form>
          </div>
        </div>
        
        <p className="text-center text-xs mt-8 flex justify-center items-center gap-2 font-medium text-slate-400">
          <ShieldCheck className="w-3.5 h-3.5" /> Wij respecteren je privacy. Je data wordt niet opgeslagen.
        </p>
      </div>

      {/* Loading Modal */}
      <AnimatePresence>
        {isAnalyzing && (
          <motion.div
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-slate-900/80 backdrop-blur-sm"
          >
            <div className="bg-white rounded-3xl p-8 max-w-lg w-full text-center shadow-2xl">
              <div className="relative w-16 h-16 mx-auto mb-6">
                <Loader2 className="w-16 h-16 animate-spin text-orange-600" />
                <Sparkles className="w-6 h-6 text-orange-500 absolute top-0 right-0 animate-pulse" />
              </div>
              <h3 className="text-2xl font-black text-slate-900 mb-2">AI Analyse bezig...</h3>
              <p className="text-slate-600 mb-8">Claude AI scant je vacature op 12+ conversie-factoren.</p>
              <div className="space-y-3 max-w-xs mx-auto text-left">
                 <Step active={analysisStep >= 0} label="Vacature parsen" />
                 <Step active={analysisStep >= 1} label="Sector detecteren" />
                 <Step active={analysisStep >= 2} label="Conversie-killers vinden" />
                 <Step active={analysisStep >= 3} label="Quick wins genereren" />
                 <Step active={analysisStep >= 4} label="Rapport opstellen" />
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Results Modal */}
      <AnimatePresence>
        {showResults && analysisResult && (
          <motion.div
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            className="fixed inset-0 bg-slate-900/90 z-[100] flex items-center justify-center p-4 backdrop-blur-md overflow-y-auto"
          >
            <motion.div
              initial={{ scale: 0.95, opacity: 0 }} animate={{ scale: 1, opacity: 1 }}
              className="bg-white rounded-2xl p-6 md:p-8 max-w-3xl w-full shadow-2xl relative my-4 max-h-[90vh] overflow-y-auto"
            >
              <button onClick={() => setShowResults(false)} className="absolute top-4 right-4 text-slate-400 hover:text-slate-600 z-10">✕</button>

              {/* Header with Score */}
              <div className="text-center mb-8 border-b border-slate-100 pb-6">
                 <div className="flex items-center justify-center gap-2 mb-3">
                   {isAiPowered && (
                     <span className="inline-flex items-center gap-1 px-3 py-1 bg-gradient-to-r from-purple-500 to-indigo-500 text-white text-xs font-bold rounded-full">
                       <Sparkles className="w-3 h-3" /> AI-Powered
                     </span>
                   )}
                   <span className="inline-flex items-center gap-1 px-3 py-1 bg-slate-100 text-slate-600 text-xs font-bold rounded-full">
                     {analysisResult.sectorDisplay}
                   </span>
                 </div>
                 <div className={`inline-flex items-center justify-center w-24 h-24 rounded-full text-4xl font-black border-4 mb-4 ${analysisResult.score >= 7 ? 'border-emerald-200 text-emerald-600 bg-emerald-50' : analysisResult.score >= 5 ? 'border-orange-200 text-orange-600 bg-orange-50' : 'border-red-200 text-red-600 bg-red-50'}`}>
                    {analysisResult.score.toFixed(1)}
                 </div>
                 <h2 className="text-2xl font-black text-slate-900">
                    {analysisResult.score >= 7 ? "Sterke basis! Nog enkele verbeterpunten." : analysisResult.score >= 5 ? "Gemiste kansen gedetecteerd" : "Urgente verbetering nodig"}
                 </h2>
                 <p className="text-slate-600 mt-2">
                    {isAiPowered ? "AI-analyse van jouw vacaturetekst" : "Basisanalyse van jouw vacaturetekst"}
                 </p>
              </div>

              {/* Findings */}
              <div className="mb-8">
                <h3 className="text-lg font-bold text-slate-900 mb-4 flex items-center gap-2">
                  <AlertTriangle className="w-5 h-5 text-orange-500" /> Bevindingen
                </h3>
                <div className="space-y-3">
                  {analysisResult.findings.map((finding, idx) => (
                     <div key={idx} className={`p-4 rounded-xl border flex gap-3 ${finding.type === 'success' ? 'bg-emerald-50 border-emerald-100 text-emerald-900' : finding.type === 'error' ? 'bg-red-50 border-red-100 text-red-900' : 'bg-orange-50 border-orange-100 text-orange-900'}`}>
                        <div className="shrink-0 mt-0.5">
                          {finding.type === 'success' ? <CheckCircle2 className="w-5 h-5 text-emerald-600" /> : finding.type === 'error' ? <AlertTriangle className="w-5 h-5 text-red-500" /> : <AlertTriangle className="w-5 h-5 text-orange-500" />}
                        </div>
                        <div className="flex-1">
                          <div className="font-bold text-sm flex items-center justify-between">
                            {finding.title}
                            {finding.impactPercentage && (
                              <span className="text-xs font-normal opacity-75">-{finding.impactPercentage}% sollicitaties</span>
                            )}
                          </div>
                          <div className="text-sm opacity-90 mt-1">{finding.description}</div>
                        </div>
                     </div>
                  ))}
                </div>
              </div>

              {/* Quick Wins */}
              {analysisResult.quickWins && analysisResult.quickWins.length > 0 && (
                <div className="mb-8">
                  <h3 className="text-lg font-bold text-slate-900 mb-4 flex items-center gap-2">
                    <Zap className="w-5 h-5 text-yellow-500" /> Quick Wins
                  </h3>
                  <div className="space-y-3">
                    {analysisResult.quickWins.map((win, idx) => (
                       <div key={idx} className="p-4 rounded-xl border border-slate-200 bg-gradient-to-r from-slate-50 to-white">
                          <div className="flex items-start justify-between gap-3">
                            <div className="flex-1">
                              <div className="font-bold text-sm text-slate-900 flex items-center gap-2">
                                <Lightbulb className="w-4 h-4 text-yellow-500" />
                                {win.action}
                              </div>
                              {win.implementation && (
                                <div className="text-sm text-slate-600 mt-2 p-3 bg-white rounded-lg border border-slate-100 font-mono text-xs">
                                  {win.implementation}
                                </div>
                              )}
                            </div>
                            {win.expectedImprovement > 0 && (
                              <div className="shrink-0 flex items-center gap-1 text-emerald-600 font-bold text-sm">
                                <TrendingUp className="w-4 h-4" />
                                +{win.expectedImprovement}%
                              </div>
                            )}
                          </div>
                       </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Rewritten Intro */}
              {analysisResult.rewrittenIntro && (
                <div className="mb-8">
                  <h3 className="text-lg font-bold text-slate-900 mb-4 flex items-center gap-2">
                    <Sparkles className="w-5 h-5 text-purple-500" /> Verbeterde Opening
                  </h3>
                  <div className="p-4 rounded-xl border-2 border-purple-200 bg-purple-50">
                    <p className="text-slate-800 italic">"{analysisResult.rewrittenIntro}"</p>
                  </div>
                </div>
              )}

              {/* CTA */}
              <div className="bg-slate-900 text-white p-6 rounded-xl text-center relative overflow-hidden">
                 <div className="relative z-10">
                    <h4 className="font-bold text-lg mb-2">Volledige optimalisatie ontvangen?</h4>
                    <p className="text-slate-300 text-sm mb-4">Ontvang je compleet herschreven vacaturetekst + persoonlijk advies.</p>
                    <button
                      onClick={openFullAnalysisForm}
                      className="bg-orange-600 hover:bg-orange-500 text-white font-bold w-full py-4 px-6 rounded-lg text-base sm:text-lg transition-colors flex items-center justify-center gap-2"
                    >
                      <Calendar className="w-5 h-5" />
                      Gratis adviesgesprek plannen
                    </button>
                 </div>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Thank You Modal */}
      <AnimatePresence>
        {showThankYou && (
          <motion.div
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            className="fixed inset-0 bg-slate-900/90 z-[100] flex items-center justify-center p-4 backdrop-blur-md"
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }} animate={{ scale: 1, opacity: 1 }}
              className="bg-white rounded-2xl p-8 md:p-10 max-w-md w-full shadow-2xl relative text-center"
            >
              <button
                onClick={() => setShowThankYou(false)}
                className="absolute top-4 right-4 text-slate-400 hover:text-slate-600"
              >
                ✕
              </button>

              <div className="w-20 h-20 bg-emerald-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <PartyPopper className="w-10 h-10 text-emerald-600" />
              </div>

              <h2 className="text-2xl md:text-3xl font-black text-slate-900 mb-3">
                Bedankt voor je aanvraag!
              </h2>

              <p className="text-slate-600 mb-8">
                Je ontvangt binnen <strong>24 uur</strong> je geoptimaliseerde vacaturetekst per e-mail.
              </p>

              <div className="bg-slate-50 rounded-xl p-6 mb-6">
                <h3 className="font-bold text-slate-900 mb-2 flex items-center justify-center gap-2">
                  <Calendar className="w-5 h-5 text-orange-600" />
                  Wil je sneller resultaat?
                </h3>
                <p className="text-sm text-slate-600 mb-4">
                  Plan een gratis 15-minuten gesprek en ontvang direct persoonlijk advies.
                </p>
                <button
                  onClick={openCalendly}
                  className="w-full bg-orange-600 hover:bg-orange-500 text-white font-bold py-4 px-6 rounded-lg transition-colors flex items-center justify-center gap-2"
                >
                  <Calendar className="w-5 h-5" />
                  Plan een gesprek
                </button>
              </div>

              <button
                onClick={() => setShowThankYou(false)}
                className="text-sm text-slate-500 hover:text-slate-700 underline"
              >
                Sluiten
              </button>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

    </section>
  );
};

const Step = ({ active, label }: { active: boolean, label: string }) => (
  <div className={`flex items-center gap-3 text-sm transition-colors ${active ? 'text-slate-900 font-bold' : 'text-slate-400'}`}>
    <div className={`w-6 h-6 rounded-full flex items-center justify-center text-xs ${active ? 'bg-orange-600 text-white' : 'bg-slate-100'}`}>
        {active ? <CheckCircle2 className="w-3.5 h-3.5" /> : null}
    </div>
    {label}
  </div>
);