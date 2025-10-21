from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm


def home(request):
    """Home page view"""
    return render(request, "kellcare/home.html")


def bestsellers(request):
    """Bestsellers page view"""
    return render(request, "kellcare/bestsellers.html")


def locations(request):
    """Locations page view"""
    context = {
        "dog_name": "Buddy",
        "dog_location": "Pet-Friendly Wellness Center",
    }
    return render(request, "kellcare/locations.html", context)


def major_locations(request):
    """Major Locations page view"""
    context = {
        "total_facilities": 15,
        "states_served": 8,
        "major_cities": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"],
        "flagship_hospital": "Kellcare Metropolitan Medical Center",
    }
    return render(request, "kellcare/major_locations.html", context)


def nursing_homes(request):
    """Nursing Homes page view"""
    context = {
        "nursing_homes": [
            {
                "title": "The Laurels at Greentree Ridge",
                "img": "https://lh3.googleusercontent.com/p/AF1QipNMdg8lLBIb4Z1KSaHLb9-Xs6tSOl25SRLHht7d=s680-w680-h510-rw",
                "details": "Details for Card 1",
                "bar": "green",
                "ratings": "4.5",
                "location": "35.6160252, -82.3240143",
                "address": "70 Sweeten Creek Road, Asheville, NC 28803",
                "food_ratings": "4.1",
                "staff_ratings": "3.9",
                "atmosphere_ratings": "4.5",
                "cleanliness_ratings": "4.2",
                "safety_ratings": "3.8",
                "dogs_allowed": "true",
                "nursing_care_ratings": "4.7",
            },
            {
                "title": "North Carolina Veterans Home",
                "img": "https://lh3.googleusercontent.com/gps-cs-s/AC9h4nqPB2Q3vGcHAmQKd7hk7weg7ZD99Ru2QYyMDdzFwKj1UUdh78znKKYjJN_JrA-wwqFH97dxhjHgjCIlVx6TR5QZ_XxEIrf-lWbtI706CDBWFOxPj6m3KfHkj12JwffBdmC5gqO2=w408-h272-k-no",
                "details": "Details for Card 2",
                "bar": "red",
                "ratings": "4.2",
                "location": "35.5951, -82.3515",
                "address": "1626 Jeurgens Court, Black Mountain, NC 28711",
                "food_ratings": "3.7",
                "staff_ratings": "4.2",
                "atmosphere_ratings": "4.0",
                "cleanliness_ratings": "3.8",
                "safety_ratings": "4.1",
                "dogs_allowed": "false",
                "nursing_care_ratings": "4.3",
            },
            {
                "title": "Swannanoa Valley Health and Rehabilitation",
                "img": "https://lh3.googleusercontent.com/p/AF1QipMyacgg_i4PymsystIyQDHQiSdR7uZqfnGKGQDU=w408-h306-k-no",
                "details": "Details for Card 3",
                "bar": "yellow",
                "ratings": "4.0",
                "location": "35.6000, -82.3550",
                "address": "1984 US Highway 70, Swannanoa, NC 28778",
                "food_ratings": "4.3",
                "staff_ratings": "3.8",
                "atmosphere_ratings": "4.2",
                "cleanliness_ratings": "4.0",
                "safety_ratings": "3.9",
                "dogs_allowed": "true",
                "nursing_care_ratings": "4.5",
            },
            {
                "title": "Stonecreek Health and Rehabilitation",
                "img": "https://lh3.googleusercontent.com/p/AF1QipPNS1U5cYxqhbtmNn3vWF9cs5mRTuQB6ANlkgl2=w408-h272-k-no",
                "details": "Details for Card 4",
                "bar": "green",
                "ratings": "4.3",
                "location": "35.6100, -82.3300",
                "address": "455 Victoria Road, Asheville, NC 28801",
                "food_ratings": "4.0",
                "staff_ratings": "4.1",
                "atmosphere_ratings": "3.9",
                "cleanliness_ratings": "4.4",
                "safety_ratings": "4.2",
                "dogs_allowed": "false",
                "nursing_care_ratings": "4.6",
            },
            {
                "title": "Mountain Ridge Wellness Center",
                "img": "https://lh3.googleusercontent.com/gps-cs-s/AC9h4npxb-KMwen-EKTZSGo0rSAZQfCKVe3Cl4NBwWDSDsoFuyk8Yy82e3VapmUnQUeJhQQ9saSMFy4tg4CoKPypuVqQA6cOZq1BrkwWdFeWIUe0HExuP1RBuMW7utFwpb0zYKBGRgkc=w408-h725-k-no",
                "details": "Details for Card 5",
                "bar": "yellow",
                "ratings": "4.6",
                "location": "35.6200, -82.3300",
                "address": "611 Old US Hwy 70 E, Black Mountain, NC 28711",
                "food_ratings": "3.9",
                "staff_ratings": "4.0",
                "atmosphere_ratings": "4.4",
                "cleanliness_ratings": "4.1",
                "safety_ratings": "4.3",
                "dogs_allowed": "true",
                "nursing_care_ratings": "4.8",
            },
            {
                "title": "Riverbend Health and Rehabilatation",
                "img": "https://lh3.googleusercontent.com/p/AF1QipNLnUNKscqOLiEEFPCIJlY3az7j5LOCxlx6r7Xk=w408-h270-k-no",
                "details": "Details for Card 6",
                "bar": "red",
                "ratings": "3.9",
                "location": "35.6250, -82.3200",
                "address": "8 Melissa Lee Drive, Jackson, NC 28711",
                "food_ratings": "4.2",
                "staff_ratings": "3.7",
                "atmosphere_ratings": "4.1",
                "cleanliness_ratings": "3.9",
                "safety_ratings": "4.0",
                "dogs_allowed": "false",
                "nursing_care_ratings": "4.4",
            },
        ]
    }
    return render(request, "kellcare/nursing_homes.html", context)


def pet_care(request):
    """Pet Care Facilities page view"""
    context = {
        "featured_pet": "Dexter",
        "pet_services": ["Veterinary Care", "Pet Grooming", "Pet Boarding", "Dog Training", "Pet Therapy", "Emergency Pet Care"],
        "total_pet_facilities": 8,
        "certified_vets": 25,
    }
    return render(request, "kellcare/pet_care.html", context)


def about(request):
    """About page view"""
    return render(request, "kellcare/about.html")


def services(request):
    """Services page view"""
    return render(request, "kellcare/services.html")


# advanced function with defaults
def contact(request, customer_name=None, customer_email=None):
    """Contact page view"""
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for your message! We will get back to you soon.")
            return redirect("kellcare:contact")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ContactForm()

    return render(request, "kellcare/contact.html", {"form": form})
