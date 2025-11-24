import React from 'react';

export const Hero = () => {
  return (
    <section className="relative py-20 md:py-28 bg-slate-900 text-white overflow-hidden">
      {/* Background Effects matching CSS */}
      <div className="absolute inset-0 opacity-40 pointer-events-none"
           style={{
             backgroundImage: `
               linear-gradient(30deg, rgba(255,255,255,0.03) 12%, transparent 12.5%, transparent 87%, rgba(255,255,255,0.03) 87.5%),
               linear-gradient(150deg, rgba(255,255,255,0.03) 12%, transparent 12.5%, transparent 87%, rgba(255,255,255,0.03) 87.5%)
             `,
             backgroundSize: '80px 140px'
           }}
      />
      
      <div className="absolute -bottom-1/2 left-1/2 -translate-x-1/2 w-[600px] h-[600px] bg-[radial-gradient(circle,rgba(255,107,53,0.15)_0%,transparent_70%)] pointer-events-none" />

      <div className="container mx-auto px-4 md:px-6 relative z-10 text-center">
        


        <h1 className="text-4xl md:text-6xl lg:text-7xl font-black text-white mb-8 leading-[1.1] max-w-5xl mx-auto">
          Ontdek waarom je <span className="text-transparent bg-clip-text bg-gradient-to-r from-orange-500 to-orange-400">geen kandidaten</span> krijgt
        </h1>

        <p className="text-lg md:text-xl font-medium text-slate-300/90 max-w-2xl mx-auto mb-12 leading-relaxed">
          Upload je vacature. Ontvang binnen 24 uur een geoptimaliseerde vacaturetekst die 40-60% meer sollicitaties genereert.
        </p>

        {/* CTA Button with Typeform Popup */}
        <div className="flex justify-center mb-12">
          <button
            data-tf-popup="01K25SKWYTKZ05DAHER9D52J94"
            data-tf-opacity="0"
            data-tf-size="100"
            data-tf-iframe-props="title=Vacature Analyse"
            data-tf-transitive-search-params
            data-tf-medium="snippet"
            className="group relative px-8 py-5 bg-gradient-to-r from-orange-600 to-orange-500 hover:from-orange-500 hover:to-orange-400 text-white rounded-2xl shadow-2xl shadow-orange-600/30 hover:shadow-orange-500/40 transition-all duration-300 hover:scale-105 hover:-translate-y-1"
          >
            <span className="flex items-center gap-3 font-black text-lg">
              <svg className="w-6 h-6 group-hover:animate-bounce" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
              Start Analyse
              <svg className="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </span>
          </button>
        </div>

        <div className="flex flex-wrap justify-center gap-x-8 gap-y-4 pt-8 border-t border-white/10 max-w-3xl mx-auto">
          <div className="flex items-center gap-2 text-sm font-bold text-slate-200/90">
            <span>🎯</span> 150+ Vacatures Geanalyseerd
          </div>
          <div className="flex items-center gap-2 text-sm font-bold text-slate-200/90">
            <span>✅</span> 92% Satisfaction Rate
          </div>
          <div className="flex items-center gap-2 text-sm font-bold text-slate-200/90">
            <span>⚡</span> 24 Uur Levertijd
          </div>
        </div>
      </div>
    </section>
  );
};