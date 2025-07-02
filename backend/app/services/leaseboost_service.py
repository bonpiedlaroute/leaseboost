import openai
import json
import logging
import re
from typing import Dict, Optional
from app.models.schemas import LeaseAnalysisResponse, Opportunity, FinancialMetrics
from app.services.market_intelligence_service import MarketIntelligenceService
from app.services.legal_compliance import LegalComplianceService
from app.config import Settings

class LeaseBoostService:
    def __init__(self, openai_api_key: str, legifrance_client_id: str = None, legifrance_client_secret: str = None,
                  logger: Optional[logging.Logger] = None):
        
        self.market_intelligence_service = MarketIntelligenceService(logger=logger)

        self.legal_compliance_service = LegalComplianceService(openai_api_key=
            openai_api_key, legifrance_client_id=legifrance_client_id,
            legifrance_client_secret=legifrance_client_secret, logger=logger)
        
        self.openai_client =  openai.OpenAI(api_key=openai_api_key)
        self.logger = logger or logging.getLogger(__name__)
    
    async def analyze_lease(self, lease_content: str, filename: str) -> LeaseAnalysisResponse:

        try:
            # 1. Extract base data

            basic_data = self._extract_basic_lease_data(lease_content)

            self.logger.info(f"Basic data: {basic_data}")
            # 2. Extract market intelligence
            market_position = await self.market_intelligence_service.get_market_position(
                city=basic_data['city'],
                address=basic_data['address'],
                surface=basic_data['surface'],
                current_rent=basic_data.get('annual_rent')
            )

            # 3. Extract legal compliance
            legal_compliance = await self.legal_compliance_service.analyze_compliance(lease_content)

            self.logger.info(f"Legal compliance: {legal_compliance}")
            # 4 enrich
            ai_analysis = self._perform_enriched_ai_analysis(
                lease_content,
                basic_data,
                market_position,
                legal_compliance
            )
            
            self.logger.info(f"AI analysis: {ai_analysis}")
            return self._build_complete_analysis(
                market_position, legal_compliance, ai_analysis, basic_data
            )
        except Exception as e:
            return self._create_fallback_analysis(f"Error analyzing lease: {str(e)}")
    
    def _extract_basic_lease_data(self, lease_content: str) -> Dict:
        
        extract_prompt = f"""
         
        Analyse ce contenu de bail commercial français et extrais UNIQUEMENT les informations suivantes :

        CONTENU BAIL:
        {lease_content}

        Tu dois extraire et retourner UNIQUEMENT un JSON avec cette structure exacte :
        {{
            "city": "ville du bien ou null si non trouvée, y compris l'arrondissement, pour les villes où il y'a des arrondissements, exemple: Paris-1er-arrondissement ou Paris-2e-arrondissement",
            "address": "adresse complète du bien ou null si non trouvée",
            "surface": nombre_en_float ou null si non trouvée,
            "annual_rent": montant_annuel_en_float ou null si non trouvé
        }}

        RÈGLES D'EXTRACTION :
        - city: Cherche la ville du bien loué, y compris l'arrondissement, pour les villes où il y'a des arrondissements, exemple: Paris-1er-arrondissement ou Paris-2e-arrondissement
        - address: Cherche l'adresse complète du bien loué (rue, numéro, ville)
        - surface: Cherche la superficie en m² (convertis en nombre décimal)
        - annual_rent: Cherche le loyer annuel en euros (convertis en nombre décimal)
        
        Si une information n'est pas présente ou ambiguë, mets null.
        Ne retourne QUE le JSON, aucun autre texte.
        """

        try:
            response = self.openai_client.chat.completions.create(
                    model=Settings.openai_model,
                    messages=[
                        {"role": "system", "content": "Tu es un expert en extraction de données de baux commerciaux français. Tu retournes uniquement du JSON valide, sans aucun texte supplémentaire."},
                        {"role": "user", "content": extract_prompt}
                    ],
                    temperature=0.1,
                    max_tokens=500
                )

            response_content = response.choices[0].message.content
            
            if response_content.startswith("```json"):
                response_content  = response_content.replace("```json", "").replace("```", "")
            
            extracted_data = json.loads(response_content)

            validated_data = {}

            # validate address
            if extracted_data.get('address') and isinstance(extracted_data['address'], str):
                validated_data['address'] = extracted_data['address'].strip()

            # validate surface
            if extracted_data.get('surface') is not None:
                try:
                    validated_data['surface'] = float(extracted_data['surface'])
                except (ValueError, TypeError):
                    pass 
            
            # validate city
            if extracted_data.get('city') is not None:
                try:
                    validated_data['city'] = extracted_data['city'].strip()
                except (ValueError, TypeError):
                    pass

            # validate annual rent
            if extracted_data.get('annual_rent') is not None:
                try:
                    validated_data['annual_rent'] = float(extracted_data['annual_rent'])
                except (ValueError, TypeError):
                    pass

            
            return validated_data
        except json.JSONDecodeError as e:
            self.logger.error(f"Error parsing JSON OpenAI: {e}") 
            return {}
        except Exception as e:
            self.logger.error(f"Error extracting basic lease data: {e}") 
            return {}
        
    def _perform_enriched_ai_analysis(self, lease_content: str, basic_data: Dict, market_position,
                                      legal_analysis: Dict) -> Dict:
 
        enriched_prompt = f"""
        Analyse ce bail commercial français avec les données, de marché et juridiques suivantes:

        DONNÉES EXTRAITES :
        - Adresse: {basic_data.get('address', 'Non identifiée')}
        - Surface: {basic_data.get('surface', 'Non précisée')} m²
        - Loyer annuel: {basic_data.get('annual_rent', 'Non identifié')}€

        POSITION MARCHÉ :
        - Position: {str(market_position.percentile_position)}
        - Médiane marché: {str(market_position.market_median_price)}
        - Votre prix: {str(market_position.your_estimated_price)}
        - Opportunité: {str(market_position.immediate_opportunity)}
        - Fiabilité: {str(market_position.confidence_level)}

        ANALYSE JURIDIQUE :
        - Score conformité: {legal_analysis.get('compliance_score', 'N/A')}
        - Alertes critiques: {len(legal_analysis.get('legal_alerts', []))}
        - Échéances urgentes: {len(legal_analysis.get('critical_deadlines', []))}

        CONTENU BAIL (extrait):
        {str(lease_content)[:4000].replace('{', '{{').replace('}', '}}')}

        Génère UNIQUEMENT un JSON avec cette structure :
        {{
        "opportunities": [
            {{
            "type": "string",
            "description": "string basée sur les données réelles ci-dessus",
            "impact": "montant précis en € ou N/A",
            "recommendation": "action concrète",
            "confidence": "pourcentage basé sur les données"
            }}
        ],
        "financial_metrics": {{
            "annual_rent": "montant ou N/A",
            "operational_charges": "montant estimé ou N/A", 
            "potential_savings": "montant basé sur les données marché",
            "optimized_rent": "montant basé sur médiane marché"
        }},
        "executive_summary": "2-3 phrases résumant les principales opportunités avec chiffres"
        }}
        """

        try:

            response = self.openai_client.chat.completions.create(
                    model=Settings.openai_model,
                    messages=[
                        {"role": "system", "content": self._get_enriched_system_prompt()},
                        {"role": "user", "content": enriched_prompt}
                    ],
                    temperature=0.1,
                    max_tokens=2000
                )

            response_content = response.choices[0].message.content
            
            if response_content.startswith("```json"):
                response_content  = response_content.replace("```json", "").replace("```", "")
            
            return json.loads(response_content)
        except Exception as e:
            self.logger.error(f"Error analyzing lease: {e}")
            return {
                "opportunities" : [],
                "financial_metrics": {},
                "executive_summary": f"Error analyzing lease: {e}"
            }
    
    def _get_enriched_system_prompt(self) -> str:
        return f"""
        Tu es un expert en baux commerciaux français avec 15 ans d'expérience.
        
        Tu reçois des données de marché RÉELLES et une analyse juridique PRÉCISE.
        
        OBLIGATION : Tous tes chiffres doivent être cohérents avec les données fournies.
        
        Pour les opportunités :
        - Utilise les données de marché pour calculer les gains précis
        - Référence les analyses juridiques pour les recommandations  
        - Donne des montants en euros, pas de pourcentages vagues
        
        Si une donnée n'est pas disponible, écris "N/A" mais explique pourquoi.
        
        Sois factuel, précis et actionnable. Le gestionnaire doit pouvoir agir sur tes recommandations dès demain.
        """
    
    def _build_complete_analysis(self, market_position, legal_analysis: Dict, ai_analysis: Dict,
                                 basic_data: Dict) -> LeaseAnalysisResponse:
        
        # enriched opportunities

        opportunities = []

        if "possible" in market_position.immediate_opportunity:
            opportunity_amount = re.findall(r'[\d,]+', market_position.immediate_opportunity)
            if opportunity_amount:
                opportunities.append(Opportunity(
                    type="Révision loyer sous-évalué (Données marché)",
                    description=f"Position {market_position.percentile_position}. Médiane marché: {market_position.market_median_price}",
                    impact=f"{opportunity_amount[0]}€/an",
                    recommendation=f"Négocier révision vers {market_position.market_median_price}",
                    confidence=market_position.confidence_level,
                    comparables_count=market_position.comparable_count
                ))
        
        # adding ai opportunities
        for opp in ai_analysis.get('opportunities', []):
            opportunities.append(Opportunity(**opp))
    
        # enriched executive summary
        executive_summary = f"""
        📊 POSITION MARCHÉ: {market_position.percentile_position}
        ⚖️ CONFORMITÉ: {legal_analysis.get('compliance_score', 'N/A')}  
        💰 OPPORTUNITÉ PRINCIPALE: {market_position.immediate_opportunity}
        
        {ai_analysis.get('executive_summary', '')}
        """

        return LeaseAnalysisResponse(
            # functionality 1: market intelligence
            market_intelligence=market_position,

            # functionality 2: legal compliance
            legal_alerts=legal_analysis.get('legal_alerts', []),
            critical_deadlines=legal_analysis.get('critical_deadlines', []),

            # functionality 3: financial optimization
            opportunities=opportunities,
            financial_metrics=ai_analysis.get('financial_metrics', {}),

            # summary
            executive_summary=executive_summary,
            analysis_confidence=ai_analysis.get('analysis_confidence', 'N/A')
        )