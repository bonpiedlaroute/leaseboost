import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Button from '../components/common/Button';
import Analytics from '../services/analytics';


const fixEncoding = (text) => {
  if(!text) return '';

  return text
    .replace(/Â²/g, '²')
    .replace(/Ã¨/g, 'è')
    .replace(/Ã©/g, 'é')
    .replace(/Ã /g, 'à')
    .replace(/Ã´/g, 'ô')
    .replace(/Ãª/g, 'ê')
    .replace(/Ã§/g, 'ç')
    .replace(/Ã¹/g, 'ù')
    .replace(/Ã»/g, 'û')
    .replace(/Ã®/g, 'î')
    .replace(/Ã¯/g, 'ï');
}

const FinancialAnalysis = () => {
  const navigate = useNavigate();
  const [analysis, setAnalysis] = useState(null);
  const [filename, setFilename] = useState('');
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');
  const [pageStartTime] = useState(Date.now());


  useEffect(() => {
    const storedAnalysis = sessionStorage.getItem('leaseAnalysis');
    const storedFilename = sessionStorage.getItem('leaseFilename');

    if(storedAnalysis) {
      try {
        setAnalysis(JSON.parse(storedAnalysis));
        setFilename(storedFilename || 'Fichier analysé');

        Analytics.trackPageView('Analysis Results');
      }
      catch (error) {
        console.error('Error parsing analysis:', error);
        navigate('/');
      }
    }
    else {
      navigate('/');
    }
    setLoading(false);
  }, [navigate]);

    useEffect(() => {
    const handleBeforeUnload = () => {
      const timeSpent = (Date.now() - pageStartTime) / 1000;
      Analytics.trackTimeOnAnalysisPage(timeSpent);
    };

    const handleVisibilityChange = () => {
      if (document.visibilityState === 'hidden') {
        const timeSpent = (Date.now() - pageStartTime) / 1000;
        Analytics.trackTimeOnAnalysisPage(timeSpent);
      }
    };

    window.addEventListener('beforeunload', handleBeforeUnload);
    document.addEventListener('visibilitychange', handleVisibilityChange);

    return () => {
      window.removeEventListener('beforeunload', handleBeforeUnload);
      document.removeEventListener('visibilitychange', handleVisibilityChange);
      
      // final track
      const timeSpent = (Date.now() - pageStartTime) / 1000;
      Analytics.trackTimeOnAnalysisPage(timeSpent);
    };
  }, [pageStartTime]);

  const handleNewAnalysis = () => {

    Analytics.trackEvent('new_analysis_requested', {
      from_page: 'analysis_results',
      previous_file: filename
    });

    sessionStorage.removeItem('leaseAnalysis');
    sessionStorage.removeItem('leaseFileName');
    navigate('/');
  };

  const handleExportPDF = () => {
    Analytics.trackReportExport('pdf');
    
    window.print();
  };

  const handlePrint = () => {
    Analytics.trackReportExport('print');

    window.print();
  };

  if( loading) {
    return (
      <div className="flex justify-center items-center min-h-[400px]">
        <div className="text-center">
          <div className="w-12 h-12 border-4 border-blue-300 border-t-blue-600 rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-[#49739c] text-lg">Chargement de l'analyse...</p>
        </div>
      </div>
    );
  }

  if (!analysis) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[400px] gap-4">
        <p className="text-[#0d141c] text-lg">Aucune analyse disponible</p>
        <Button 
          unstyled 
          className="bg-[#0c7ff2] text-white px-6 py-2 rounded-lg hover:bg-blue-600"
          onClick={handleNewAnalysis}
        >
          Analyser un nouveau bail
        </Button>
      </div>
    );
  }

  const tabs = [
    { id: 'overview', label: '📊 Vue d\'ensemble', icon: '📊' },
    { id: 'market', label: '🏢 Position Marché', icon: '🏢' },
    { id: 'legal', label: '⚖️ Conformité', icon: '⚖️' },
    { id: 'opportunities', label: '💰 Opportunités', icon: '💰' }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* header with executive summary */}
      <div className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 py-4 md:py-6">
          <div className="flex flex-col md:flex-row md:justify-between md:items-start gap-4">
            <div className="flex-1">
              <h1 className="text-xl md:text-3xl font-bold text-gray-900 mb-2">
                📋 Analyse Complète - {filename}
              </h1>
              <div className="bg-gradient-to-r from-blue-50 to-green-50 p-3 md:p-4 rounded-lg border border-blue-200">
                <h2 className="font-semibold text-gray-900 mb-2">📋 Résumé Exécutif</h2>
                <p className="text-gray-700 text-sm leading-relaxed whitespace-pre-line">
                  {analysis.executive_summary}
                </p>
                <div className="mt-3 flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-4 text-xs">
                  <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded">
                    Fiabilité: {analysis.analysis_confidence}
                  </span>
                  <span className="text-gray-500">
                    Analysé le {new Date().toLocaleDateString('fr-FR')}
                  </span>
                </div>
              </div>
            </div>
            <div className="flex flex-col sm:flex-row gap-2 md:mt-0">
              <Button 
                unstyled 
                className="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-200 text-sm"
                onClick={handleNewAnalysis}
              >
                ↩️ Nouvelle analyse
              </Button>
              <Button 
                unstyled 
                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 text-sm"
                onClick={handlePrint}
              >
                🖨️ Imprimer
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* tabs navigation */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4">
          <nav className="flex space-x-2 md:space-x-8 overflow-x-auto">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-4 px-2 border-b-2 font-medium text-xs md:text-sm transition-colors whitespace-nowrap ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </nav>
        </div>
      </div>

      {/* tabs content */}
      <div className="max-w-7xl mx-auto px-4 py-4 md:py-6">
        
        {/* global view */}
        {activeTab === 'overview' && (
          <div className="space-y-6">
            
            {/* keys metrics */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              <div className="bg-white p-4 md:p-6 rounded-lg border border-gray-200">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                      <span className="text-blue-600 text-sm">🏢</span>
                    </div>
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-500">Position Marché</p>
                    <p className="text-lg md:text-xl font-semibold text-gray-900">
                      {analysis.market_intelligence?.percentile_position?.split(' - ')[0] || 'N/A'}
                    </p>
                  </div>
                </div>
              </div>
              
              <div className="bg-white p-4 md:p-6 rounded-lg border border-gray-200">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <div className="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
                      <span className="text-green-600 text-sm">⚖️</span>
                    </div>
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-500">Conformité</p>
                    <p className="text-lg md:text-xl font-semibold text-gray-900">
                      {analysis.compliance_score?.split(' - ')[0] || 'N/A'}
                    </p>
                  </div>
                </div>
              </div>
              
              <div className="bg-white p-4 md:p-6 rounded-lg border border-gray-200">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <div className="w-8 h-8 bg-yellow-100 rounded-lg flex items-center justify-center">
                      <span className="text-yellow-600 text-sm">💰</span>
                    </div>
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-500">Opportunités</p>
                    <p className="text-lg md:text-xl font-semibold text-gray-900">
                      {analysis.opportunities?.length || 0}
                    </p>
                  </div>
                </div>
              </div>
              
              <div className="bg-white p-4 md:p-6 rounded-lg border border-gray-200">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <div className="w-8 h-8 bg-red-100 rounded-lg flex items-center justify-center">
                      <span className="text-red-600 text-sm">🚨</span>
                    </div>
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-500">Alertes</p>
                    <p className="text-lg md:text-xl font-semibold text-gray-900">
                      {(analysis.legal_alerts?.length || 0) + (analysis.critical_deadlines?.length || 0)}
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* urgent alerts if any */}
            {(analysis.critical_deadlines?.length > 0 || analysis.legal_alerts?.some(a => a.severity === 'HIGH')) && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4 md:p-6">
                <h3 className="text-base md:text-lg font-semibold text-red-900 mb-4">
                  🚨 Actions Urgentes Requises
                </h3>
                <div className="space-y-3">
                  {analysis.critical_deadlines?.slice(0, 2).map((deadline, index) => (
                    <div key={index} className="flex items-start space-x-3">
                      <div className="flex-shrink-0 w-2 h-2 bg-red-500 rounded-full mt-2"></div>
                      <div>
                        <p className="font-medium text-red-900">{deadline.type}</p>
                        <p className="text-sm text-red-700">
                          Échéance: {deadline.date} ({deadline.days_remaining} jours restants)
                        </p>
                        <p className="text-sm text-red-600">{deadline.action_required}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Opportunities */}
            {analysis.market_intelligence?.immediate_opportunity?.includes('possible') && (
              <div className="bg-green-50 border border-green-200 rounded-lg p-4 md:p-6">
                <h3 className="text-base md:text-lg font-semibold text-green-900 mb-2">
                  💰 Opportunité Principale Identifiée
                </h3>
                <p className="text-green-800 text-base md:text-lg font-medium">
                  {analysis.market_intelligence.immediate_opportunity}
                </p>
                <p className="text-sm text-green-600 mt-2">
                  Basé sur {analysis.market_intelligence.comparable_count} comparables du marché local
                </p>
              </div>
            )}
          </div>
        )}

        {/* Market positon */}
        {activeTab === 'market' && (
          <div className="space-y-6">
            <div className="bg-white rounded-lg border border-gray-200 p-4 md:p-6">
              <h2 className="text-lg md:text-xl font-bold text-gray-900 mb-6">🏢 Analyse de Position Marché</h2>
              
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <h3 className="font-semibold text-gray-900 mb-4">📍 Votre Position</h3>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Position marché:</span>
                      <span className="font-medium">{analysis.market_intelligence?.percentile_position || 'N/A'}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Votre prix estimé:</span>
                      <span className="font-medium">{analysis.market_intelligence?.your_estimated_price || 'N/A'}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Médiane marché:</span>
                      <span className="font-medium">{analysis.market_intelligence?.market_median_price || 'N/A'}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Fiabilité:</span>
                      <span className="font-medium">{analysis.market_intelligence?.confidence_level || 'N/A'}</span>
                    </div>
                  </div>
                </div>
                
                <div>
                  <h3 className="font-semibold text-gray-900 mb-4">💡 Opportunité</h3>
                  <div className="bg-blue-50 p-4 rounded-lg">
                    <p className="text-blue-900 font-medium">
                      {analysis.market_intelligence?.immediate_opportunity || 'Analyse en cours...'}
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* Comparables */}
            {analysis.market_intelligence?.comparables?.length > 0 && (
              <div className="bg-white rounded-lg border border-gray-200 p-4 md:p-6">
                <h3 className="text-base md:text-lg font-semibold text-gray-900 mb-4">
                  📊 Comparables du Marché Local ({analysis.market_intelligence.comparable_count} identifiés)
                </h3>
                <div className="overflow-x-auto">
                  <table className="w-full text-sm min-w-[600px]">
                    <thead>
                      <tr className="border-b border-gray-200">
                        <th className="text-left py-3 px-2 font-medium text-gray-700">Adresse</th>
                        <th className="text-left py-3 px-2 font-medium text-gray-700">Surface</th>
                        <th className="text-left py-3 px-2 font-medium text-gray-700">Prix/m²</th>
                        <th className="text-left py-3 px-2 font-medium text-gray-700">Distance</th>
                        <th className="text-left py-3 px-2 font-medium text-gray-700">Similarité</th>
                      </tr>
                    </thead>
                    <tbody>
                      {analysis.market_intelligence.comparables.map((comp, index) => (
                        <tr key={index} className="border-b border-gray-100">
                          <td className="py-3 px-2 text-gray-900">{fixEncoding(comp.address)}</td>
                          <td className="py-3 px-2 text-gray-600">{comp.surface}m²</td>
                          <td className="py-3 px-2 font-medium text-gray-900">{comp.price_per_sqm}€</td>
                          <td className="py-3 px-2 text-gray-600">{comp.distance_km}km</td>
                          <td className="py-3 px-2">
                            <div className={`inline-flex px-2 py-1 text-xs rounded-full ${
                              comp.similarity_score > 0.8 ? 'bg-green-100 text-green-800' :
                              comp.similarity_score > 0.6 ? 'bg-yellow-100 text-yellow-800' :
                              'bg-gray-100 text-gray-800'
                            }`}>
                              {(comp.similarity_score * 100).toFixed(0)}%
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Legal compliance */}
        {activeTab === 'legal' && (
          <div className="space-y-6">
            
            {/* Compliance score */}
            <div className="bg-white rounded-lg border border-gray-200 p-4 md:p-6">
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6 gap-4">
                <h2 className="text-lg md:text-xl font-bold text-gray-900">⚖️ Conformité Juridique</h2>
                <div className="text-left sm:text-right">
                  <div className="text-2xl font-bold text-gray-900">
                    {analysis.compliance_score?.split(' - ')[0] || 'N/A'}
                  </div>
                  <div className="text-sm text-gray-500">Score de conformité</div>
                </div>
              </div>
              
              {analysis.compliance_score?.includes(' - ') && (
                <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                  <p className="text-yellow-800">
                    {analysis.compliance_score.split(' - ')[1]}
                  </p>
                </div>
              )}
            </div>

            {/* Critical deadlines */}
            {analysis.critical_deadlines?.length > 0 && (
              <div className="bg-white rounded-lg border border-gray-200 p-4 md:p-6">
                <h3 className="text-base md:text-lg font-semibold text-gray-900 mb-4">📅 Échéances Critiques</h3>
                <div className="space-y-4">
                  {analysis.critical_deadlines.map((deadline, index) => (
                    <div key={index} className={`p-4 rounded-lg border ${
                      deadline.urgency === 'HIGH' ? 'bg-red-50 border-red-200' :
                      deadline.urgency === 'MEDIUM' ? 'bg-yellow-50 border-yellow-200' :
                      'bg-blue-50 border-blue-200'
                    }`}>
                      <div className="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-3">
                        <div className="flex-1">
                          <h4 className="font-medium text-gray-900">{deadline.type}</h4>
                          <p className="text-sm text-gray-600 mt-1">{deadline.action_required}</p>
                          {deadline.potential_loss && (
                            <p className="text-sm text-red-600 mt-1 italic">
                              ⚠️ {deadline.potential_loss}
                            </p>
                          )}
                        </div>
                        <div className="text-left sm:text-right">
                          <div className={`font-bold ${
                            deadline.days_remaining < 30 ? 'text-red-600' :
                            deadline.days_remaining < 90 ? 'text-yellow-600' :
                            'text-blue-600'
                          }`}>
                            {deadline.days_remaining} jours
                          </div>
                          <div className="text-xs text-gray-500">{deadline.date}</div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Legal alerts */}
            {analysis.legal_alerts?.length > 0 && (
              <div className="bg-white rounded-lg border border-gray-200 p-4 md:p-6">
                <h3 className="text-base md:text-lg font-semibold text-gray-900 mb-4">⚠️ Alertes Juridiques</h3>
                <div className="space-y-4">
                  {analysis.legal_alerts.map((alert, index) => (
                    <div key={index} className={`p-4 rounded-lg border ${
                      alert.severity === 'HIGH' ? 'bg-red-50 border-red-200' :
                      alert.severity === 'MEDIUM' ? 'bg-yellow-50 border-yellow-200' :
                      'bg-blue-50 border-blue-200'
                    }`}>
                      <div className="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-3">
                        <div className="flex-1">
                          <div className="flex flex-col sm:flex-row sm:items-center gap-2">
                            <h4 className="font-medium text-gray-900">{alert.type}</h4>
                            <span className={`px-2 py-1 text-xs rounded self-start ${
                              alert.severity === 'HIGH' ? 'bg-red-100 text-red-800' :
                              alert.severity === 'MEDIUM' ? 'bg-yellow-100 text-yellow-800' :
                              'bg-blue-100 text-blue-800'
                            }`}>
                              {alert.severity}
                            </span>
                          </div>
                          <p className="text-sm text-gray-600 mt-1">{alert.description}</p>
                          <p className="text-sm text-gray-800 mt-2 font-medium">{alert.action_required}</p>
                          <p className="text-xs text-gray-500 mt-1">📖 {alert.legal_reference}</p>
                          {alert.financial_impact && (
                            <p className="text-sm text-red-600 mt-1">💰 {alert.financial_impact}</p>
                          )}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Opportunities */}
        {activeTab === 'opportunities' && (
          <div className="space-y-6">
            
            {/* financial metrics */}
            <div className="grid md:grid-cols-2 gap-6">
              <div className="bg-white rounded-lg border border-gray-200 p-4 md:p-6">
                <h3 className="text-base md:text-lg font-semibold text-gray-900 mb-4">📊 Métriques Actuelles</h3>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Loyer annuel:</span>
                    <span className="font-medium">{analysis.financial_metrics?.annual_rent || 'N/A'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Charges exploitation:</span>
                    <span className="font-medium">{analysis.financial_metrics?.operational_charges || 'N/A'}</span>
                  </div>
                </div>
              </div>
              
              <div className="bg-green-50 rounded-lg border border-green-200 p-4 md:p-6">
                <h3 className="text-base md:text-lg font-semibold text-green-900 mb-4">🎯 Potentiel Optimisé</h3>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-green-700">Loyer optimisé:</span>
                    <span className="font-medium text-green-900">{analysis.financial_metrics?.optimized_rent || 'N/A'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-green-700">Économies potentielles:</span>
                    <span className="font-bold text-green-900 text-lg">{analysis.financial_metrics?.potential_savings || 'N/A'}</span>
                  </div>
                </div>
              </div>
            </div>

            {/* List of opportunities */}
            {analysis.opportunities?.length > 0 && (
              <div className="bg-white rounded-lg border border-gray-200 p-4 md:p-6">
                <h3 className="text-base md:text-lg font-semibold text-gray-900 mb-6">💰 Opportunités d'Optimisation Identifiées</h3>
                <div className="space-y-4">
                  {analysis.opportunities.map((opportunity, index) => (
                    <div key={index} className="border border-gray-200 rounded-lg p-4">
                      <div className="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-3">
                        <div className="flex-1">
                          <div className="flex flex-col sm:flex-row sm:items-center gap-2 mb-2">
                            <h4 className="font-medium text-gray-900">{opportunity.type}</h4>
                            {opportunity.confidence && (
                              <span className="bg-blue-100 text-blue-800 px-2 py-1 text-xs rounded self-start">
                                Confiance: {opportunity.confidence}
                              </span>
                            )}
                          </div>
                          <p className="text-sm text-gray-600 mb-2">{opportunity.description}</p>
                          <p className="text-sm text-gray-800 font-medium mb-2">
                            📋 {opportunity.recommendation}
                          </p>
                          
                          {opportunity.legal_basis && (
                            <p className="text-xs text-gray-500 mb-1">
                              📖 {opportunity.legal_basis}
                            </p>
                          )}
                          
                          {opportunity.comparables_count && (
                            <p className="text-xs text-blue-600">
                              📊 Basé sur {opportunity.comparables_count} comparables de marché
                            </p>
                          )}
                        </div>
                        
                        <div className="text-left sm:text-right">
                          <div className={`text-lg font-bold ${
                            opportunity.impact === 'N/A' ? 'text-gray-500' : 'text-green-600'
                          }`}>
                            {opportunity.impact === 'N/A' ? 'À évaluer' : opportunity.impact}
                          </div>
                          {opportunity.impact !== 'N/A' && (
                            <div className="text-xs text-gray-500">Impact annuel</div>
                          )}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Footer with actions */}
      <div className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <div className="text-sm text-gray-600 text-center md:text-left">
              📞 Besoin d'une analyse approfondie ? 
              <a href="mailto:info@leaseboost.fr" className="text-blue-600 hover:underline ml-1">
                Contactez nos experts
              </a>
            </div>
            <div className="flex flex-col sm:flex-row gap-3 w-full md:w-auto">
              
              <Button
                unstyled 
                className="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-200 text-sm"
                onClick={handleNewAnalysis}
              >
                📄 Analyser un autre bail
              </Button>
              <Button 
                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
                onClick={handleExportPDF}
              >
                📄 Exporter le rapport PDF
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FinancialAnalysis;