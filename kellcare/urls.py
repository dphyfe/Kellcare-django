from django.urls import path
from . import views

app_name = "kellcare"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("services/", views.services, name="services"),
    path("contact/", views.contact, name="contact"),
    path("bestsellers/", views.bestsellers, name="bestsellers"),
]
