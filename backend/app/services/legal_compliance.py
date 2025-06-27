import json
import httpx
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import asdict
import openai
import logging
from app.models.schemas import LegalAlert, CriticalDeadline
from app.utils.data.legal_framework import LEGAL_FRAMEWORK
from app.config import Settings

class LegalComplianceService:
    """ legal compliance service"""

    def __init__(self, openai_api_key: str, legifrance_client_id: str = None, legifrance_client_secret: str = None,
                  logger: Optional[logging.Logger] = None):
        self.legal_framework = LEGAL_FRAMEWORK
        self.openai_client = openai.OpenAI(api_key=openai_api_key)

        # legifrance configuration
        self.legifrance_client_id = legifrance_client_id
        self.legifrance_client_secret = legifrance_client_secret
        self.legifrance_base_url = "https://api.piste.gouv.fr"
        self.legifrance_token = None
        self.logger = logger or logging.getLogger(__name__)
    
    async def analyze_compliance(self, lease_content: str) -> Dict:

        # 1. check indexation
        indexation_alerts = await self._check_indexation_compliance(lease_content)

        # 2. extract critical deadlines
        critical_deadlines = await self._extract_critical_deadlines(lease_content)

        # 3. check legal issues
        clause_alerts = await self._check_problematic_clauses(lease_content)

        # 4. compute compliance score
        all_alerts = indexation_alerts + clause_alerts
        compliance_score = self._compute_compliance_score(all_alerts)

        return {
            "legal_alerts": all_alerts,
            "critical_deadlines": critical_deadlines,
            "compliance_score": compliance_score
        }
    
    async def _check_indexation_compliance(self, content: str) -> List[LegalAlert]:

        alerts = []

        extraction_prompt = f"""
        Analyse le contenu de ce bail commercial et identifie tous les indices d'indexation mentionnés.
        
        Indices valides actuels:
        - ILAT (Indice des Loyers des Activités Tertiaires) - obligatoire depuis 2022
        - ILC (Indice des Loyers Commerciaux) - pour commerce/artisanat
        
        Indices obsolètes depuis 2022:
        - ICC (Indice du Coût de la Construction) 
        - ICT (Indice du Coût des Travaux)
        
        Bail à analyser:
        {content[:3000]}  # Limitons pour éviter les tokens excessifs
        
        Réponds uniquement en JSON avec cette structure:
        {{
            "indices_found": ["liste des indices trouvés"],
            "has_obsolete_indices": true/false,
            "obsolete_indices": ["liste des indices obsolètes trouvés"],
            "context": "phrase où l'indice obsolète est mentionné"
        }}
        """

        try:
            response = self.openai_client.chat.completions.create(
                model=Settings.openai_model,
                messages=[
                    {"role": "system", "content": "Tu es un expert juridique en baux commerciaux. Réponds uniquement en JSON valide."},
                    {"role": "user", "content": extraction_prompt}
                ],
                temperature=0.1,
                max_tokens=500
            )

            response_content = response.choices[0].message.content
            if response_content.startswith("```json"):
                response_content  = response_content.replace("```json", "").replace("```", "")
            
            result = json.loads(response_content)

            if result.get("has_obsolete_indices"):
                alerts.append(LegalAlert(
                    severity="HIGH",
                    type="Indexation obsolète",
                    description=f"Indices obsolètes détectés: { ', '.join(result.get('obsolete_indices', []))}",
                    legal_reference="Décret n°2022-1267 du 30 septembre 2022",
                    action_required="Notifier changement d'indice vers ILAT",
                    financial_impact="Perte d'indexation légale + risque contentieux"
                ))
        except json.JSONDecodeError as e:
            self.logger.error(f"Erreur extraction indexation: {e}")
            if 'response' in locals():
                self.logger.error(f"Response received: {response.choices[0].message.content}")

        except Exception as e:
            self.logger.error(f"Erreur extraction indexation: {e}")
            # in case of open ai error, we return an empty list


        return alerts

    async def _extract_critical_deadlines(self, content: str) -> List[CriticalDeadline]:

        deadlines = []

        extraction_prompt = f"""
        Analyse ce bail commercial pour identifier toutes les échéances critiques.
        
        Types d'échéances à rechercher:
        - Révisions triennales (tous les 3 ans)
        - Renouvellement de bail
        - Dates de congé/préavis
        - Échéances de paiement importantes
        
        Date actuelle: {datetime.now().strftime("%d/%m/%Y")}
        
        Bail à analyser:
        {content[:4000]}
        
        Réponds en JSON avec cette structure:
        {{
            "deadlines": [
                {{
                    "type": "Type d'échéance",
                    "date": "DD/MM/YYYY",
                    "description": "Description détaillée",
                    "urgency_level": "HIGH/MEDIUM/LOW"
                }}
            ]
        }}
        """

        try:
            response = self.openai_client.chat.completions.create(
                model=Settings.openai_model,
                messages=[
                    {"role": "system", "content": " Tu es un expert en gestion de baux commerciaux. Extrais uniquement les dates futures. Réponds uniquement en JSON valide. "},
                    {"role": "user", "content": extraction_prompt}
                ],
                temperature=0.1,
                max_tokens=800
            )

            response_content = response.choices[0].message.content.strip()
            if response_content.startswith("```json"):
                response_content = response_content.replace("```json", "").replace("```", "").strip()

            result = json.loads(response_content)

            for deadline_data in result.get("deadlines", []):
                try:
                    deadline_date = datetime.strptime(deadline_data["date"], "%d/%m/%Y")

                    if deadline_date > datetime.now():
                        days_remaining = (deadline_date - datetime.now()).days

                        urgency_mapping = {
                            "HIGH":"HIGH",
                            "MEDIUM":"MEDIUM",
                            "LOW":"LOW"
                        }

                        urgency = urgency_mapping.get(deadline_data.get("urgency_level"), "MEDIUM")

                        deadlines.append(CriticalDeadline(
                            type=deadline_date["type"],
                            date=deadline_data["date"],
                            days_remaining=days_remaining,
                            urgency=urgency,
                            action_required=f"Action requise pour : {deadline_data['description']}",
                            potential_loss=f"Impact estimé: {days_remaining * 50}€/ jour si non traité"
                        ))
                except ValueError:
                    continue
        except json.JSONDecodeError as e:
            self.logger.error(f"Error parsing JSON deadlines: {e}")
            if 'response' in locals():
                self.logger.error(f"Response received: {response.choices[0].message.content}")

        except Exception as e:
            self.logger.error(f"Error extracting deadlines: {e}")

        return sorted(deadlines, key= lambda x: x.days_remaining)
    
    async def _check_problematic_clauses(self, content: str) -> List[LegalAlert]:

        alerts = []

        # 1. extract clauses
        clauses = await self._extract_clauses_with_ai(content)

        # 2. check legal with legifrance
        for clause in clauses:
            legal_verification = await self._verify_clause_legality(clause)

            if legal_verification.get("is_problematic"):

                alerts.append(LegalAlert(
                    severity=legal_verification.get("severity", "MEDIUM"),
                    type=legal_verification.get("violation_type", "Clause problématique"),
                    description=legal_verification.get("description", "Clause non conforme détectée"),
                    legal_reference=legal_verification.get("legal_reference", "Code de commerce"),
                    action_required=legal_verification.get("action_required", "Réviser la clause"),
                    financial_impact=legal_verification.get("financial_impact", "Risque contentieux")
                ))
                

        return alerts
    
    async def _extract_clauses_with_ai(self, content: str) -> List[Dict]:

        extraction_prompt = f"""
        Extrais les clauses importantes de ce bail commercial:
        
        Types de clauses à identifier:
        - Clauses de résiliation/sortie anticipée
        - Clauses de révision de loyer
        - Clauses de destination
        - Clauses de durée
        - Clauses de garantie
        - Clauses de transfert/cession
        
        Bail:
        {content[:4000]}
        
        Réponds en JSON:
        {{
            "clauses": [
                {{
                    "type": "type de clause",
                    "content": "contenu de la clause",
                    "article_reference": "article du bail si mentionné"
                }}
            ]
        }}
        """

        try:
            response = self.openai_client.chat.completions.create(
                model=Settings.openai_model,
                messages=[
                    {"role": "system", "content": "Tu es un juriste spécialisé en baux commerciaux. Extrais uniquement les clauses importantes."},
                    {"role": "user", "content": extraction_prompt}
                ],
                temperature=0.1,
                max_tokens=1000
            )

            response_content = response.choices[0].message.content.strip()
            
            if response_content.startswith("```json"):
                response_content = response_content.replace("```json", "").replace("```", "").strip()


            result = json.loads(response_content)

            return result.get("clauses", [])
        
        except json.JSONDecodeError as e:
            self.logger.error(f"Erreur parsing JSON clauses: {e}")
            if 'response' in locals():
                self.logger.error(f"response received: {response.choices[0].message.content}")

            return []
        except Exception as e:
            self.logger.error(f"Erreur extraction clauses: {e}")
            return []
    
    async def _verify_clause_legality(self, clause: Dict) -> Dict:

        # search in legifrance
        legal_context = await self._get_legal_context_from_legifrance(clause["type"])

        # analyze with AI
        verification_prompt = f"""
        Analyse cette clause de bail commercial pour détecter les problèmes légaux:
        
        Clause à analyser:
        Type: {clause["type"]}
        Contenu: {clause["content"]}
        
        Contexte légal de référence:
        {legal_context}
        
        Évalue si cette clause:
        - Respecte le code de commerce
        - Contient des termes abusifs
        - Est conforme aux dernières évolutions légales
        
        Réponds en JSON:
        {{
            "is_problematic": true/false,
            "severity": "HIGH/MEDIUM/LOW",
            "violation_type": "Type de violation",
            "description": "Description du problème",
            "legal_reference": "Article de loi applicable",
            "action_required": "Action corrective",
            "financial_impact": "Impact financier estimé"
        }}
        """
        try:
            response = self.openai_client.chat.completions.create(
                model=Settings.openai_model,
                messages=[
                    {"role": "system", "content": "Tu es un expert juridique en droit commercial. Sois précis et factuel."},
                    {"role": "user", "content": verification_prompt}
                ],
                temperature=0.1,
                max_tokens=600
            )

            response_content = response.choices[0].message.content.strip()

            if response_content.startswith("```json"):
                response_content = response_content.replace("```json", "").replace("```", "").strip()

            return json.loads(response_content)
        
        except json.JSONDecodeError as e:
            self.logger.error(f"Error during json parsing: {e}")
            if 'response' in locals():
                self.logger.error(f"response received: {response.choices[0].message.content}")
            return {"is_problematic": False}
        except Exception as e:
            self.logger.error(f"Error during clause verification: {e}")
            return {"is_problematic": False}
        
    async def _authenticate_legifrance(self) -> str:

        if not self.legifrance_client_id or not self.legifrance_client_secret:
            self.logger.error("Missing legifrance credentials - using local framework")
            return None

        try:
            async with httpx.AsyncClient() as client:
                auth_url = f"oauth.{self.legifrance_base_url}/token"
                auth_data = {
                    "grant_type": "client_credentials",
                    "client_id": self.legifrance_client_id,
                    "client_secret": self.legifrance_client_secret,
                    "scope":"openid"
                }

                headers = {
                    "Content-Type": "application/x-www-form-urlencoded"
                }
                
                response = await client.post(auth_url, data=auth_data, headers=headers)

                response.raise_for_status()

                token_data = response.json()

                self.legifrance_token = token_data.get("access_token")
                self.logger.info(f" Authentication successful with LegiFrance")
                return self.legifrance_token
        except Exception as e:
            self.logger.error(f"Error during LegiFrance authentication: {e}")
            return None
    
    async def _get_legal_context_from_legifrance(self, clause_type: str) -> str:

        legal_mapping = {
            "résiliation":"L145-4",
            "destination": "L145-47",
            "durée": "L145-4",
            "révision":"L145-38",
            "garantie":"L145-40",
            "cession":"L145-16"
        }

        article = legal_mapping.get(clause_type.lower(), "L145-1")

        if not self.legifrance_token:
            await self._authenticate_legifrance()

        if not self.legifrance_token:
            return f"Article {article} Code de commerce - voir le framework local pour détails"
        
        try:
            async with httpx.AsyncClient() as client:
                search_url = f"{self.legifrance_base_url}/search"

                headers = {
                    "Authorization": f"Bearer {self.legifrance_token}",
                    "Content-Type": "application/json"
                }

                search_params = {
                    "query": f"article {article} code de commerce",
                    "type": "code",
                    "typePagination": "DEFAULT",
                    "sort": "PERTINENCE",
                    "pageNumber": 1,
                    "pageSize": 1
                }

                response = await client.post(search_url, json=search_params, headers=headers)

                response.raise_for_status()

                search_results = response.json()

                if search_results.get("results"):
                    first_result = search_results["results"][0]

                    article_text = first_result.get("text", "")

                    return f"Article {article} du Code de commerce: {article_text[:500]}..."
                else:
                    return f"Article {article} du Code de commerce - Texte non trouvé via API"

        except Exception as e:
            self.logger.error(f" Error during LegiFrance search: {e}")
            # fall back local
            return f"Article {article} du Code de Commerce - Voir framework local pour les détails"


    def _compute_compliance_score(self, alerts: List[LegalAlert]) -> str:

        if not alerts:
            return "95% - Excellent"
        
        high_alerts = len([a for a in alerts if a.severity == "HIGH"])
        medium_alerts = len([a for a in alerts if a.severity == "MEDIUM"])

        if high_alerts > 0:
            return f"{max(50, 90 -high_alerts*20)}% - Risques critiques détectés"
        elif medium_alerts > 2:
            return f"{max(70, 85 - medium_alerts*5)}% - Améliorations recommandées"
        else:
            return "85% - Conforme avec réserves mineures"

class LegalComplianceConfig:

    def __init__(self,
                 openai_api_key: str,
                 legifrance_client_id : Optional[str] = None,
                 legifrance_client_secret: Optional[str] = None):
        self.openai_api_key = openai_api_key
        self.legifrance_client_id = legifrance_client_id
        self.legifrance_client_secret = legifrance_client_secret

def create_legal_compliance_service(config: LegalComplianceConfig) -> LegalComplianceService:

        return LegalComplianceService(
            openai_api_key=config.openai_api_key,
            legifrance_client_id=config.legifrance_client_id,
            legifrance_client_secret=config.legifrance_client_secret
        )