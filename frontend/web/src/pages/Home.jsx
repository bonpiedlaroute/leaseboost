import React from 'react';
import Button from '../components/common/Button';

const Home = () => {
  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{
      __html: JSON.stringify({
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": "Analyse de Baux Commerciaux - LeaseBoost",
        "description": "Solution IA pour l'analyse et l'optimisation des baux commerciaux",
        "breadcrumb": {
          "@type": "BreadcrumbList",
          "itemListElement": [{
            "@type": "ListItem",
            "position": 1,
            "name": "Accueil",
            "item": "https://leaseboost.fr/"
          }]
        }
      })
    }} />

      <div className="flex flex-wrap justify-between gap-3 p-4">
      <h1 className="text-[#0d141c] tracking-light text-2xl sm:text-[32px] font-bold leading-tight min-w-0 sm:min-w-72">Analyse de Baux Commerciaux par Intelligence Artificielle</h1>
      </div>
      <div className="flex flex-wrap justify-between gap-3 p-4">
        <p className="text-[#0d141c] tracking-light text-2xl sm:text-[32px] font-bold leading-tight min-w-0 sm:min-w-72">Analyse de Bail</p>
      </div>
      <div className="flex flex-col p-4">
        <div className="flex flex-col items-center gap-6 rounded-lg border-2 border-dashed border-[#cedbe8] px-4 sm:px-6 py-10 sm:py-14">
          <div className="flex w-full max-w-[480px] flex-col items-center gap-2 px-4">
            <p className="text-[#0d141c] text-base sm:text-lg font-bold leading-tight tracking-[-0.015em] text-center">
              Déposez vos baux ici ou cliquez pour parcourir
            </p>
            <p className="text-[#0d141c] text-xs sm:text-sm font-normal leading-normal text-center">
              Formats acceptés : PDF, DOCX. Jusqu'à 10 fichiers simultanément..
            </p>
          </div>
          <Button unstyled className="flex min-w-[120px] sm:min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 px-4 bg-[#e7edf4] text-[#0d141c] text-sm font-bold leading-normal tracking-[0.015em] w-full sm:w-auto" >
            <span className="truncate">Lancer l'analyse</span></Button>
        </div>
      </div>
      <p className="text-[#49739c] text-xs sm:text-sm font-normal leading-normal pb-3 pt-1 px-4 text-center underline">
        En important vos documents, vous acceptez nos conditions générales d'utilisations et notre Politique de confidentialité.
      </p>
        
        <main className="w-full max-w-4xl mx-auto px-4 py-8 sm:py-12" itemScope itemType="https://schema.org/Article">
        {/* Main header */}
        <header className="text-center mb-8 sm:mb-12">
          <h2 className="text-[#0d141c] text-2xl sm:text-3xl lg:text-4xl font-bold leading-tight tracking-[-0.015em] mb-4">
            Le problème fondamental des baux commerciaux : des millions cachés dans les angles morts contractuels
          </h2>
          <p className="text-[#49739c] text-lg sm:text-xl font-medium leading-normal" itemProp="description">
            Le défi invisible des gestionnaires d'actifs immobiliers commerciaux
          </p>
        </header>

        {/* Introduction */}
        <section className="mb-8 sm:mb-12">
          <p className="text-[#0d141c] text-base sm:text-lg leading-relaxed mb-6">
            Chaque année en France, les sociétés foncières et gestionnaires d'actifs immobiliers laissent fuir des millions d'euros de revenus locatifs, sans même s'en apercevoir. Ce n'est pas par négligence ou incompétence – c'est la conséquence d'un système de gestion des baux commerciaux fondamentalement défaillant.
          </p>
        </section>

        {/* Triple constraint */}
        <section className="mb-8 sm:mb-12">
          <h2 className="text-[#0d141c] text-xl sm:text-2xl font-bold leading-tight tracking-[-0.015em] mb-6">
            La triple contrainte impossible
          </h2>
          <p className="text-[#0d141c] text-base sm:text-lg leading-relaxed mb-6">
            Les gestionnaires d'actifs immobiliers font face à un défi structurel qui semble insurmontable :
          </p>
          
          <div className="grid gap-6 sm:gap-8 md:grid-cols-3">
            <div className="p-6 rounded-lg border border-[#cedbe8] bg-white">
              <h3 className="text-[#0d141c] text-lg font-bold mb-4">Volume écrasant de documentation juridique</h3>
              <ul className="text-[#49739c] text-sm leading-relaxed space-y-2">
                <li>• Portefeuilles de dizaines ou centaines de baux, chacun comptant 30-50 pages</li>
                <li>• Des milliers de clauses complexes à surveiller simultanément</li>
                <li>• Des conditions spécifiques dissimulées dans un langage juridique dense</li>
              </ul>
            </div>
            
            <div className="p-6 rounded-lg border border-[#cedbe8] bg-white">
              <h3 className="text-[#0d141c] text-lg font-bold mb-4">Complexité croissante des cadres contractuels</h3>
              <ul className="text-[#49739c] text-sm leading-relaxed space-y-2">
                <li>• Formulations ambiguës ouvrant la porte à diverses interprétations</li>
                <li>• Clauses d'indexation aux mécanismes de calcul sophistiqués</li>
                <li>• Références croisées entre documents multipliant les risques d'erreur</li>
              </ul>
            </div>
            
            <div className="p-6 rounded-lg border border-[#cedbe8] bg-white">
              <h3 className="text-[#0d141c] text-lg font-bold mb-4">Ressources humaines limitées</h3>
              <ul className="text-[#49739c] text-sm leading-relaxed space-y-2">
                <li>• Équipes juridiques sollicitées sur des urgences opérationnelles</li>
                <li>• Gestionnaires d'actifs focalisés sur les nouveaux développements</li>
                <li>• Impossibilité pratique d'analyser manuellement chaque bail</li>
              </ul>
            </div>
          </div>
        </section>

        {/* Financial consequences */}
        <section className="mb-8 sm:mb-12">
          <h2 className="text-[#0d141c] text-xl sm:text-2xl font-bold leading-tight tracking-[-0.015em] mb-6">
            Les conséquences financières concrètes
          </h2>
          <p className="text-[#0d141c] text-base sm:text-lg leading-relaxed mb-6">
            Cette triple contrainte engendre des pertes financières substantielles qui restent largement sous-estimées :
          </p>

          <div className="space-y-6 sm:space-y-8">
            <article className="p-6 rounded-lg bg-red-50 border border-red-200">
              <h3 className="text-[#0d141c] text-lg font-bold mb-4 flex items-center">
                <span className="bg-red-500 text-white rounded-full w-8 h-8 flex items-center justify-center text-sm font-bold mr-3 flex-shrink-0 min-w-[2rem] min-h-[2rem]">1</span>
                Revenus non perçus : la fuite silencieuse de trésorerie
              </h3>
              <p className="text-[#0d141c] text-sm leading-relaxed mb-3">
                <strong>Problème concret :</strong> Les indexations et revalorisations prévues aux contrats ne sont pas appliquées correctement ou dans les délais optimaux.
              </p>
              <p className="text-[#0d141c] text-sm leading-relaxed mb-4">
                <strong>Impact financier :</strong> Pour une foncière de taille moyenne (50-100 baux), cette sous-exploitation représente typiquement 5-8% des revenus locatifs potentiels – soit souvent 200-500K€ annuels qui s'évaporent simplement par manque de suivi optimal.
              </p>
              <blockquote className="border-l-4 border-red-400 pl-4 italic text-[#49739c] text-sm">
                "Nous avons découvert par hasard qu'une clause d'indexation avait été mal interprétée sur un centre commercial pendant trois ans. Le préjudice dépassait 180.000€, non récupérables car au-delà du délai de prescription." – Directeur Asset Management, foncière régionale
              </blockquote>
            </article>

            <article className="p-6 rounded-lg bg-orange-50 border border-orange-200">
              <h3 className="text-[#0d141c] text-lg font-bold mb-4 flex items-center">
                <span className="bg-orange-500 text-white rounded-full w-8 h-8 flex items-center justify-center text-sm font-bold mr-3 flex-shrink-0 min-w-[2rem] min-h-[2rem]">2</span>
                Risques juridiques non identifiés : la bombe à retardement
              </h3>
              <p className="text-[#0d141c] text-sm leading-relaxed mb-3">
                <strong>Problème concret :</strong> Des formulations ambiguës ou clauses atypiques créent des vulnérabilités exploitables par les locataires, particulièrement dans un contexte économique tendu.
              </p>
              <p className="text-[#0d141c] text-sm leading-relaxed mb-4">
                <strong>Impact financier :</strong> Les litiges résultant de ces ambiguïtés entraînent des coûts moyens de 35-50K€ par cas, sans compter les pertes de loyers pendant les procédures et les relations commerciales dégradées.
              </p>
              <blockquote className="border-l-4 border-orange-400 pl-4 italic text-[#49739c] text-sm">
                "Un bail commercial contenait une clause de sortie anticipée mal formulée. Le locataire l'a utilisée pour quitter les lieux prématurément, nous laissant avec une vacance de 8 mois et 120.000€ de loyers perdus." – Asset Manager, fonds d'investissement immobilier
              </blockquote>
            </article>

            <article className="p-6 rounded-lg bg-yellow-50 border border-yellow-200">
              <h3 className="text-[#0d141c] text-lg font-bold mb-4 flex items-center">
                <span className="bg-yellow-500 text-white rounded-full w-8 h-8 flex items-center justify-center text-sm font-bold mr-3 flex-shrink-0 min-w-[2rem] min-h-[2rem]">3</span>
                Opportunités manquées : l'invisible coût d'opportunité
              </h3>
              <p className="text-[#0d141c] text-sm leading-relaxed mb-3">
                <strong>Problème concret :</strong> Les moments optimaux pour renégocier, les leviers contractuels disponibles et les comparaisons avec les performances du marché restent inexploités.
              </p>
              <p className="text-[#0d141c] text-sm leading-relaxed mb-4">
                <strong>Impact financier :</strong> Les renégociations sous-optimales ou tardives aboutissent à des conditions inférieures aux standards du marché, avec un impact estimé à 3-6% sur la valeur globale des actifs.
              </p>
              <blockquote className="border-l-4 border-yellow-400 pl-4 italic text-[#49739c] text-sm">
                "Sans analyse comparative, nous avons longtemps maintenu des conditions de loyer variables sous-optimales pour notre portefeuille retail. L'écart avec les pratiques de marché nous coûtait 12-15% de revenus potentiels." – Directeur immobilier, enseigne nationale
              </blockquote>
            </article>
          </div>
        </section>

        {/* Status quo */}
        <section className="mb-8 sm:mb-12">
          <h2 className="text-[#0d141c] text-xl sm:text-2xl font-bold leading-tight tracking-[-0.015em] mb-6">
            Le statu quo insoutenable
          </h2>
          <p className="text-[#0d141c] text-base sm:text-lg leading-relaxed mb-6">
            Face à ces défis, les solutions existantes s'avèrent largement insuffisantes :
          </p>
          <ul className="text-[#49739c] text-base leading-relaxed space-y-3 mb-6">
            <li>• Les approches manuelles sont dépassées par la volumétrie et la complexité</li>
            <li>• Les logiciels traditionnels se contentent de stocker les documents sans les comprendre</li>
            <li>• Les cabinets de conseil proposent des audits ponctuels coûteux sans résolution systémique</li>
          </ul>
          <p className="text-[#0d141c] text-base sm:text-lg leading-relaxed">
            Le résultat ? Un sentiment permanent d'incertitude sur la performance réelle du portefeuille, un stress constant face aux risques non identifiés, et la frustration de savoir que des revenus substantiels restent inexploités chaque année.
          </p>
        </section>

        {/* Transformation opportunity */}
        <section className="mb-8 sm:mb-12">
          <h2 className="text-[#0d141c] text-xl sm:text-2xl font-bold leading-tight tracking-[-0.015em] mb-6">
            L'opportunité de transformation
          </h2>
          <p className="text-[#0d141c] text-base sm:text-lg leading-relaxed mb-6">
            Ce qui était autrefois impossible devient aujourd'hui réalisable. L'intelligence artificielle spécialisée dans l'analyse des baux commerciaux offre enfin une solution à cette problématique structurelle :
          </p>
          <div className="grid gap-4 sm:grid-cols-2">
            <div className="p-4 rounded-lg bg-green-50 border border-green-200">
              <p className="text-[#0d141c] text-sm font-medium">✓ Analyse exhaustive et instantanée de chaque clause de chaque bail</p>
            </div>
            <div className="p-4 rounded-lg bg-green-50 border border-green-200">
              <p className="text-[#0d141c] text-sm font-medium">✓ Détection automatique des risques, opportunités et anomalies</p>
            </div>
            <div className="p-4 rounded-lg bg-green-50 border border-green-200">
              <p className="text-[#0d141c] text-sm font-medium">✓ Quantification précise de l'impact financier potentiel</p>
            </div>
            <div className="p-4 rounded-lg bg-green-50 border border-green-200">
              <p className="text-[#0d141c] text-sm font-medium">✓ Recommandations actionnables priorisées par ROI</p>
            </div>
          </div>
          <p className="text-[#0d141c] text-base sm:text-lg leading-relaxed mt-6">
            Imaginez pouvoir enfin avoir une visibilité complète et une maîtrise totale de votre portefeuille de baux commerciaux – transformant une source d'inquiétude en un levier stratégique de création de valeur.
          </p>
        </section>

        {/* LeaseBoost solution */}
        <section className="text-center bg-gradient-to-r from-blue-50 to-indigo-50 p-8 rounded-xl border border-blue-200">
          <h2 className="text-[#0d141c] text-2xl sm:text-3xl font-bold leading-tight tracking-[-0.015em] mb-4">
            La solution LeaseBoost : de l'angle mort à la vision 20/20
          </h2>
          <p className="text-[#0d141c] text-base sm:text-lg leading-relaxed mb-6">
            LeaseBoost est la première solution d'intelligence artificielle spécialement conçue pour résoudre ce problème fondamental des foncières et gestionnaires d'actifs immobiliers commerciaux.
          </p>
          <p className="text-[#49739c] text-base leading-relaxed mb-6">
            Notre plateforme ne se contente pas de stocker vos baux – elle les comprend, les analyse et transforme cette compréhension en leviers d'optimisation financière concrets et actionnables.
          </p>
          <p className="text-[#0d141c] text-base leading-relaxed mb-8">
            Chaque jour, nos clients découvrent des opportunités d'optimisation insoupçonnées et sécurisent des milliers d'euros de revenus additionnels, tout en réduisant drastiquement leurs risques juridiques et opérationnels.
          </p>
          <div className="bg-white p-6 rounded-lg border border-blue-300 mb-6">
            <p className="text-[#0d141c] text-lg font-medium leading-relaxed">
              La question n'est plus de savoir si vous pouvez vous permettre d'adopter une solution d'analyse intelligente de vos baux commerciaux, mais plutôt si vous pouvez vous permettre de continuer à opérer sans elle.
            </p>
          </div>
          <button className="bg-[#0c7ff2] text-white px-8 py-3 rounded-lg font-bold text-base hover:bg-blue-600 transition-colors">
            Découvrez comment LeaseBoost peut révéler et débloquer la valeur cachée dans votre portefeuille de baux commerciaux
          </button>
        </section>
        <section className="text-center py-8 border-t border-[#e7edf4] mt-12">
          <p className="text-[#49739c] text-base mb-2">Une question ? Contactez-nous</p>
          <a 
            href="mailto:info@leaseboost.fr" 
            className="text-[#0c7ff2] text-lg font-medium hover:underline"
          >
            info@leaseboost.fr
          </a>
        </section>
      </main>
    </>
  );
};

export default Home;