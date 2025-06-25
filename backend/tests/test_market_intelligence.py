import pytest
import asyncio
import pandas as pd
import logging
from unittest.mock import Mock, patch, AsyncMock
from app.services.market_data_service import MarketDataService
from app.services.market_intelligence_service import MarketIntelligenceService
from app.models.schemas import MarketPosition, MarketComparable

pytest_plugins = ['pytest_asyncio']

class TestMarketDataService:
    
    @pytest.fixture
    def mock_sheet_data(self):
        today = pd.Timestamp.now(tz='UTC')

        return pd.DataFrame([
            {
                'ID': 'test1',
                'TITLE': 'Local commercial 150 m²',
                'PRICE': 5625,  
                'PRICE PER SQUARE METER': '', 
                'CITY': 'Paris 75001',
                'AREA': 150,
                'LAT': 48.8566,
                'LNG': 2.3522,
                'LAST PUBLICATION DATE': today.isoformat(),
                'REGION': 'Ile-de-France',
                'DEPARTMENT': 'Paris'
            },
            {
                'ID': 'test2', 
                'TITLE': 'Bureau centre ville 200 m²',
                'PRICE': 8667,  
                'PRICE PER SQUARE METER': '',  
                'CITY': 'Paris 75008', 
                'AREA': 200,
                'LAT': 48.8738,
                'LNG': 2.2950,
                'LAST PUBLICATION DATE': today.isoformat(),
                'REGION': 'Ile-de-France',
                'DEPARTMENT': 'Paris'
            },
            {
                'ID': 'test3',
                'TITLE': 'Local commercial Boulogne',
                'PRICE': 3800, 
                'PRICE PER SQUARE METER': '',
                'CITY': 'Boulogne-Billancourt 92100',
                'AREA': 120,
                'LAT': 48.8370,
                'LNG': 2.2400,
                'LAST PUBLICATION DATE': today.isoformat(),
                'REGION': 'Ile-de-France', 
                'DEPARTMENT': 'Hauts-de-Seine'
            },
            {
                'ID': 'test4',
                'TITLE': 'Bureau Lyon Part-Dieu',
                'PRICE': 4350, 
                'PRICE PER SQUARE METER': '',
                'CITY': 'Lyon 69003',
                'AREA': 180,
                'LAT': 45.7640,
                'LNG': 4.8357,
                'LAST PUBLICATION DATE': today.isoformat(),
                'REGION': 'Auvergne-Rhône-Alpes',
                'DEPARTMENT': 'Rhône'
            },
            
            {
                'ID': 'test5',
                'TITLE': 'Test aberrant surface',
                'PRICE': 450,  
                'PRICE PER SQUARE METER': '',
                'CITY': 'Paris 75001',
                'AREA': 5,  
                'LAT': 48.8566,
                'LNG': 2.3522,
                'LAST PUBLICATION DATE': today.isoformat(),
                'REGION': 'Ile-de-France',
                'DEPARTMENT': 'Paris'
            },
            {
                'ID': 'test6', 
                'TITLE': 'Test prix aberrant',
                'PRICE': 25000,  
                'CITY': 'Paris 75001',
                'AREA': 100,
                'LAT': 48.8566,
                'LNG': 2.3522,
                'LAST PUBLICATION DATE': today.isoformat(),
                'REGION': 'Ile-de-France',
                'DEPARTMENT': 'Paris'
            }
        ])
    
    @pytest.fixture
    def service(self):
        """ MarketDataService with test logger"""
        test_logger = logging.getLogger('market_data_service_test')
        test_logger.setLevel(logging.DEBUG)
        return MarketDataService(logger=test_logger)
    
    def test_clean_sheet_data(self, service, mock_sheet_data):
        """Testing cleaning data with real columns"""
        
        cleaned_data = service._clean_sheet_data(mock_sheet_data)
        
        #  structure verification
        assert 'final_price_per_sqm' in cleaned_data.columns
        assert 'city_normalized' in cleaned_data.columns
        
        # cleaning checks (4 ok + 2 wrong = 4 remaining)
        assert len(cleaned_data) == 4  # 2 wrong lines deleted
        
        # check computed price (PRICE / AREA)
        assert all(cleaned_data['final_price_per_sqm'] >= 5)
        assert all(cleaned_data['final_price_per_sqm'] <= 2000)
        
        # check surface
        assert all(cleaned_data['AREA'] >= 10)
        
        # check normalized city
        assert 'PARIS' in cleaned_data['city_normalized'].values
        assert 'BOULOGNE-BILLANCOURT' in cleaned_data['city_normalized'].values
        assert 'LYON' in cleaned_data['city_normalized'].values
        
        # check price/m²/year : (5625€/month × 12) ÷ 150m² = 450€/m²/an
        paris_row = cleaned_data[cleaned_data['city_normalized'] == 'PARIS'].iloc[0]
        expected_price_per_sqm_year = (5625 * 12) / 150  # 450€/m²/an
        assert abs(paris_row['final_price_per_sqm'] - expected_price_per_sqm_year) < 1
    
    def test_calculate_surface_similarity(self, service):
        
        # same surface
        assert service._calculate_surface_similarity(100, 100) == 1.0
        
        # similar surface
        assert service._calculate_surface_similarity(100, 120) == pytest.approx(0.833, rel=1e-2)
        
        # very different surface
        assert service._calculate_surface_similarity(100, 300) == pytest.approx(0.333, rel=1e-2)
        
        # edges cases
        assert service._calculate_surface_similarity(0, 100) == 0
        assert service._calculate_surface_similarity(100, 0) == 0
    
    @patch('gspread.service_account')
    @pytest.mark.asyncio
    async def test_find_exact_city_matches(self, mock_gspread, service, mock_sheet_data):
        """Testing exact city matches"""
        
        # Setup with clean data
        service.sheet_data = service._clean_sheet_data(mock_sheet_data)
        
        # Test : search Paris
        matches = service._find_exact_city_matches('Paris', 150)
        
        assert len(matches) == 2  # 2 valid announces  (test1 et test2)
        assert all(match['distance_km'] == 0.0 for match in matches)  # same city
        assert matches[0]['similarity_score'] >= matches[1]['similarity_score']  # sort by pertinence
        
        # check comparables structures
        for match in matches:
            assert 'address' in match
            assert 'price_per_sqm' in match
            assert 'surface' in match
            assert 'source' in match
            assert match['source'] == 'sheet_exact'
        
        # Test : unfound city
        no_matches = service._find_exact_city_matches('Toulouse', 150)
        assert len(no_matches) == 0
    
    def test_calculate_surface_similarity(self, service):
        """Testing surface similarity"""
        
        # same surface
        assert service._calculate_surface_similarity(100, 100) == 1.0
        
        # similar surface
        assert service._calculate_surface_similarity(100, 120) == pytest.approx(0.833, rel=1e-2)
        
        # very different surface
        assert service._calculate_surface_similarity(100, 300) == pytest.approx(0.333, rel=1e-2)
        
        # edges cases
        assert service._calculate_surface_similarity(0, 100) == 0
        assert service._calculate_surface_similarity(100, 0) == 0
    
    @patch('gspread.service_account')
    @pytest.mark.asyncio
    async def test_find_exact_city_matches(self, mock_gspread, service, mock_sheet_data):
        """Testing exact city"""
        
        # Setup with clean data
        service.sheet_data = service._clean_sheet_data(mock_sheet_data)
        
        # Test : search in Paris
        matches = service._find_exact_city_matches('Paris', 150)
        
        assert len(matches) == 2 
        assert all(match['distance_km'] == 0.0 for match in matches)  
        assert matches[0]['similarity_score'] >= matches[1]['similarity_score']  
        
        # check comparables structures
        for match in matches:
            assert 'address' in match
            assert 'price_per_sqm' in match
            assert 'surface' in match
            assert 'source' in match
            assert match['source'] == 'sheet_exact'
        
        # Test unfounf
        no_matches = service._find_exact_city_matches('Toulouse', 150)
        assert len(no_matches) == 0
    
    @patch('gspread.service_account')
    @pytest.mark.asyncio
    async def test_find_nearby_matches(self, mock_gspread, service, mock_sheet_data):
        """Test de recherche par proximité géographique"""
        
        # Setup
        service.sheet_data = service._clean_sheet_data(mock_sheet_data)
        
        # coordonates with center of Paris
        target_lat, target_lon = 48.8566, 2.3522
        
        # testing search in 20km
        nearby_matches = await service._find_nearby_matches(
            target_lat, target_lon, 150, radius_km=20
        )
        
        # should find at least 2
        assert len(nearby_matches) >= 2
        
        # checking distances
        for match in nearby_matches:
            assert match['distance_km'] <= 20
            assert 'similarity_score' in match
            assert match['source'] == 'sheet_nearby'
    
    def test_determine_region(self, service):
        
        assert service._determine_region('Paris') == 'paris_center'
        assert service._determine_region('Boulogne-Billancourt') == 'paris_banlieue'
        assert service._determine_region('Drancy') == 'paris_banlieue' 
        assert service._determine_region('Nanterre') == 'paris_banlieue'
        assert service._determine_region('Versailles') == 'idf_extended'
        assert service._determine_region('Meaux') == 'idf_extended'
        assert service._determine_region('Lyon') == 'other'
    
    def test_get_regional_baseline(self, service):
        
        assert service._get_regional_baseline('Paris') == 450
        assert service._get_regional_baseline('Drancy') == 480 
        assert service._get_regional_baseline('Versailles') == 220
        assert service._get_regional_baseline('Lyon') == 180
    
    @patch('gspread.service_account')
    @pytest.mark.asyncio
    async def test_get_market_comparables_full_workflow(self, mock_gspread, service, mock_sheet_data):
        """Testing complete workflow"""
        
        # Mock Google Sheets with real columns
        mock_sheet = Mock()
        mock_sheet.get_all_records.return_value = mock_sheet_data.to_dict('records')
        mock_gspread.return_value.open_by_url.return_value.sheet1 = mock_sheet
        
        # nominal case : Paris
        comparables = await service.get_market_comparables('Paris', 150)
        
        assert len(comparables) > 0
        assert all('price_per_sqm' in comp for comp in comparables)
        assert all('similarity_score' in comp for comp in comparables)
        assert all('address' in comp for comp in comparables)
        
        # check price coherence
        for comp in comparables:
            assert comp['price_per_sqm'] > 0
            assert comp['surface'] > 0
        
        # Tests cases with GPS coordinates
        comparables_with_gps = await service.get_market_comparables(
            'Paris', 150, target_lat=48.8566, target_lon=2.3522
        )
        assert len(comparables_with_gps) > 0
        
        # Testing fallback city unfound
        fallback_comparables = await service.get_market_comparables('Ville Inexistante', 150)
        
        assert len(fallback_comparables) >= 1 
        assert all('source' in comp for comp in fallback_comparables)
    
    def test_data_freshness_info(self, service):
        
        # before loading
        freshness = service.get_data_freshness_info()
        assert not freshness['data_available']
        assert freshness['records_count'] == 0
        
        # simulate data loaded
        service.sheet_data = pd.DataFrame([{'test': 1}])
        service.last_refresh = pd.Timestamp.now()
        
        freshness_after = service.get_data_freshness_info()
        assert freshness_after['data_available']
        assert freshness_after['records_count'] == 1
    
    def test_cache_status(self, service):
        """Test du statut du cache"""
        
        # clean cache
        assert "No data" in service.get_cache_status()
        
        # with data
        service.sheet_data = pd.DataFrame([{'test': 1}] * 100)
        service.last_refresh = pd.Timestamp.now()
        
        status = service.get_cache_status()
        assert "fresh" in status and "100" in status
    
    @patch('gspread.service_account')
    @pytest.mark.asyncio
    async def test_error_handling(self, mock_gspread, service):
        """Test de gestion d'erreurs"""
        

        mock_gspread.side_effect = Exception("Erreur connexion")
        

        result = await service.get_market_comparables('Test', 100)
        
        assert len(result) > 0  
        assert result[0]['source'] == 'emergency_fallback'


class TestWithRealDataStructure:
    """Tests spécifiques à la structure de vos données Drancy"""
    
    @pytest.fixture
    def drancy_data(self):
        """Données basées sur votre exemple Drancy"""
        return pd.DataFrame([{
            'ID': 'c89a5532b2497401450eb809e9a54eb7',
            'TITLE': 'Local commercial 350 m²',
            'PRICE': 6967,  # Prix mensuel
            'PRICE PER SQUARE METER': '',  # Vide comme dans vos données
            'CITY': 'Drancy 93700',
            'AREA': 350,
            'LAT': 48.91448,
            'LNG': 2.46143,
            'LAST PUBLICATION DATE': '2025-06-12 13:32:01+00',
            'REGION': 'Ile-de-France',
            'DEPARTMENT': 'Seine-Saint-Denis'
        }])
    
    @pytest.fixture 
    def service(self):
        test_logger = logging.getLogger('test_drancy')
        return MarketDataService(logger=test_logger)
    
    def test_drancy_data_processing(self, service, drancy_data):
        
        cleaned = service._clean_sheet_data(drancy_data)
        

        assert len(cleaned) == 1
        assert cleaned.iloc[0]['city_normalized'] == 'DRANCY'
        
        # annual computed price : (6967€/month × 12) ÷ 350m² = 238.87€/m²/year
        expected_price_year = (6967 * 12) / 350  # 238.87€/m²/an
        actual_price = cleaned.iloc[0]['final_price_per_sqm']
        assert abs(actual_price - expected_price_year) < 1
        
        # same coordinates
        assert cleaned.iloc[0]['LAT'] == 48.91448
        assert cleaned.iloc[0]['LNG'] == 2.46143
    
    def test_drancy_region_mapping(self, service):
        
        assert service._determine_region('Drancy') == 'paris_banlieue'
        assert service._get_regional_baseline('Drancy') == 480


class TestMarketIntelligenceIntegration:
    
    @pytest.fixture
    def service(self):
        return MarketIntelligenceService()
    
    @patch('gspread.service_account')
    @patch('app.services.market_intelligence_service.geocode_address')
    @pytest.mark.asyncio
    async def test_mvp_integration(self, mock_geocode, mock_gspread, service):
        """ MVP integration tests simplify"""
        
        # Mock Data
        mock_data = [{
            'ID': 'test1',
            'TITLE': 'Local test',
            'PRICE': 5000,  # 5000€/month
            'PRICE PER SQUARE METER': '',
            'CITY': 'Paris 75003',
            'AREA': 100,
            'LAT': 48.8566,
            'LNG': 2.3522,
            'LAST PUBLICATION DATE': '2024-01-01 00:00:00+00'
        }]
        
        mock_sheet = Mock()
        mock_sheet.get_all_records.return_value = mock_data
        mock_gspread.return_value.open_by_url.return_value.sheet1 = mock_sheet
        
        mock_geocode.return_value = {'lat': 48.8566, 'lon': 2.3522}
        

        result = await service.get_market_position(
            city="Paris 3e",
            address="Test Address, Paris",
            surface=100,
            current_rent=60000  # 60000€/year = 5000€/month
        )
        

        assert isinstance(result, MarketPosition)
        assert result.market_median_price is not None
        assert result.comparable_count >= 0


# Pytest configuration for asyncio
@pytest.fixture(scope="session")
def event_loop():
    """Fixture to manage asyncio event loop"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# Debugging utilities 
def debug_dataframe_structure(df):
    """Helper for dataframe debugging"""
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print(f"Sample data:\n{df.head()}")
    print(f"Data types:\n{df.dtypes}")


if __name__ == "__main__":
    # to directly run the test
    pytest.main([__file__, "-v", "--tb=short"])