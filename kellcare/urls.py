from django.urls import path
from . import views

app_name = "kellcare"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("services/", views.services, name="services"),
    path("contact/", views.contact, name="contact"),
    path("bestsellers/", views.bestsellers, name="bestsellers"),
    path("urgent-care/", views.urgent_care, name="urgent_care"),
    path("locations/", views.locations, name="locations"),
    path("nursing-homes/", views.nursing_homes, name="nursing_homes"),
]
