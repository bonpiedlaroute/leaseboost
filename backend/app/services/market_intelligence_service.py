import asyncio
from typing import Dict, List, Optional
from app.services.market_data_service import MarketDataService
from app.models.schemas import MarketPosition, MarketComparable
from app.utils.geocoding import geocode_address

import logging
import statistics

class MarketIntelligenceService:


    def __init__(self, logger: Optional[logging.Logger] = None):
        self.market_data_service = MarketDataService(logger)
        self.logger = logger or logging.getLogger(__name__)

    async def get_market_position(self, city:str, address:str, surface:float,
                                  current_rent: Optional[float] = None) -> MarketPosition:
            
        try:
            # geocode address
            coordinates = await geocode_address(address)

            # get comparables
            comparables_data = await self.market_data_service.get_market_comparables(
                target_city=city,
                target_surface=surface,
                target_lat=coordinates.get('lat') if coordinates else None,
                target_lon=coordinates.get('lon') if coordinates else None                
            )

            # convert market comparables
            market_comparables = self._convert_to_market_comparables(comparables_data)

            # compute market position
            market_position = self._calculate_detailed_market_position(
                address,
                surface,
                current_rent, 
                market_comparables
            )

            return market_position
        except Exception as e:
            logging.error(f"Error computing market position: {str(e)}")
            return self._create_fallback_market_position(f"Error computing market position: {str(e)}")
    
    def _convert_to_market_comparables(self, comparables_data: List[Dict]) -> List[MarketComparable]:

        market_comparables = []
        for comp in comparables_data:
            market_comparables.append(MarketComparable(
                address=comp['address'],
                distance_km=comp['distance_km'],
                price_per_sqm=comp['price_per_sqm'],
                transaction_date=comp['transaction_date'],
                surface=comp['surface'],
                similarity_score=comp['similarity_score']
            ))
        
        return market_comparables
    
    def _calculate_detailed_market_position(self, address: str, surface: float, current_rent: Optional[float],
                                            comparables: List[MarketComparable]) -> MarketPosition:
        
        if not comparables:
            return self._create_fallback_market_position("No comparables found")
        
        #  1. computation of market statistics
        market_prices = [comp.price_per_sqm for comp in comparables]
        market_prices.sort()

        if len(market_prices) > 4:
            trim_count = max(1, len(market_prices) // 10 )
            trimmed_prices = market_prices[trim_count: - trim_count]
        else:
            trimmed_prices = market_prices

        median_price = statistics.median(trimmed_prices)
        mean_price = statistics.mean(trimmed_prices)

        # 2. price estimation
        if current_rent:
            current_price_per_sqm = current_rent / surface
        else:
            current_price_per_sqm = self._estimate_current_rent(trimmed_prices, surface)

        # 3. percentile
        below_current = len([p for p in market_prices if p < current_price_per_sqm])
        percentile = (below_current / len(market_prices)) * 100

        # 4 opportunity analysis

        opportunity_analysis = self._calculate_opportunity_analysis(current_price_per_sqm,
                                                                    median_price,
                                                                    mean_price,
                                                                    surface,
                                                                    percentile
                                                                    )
        
        # 5 assess data quality
        data_quality = self._assess_data_quality(comparables)
        return MarketPosition(
            percentile_position= opportunity_analysis['position_text'],
            market_median_price=f"{median_price:.0f}",
            your_estimated_price=f"{current_price_per_sqm:.2f}",
            immediate_opportunity=data_quality['opportunity_text'],
            confidence_level=f"{data_quality['confidence_percentabe']}",
            comparable_count=len(comparables),
            comparables=comparables
        )
    
    def _estimate_current_rent(self, market_prices: List[float], surface: float) -> float:

        median_market = statistics.median(market_prices)

        if surface > 500:
            undervalue_factor = 0.88
        elif surface > 200:
            undervalue_factor = 0.85
        else:
            undervalue_factor = 0.82

        return median_market * undervalue_factor
    
    def _calculate_opportunity_analysis(self, current_price: float, median_price: float, mean_price: float, surface: float, 
                                        percentile: float) -> Dict[str, str]:
        
        # compute spread
        gap_vs_median = median_price  - current_price
        annual_opportunity = gap_vs_median * surface

        # percentage
        percent_gap = (gap_vs_median / median_price) * 100 if median_price > 0 else 0

        # intelligent classification
        if percentile <= 15:
            position_text = f"{int(percentile)}ème percentile - LARGEMENT SOUS-ÉVALUÉ"
            if annual_opportunity > 0:
                opportunity_text = f" Opportunité majeure: +{annual_opportunity:,.0f}€/an (+{percent_gap:.0f}%)"
            else:
                opportunity_text = "Déjà très bien positionné"

        elif percentile <= 35:
            position_text = f"{int(percentile)}ème percentile - SOUS-ÉVALUÉ"
            if annual_opportunity > 0:
                opportunity_text = f" Potentiel: +{annual_opportunity:,.0f}€/an (+{percent_gap:.0f}%)"
            else:
                opportunity_text = "Correctement positionné"

        elif percentile <= 65:
            position_text = f"{int(percentile)}ème percentile - Dans la norme"
            if abs(annual_opportunity) < surface * 50: # less than 50€ per year of spread
                opportunity_text = "Prix aligné sur le marché"
            elif annual_opportunity > 0:
                opportunity_text = f"Légère opportunité: +{annual_opportunity:,.0f}€/an"
            else:
                opportunity_text = f"Légèrement au-dessus: {annual_opportunity:,.0f}€/an"

        else:
            position_text = f"{int(percentile)}ème percentile - Au-dessus du marché"
            if annual_opportunity < 0:
                opportunity_text = f" Risque: {abs(annual_opportunity):,.0f}€/an au dessus du marché"
            else:
                opportunity_text = "Dans le haute de la fourchette"
        
        return {
            'position_text': position_text,
            'opportunity_text': opportunity_text
        }

    def _assess_data_quality(self, comparables: List[MarketComparable]) -> Dict:

        # quality factor
        count_factor = min(len(comparables)/8, 1.0)

        # quality score
        similarity_scores = [ comp.similarity_score for comp in comparables]
        avg_similarity = statistics.mean(similarity_scores) if similarity_scores else 0

        # data source
        sources = [getattr(comp, 'source', 'unknown') for comp in comparables]
        source_quality = 1.0
        if any('fallback' in str(s) for s in sources):
            source_quality = 0.7
        elif any('estimation' in str(s) for s in sources):
            source_quality = 0.8

        # Score global
        global_confidence = count_factor * avg_similarity * source_quality
        confidence_percentage = int(global_confidence *  100)

        return {
            'confidence_percentage': min (confidence_percentage, 95), 
            'count_factor': count_factor,
            'similarity_score': avg_similarity,
            'source_quality': source_quality
        }
    
    def _select_best_comparables_for_display(self, comparables: List[MarketComparable], 
                                             count: int) -> List[MarketComparable]:
        
        sorted_comparables = sorted(
            comparables,
            key=lambda x: (x.similarity_score, -x.distance_km),
            reverse=True
        )

        return sorted_comparables[:count]
    
    def _create_fallback_market_position(self, error_msg: str) -> MarketPosition:

        return MarketPosition(
            percentile_position="Position non déterminée",
            market_median_price="N/A",
            your_estimated_price="N/A",
            immediate_opportunity= f"Analyse impossible: {error_msg}",
            confidence_level="0%",
            comparable_count=0,
            comparables=[]
        )
        



