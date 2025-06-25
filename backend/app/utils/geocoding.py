import asyncio
from typing import Optional, Dict
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import logging



class GeocodingService:

    def __init__(self, logger: Optional[logging.Logger] = None):

        self.geocoder = Nominatim(user_agent="market_intelligence_leaseboost")
        self.cache = {}
        self.logger = logger or logging.getLogger(__name__)

    async def geocode_address(self, address: str) ->  Optional[Dict[str, float]]:

        if not address or len(address.strip()) < 5:
            return None
        
        cache_key = address.lower().strip()

        if cache_key in self.cache:
            return self.cache[cache_key]
        
        try:
            location = await asyncio.wait_for(
                asyncio.to_thread(self.geocoder.geocode, f"{address}, France"),
                timeout=5.0
            )

            if location:
                result = {
                    'lat': location.latitude,
                    'lon': location.longitude
                }

                self.cache[cache_key] = result
                return result
            else:
                self.logger.warning(f"Geocoding failed for address: {address}")
                return None

        except (GeocoderTimedOut, GeocoderUnavailable, asyncio.TimeoutError) as e:
            self.logger.warning(f"Geocoding timed out for address: {address}")
            return None
        except Exception as e:
            self.logger.warning(f"Geocoding failed for address: {address} : {str(e)}")
            return None

geocoding_service = GeocodingService()

async def geocode_address(address: str) -> Optional[Dict[str, float]]:
    return await geocoding_service.geocode_address(address)