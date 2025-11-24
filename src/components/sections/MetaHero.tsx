import { Upload, ArrowRight, CheckCircle2 } from 'lucide-react';

export const MetaHero = () => {
  const scrollToAnalyzer = () => {
    const analyzerSection = document.getElementById('analyse-tool');
    if (analyzerSection) {
      analyzerSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
      setTimeout(() => {
        const textarea = analyzerSection.querySelector('textarea');
        if (textarea) {
          textarea.focus();
        }
      }, 800);
    }
  };

  return (
    <section className="relative pt-20 pb-32 md:pt-28 md:pb-40 bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white overflow-hidden">
      {/* Background Effects */}
      <div className="absolute inset-0 opacity-30 pointer-events-none"
           style={{
             backgroundImage: `
               linear-gradient(30deg, rgba(255,255,255,0.03) 12%, transparent 12.5%, transparent 87%, rgba(255,255,255,0.03) 87.5%),
               linear-gradient(150deg, rgba(255,255,255,0.03) 12%, transparent 12.5%, transparent 87%, rgba(255,255,255,0.03) 87.5%)
             `,
             backgroundSize: '80px 140px'
           }}
      />

      {/* Gradient Glow */}
      <div className="absolute -bottom-1/2 left-1/2 -translate-x-1/2 w-[800px] h-[800px] bg-[radial-gradient(circle,rgba(255,107,53,0.2)_0%,transparent_70%)] pointer-events-none animate-pulse" />

      {/* Fade Out at Bottom */}
      <div className="absolute bottom-0 left-0 right-0 h-48 bg-gradient-to-b from-transparent via-slate-900/50 to-slate-900/0 pointer-events-none" />

      <div className="container mx-auto px-4 md:px-6 relative z-10 text-center">

        {/* Badge */}
        <div className="inline-flex items-center gap-2 px-4 py-2 bg-orange-500/10 border border-orange-500/30 rounded-full text-orange-400 text-sm font-bold mb-8">
          <CheckCircle2 className="w-4 h-4" />
          Speciaal voor Meta Adverteerders
        </div>

        {/* Headline */}
        <h1 className="text-4xl md:text-6xl lg:text-7xl font-black text-white mb-6 leading-[1.1] max-w-5xl mx-auto">
          Stop met geld verspillen aan <span className="text-transparent bg-clip-text bg-gradient-to-r from-orange-500 to-orange-400">slechte vacatureteksten</span>
        </h1>

        {/* Subheadline */}
        <p className="text-xl md:text-2xl font-semibold text-slate-200/90 max-w-3xl mx-auto mb-8 leading-relaxed">
          Jouw Meta advertenties presteren niet door één simpele reden: je vacaturetekst converteert niet.
        </p>

        {/* Value Proposition */}
        <div className="max-w-2xl mx-auto mb-12 bg-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-2xl p-8">
          <p className="text-lg text-slate-300 leading-relaxed mb-6">
            <strong className="text-white">Gemiddelde Meta adverteerder:</strong> betaalt €5-15 per klik en verliest 80% van de bezoekers door een slechte vacaturetekst.
          </p>
          <p className="text-lg text-orange-400 font-bold">
            Upload je vacature en ontdek binnen 24 uur hoe je 2-3x meer sollicitaties krijgt uit dezelfde clicks.
          </p>
        </div>

        {/* CTA Button */}
        <div className="flex justify-center mb-12">
          <button
            onClick={scrollToAnalyzer}
            className="group relative px-10 py-6 bg-gradient-to-r from-orange-600 to-orange-500 hover:from-orange-500 hover:to-orange-400 text-white rounded-2xl shadow-2xl shadow-orange-600/40 hover:shadow-orange-500/50 transition-all duration-300 hover:scale-105 hover:-translate-y-1"
          >
            <span className="flex items-center gap-3 font-black text-xl">
              <Upload className="w-7 h-7 group-hover:animate-bounce" />
              Analyseer Nu Gratis
              <ArrowRight className="w-6 h-6 group-hover:translate-x-1 transition-transform" />
            </span>
          </button>
        </div>

        {/* Social Proof */}
        <div className="flex flex-wrap justify-center gap-x-10 gap-y-4 pt-8 border-t border-white/10 max-w-4xl mx-auto">
          <div className="flex items-center gap-2 text-sm font-bold text-slate-200/90">
            <span>🎯</span> 150+ Vacatures Geoptimaliseerd
          </div>
          <div className="flex items-center gap-2 text-sm font-bold text-slate-200/90">
            <span>💰</span> Gemiddeld 60% Lagere CPH
          </div>
          <div className="flex items-center gap-2 text-sm font-bold text-slate-200/90">
            <span>⚡</span> 24 Uur Levertijd
          </div>
        </div>
      </div>
    </section>
  );
};
