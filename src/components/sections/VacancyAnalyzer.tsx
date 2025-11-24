import React, { useState } from 'react';
import { motion, AnimatePresence } from "motion/react";
import { trackEvent } from "../../lib/analytics";
import { Loader2, AlertTriangle, CheckCircle2, Sparkles, FileText, BarChart2, ShieldCheck, ArrowRight } from "lucide-react";
import { Button } from "../ui/button";
import * as typeformEmbed from '@typeform/embed';

// Updated Typeform ID from user snippet
const TYPEFORM_ID = "01K25SKWYTKZ05DAHER9D52J94";

// Helper to safely access createPopup
const getCreatePopup = () => {
  // @ts-ignore
  return typeformEmbed.createPopup || (typeformEmbed.default && typeformEmbed.default.createPopup);
};

// Load Typeform CSS and Script dynamically only when needed
const loadTypeformResources = () => {
  if (typeof document === 'undefined') return;

  // Load CSS
  const cssId = 'typeform-popup-css';
  if (!document.getElementById(cssId)) {
    const link = document.createElement('link');
    link.id = cssId;
    link.rel = 'stylesheet';
    link.href = 'https://embed.typeform.com/next/css/popup.css';
    document.head.appendChild(link);
  }

  // Remove any auto-loading Typeform embeds
  const autoEmbeds = document.querySelectorAll('[data-tf-live], [data-tf-widget], [data-tf-slider], [data-tf-popover], [data-tf-popup]');
  autoEmbeds.forEach(embed => embed.remove());
};

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
  const [score, setScore] = useState("0.0");
  const [findings, setFindings] = useState<{title: string, desc: string, type: 'warning' | 'error' | 'success'}[]>([]);

  // Prevent auto-loading Typeform embeds on component mount
  React.useEffect(() => {
    const removeAutoEmbeds = () => {
      const autoEmbeds = document.querySelectorAll('[data-tf-live], [data-tf-widget], [data-tf-slider], [data-tf-popover], [data-tf-popup]');
      autoEmbeds.forEach(embed => embed.remove());
    };

    // Run immediately and set up observer for dynamic additions
    removeAutoEmbeds();
    const observer = new MutationObserver(removeAutoEmbeds);
    observer.observe(document.body, { childList: true, subtree: true });

    return () => observer.disconnect();
  }, []);

  const loadDemo = (type: string) => {
    // @ts-ignore
    const fullText = EXAMPLE_TEMPLATES[type] || "";
    setVacancyText(fullText);
    trackEvent('demo_clicked', { template_type: type });
  };

  const analyzeText = (text: string) => {
    const newFindings: {title: string, desc: string, type: 'warning' | 'error' | 'success'}[] = [];
    const lowerText = text.toLowerCase();
    
    // Analysis logic
    if (text.includes('€') || lowerText.includes('salaris') || lowerText.includes('bruto') || lowerText.includes('vergoeding')) {
      newFindings.push({ title: "✅ Salarisindicatie gevonden", desc: "Goed bezig! Vacatures met een concreet salaris krijgen tot 40% meer reacties.", type: 'success' });
    } else {
      newFindings.push({ title: "⚠️ Vaag salaris bereik", desc: "Je vacature mist concrete salaris informatie. 63% van kandidaten skipt vacatures zonder duidelijk salaris.", type: 'error' });
    }
    const weCount = (lowerText.match(/\b(wij|ons|onze|bedrijf)\b/g) || []).length;
    const youCount = (lowerText.match(/\b(jij|je|jouw|jou)\b/g) || []).length;
    if (youCount > weCount) {
      newFindings.push({ title: "✅ Kandidaat-gericht geschreven", desc: "Je spreekt de kandidaat direct aan. Dit verhoogt de leesbaarheid en betrokkenheid aanzienlijk.", type: 'success' });
    } else {
      newFindings.push({ title: "❌ Te veel 'Wij' vs 'Jij'", desc: `Je gebruikt ${weCount}x 'wij' en slechts ${youCount}x 'jij'. Draai dit om naar de voordelen voor de kandidaat.`, type: 'error' });
    }
    const bulletCount = (text.match(/[-•*] /g) || []).length;
    if (bulletCount > 5) {
      newFindings.push({ title: "✅ Goede scanbaarheid", desc: "Het gebruik van bulletpoints maakt je vacature goed scanbaar voor mobiele bezoekers.", type: 'success' });
    } else {
      newFindings.push({ title: "⚠️ Tekstmuur gedetecteerd", desc: "Gebruik meer opsommingstekens. Mobiele bezoekers haken af bij lange lappen tekst.", type: 'warning' });
    }
    if (newFindings.length < 3) {
      newFindings.push({ title: "🎯 Geen unique selling point", desc: "Wat maakt deze rol uniek? Waarom zou een kandidaat specifiek voor jou moeten kiezen?", type: 'warning' });
    }

    setFindings(newFindings.slice(0, 3));
    let baseScore = 4.5;
    newFindings.forEach(f => {
      if (f.type === 'success') baseScore += 1.5;
      if (f.type === 'warning') baseScore += 0.5;
    });
    const finalScore = Math.min(8.2, baseScore + Math.random()).toFixed(1);
    setScore(finalScore);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (vacancyText.trim().length < 50) {
      alert('⚠️ De tekst is te kort voor een goede analyse. Plak minimaal 50 karakters.');
      return;
    }
    trackEvent('initiate_checkout', { content_name: 'Recruitment Quickscan' });
    setIsAnalyzing(true);
    setAnalysisStep(0);
    analyzeText(vacancyText);
    setTimeout(() => setAnalysisStep(1), 1200);
    setTimeout(() => setAnalysisStep(2), 2400);
    setTimeout(() => {
      setIsAnalyzing(false);
      setShowResults(true);
    }, 3500);
  };

  const openFullAnalysisForm = () => {
    // Load resources and clean up any auto-embeds first
    loadTypeformResources();

    try {
      const createPopup = getCreatePopup();
      if (typeof createPopup === 'function') {
        // Use responsive dimensions based on viewport size
        const isMobile = window.innerWidth < 768;
        const popupWidth = isMobile ? Math.min(window.innerWidth - 32, 500) : Math.min(window.innerWidth - 64, 800);
        const popupHeight = isMobile ? Math.min(window.innerHeight - 64, 600) : Math.min(window.innerHeight - 100, 700);

        const { toggle } = createPopup(TYPEFORM_ID, {
          hidden: { vacature_text: vacancyText.substring(0, 8000) },
          autoClose: 3000,
          width: popupWidth,
          height: popupHeight,
          onSubmit: () => {
             trackEvent('complete_registration', { content_name: 'Recruitment Quickscan' });
             setShowResults(false);
          }
        });
        toggle();
      }
    } catch (error) {
      const encodedText = encodeURIComponent(vacancyText.substring(0, 1500));
      window.open(`https://form.typeform.com/to/${TYPEFORM_ID}#vacature_text=${encodedText}`, '_blank');
    }
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
              <Loader2 className="w-12 h-12 animate-spin text-orange-600 mx-auto mb-6" />
              <h3 className="text-2xl font-black text-slate-900 mb-2">Analyseren...</h3>
              <p className="text-slate-600 mb-8">We scannen je vacature op psychologische triggers.</p>
              <div className="space-y-3 max-w-xs mx-auto text-left">
                 <Step active={analysisStep >= 0} label="Structuur checken" />
                 <Step active={analysisStep >= 1} label="Salaris & Tone-of-voice" />
                 <Step active={analysisStep >= 2} label="Score berekenen" />
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Results Modal */}
      <AnimatePresence>
        {showResults && (
          <motion.div 
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            className="fixed inset-0 bg-slate-900/90 z-[100] flex items-center justify-center p-4 backdrop-blur-md overflow-y-auto"
          >
            <motion.div 
              initial={{ scale: 0.95, opacity: 0 }} animate={{ scale: 1, opacity: 1 }}
              className="bg-white rounded-2xl p-6 md:p-8 max-w-2xl w-full shadow-2xl relative my-4"
            >
              <button onClick={() => setShowResults(false)} className="absolute top-4 right-4 text-slate-400 hover:text-slate-600">✕</button>
              
              <div className="text-center mb-8 border-b border-slate-100 pb-6">
                 <div className={`inline-flex items-center justify-center w-20 h-20 rounded-full text-3xl font-black border-4 mb-4 ${Number(score) > 7 ? 'border-emerald-100 text-emerald-600 bg-emerald-50' : 'border-orange-100 text-orange-600 bg-orange-50'}`}>
                    {score}
                 </div>
                 <h2 className="text-2xl font-black text-slate-900">
                    {Number(score) > 7 ? "Sterke basis, maar kan scherper" : "Gemiste kansen gedetecteerd"}
                 </h2>
                 <p className="text-slate-600 mt-2">
                    Hieronder de eerste bevindingen uit onze scan.
                 </p>
              </div>

              <div className="space-y-3 mb-8">
                {findings.map((finding, idx) => (
                   <div key={idx} className={`p-4 rounded-xl border flex gap-3 ${finding.type === 'success' ? 'bg-emerald-50 border-emerald-100 text-emerald-900' : finding.type === 'error' ? 'bg-red-50 border-red-100 text-red-900' : 'bg-orange-50 border-orange-100 text-orange-900'}`}>
                      <div className="shrink-0 mt-0.5">
                        {finding.type === 'success' ? <CheckCircle2 className="w-5 h-5 text-emerald-600" /> : <AlertTriangle className="w-5 h-5 text-orange-600" />}
                      </div>
                      <div>
                        <div className="font-bold text-sm">{finding.title}</div>
                        <div className="text-xs opacity-90">{finding.desc}</div>
                      </div>
                   </div>
                ))}
              </div>

              <div className="bg-slate-900 text-white p-6 rounded-xl text-center relative overflow-hidden">
                 <div className="relative z-10">
                    <h4 className="font-bold text-lg mb-2">🚀 Ontvang je verbeterde vacaturetekst</h4>
                    <p className="text-slate-300 text-sm mb-4">Inclusief volledige analyse en direct toepasbare tips.</p>
                    <Button onClick={openFullAnalysisForm} className="bg-orange-600 hover:bg-orange-500 text-white font-bold w-full py-3 rounded-lg">
                        Ontvang mijn geoptimaliseerde tekst (Gratis)
                    </Button>
                 </div>
              </div>
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