import pytest
import json
import os
from datetime import datetime, timedelta
from app.services.legal_compliance import LegalComplianceService, LegalComplianceConfig, create_legal_compliance_service
from app.models.schemas import LegalAlert, CriticalDeadline



class TestLegalComplianceService:

    @pytest.fixture
    def service(self):
        openai_key = os.getenv("OPENAI_API_KEY")
        legifrance_client_id = os.getenv("LEGIFRANCE_CLIENT_ID")
        legifrance_client_secret = os.getenv("LEGIFRANCE_CLIENT_SECRET")

        if not openai_key:
            pytest.skip("OPENAI_API_KEY is not set in .env")

        return LegalComplianceService(
            openai_api_key=openai_key,
            legifrance_client_id=legifrance_client_id,
            legifrance_client_secret=legifrance_client_secret
        )
    
    @pytest.fixture
    def lease_with_icc(self):
        return """
        BAIL COMMERCIAL
        
        Article 3 - Indexation du loyer
        Le loyer sera révisé annuellement selon l'indice du coût de la construction (ICC) 
        publié par l'INSEE au 4ème trimestre de chaque année.
        
        Article 5 - Durée
        Le présent bail est consenti pour une durée de 9 ans.
        """
    @pytest.fixture
    def lease_with_deadline(self):

        future_date = (datetime.now() + timedelta(days=60)).strftime("%d/%m/%Y")

        return f"""
        BAIL COMMERCIAL
        
        Article 7 - Révision triennale
        Une révision du loyer pourra être demandée à compter du {future_date}
        selon les dispositions de l'article L145-38 du Code de commerce.
        
        Le bailleur devra notifier cette révision 90 jours avant l'échéance.
        """
    
    @pytest.fixture
    def lease_with_clause_issue(self):

        return """
        BAIL COMMERCIAL
        
        Article 12 - Résiliation
        Le bailleur peut résilier le bail à tout moment, de manière unilatérale,
        sans préavis ni justification, moyennant simple notification.
        
        Le preneur ne dispose d'aucun recours contre cette décision.
        """
    @pytest.mark.asyncio
    async def test_analyze_compliance_structure_reelle(self, service, lease_with_icc):

        result = await service.analyze_compliance(lease_with_icc)

        assert isinstance(result, dict)
        assert "legal_alerts" in result
        assert "critical_deadlines" in result
        assert "compliance_score" in result
        assert isinstance(result["legal_alerts"], list)
        assert isinstance(result["critical_deadlines"], list)
        assert isinstance(result["compliance_score"], str)
        assert "%" in result["compliance_score"]
    
    @pytest.mark.asyncio
    async def test_detection_icc_obselete_reel(self, service, lease_with_icc):

        alerts = await service._check_indexation_compliance(lease_with_icc)
        
        assert len(alerts) >= 0

        indexation_alerts = [a for a in alerts if "indexation" in a.type]

        if len(indexation_alerts) >= 1:
            alert = indexation_alerts[0]

            assert alert.severity == "HIGH"
            assert "ICC" in alert.description or "obsolète" in alert.description
    
    @pytest.mark.asyncio
    async def test_critical_deadlines_extraction(self, service, lease_with_deadline):

        deadlines = await service._extract_critical_deadlines(lease_with_deadline)

        
        assert isinstance(deadlines, list)

        if len(deadlines) >= 1:
            deadline = deadlines[0]

            assert deadline.days_remaining > 0
            assert deadline.days_remaining < 100
            assert deadline.urgency in ["HIGH", "MEDIUM", "LOW"]
            assert "révision" in deadline.type.lower()

    @pytest.mark.asyncio
    async def test_extraction_real_clauses(self, service,  lease_with_clause_issue):

        clauses = await service._extract_clauses_with_ai(lease_with_clause_issue)

        assert len(clauses) >= 1

        resiliation_clauses = [ c for c in clauses if "résiliation" in c["type"].lower()]

        assert len(resiliation_clauses) >=  1

        clause = resiliation_clauses[0]

        assert "unilatérale" in clause["content"] or "tout moment" in clause["content"]

    @pytest.mark.asyncio
    async def test_check_legal_clauses(self, service):

        problematic_clause = {
            "type": "résiliation",
            "content": "Le bailleur peut résilier à tout moment sans justification",
            "article_reference": "Article 12"
        }

        result = await service._verify_clause_legality(problematic_clause)

        assert "is_problematic" in result
        assert isinstance(result["is_problematic"], bool)

        if result["is_problematic"]:
            assert "severity" in result
            assert result["severity"] in ["HIGH", "MEDIUM", "LOW"]
        
    @pytest.mark.asyncio
    async def test_authentication_legifrance(self, service):


        if service.legifrance_client_id and service.legifrance_client_secret:
            token = await service._authenticate_legifrance()

            
            assert isinstance(token, str)
            assert len(token) > 10 
            assert service.legifrance_token == token
            

    @pytest.mark.asyncio
    async def test_get_legal_context_legifrance(self, service):

        context = await service._get_legal_context_from_legifrance("résiliation")

        assert isinstance(context, str)
        assert len(context) > 20
        assert "L145" in context or "Code de commerce" in context
    
    @pytest.mark.asyncio
    async def test_complete_workflow_compliance(self, service, lease_with_icc):

        result = await service.analyze_compliance(lease_with_icc)

        assert isinstance(result["legal_alerts"], list)

        if len(result["legal_alerts"]) >= 1:
            indexation_alerts = [a for a in result["legal_alerts"] if "indexation" in a.type]

        score_text = result["compliance_score"]

        assert "%" in score_text

        if any(a.severity == "HIGH" for a in result["legal_alerts"]):
            assert "Excellent" not  in score_text

    @pytest.mark.asyncio
    async def test_error_management_openai_api(self, service):

        bad_service = LegalComplianceService(openai_api_key="sk-invalid-key")

        alerts = await bad_service._check_indexation_compliance("Lease test")

        assert isinstance(alerts, list)
    
    @pytest.mark.asyncio
    async def test_performance_compliance(self, service, lease_with_icc):

        start_time = datetime.now()

        result = await service.analyze_compliance(lease_with_icc)

        duration = (datetime.now() -start_time).total_seconds()

        assert duration < 30.0


        assert isinstance(result, dict)
        assert len(result) == 3

class TestLegalComplianceIntegration:

    @pytest.mark.asyncio
    async def test_config_and_create_service(self):
        openai_key = os.getenv("OPENAI_API_KEY")

        if not openai_key:
            pytest.skip("OPENAI_API_KEY is not set in .env")
        
        config = LegalComplianceConfig(
            openai_api_key=openai_key,
            legifrance_client_id=os.getenv("LEGIFRANCE_CLIENT_ID"),
            legifrance_client_secret=os.getenv("LEGIFRANCE_CLIENT_SECRET")
        )

        service = create_legal_compliance_service(config)

        assert isinstance(service, LegalComplianceService)
        assert service.openai_client.api_key == openai_key
    
    @pytest.mark.asyncio
    async def test_analyze_real_lease(self):

        openai_key = os.getenv("OPENAI_API_KEY")
        if not openai_key:
            pytest.skip("OPENAI_API_KEY is not set in .env")
        
        service = LegalComplianceService(openai_api_key=openai_key)
        complete_lease = """
        BAIL COMMERCIAL
        
        ENTRE LES SOUSSIGNÉS :
        Monsieur Jean MARTIN, propriétaire
        Société ABC SARL, preneur
        
        Article 1 - Objet et destination
        Location de locaux commerciaux sis 123 rue de la Paix, 75001 Paris.
        Destination : commerce de détail uniquement.
        
        Article 2 - Durée  
        Bail consenti pour 9 ans à compter du 1er janvier 2023.
        Renouvellement automatique sauf congé 6 mois avant le 31 décembre 2031.
        
        Article 3 - Loyer et révision
        Loyer mensuel : 5 000 euros HT.
        Révision annuelle selon ICC publié par l'INSEE.
        Révision triennale possible à compter du 1er janvier 2026.
        
        Article 4 - Résiliation
        Le bailleur peut résilier à tout moment moyennant préavis de 3 mois.
        Le preneur supporte tous les frais de résiliation.
        
        Article 5 - Charges
        Toutes charges, taxes et impositions à la charge du preneur.
        """

        result = await service.analyze_compliance(complete_lease)

        assert len(result["legal_alerts"]) >= 1

        alert_types = [alert.type for alert in result["legal_alerts"]]

        indexation_found = any("indexation" in alert_type for alert_type in alert_types)


        if len(result["critical_deadlines"]) > 0:
            deadline = result["critical_deadlines"][0]
            assert deadline.days_remaining > 0

        assert "%" in result["compliance_score"]

    @pytest.mark.asyncio
    async def test_many_leases(self):

        openai_key = os.getenv("OPENAI_API_KEY")
        if not openai_key:
            pytest.skip("OPENAI_API_KEY is not set in .env")

        service = LegalComplianceService(openai_api_key=openai_key)

        leases_test = [
            "Bail avec ILAT conforme",
            "Bail avec ICC obsolète selon l'indice du coût de la construction",
            "Bail standard sans problème particulier"
        ]

        results = []

        for i, lease in enumerate(leases_test):
            output = await service.analyze_compliance(lease)
            results.append(output)
        
        assert len(results) == 3

        for result in results:

            assert "legal_alerts" in result
            assert "critical_deadlines" in result
            assert "compliance_score" in result

        alerts_counts = [len(r["legal_alerts"]) for r in results]

        assert all(isinstance(count, int) and count >= 0 for count in alerts_counts)

class TestPerformanceReal:

    @pytest.mark.asyncio
    async def test_huge_lease(self):

        openai_key = os.getenv("OPENAI_API_KEY")
        if not openai_key:
            pytest.skip("OPENAI_API_KEY is not set in .env")

        service = LegalComplianceService(openai_api_key=openai_key)

        huge_lease = ""

        for i in range(50):
            huge_lease += f"""
                 Artilce {i+1} - Clause standard {i+1}.
                 Texte standard répétitif pour article {i+1}.
                 Cette clause ne contient rien de particulier.                   
                """
        # Add problematic clause
        huge_lease += """
        Article 51 - Indexation
        le loyer sera revisé selo l'ICC publié par l'INSEE
        """

        start_time =  datetime.now()

        result = await service.analyze_compliance(huge_lease)

        duration = (datetime.now() - start_time).total_seconds()

        assert duration < 45.0

        indexation_alerts = [a for a in result["legal_alerts"] if "indexation" in a.type]

        assert isinstance(indexation_alerts, list)