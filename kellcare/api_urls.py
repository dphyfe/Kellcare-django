from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import DepartmentViewSet, DoctorViewSet, PatientViewSet, AppointmentViewSet, ContactMessageViewSet, UserViewSet
from .auth_views import get_auth_token, refresh_auth_token, get_user_info, cors_test
from .geocoding_views import geocode_address, reverse_geocode, update_doctor_coordinates, update_patient_coordinates, bulk_update_coordinates, geocoding_info

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r"departments", DepartmentViewSet)
router.register(r"doctors", DoctorViewSet)
router.register(r"patients", PatientViewSet)
router.register(r"appointments", AppointmentViewSet)
router.register(r"contact-messages", ContactMessageViewSet)
router.register(r"users", UserViewSet)

# The API URLs are now determined automatically by the router
urlpatterns = [
    path("", include(router.urls)),
    # Authentication endpoints
    path("auth/token/", get_auth_token, name="get_auth_token"),
    path("auth/refresh-token/", refresh_auth_token, name="refresh_auth_token"),
    path("auth/user/", get_user_info, name="get_user_info"),
    # Geocoding endpoints
    path("geocode/address/", geocode_address, name="geocode_address"),
    path("geocode/reverse/", reverse_geocode, name="reverse_geocode"),
    path("geocode/doctor/update/", update_doctor_coordinates, name="update_doctor_coordinates"),
    path("geocode/patient/update/", update_patient_coordinates, name="update_patient_coordinates"),
    path("geocode/bulk-update/", bulk_update_coordinates, name="bulk_update_coordinates"),
    path("geocode/info/", geocoding_info, name="geocoding_info"),
    # CORS test endpoint
    path("cors-test/", cors_test, name="cors_test"),
]
