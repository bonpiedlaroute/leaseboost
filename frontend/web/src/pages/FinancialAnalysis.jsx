import React from 'react';
import Button from '../components/common/Button';


const FinancialAnalysis = () => {
    return (
        <>
        <div className="flex flex-wrap justify-between gap-3 p-4">
        <div className="flex min-w-72 flex-col gap-3">
          <p className="text-[#0d141c] tracking-light text-2xl sm:text-[32px] font-bold leading-tight">Analyse financière</p>
          <p className="text-[#49739c] text-sm font-normal leading-normal">
          Analyses financières détaillées et opportunités d'optimisation pour vos baux.
          </p>
        </div>
      </div>
      
      <h2 className="text-[#0d141c] text-xl sm:text-[22px] font-bold leading-tight tracking-[-0.015em] px-4 pb-3 pt-5">Opportunités</h2>
      <div className="px-4 py-3">
        <div className="overflow-x-auto">
          <div className="flex overflow-hidden rounded-lg border border-[#cedbe8] bg-slate-50 min-w-[800px]">
            <table className="flex-1">
              <thead>
                <tr className="bg-slate-50">
                  <th className="px-2 sm:px-4 py-3 text-left text-[#0d141c] w-[200px] sm:w-[400px] text-xs sm:text-sm font-medium leading-normal">
                    Opportunité
                  </th>
                  <th className="px-2 sm:px-4 py-3 text-left text-[#0d141c] w-[200px] sm:w-[400px] text-xs sm:text-sm font-medium leading-normal">
                    Description
                  </th>
                  <th className="px-2 sm:px-4 py-3 text-left text-[#0d141c] w-[120px] sm:w-60 text-xs sm:text-sm font-medium leading-normal">Impact</th>
                  <th className="px-2 sm:px-4 py-3 text-left text-[#0d141c] w-[200px] sm:w-[400px] text-xs sm:text-sm font-medium leading-normal">
                    Récommendation
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr className="border-t border-t-[#cedbe8]">
                  <td className="h-[72px] px-2 sm:px-4 py-2 w-[200px] sm:w-[400px] text-[#0d141c] text-xs sm:text-sm font-normal leading-normal">
                    Augmentation de loyer
                  </td>
                  <td className="h-[72px] px-2 sm:px-4 py-2 w-[200px] sm:w-[400px] text-[#49739c] text-xs sm:text-sm font-normal leading-normal">
                    Négocier une hausse de loyer car vous êtes largement en dessous du marché.
                  </td>
                  <td className="h-[72px] px-2 sm:px-4 py-2 w-[120px] sm:w-60 text-xs sm:text-sm font-normal leading-normal">
                    <Button unstyled className="flex min-w-[80px] sm:min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-6 sm:h-8 px-2 sm:px-4 bg-[#e7edf4] text-[#0d141c] text-xs sm:text-sm font-medium leading-normal w-full">
                      <span className="truncate">Gain: 15 000 €</span>
                    </Button>
                  </td>
                  <td className="h-[72px] px-2 sm:px-4 py-2 w-[200px] sm:w-[400px] text-[#49739c] text-xs sm:text-sm font-normal leading-normal">
                  Présentez les données de marché au propriétaire et proposez un loyer révisé.
                  </td>
                </tr>
                <tr className="border-t border-t-[#cedbe8]">
                  <td className="h-[72px] px-2 sm:px-4 py-2 w-[200px] sm:w-[400px] text-[#0d141c] text-xs sm:text-sm font-normal leading-normal">
                  Optimisation des charges locatives 
                  </td>
                  <td className="h-[72px] px-2 sm:px-4 py-2 w-[200px] sm:w-[400px] text-[#49739c] text-xs sm:text-sm font-normal leading-normal">
                  Examinez et contestez les charges d'exploitation, en ciblant les coûts maîtrisables.
                  </td>
                  <td className="h-[72px] px-2 sm:px-4 py-2 w-[120px] sm:w-60 text-xs sm:text-sm font-normal leading-normal">
                    <Button unstyled variant="tertiary" className="flex min-w-[80px] sm:min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-6 sm:h-8 px-2 sm:px-4 bg-[#e7edf4] text-[#0d141c] text-xs sm:text-sm font-medium leading-normal w-full">
                      <span className="truncate">Gain: 8 000 €</span>
                    </Button>
                  </td>
                  <td className="h-[72px] px-2 sm:px-4 py-2 w-[200px] sm:w-[400px] text-[#49739c] text-xs sm:text-sm font-normal leading-normal">
                  Demandez une ventilation détaillée des charges et identifiez les anomalies ou les leviers de négociation.
                  </td>
                </tr>
                <tr className="border-t border-t-[#cedbe8]">
                  <td className="h-[72px] px-2 sm:px-4 py-2 w-[200px] sm:w-[400px] text-[#0d141c] text-xs sm:text-sm font-normal leading-normal">
                  Potentiel de sous-location
                  </td>
                  <td className="h-[72px] px-2 sm:px-4 py-2 w-[200px] sm:w-[400px] text-[#49739c] text-xs sm:text-sm font-normal leading-normal">
                  Explorez les options de sous-location pour l'espace non occupé afin de réduire vos coûts.
                  </td>
                  <td className="h-[72px] px-2 sm:px-4 py-2 w-[120px] sm:w-60 text-xs sm:text-sm font-normal leading-normal">
                    <Button unstyled className="flex min-w-[80px] sm:min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-6 sm:h-8 px-2 sm:px-4 bg-[#e7edf4] text-[#0d141c] text-xs sm:text-sm font-medium leading-normal w-full">
                      <span className="truncate">Revenus: 12 000 €</span>
                    </Button>
                  </td>
                  <td className="h-[72px] px-2 sm:px-4 py-2 w-[200px] sm:w-[400px] text-[#49739c] text-xs sm:text-sm font-normal leading-normal">
                  Évaluez le marché de la sous-location et identifiez des locataires potentiels pour l'espace non occupé.
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <h2 className="text-[#0d141c] text-xl sm:text-[22px] font-bold leading-tight tracking-[-0.015em] px-4 pb-3 pt-5">Comparaison financière</h2>
      <div className="flex flex-wrap gap-4 px-4 py-6">
        <div className="flex flex-1 min-w-0 flex-col gap-2 rounded-lg border border-[#cedbe8] p-4 sm:p-6">
          <p className="text-[#0d141c] text-base font-medium leading-normal">Location annuelle</p>
          <p className="text-[#0d141c] tracking-light text-2xl sm:text-[32px] font-bold leading-tight truncate">150 000 €</p>
          <p className="text-[#49739c] text-base font-normal leading-normal">Bail boosté</p>
          <div className="grid min-h-[120px] sm:min-h-[180px] grid-flow-col gap-6 grid-rows-[1fr_auto] items-end justify-items-center px-3">
            <div className="border-[#49739c] bg-[#e7edf4] border-t-2 w-full" style={{ height: '70%' }}></div>
            <p className="text-[#49739c] text-xs sm:text-[13px] font-bold leading-normal tracking-[0.015em]">Bail boosté</p>
            <div className="border-[#49739c] bg-[#e7edf4] border-t-2 w-full" style={{ height: '20%' }}></div>
            <p className="text-[#49739c] text-xs sm:text-[13px] font-bold leading-normal tracking-[0.015em]">Bail actuel</p>
          </div>
        </div>
        <div className="flex flex-1 min-w-0 flex-col gap-2 rounded-lg border border-[#cedbe8] p-4 sm:p-6">
          <p className="text-[#0d141c] text-base font-medium leading-normal">Charges d'exploitation</p>
          <p className="text-[#0d141c] tracking-light text-2xl sm:text-[32px] font-bold leading-tight truncate">40 000 €</p>
          <p className="text-[#49739c] text-base font-normal leading-normal">Charges actuelles</p>
          <div className="grid min-h-[120px] sm:min-h-[180px] grid-flow-col gap-6 grid-rows-[1fr_auto] items-end justify-items-center px-3">
            <div className="border-[#49739c] bg-[#e7edf4] border-t-2 w-full" style={{ height: '80%' }}></div>
            <p className="text-[#49739c] text-xs sm:text-[13px] font-bold leading-normal tracking-[0.015em]">Charges actuelles</p>
            <div className="border-[#49739c] bg-[#e7edf4] border-t-2 w-full" style={{ height: '50%' }}></div>
            <p className="text-[#49739c] text-xs sm:text-[13px] font-bold leading-normal tracking-[0.015em]">Charges optimisées</p>
          </div>
        </div>
      </div>
      <p className="text-[#0d141c] text-base font-normal leading-normal pb-3 pt-1 px-4">
      Cette optimisation peut générer des économies annuelles de 23 000 €.
      </p>
      <div className="flex px-4 py-3 justify-end">
        <Button unstyled className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 px-4 bg-[#0c7ff2] text-slate-50 text-sm font-bold leading-normal tracking-[0.015em] w-full sm:w-auto">
          <span className="truncate">Exporter le rapport PDF</span>
          </Button>
      </div>
        </>
    );
};

export default FinancialAnalysis;