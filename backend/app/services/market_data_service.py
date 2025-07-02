import asyncio
import gspread
from typing import List, Dict, Optional
import pandas as pd
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from datetime import datetime,  timedelta
from app.utils.cities import postalcodeByCity

import statistics
import logging
import requests
from app.config import Settings
from io import StringIO

class GoogleSheetsService:
    @staticmethod
    def read_public_sheet(sheet_id: str, gid: int = 0) -> Optional[pd.DataFrame]:
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            df = pd.read_csv(StringIO(response.text))
            return df

        except Exception as e:
            print(f"Error fetching data from Google Sheets: {e}")
            return None

sheets_service = GoogleSheetsService()   

class MarketDataService:
    """
    Service to retrieve data, from now only from a google sheet
    """

    def __init__(self, logger: Optional[logging.Logger] = None):
        self.sheet_id = Settings.sheet_id
        self.sheet_data = None
        self.last_refresh = None
        self.geocoder = Nominatim(user_agent="leastboost_intelligence")

        self.logger = logger or logging.getLogger(__name__)
        self.city_coordinates_cache = {}

    async def get_market_comparables(self, target_city: str, target_surface: float,
                                     target_lat: Optional[float] = None,
                                     target_lon: Optional[float] = None) -> List[Dict]:
        """
        get comparables with fallback
        """

        try:
            # 1.refresh data if necessary
            await self._refresh_data_if_needed()

            if self.sheet_data is None or self.sheet_data.empty:
                return self._generate_fallback_comparables(target_city, target_surface)

            # 2. search exact city
            exact_matches = self._find_exact_city_matches(target_city, target_surface)

            if exact_matches is None:
                exact_matches = []

            if len(exact_matches) >= 3:
                return exact_matches[:10]

            # 3. search closest city
            if target_lat and target_lon:
                nearby_matches = await self._find_nearby_matches(target_lat, target_lon, target_surface,
                                                                 radius_km=15)
                if nearby_matches is None:
                    nearby_matches = []

                # combined exact and close matches
                combined_matches = exact_matches + nearby_matches
                if len(combined_matches) >= 3:
                    return self._deduplicate_and_rank(combined_matches)[:10]

            # 4. regional fallback    
            regional_matches = self._find_regional_matches(target_city, target_surface)

            if regional_matches is None:
                regional_matches = []

            if len(regional_matches) >= 2:
                all_matches = exact_matches + regional_matches
                return self._deduplicate_and_rank(all_matches)[:10]


            # 5. last fallback with simulate data
            return self._generate_smart_fallback(target_city, target_surface, exact_matches)
        
        except Exception as e:
            self.logger.error(f"Error in get_market_comparables: {e}")
            return self._generate_fallback_comparables(target_city, target_surface)
        
    async def _refresh_data_if_needed(self):
        """
        refresh optimized for weekly update
        """

        should_refresh = False
        refresh_reason = ""

        # 1. first load
        if self.last_refresh is None:
            should_refresh = True
            refresh_reason = "first_load"


        # 2. weekly update
        elif datetime.now() - self.last_refresh > timedelta(days=3):
            should_refresh = True
            refresh_reason = f"refresh programmed at {self.last_refresh.strftime('%Y-%m-%d %H:%M')}"

        # 3. manual refresh
        elif hasattr(self, '_force_refresh') and self._force_refresh:
            should_refresh = True
            refresh_reason = "force_refresh"
            self._force_refresh = False

        if should_refresh:
            try:
                self.logger.info(f" {refresh_reason}")


                new_df = sheets_service.read_public_sheet(self.sheet_id)

                if self.sheet_data is not None:
                    old_count = len(self.sheet_data)
                    new_count = len(new_df)

                    if abs(new_count - old_count) < 5 and new_count > 0:
                        self.logger.info(f" Minor changess detected: {old_count} - > {new_count} announces")
                    else:
                        self.logger.info(f" Major changes detected: {old_count} - > {new_count} announces")
                
                self.sheet_data = self._clean_sheet_data(new_df)

                # metrics on data
                self._log_data_metrics()

                self.last_refresh = datetime.now()
                self.logger.info(f" Data refreshed : {len(self.sheet_data)} validated announces ")
        
            except Exception as e:
                self.logger.error(f" Error refreshing google sheet data: {str(e)}")
                if self.sheet_data is None:
                    self.logger.warning(f" No data available, using fallback")

    def force_refresh(self):
        self._force_refresh = True
        self.logger.info(" Force refresh triggered for the next request")

    def _log_data_metrics(self):
        """"
        Log metrics on data quality
        """
        if self.sheet_data is not None or self.sheet_data.empty:
            self.logger.warning(f" No data available")
            return
        
        if 'CITY' in self.sheet_data.columns:
            cities_count = self.sheet_data['CITY'].nunique()
            self.logger.info(f" {cities_count} cities in the dataset")
    

    def _clean_sheet_data(self, df : pd.DataFrame) -> pd.DataFrame:

        if df.empty:
            return df
        
        self.logger.info(f" Cleaning {len(df)} raw announces")

        df.columns = [col.strip() for col in df.columns]

        df['calculated_price_per_sqm'] = None

        # if PRICE PER SQUARE is empty, compute it based on PRICE and AREA
        mask_empty_price_sqm = (df['PRICE PER SQUARE METER'].isna()) | (df['PRICE PER SQUARE METER'] == '') | (df['PRICE PER SQUARE METER'] == 0)
        mask_has_price_area = (df['PRICE'].notna()) & (df['AREA'].notna()) & (df['PRICE'] > 0) & (df['AREA'] > 0)

        try:
            df.loc[mask_empty_price_sqm & mask_has_price_area, 'calculated_price_per_sqm'] = (
            pd.to_numeric(df['PRICE'], errors='coerce') * 12 / pd.to_numeric(df['AREA'], errors='coerce')
            )
            calculated_count = mask_empty_price_sqm.sum()
            self.logger.info(f" Price/m² computed for {calculated_count} annonces")
        except Exception as e:
            self.logger.warning(f" Error in the compute price/m²: {e}")

        # use PRICE PER SQUARE METER if available otherwise compute
        df['price_per_sqm_numeric'] = pd.to_numeric(df['PRICE PER SQUARE METER'], errors='coerce')
        df['final_price_per_sqm'] = df['price_per_sqm_numeric'].fillna(df['calculated_price_per_sqm'])
        
        # Filtrering recent announces ( less than 8 weeks ago)
        if 'LAST PUBLICATION DATE' in df.columns:
            try:
                df['publication_date'] = pd.to_datetime(df['LAST PUBLICATION DATE'], errors='coerce')
                cutoff_date = pd.Timestamp.now(tz='UTC') - timedelta(weeks=8)
                
                before_count = len(df)
                df = df[df['publication_date'] >= cutoff_date].copy()
                after_count = len(df)
                
                if before_count > after_count:
                    self.logger.info(f" Filtered {before_count - after_count} announces > 8 weeks")
            except Exception as e:
                self.logger.warning(f" No filtering by date: {e}")
        
        # qualilty filter with real columns
        initial_count = len(df)
        
        df_clean = df[
            (df['final_price_per_sqm'].notna()) &
            (pd.to_numeric(df['final_price_per_sqm'], errors='coerce') > 5) &  # Minimum price
            (pd.to_numeric(df['final_price_per_sqm'], errors='coerce') < 2000) &  # Maximum price
            (df['AREA'].notna()) &
            (pd.to_numeric(df['AREA'], errors='coerce') > 10) &  # mininum area
            (pd.to_numeric(df['AREA'], errors='coerce') < 5000) &  # maximum area
            (df['CITY'].notna()) &
            (df['CITY'].str.len() > 2)  # Validated city
        ].copy()
        
        quality_filtered = initial_count - len(df_clean)
        if quality_filtered > 0:
            self.logger.info(f" Removed {quality_filtered} bad quality announces")
        
        # type conversion
        df_clean['final_price_per_sqm'] = pd.to_numeric(df_clean['final_price_per_sqm'], errors='coerce')
        df_clean['AREA'] = pd.to_numeric(df_clean['AREA'], errors='coerce')
        
        # Normalize city
        df_clean['city_normalized'] = df_clean['CITY'].str.replace(r'\s+\d{5}', '', regex=True).str.upper().str.strip()
        
        final_df = df_clean.dropna(subset=['final_price_per_sqm', 'AREA'])
        
        self.logger.info(f" Result: {len(final_df)} usable announces")
        return final_df
    
    def _find_exact_city_matches(self, target_city:str, target_surface: float) -> List[Dict]:

        if self.sheet_data is None:
            return []
        
        target_normalized = target_city.upper().strip()

        # filtering by city
        city_matches = self.sheet_data[ self.sheet_data['city_normalized'] == target_normalized].copy()

        if city_matches.empty:
            return []
        
        # scoring by surface similarity
        city_matches['similarity_score'] = city_matches['AREA'].apply(lambda x : self._calculate_surface_similarity(target_surface, x))

        comparables = []

        for _, row in city_matches.iterrows():
            if row['similarity_score'] > 0.3: # threshold
                comparables.append({
                    'address': f"{row.get('TITLE', 'Bien immobilier')} - {row['CITY']}",
                    'distance_km': 0.0, # same city
                    'price_per_sqm': float(row['final_price_per_sqm']),
                    'transaction_date': str(row.get('LAST PUBLICATION DATE', '2024'))[:10],
                    'surface': float(row['AREA']),
                    'similarity_score': row['similarity_score'],
                    'source':'sheet_exact'
                })

        return sorted(comparables, key=lambda x: x['similarity_score'], reverse=True)

    async def _find_nearby_matches(self, target_lat: float, target_lon: float, target_surface: float, radius_km = 15) -> List[Dict]:

        if self.sheet_data is None:
            return []
        
        nearby_comparables = []

        for _, row in self.sheet_data.iterrows():
            try:
                row_lat, row_lon = None, None

                if pd.notna(row.get('LAT')) and pd.notna(row.get('LNG')):
                    row_lat, row_lon = float(row['LAT']), float(row['LNG'])
                else:
                    city = row['CITY'].strip()
                    if city not in self.city_coordinates_cache:
                        location = self.geocoder.geocode(f"{city}, France")
                        if location:
                            self.city_coordinates_cache[city] = {
                                'lat': location.latitude,
                                'lon': location.longitude
                            }
                        else:
                            continue

                    city_coords = self.city_coordinates_cache[city]
                    row_lat, row_lon = city_coords['lat'], city_coords['lon']

                distance  = geodesic((row_lat, row_lon), (target_lat, target_lon)).kilometers
                
                if distance <= radius_km:

                    surface_score = self._calculate_surface_similarity(target_surface, row['AREA'])
                    distance_score = max(0, 1 - (distance / radius_km))  # normalize distance
                    combined_score = (surface_score * 0.7) + (distance_score * 0.3)

                    if combined_score > 0.2:
                        nearby_comparables.append({
                            'address': f"{row.get('TITLE', 'Bien immobilier')} - {row['CITY']}",
                            'distance_km': round(distance, 1),
                            'price_per_sqm': float(row['final_price_per_sqm']),
                            'transaction_date': str(row.get('LAST PUBLICATION DATE', '2024'))[:10],
                            'surface': float(row['AREA']),
                            'similarity_score': combined_score,
                            'source':'sheet_nearby'
                        })
            except Exception as e:
                self.logger.error(f"Error processing row: {row}")
                continue
        self.logger.info(f"finished finding nearby matches : {len(nearby_comparables)} found")
        return sorted(nearby_comparables, key=lambda x: x['similarity_score'], reverse=True)
    
    def _find_regional_matches(self, target_city: str, target_surface: float) -> List[Dict]:

        if self.sheet_data is None:
            return []
        
        target_region = self._determine_region(target_city)

        regional_cities = self._get_regional_cities(target_region)

        regional_matches = self.sheet_data[
            self.sheet_data['city_normalized'].isin([c.upper() for c in regional_cities])
        ].copy()

        if regional_matches.empty:
            return []
        
        regional_matches['similarity_score'] = regional_matches['AREA'].apply(
            lambda x : self._calculate_surface_similarity(target_surface, x) * 0.8
        )

        comparables = []

        for _, row in regional_matches.iterrows():
            if row['similarity_score'] > 0.2:
                comparables.append({
                    'address': f"Secteur {row['CITY']} (données régionales)",
                    'distance_km':8.0,
                    'price_per_sqm': float(row['final_price_per_sqm']),
                    'transaction_date': str(row.get('LAST PUBLICATION DATE', '2024'))[:10],
                    'surface': float(row['AREA']),
                    'similarity_score': row['similarity_score'],
                    'source' : 'sheet_regional'
                })

        return sorted(comparables, key=lambda x: x['similarity_score'], reverse=True)
    
    def _generate_smart_fallback(self, target_city: str, target_surface: float, existing_matches: List[Dict]) -> List[Dict]:

        smart_comparables = existing_matches.copy()

        if self.sheet_data is not None and not self.sheet_data.empty:
            regional_prices = self.sheet_data['final_price_per_sqm'].tolist()
            regional_median = statistics.median(regional_prices)
        else:
            regional_median = self._get_regional_baseline(target_city)

        simulated_addresses = [
            f"Secteur {target_city} - Estimation marché",
            f"Zone comparable {target_city}",
            f"Référence régional proche"
        ]

        for i, address in enumerate(simulated_addresses):

            price_variation = (-0.15 + (i*0.1)) # -15% to +5%
            estimated_price = regional_median * (1 + price_variation)

            smart_comparables.append({
                'address': address,
                'distance_km': 2.0 + i,
                'price_per_sqm': round(estimated_price, 0),
                'transaction_date': '2024 (estimation)',
                'surface': target_surface * (0.9 + (i * 0.1)),
                'similarity_score': 0.6 - (i * 0.1),
                'source': 'intelligent_fallback'
            })

        return smart_comparables
    
    def _calculate_surface_similarity(self, target: float, comparable : float) -> float:

        if target <= 0 or comparable <= 0:
            return 0
        
        return min(target, comparable) / max(target, comparable)
    
    def _determine_region(self, city:str) -> str:

        city_lower = city.lower()

        if city_lower.startswith('paris'):
            return 'paris_center'
        else:
            if city_lower in postalcodeByCity:
                postal_code = postalcodeByCity[city_lower]

                dept_code = postal_code[:2]
                if dept_code in ['92', '93', '94']:
                    return 'paris_banlieue'
                elif dept_code in ['77', '78', '91', '95']:
                    return 'idf_extended'
                else:
                    return 'other'
            else:
                return 'other'
    
    def _get_regional_cities(self, region: str) -> List[str]:

        regional_mapping = {
            'paris_center' : ['Paris', 'Boulogne-Billancourt', 'Neuilly-sur-Seine'],
            'paris_banlieue': ['Nanterre', 'Creteil', 'Saint-Denis', 'Montreuil', 'Drancy'],
            'idf_extended': ['Versailles', 'Meaux', 'Evry', 'Pontoise'],
            'other':[]
        }

        return regional_mapping.get(region, [])
    
    def _get_regional_baseline(self, city:str) -> float:

        region = self._determine_region(city)

        baselines = {
            'paris_center': 450,
            'paris_banlieue': 480,
            'idf_extended': 220,
            'other': 180
        }

        return baselines.get(region, 200)
    
    def _deduplicate_and_rank(slef, comparables: List[Dict]) -> List[Dict]:

        seen = set()
        unique_comparables = []

        for comp in comparables:
            key = f"{comp['address']}_{comp['price_per_sqm']}"
            if key not in seen:
                seen.add(key)
                unique_comparables.append(comp)
    
        return unique_comparables
    
    def get_data_freshness_info(self) -> Dict:

        info = {
            'last_refresh': self.last_refresh,
            'data_available': self.sheet_data is not None and not self.sheet_data.empty,
            'records_count': len(self.sheet_data) if self.sheet_data is not None else 0,
            'needs_refresh': False,
            'next_refresh_due': None
        }

        if self.last_refresh:
            days_since_refresh = (datetime.now() - self.last_refresh).days
            info['days_since_refresh'] = days_since_refresh
            info['needs_refresh'] = days_since_refresh >= 3
            info['next_refresh_due'] = self.last_refresh + timedelta(days=3)

        return info
    
    async def get_market_comparables_with_cache_info(self, target_city:str, target_surface: float,
                                                     target_lat: Optional[float] = None,
                                                     target_lon: Optional[float] = None) -> Dict:
        
        comparables = await self.get_market_comparables(target_city, target_surface, target_lat, target_lon)

        freshness_info = self.get_data_freshness_info()

        source_analysis = {}
        for comp in comparables:
            source = comp.get('source', 'unknown')
            source_analysis[source] = source_analysis.get(source, 0) + 1

        return {
            'comparables': comparables,
            'data_freshness': freshness_info,
            'source_distribution': source_analysis,
            'total_comparables' : len(comparables),
            'data_quality_score': self._calculate_data_quality_score(comparables)
        }
    
    def _calculate_data_quality_score(self, comparables: List[Dict]) -> float:


        if not comparables:
            return 0.0
        
        quality_factors = []

        # factor 1 : number of real comparables vs fallback


        real_sources = ['sheet_data', 'sheet_nearby', 'sheet_regional']
        real_count = sum(1 for comp in comparables if comp.get('source') in real_sources)
        real_ratio = real_count / len(comparables)
        quality_factors.append(real_ratio)

        # factor 2: mean of score similarity
        similarity_scores = [ comp.get('similarity_score', 0) for comp in comparables]
        avg_similarity = sum(similarity_scores) / len(similarity_scores)
        quality_factors.append(avg_similarity)

        # factor 3 : freshness of data
        freshness_info = self.get_data_freshness_info()
        if freshness_info['last_refresh']:
            days_old = (datetime.now() - freshness_info['last_refresh']).days
            freshness_score = max (0, 1 - (days_old / 14))
            quality_factors.append(freshness_score)

        return sum(quality_factors) / len(quality_factors)

    def _generate_fallback_comparables(self, city: str, surface: float) -> List[Dict]:

        baseline_price = self._get_regional_baseline(city)

        return [{
            'address': f'estimation {city}',
            'distance_km': 0,
            'price_per_sqm': baseline_price,
            'transaction_date': '2024 (estimation)',
            'surface': surface,
            'similarity_score': 0.5,
            'source': 'emergency_fallback'
        }]

    def get_cache_status(self) -> str:

        if self.sheet_data is None:
            return " No data loaded"
        
        freshness = self.get_data_freshness_info()

        if not freshness['data_available']:
            return f" empty data"
        
        if freshness['needs_refresh']:
            return f" Refresh needed ({freshness['days_since_refresh']} days old)"
        
        return f" Data is fresh ({freshness['records_count']} days old)"
