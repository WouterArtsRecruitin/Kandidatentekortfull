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