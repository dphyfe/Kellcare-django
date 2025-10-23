"""
API consumption utilities for making HTTP requests to Django REST Framework endpoints
"""

import requests
import logging

logger = logging.getLogger(__name__)


class APIClient:
    """
    Client for consuming Django REST Framework API endpoints
    """

    def __init__(self, base_url="http://127.0.0.1:8000", token=None):
        """
        Initialize API client

        Args:
            base_url (str): Base URL for API endpoints
            token (str): Authentication token (optional)
        """
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.session = requests.Session()

        # Set default headers
        self.session.headers.update(
            {
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

        # Add authentication if token provided
        if token:
            self.session.headers.update({"Authorization": f"Token {token}"})

    def _make_request(self, method, endpoint, **kwargs):
        """
        Make HTTP request to API endpoint

        Args:
            method (str): HTTP method (GET, POST, PUT, DELETE)
            endpoint (str): API endpoint path
            **kwargs: Additional request parameters

        Returns:
            dict: JSON response data or None if error
        """
        url = f"{self.base_url}{endpoint}"

        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {method} {url} - {e}")
            return None
        except ValueError as e:
            logger.error(f"Invalid JSON response: {method} {url} - {e}")
            return None

    def get(self, endpoint, params=None):
        """GET request to API endpoint"""
        return self._make_request("GET", endpoint, params=params)

    def post(self, endpoint, data=None):
        """POST request to API endpoint"""
        return self._make_request("POST", endpoint, json=data)

    def put(self, endpoint, data=None):
        """PUT request to API endpoint"""
        return self._make_request("PUT", endpoint, json=data)

    def delete(self, endpoint):
        """DELETE request to API endpoint"""
        return self._make_request("DELETE", endpoint)


def get_api_client(request=None, base_url=None):
    """
    Get configured API client instance

    Args:
        request: Django request object (for getting auth token)
        base_url: Custom base URL (defaults to current request's host)

    Returns:
        APIClient: Configured API client
    """
    # Determine base URL
    if not base_url and request:
        base_url = request.build_absolute_uri("/")
    elif not base_url:
        base_url = "http://127.0.0.1:8000"

    # Get authentication token if available
    token = None
    if request and hasattr(request, "user") and request.user.is_authenticated:
        # Try to get token from user's auth token
        try:
            from rest_framework.authtoken.models import Token

            token_obj = Token.objects.get(user=request.user)
            token = token_obj.key
        except Exception:
            pass

    return APIClient(base_url=base_url, token=token)


# Convenience functions for common API calls
def fetch_departments(request=None, **params):
    """Fetch departments from API"""
    client = get_api_client(request)
    return client.get("/api/departments/", params=params)


def fetch_doctors(request=None, **params):
    """Fetch doctors from API"""
    client = get_api_client(request)
    return client.get("/api/doctors/", params=params)


def fetch_patients(request=None, **params):
    """Fetch patients from API"""
    client = get_api_client(request)
    return client.get("/api/patients/", params=params)


def fetch_appointments(request=None, **params):
    """Fetch appointments from API"""
    client = get_api_client(request)
    return client.get("/api/appointments/", params=params)


def geocode_address_via_api(request, address):
    """Geocode address via API endpoint"""
    client = get_api_client(request)
    return client.post("/api/geocode/address/", data={"address": address})


def reverse_geocode_via_api(request, latitude, longitude):
    """Reverse geocode coordinates via API endpoint"""
    client = get_api_client(request)
    return client.post("/api/geocode/reverse/", data={"latitude": latitude, "longitude": longitude})
