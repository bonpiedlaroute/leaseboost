import pytest
import json
import os
from unittest.mock import MagicMock
from app.services.leaseboost_service import LeaseBoostService


class TestLeaseBoostService:

    @pytest.fixture
    def service(self):

        openai_key = os.getenv("OPENAI_API_KEY")
        if not openai_key:
            pytest.skip("OPENAI_API_KEY is not set in .env")

        return LeaseBoostService(openai_api_key=openai_key,
                                 legifrance_client_id=os.getenv("LEGIFRANCE_CLIENT_ID"),
                                 legifrance_client_secret=os.getenv("LEGIFRANCE_CLIENT_SECRET")
                                 )
    
    @pytest.fixture
    def complete_lease_with_data(self):

        return """
        BAIL COMMERCIAL

        ENTRE LES SOUSSIGNÉS :
        Monsieur Jean MARTIN, propriétaire
        Société ABC COMMERCE SARL, preneur

        Article 1 - Objet et destination
        Location de locaux commerciaux situés au 123 rue de Rivoli, 75001 Paris,
        d'une superficie de 85,50 m² (quatre-vingt-cinq mètres carrés et cinquante décimètres carrés).

        Article 2 - Loyer
        Le loyer mensuel est fixé à 4 500 euros hors taxes.
        Soit un loyer annuel de 54 000 euros HT.

        Article 3 - Durée
        Le présent bail est consenti pour une durée de 9 ans.
        """
    
    @pytest.fixture
    def partial_lease_without_data(self):
        return """
        CONTRAT DE LOCATION COMMERCIALE

        Article 1 - Objet
        Location d'un local commercial situé dans le centre-ville.
        
        Article 2 - Conditions générales
        Le présent contrat est établi selon les dispositions légales en vigueur.
        Les modalités financières seront définies ultérieurement.

        Article 3 - Obligations
        Le preneur s'engage à respecter la destination commerciale des lieux.
        """
    
    @pytest.fixture
    def market_position_mock(self):

        mock = MagicMock()

        mock.percentile_position = "25ème percentile (sous-évalué)"
        mock.market_median_price = "6500€/mois"
        mock.your_estimated_price = "4500€/mois"
        mock.immediate_opportunity = "Révision possible +2000€/mois soit +24000€/an"
        mock.confidence_level = "85%"
        mock.comparable_count = 12
        return mock
    
    @pytest.fixture
    def legal_analysis_mock(self):

        return {
            "compliance_score": "75% - Améliorations recommandées",
            "legal_alerts": [
                {"type": "Indexation obsolète", "severity": "HIGH"},
                {"type": "Clause résiliation", "severity": "MEDIUM"}
            ],
            "critical_deadlines": [
                {"type": "Révision triennale", "days_remaining": 90}
            ]
        }
    
    def test_extract_basic_lease_data_complete(self, service, complete_lease_with_data):

        result = service._extract_basic_lease_data(complete_lease_with_data)

        assert isinstance(result, dict)

        #print(f"Données extraites: {result}")

        if 'address' in result:
            assert isinstance(result['address'], str)
            assert len(result['address']) > 5

            assert any(keyword in result['address'].lower() for keyword in ['rivoli', 'paris', '75001', '123'])
        
        if 'surface' in result:
            assert isinstance(result['surface'], (int, float))
            assert 80 <= result['surface'] <= 90 # expected 85.5 m2

        if 'annual_rent' in result:
            assert isinstance(result['annual_rent'], (int, float))
            assert 50000 <= result['annual_rent'] <= 60000 # expected 54 000€

    def test_extract_basic_lease_data_incomplete(self, service, partial_lease_without_data):

        result = service._extract_basic_lease_data(partial_lease_without_data)

        assert isinstance(result, dict)

        #print(f"extracted data: {result}")

        for key, value in result.items():
            if key == 'address' and value is not None:
                assert isinstance(value, str)
                assert len(value) > 0
            elif key == 'surface' and value is not None:
                assert isinstance(value, (int, float))
                assert value > 0
            elif key == 'annual_rent' and value is not None:
                assert isinstance(value, (int, float))
                assert value > 0
    

    def test_perform_enriched_ai_analysis_complete_data(self, service, market_position_mock, legal_analysis_mock):
        lease_content = """
         BAIL COMMERCIAL - 123 rue de Rivoli, Paris
        
        Article 1 - Loyer
        Loyer mensuel: 4500€ HT pour 85m²
        
        Article 2 - Révision  
        Révision triennale selon ILAT
        
        Article 3 - Résiliation
        Résiliation possible avec préavis 6 mois
        """

        basic_data = {
            "address": "123 rue de Rivoli, 75001 Paris",
            "surface": 85.5,
            "annual_rent": 54000
        }

        result = service._perform_enriched_ai_analysis(lease_content, basic_data, market_position_mock, legal_analysis_mock)

        assert isinstance(result, dict)
        assert "opportunities" in result
        assert "financial_metrics" in result
        assert "executive_summary" in result

        #print(f" Analyse enrichie: {json.dumps(result, indent=2, ensure_ascii=False)}")

        assert isinstance(result["opportunities"], list)

        if result["opportunities"]:
            first_opp = result["opportunities"][0]

            assert "type" in first_opp
            assert "description" in first_opp
            assert "impact" in first_opp
            assert "recommendation" in first_opp
            assert "confidence" in first_opp

        assert isinstance(result["financial_metrics"], dict)

        assert isinstance(result["executive_summary"], str)
        assert len(result["executive_summary"]) > 20
  
    def test_perform_enriched_ai_analysis_minimal_data(self, service):

        lease_content = "Bail commercial basique sans détails spécifiques"

        basic_data = {
            "address": None,
            "surface": None,
            "annual_rent": None
        }
        

        market_position_mock = MagicMock()
        market_position_mock.percentile_position = "Position non déterminée"
        market_position_mock.market_median_price = "N/A"
        market_position_mock.your_estimated_price = "N/A"
        market_position_mock.immediate_opportunity = "Données insuffisantes"
        market_position_mock.confidence_level = "0%"

        legal_analysis_mock = {
            "compliance_score": "N/A",
            "legal_alerts": [],
            "critical_deadlines": []
        }
        
        result = service._perform_enriched_ai_analysis(
            lease_content, basic_data, market_position_mock, legal_analysis_mock
        )

        assert isinstance(result, dict)
        assert "opportunities" in result
        assert "financial_metrics" in result
        assert "executive_summary" in result

        summary_lower = result["executive_summary"].lower()
        #print(f"Summary: {summary_lower}")
        assert any(keyword in summary_lower for keyword in ['n/a', 'insuffisant', 'manquant', 'indisponible',
                                                            'non déterminé', 'non précis', 'non identifié', 'incomplet', 'limité',
            'absent', 'vide', 'sans', 'aucun', 'pas de', 'données manquantes'])

    def test_integration_extract_and_analyze(self, service, complete_lease_with_data, market_position_mock, legal_analysis_mock):

        # 1. Extract basic lease data
        basic_data = service._extract_basic_lease_data(complete_lease_with_data)

        # 2. Perform enriched analysis
        enriched_analysis = service._perform_enriched_ai_analysis(complete_lease_with_data, basic_data, market_position_mock, legal_analysis_mock)


        #print(f"rich analysis integrated : {json.dumps(enriched_analysis, indent=2, ensure_ascii=False)}")


        assert isinstance(basic_data, dict)
        assert isinstance(enriched_analysis, dict)

        if 'annual_rent' in basic_data and basic_data['annual_rent']:
            financial_metrics = enriched_analysis.get("financial_metrics", {})

            assert isinstance(financial_metrics, dict)

    def test_extract_basic_lease_data_malformed_json_handling(self, service):

        # Test with malformed JSON
        problematic_content = """
        Bail avec des caractères spéciaux: €, %, "guillemets", 'apostrophes'
        Et des montants ambigus: 1.500,50€ ou 1,500.50€
        Adresse avec virgules: 123, rue de la Paix, 2ème étage, 75001 Paris
        """
        basic_data = service._extract_basic_lease_data(problematic_content)

        assert isinstance(basic_data, dict)
        

        #print(f"Result with problematic content: {basic_data}")

        for key, value in basic_data.items():
            if value is not None:
                if key == 'address':
                    assert isinstance(value, str)
                    assert len(value) > 0
                elif key == 'surface':
                    assert isinstance(value, (int, float))
                    assert value > 0
                elif key == 'annual_rent':
                    assert isinstance(value, (int, float))
                    assert value > 0

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])