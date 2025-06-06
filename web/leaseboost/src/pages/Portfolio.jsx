import React from 'react';


const Portfolio = () => {
    return (
        <>
        <div className="flex flex-wrap justify-between gap-3 p-4">
        <div className="flex min-w-0 flex-col gap-3">
          <p className="text-[#0d141c] tracking-light text-2xl sm:text-[32px] font-bold leading-tight">Vue d'ensemble du portefeuille</p>
          <p className="text-[#49739c] text-sm font-normal leading-normal">
          Analysez et optimisez votre portefeuille de baux commerciaux grâce à l'intelligence artificielle.
          </p>
        </div>
      </div>
      <div className="flex flex-col sm:flex-row sm:flex-wrap gap-4 p-4">
        <div className="flex flex-1 min-w-full sm:min-w-[300px] lg:min-w-[158px] flex-col gap-2 rounded-lg p-6 border border-[#cedbe8]">
          <p className="text-[#0d141c] text-base font-medium leading-normal">Loyers en dessous du marché</p>
          <p className="text-[#0d141c] tracking-light text-2xl font-bold leading-tight">250 000 €</p>
          <p className="text-[#078838] text-base font-medium leading-normal">+10%</p>
        </div>
        <div className="flex flex-1 min-w-full sm:min-w-[300px] lg:min-w-[158px] flex-col gap-2 rounded-lg p-6 border border-[#cedbe8]">
          <p className="text-[#0d141c] text-base font-medium leading-normal">Risques contractuels</p>
          <p className="text-[#0d141c] tracking-light text-2xl font-bold leading-tight">12</p>
          <p className="text-[#e73908] text-base font-medium leading-normal">-5%</p>
        </div>
        <div className="flex flex-1 min-w-full sm:min-w-[300px] lg:min-w-[158px] flex-col gap-2 rounded-lg p-6 border border-[#cedbe8]">
          <p className="text-[#0d141c] text-base font-medium leading-normal">Opportunités d'optimisation identifiées</p>
          <p className="text-[#0d141c] tracking-light text-2xl font-bold leading-tight">8</p>
          <p className="text-[#078838] text-base font-medium leading-normal">+15%</p>
        </div>
      </div>
      <h2 className="text-[#0d141c] text-xl sm:text-[22px] font-bold leading-tight tracking-[-0.015em] px-4 pb-3 pt-5">Visualisation des risques</h2>
      <div className="flex flex-col lg:flex-row gap-4 px-4 py-6">
        <div className="flex flex-1 min-w-0 flex-col gap-2">
          <p className="text-[#0d141c] text-base font-medium leading-normal">Répartition des risques contractuels</p>
          <p className="text-[#0d141c] tracking-light text-2xl sm:text-[32px] font-bold leading-tight truncate">12</p>
          <p className="text-[#49739c] text-base font-normal leading-normal">Actuel</p>
          <div className="grid min-h-[120px] sm:min-h-[180px] gap-x-4 gap-y-6 grid-cols-[auto_1fr] items-center py-3">
            <p className="text-[#49739c] text-xs sm:text-[13px] font-bold leading-normal tracking-[0.015em]">Légal</p>
            <div className="h-full flex-1">
              <div className="border-[#49739c] bg-[#e7edf4] border-r-2 h-full" style={{ width: '50%' }}></div>
            </div>
            <p className="text-[#49739c] text-[13px] font-bold leading-normal tracking-[0.015em]">Financier</p>
            <div className="h-full flex-1">
              <div className="border-[#49739c] bg-[#e7edf4] border-r-2 h-full" style={{ width: '90%' }}></div>
            </div>
            <p className="text-[#49739c] text-xs sm:text-[13px] font-bold leading-normal tracking-[0.015em]">Opérationnel</p>
            <div className="h-full flex-1">
              <div className="border-[#49739c] bg-[#e7edf4] border-r-2 h-full" style={{ width: '40%' }}></div>
            </div>
          </div>
        </div>
        <div className="flex flex-1 min-w-0 flex-col gap-2">
          <p className="text-[#0d141c] text-base font-medium leading-normal">Répartition par niveau de gravité</p>
          <p className="text-[#0d141c] tracking-light text-2xl sm:text-[32px] font-bold leading-tight truncate">100%</p>
          <p className="text-[#49739c] text-base font-normal leading-normal">Actuel</p>
          <div className="grid min-h-[120px] sm:min-h-[180px] grid-flow-col gap-6 grid-rows-[1fr_auto] items-end justify-items-center px-3">
            <div className="border-[#49739c] bg-[#e7edf4] border-t-2 w-full" style={{ height: '30%' }}></div>
            <p className="text-[#49739c] text-xs sm:text-[13px] font-bold leading-normal tracking-[0.015em]">Haut</p>
            <div className="border-[#49739c] bg-[#e7edf4] border-t-2 w-full" style={{ height: '90%' }}></div>
            <p className="text-[#49739c] text-xs sm:text-[13px] font-bold leading-normal tracking-[0.015em]">Moyen</p>
            <div className="border-[#49739c] bg-[#e7edf4] border-t-2 w-full" style={{ height: '80%' }}></div>
            <p className="text-[#49739c] text-xs sm:text-[13px] font-bold leading-normal tracking-[0.015em]">Bas</p>
          </div>
        </div>
      </div>
        </>
    );
};
export default Portfolio;