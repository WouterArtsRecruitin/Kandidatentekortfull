import React from 'react';

const stats = [
  { number: "150+", label: "Vacatures succesvol geoptimaliseerd" },
  { number: "40-60%", label: "Meer sollicitaties gemiddeld" },
  { number: "Direct", label: "Gratis preview analyse" },
  { number: "24 uur", label: "Geoptimaliseerde vacature" },
];

export const Stats = () => {
  return (
    <section className="bg-white py-16 shadow-[0_-8px_24px_rgba(15,23,42,0.06)] relative z-20">
      <div className="container mx-auto px-4 md:px-6">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8 md:gap-12 max-w-6xl mx-auto">
          {stats.map((stat, index) => (
            <div key={index} className="text-center">
              <div className="text-4xl md:text-5xl font-black text-transparent bg-clip-text bg-gradient-to-br from-orange-500 to-blue-500 mb-2 tracking-tighter">
                {stat.number}
              </div>
              <div className="text-sm md:text-base font-semibold text-slate-600 leading-snug">
                {stat.label}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};
