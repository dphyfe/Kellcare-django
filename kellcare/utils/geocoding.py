"""
Geocoding utilities for converting addresses to coordinates
"""

from geopy.geocoders import Nominatim, GoogleV3
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class GeocodeService:
    """
    Service class for geocoding addresses to coordinates
    """

    def __init__(self, service="nominatim"):
        """
        Initialize geocoding service

        Args:
            service (str): 'nominatim' (free) or 'google' (requires API key)
        """
        self.service = service
        self.geocoder = self._get_geocoder()

    def _get_geocoder(self):
        """Get the appropriate geocoder instance"""
        if self.service == "google":
            # Google Maps API (requires API key in settings)
            api_key = getattr(settings, "GOOGLE_MAPS_API_KEY", None)
            if not api_key:
                logger.warning("Google Maps API key not found, falling back to Nominatim")
                return Nominatim(user_agent="kellcare_healthcare_app")
            return GoogleV3(api_key=api_key)
        else:
            # Nominatim (OpenStreetMap) - Free but rate limited
            return Nominatim(user_agent="kellcare_healthcare_app")

    def get_coordinates(self, address):
        """
        Convert address to coordinates

        Args:
            address (str): Full address string

        Returns:
            dict: {
                'latitude': float,
                'longitude': float,
                'formatted_address': str,
                'success': bool,
                'error': str or None
            }
        """
        try:
            location = self.geocoder.geocode(address, timeout=10)

            if location:
                return {"latitude": location.latitude, "longitude": location.longitude, "formatted_address": location.address, "success": True, "error": None}
            else:
                return {"latitude": None, "longitude": None, "formatted_address": None, "success": False, "error": "Address not found"}

        except GeocoderTimedOut:
            logger.error(f"Geocoding timeout for address: {address}")
            return {"latitude": None, "longitude": None, "formatted_address": None, "success": False, "error": "Geocoding service timed out"}

        except GeocoderServiceError as e:
            logger.error(f"Geocoding service error for address {address}: {str(e)}")
            return {"latitude": None, "longitude": None, "formatted_address": None, "success": False, "error": f"Geocoding service error: {str(e)}"}

        except Exception as e:
            logger.error(f"Unexpected geocoding error for address {address}: {str(e)}")
            return {"latitude": None, "longitude": None, "formatted_address": None, "success": False, "error": f"Unexpected error: {str(e)}"}

    def reverse_geocode(self, latitude, longitude):
        """
        Convert coordinates to address

        Args:
            latitude (float): Latitude coordinate
            longitude (float): Longitude coordinate

        Returns:
            dict: {
                'address': str,
                'success': bool,
                'error': str or None
            }
        """
        try:
            location = self.geocoder.reverse(f"{latitude}, {longitude}", timeout=10)

            if location:
                return {"address": location.address, "success": True, "error": None}
            else:
                return {"address": None, "success": False, "error": "Coordinates not found"}

        except GeocoderTimedOut:
            logger.error(f"Reverse geocoding timeout for coordinates: {latitude}, {longitude}")
            return {"address": None, "success": False, "error": "Geocoding service timed out"}

        except GeocoderServiceError as e:
            logger.error(f"Reverse geocoding service error: {str(e)}")
            return {"address": None, "success": False, "error": f"Geocoding service error: {str(e)}"}

        except Exception as e:
            logger.error(f"Unexpected reverse geocoding error: {str(e)}")
            return {"address": None, "success": False, "error": f"Unexpected error: {str(e)}"}


# Convenience functions
def address_to_coordinates(address, service="nominatim"):
    """
    Quick function to convert address to coordinates

    Args:
        address (str): Full address string
        service (str): 'nominatim' or 'google'

    Returns:
        dict: Geocoding result
    """
    geocode_service = GeocodeService(service=service)
    return geocode_service.get_coordinates(address)


def coordinates_to_address(latitude, longitude, service="nominatim"):
    """
    Quick function to convert coordinates to address

    Args:
        latitude (float): Latitude coordinate
        longitude (float): Longitude coordinate
        service (str): 'nominatim' or 'google'

    Returns:
        dict: Reverse geocoding result
    """
    geocode_service = GeocodeService(service=service)
    return geocode_service.reverse_geocode(latitude, longitude)


# Usage examples:
"""
# Basic usage
from kellcare.utils.geocoding import address_to_coordinates, coordinates_to_address

# Convert address to coordinates
result = address_to_coordinates("1600 Amphitheatre Parkway, Mountain View, CA")
if result['success']:
    print(f"Latitude: {result['latitude']}")
    print(f"Longitude: {result['longitude']}")
    print(f"Formatted: {result['formatted_address']}")

# Convert coordinates to address
result = coordinates_to_address(37.4224764, -122.0842499)
if result['success']:
    print(f"Address: {result['address']}")

# Using Google Maps (requires API key in settings.py)
result = address_to_coordinates("123 Main St, New York, NY", service='google')
"""
