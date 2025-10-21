from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import DepartmentViewSet, DoctorViewSet, PatientViewSet, AppointmentViewSet, ContactMessageViewSet, UserViewSet

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
]
