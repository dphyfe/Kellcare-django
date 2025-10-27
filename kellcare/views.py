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
        "dog_name": "Dexter",
        "dog_location": "Pet-Friendly Wellness Center",
    }
    return render(request, "kellcare/locations.html", context)


def major_locations(request):
    """Major Locations page view - now consuming Django REST Framework API"""
    from .api_client import fetch_departments, fetch_doctors

    # Fetch data from API endpoints instead of direct database access
    departments_data = fetch_departments(request)
    doctors_data = fetch_doctors(request)

    # Default values in case API calls fail
    total_departments = 0
    total_doctors = 0
    major_specializations = []
    flagship_hospital = "Kellcare Medical Center"
    departments_list = []

    # Process departments data from API
    if departments_data and "results" in departments_data:
        departments_list = departments_data["results"]
        total_departments = len(departments_list)
        if departments_list:
            flagship_hospital = departments_list[0]["name"]

    # Process doctors data from API
    if doctors_data and "results" in doctors_data:
        doctors_list = doctors_data["results"]
        total_doctors = len(doctors_list)

        # Count specializations from API data
        specialization_counts = {}
        for doctor in doctors_list:
            spec = doctor.get("specialization", "general")
            specialization_counts[spec] = specialization_counts.get(spec, 0) + 1

        # Get top 5 specializations
        sorted_specs = sorted(specialization_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        major_specializations = [spec[0].replace("_", " ").title() for spec in sorted_specs]

    context = {
        "total_facilities": total_departments,
        "total_doctors": total_doctors,
        "states_served": 8,  # This could be calculated from doctor addresses if needed
        "major_cities": major_specializations,  # Using specializations instead of cities
        "flagship_hospital": flagship_hospital,
        "departments_with_counts": departments_list[:6],  # Top 6 departments
        "api_source": "Django REST Framework API",  # Show that data comes from API
        # YOUR CUSTOM CONTEXT - Add any data you want here
        "custom_message": "Welcome to Kellcare Healthcare Network!",
        "company_founded": 1995,
        "ceo_name": "Dr. Sarah Mitchell",
        "awards": ["Best Healthcare Provider 2024", "Excellence in Patient Care 2023", "Innovation Award 2022"],
        "featured_services": {"emergency": "24/7 Emergency Care", "telehealth": "Virtual Consultations", "specialist": "Expert Specialist Care"},
        "patient_satisfaction": 98.5,
        "custom_data": {"current_year": 2025, "locations_expanded": True, "new_technology": "AI-Powered Diagnostics"},
        # DYNAMIC ADDRESS DATA
        "flagship_address": {
            "street": "1000 Medical Plaza Drive",
            "district": "Metropolitan Health District",
            "city": "New York",
            "state": "NY",
            "zip": "10001",
            "main_phone": "(555) 100-2000",
            "emergency_phone": "(555) 911-HELP",
            "formatted_address": "1000 Medical Plaza Drive, Metropolitan Health District, New York, NY 10001",
        },
        # Multiple location addresses
        "regional_addresses": {
            "east_coast": {
                "new_york": {"name": "Kellcare Manhattan Medical Center", "street": "1000 Medical Plaza Drive", "city": "New York", "state": "NY", "zip": "10001", "phone": "(555) 100-2000"},
                "boston": {"name": "Kellcare New England Medical", "street": "450 Healthcare Boulevard", "city": "Boston", "state": "MA", "zip": "02115", "phone": "(617) 555-3000"},
                "philadelphia": {"name": "Kellcare Liberty Medical", "street": "789 Independence Avenue", "city": "Philadelphia", "state": "PA", "zip": "19104", "phone": "(215) 555-4000"},
            },
            "west_coast": {
                "los_angeles": {"name": "Kellcare Pacific Medical", "street": "2500 Sunset Medical Drive", "city": "Los Angeles", "state": "CA", "zip": "90027", "phone": "(213) 555-5000"},
                "san_francisco": {"name": "Kellcare Bay Area Medical", "street": "1850 Golden Gate Health Plaza", "city": "San Francisco", "state": "CA", "zip": "94115", "phone": "(415) 555-6000"},
            },
        },
    }
    return render(request, "kellcare/major_locations.html", context)


def nursing_homes(request):
    """Nursing Homes page view - now consuming Django REST Framework API and geocoding API"""
    from .api_client import fetch_doctors, fetch_departments, geocode_address_via_api
    import random

    # Fetch data from API endpoints instead of direct database access
    doctors_data = fetch_doctors(request)
    departments_data = fetch_departments(request)

    nursing_homes_data = []

    # Process doctors data from API
    if doctors_data and "results" in doctors_data:
        doctors_list = doctors_data["results"]

        # Filter for relevant specializations
        nursing_doctors = [doc for doc in doctors_list if doc.get("specialization") in ["general", "cardiology", "neurology"]]

        # Convert API data to format expected by template
        for doctor in nursing_doctors:
            # Generate some sample ratings (in production, these would come from a ratings model)
            base_rating = round(random.uniform(3.5, 4.8), 1)

            # Use existing coordinates or try to geocode via API
            location_coords = ""
            if doctor.get("latitude") and doctor.get("longitude"):
                location_coords = f"{doctor['latitude']}, {doctor['longitude']}"
            elif doctor.get("address"):
                # Try to geocode via API endpoint
                try:
                    geocode_result = geocode_address_via_api(request, doctor["address"])
                    if geocode_result and geocode_result.get("latitude"):
                        location_coords = f"{geocode_result['latitude']}, {geocode_result['longitude']}"
                    else:
                        location_coords = "0, 0"  # Default if geocoding fails
                except Exception:
                    location_coords = "0, 0"  # Default if API call fails
            else:
                location_coords = "0, 0"

            # Get user info from nested data
            user_data = doctor.get("user", {})
            first_name = user_data.get("first_name", "Unknown")
            last_name = user_data.get("last_name", "Doctor")

            # Create nursing home data structure from API data
            nursing_home = {
                "title": f"Dr. {first_name} {last_name} Medical Center",
                "img": doctor.get("photo") or "https://via.placeholder.com/400x300?text=Medical+Facility",
                "details": doctor.get("bio") or f"Specializing in {doctor.get('specialization', 'General').replace('_', ' ').title()}",
                "bar": "green" if base_rating >= 4.3 else "yellow" if base_rating >= 4.0 else "red",
                "ratings": str(base_rating),
                "location": location_coords,
                "address": doctor.get("address", "Address not provided"),
                "food_ratings": str(round(base_rating + random.uniform(-0.5, 0.3), 1)),
                "staff_ratings": str(round(base_rating + random.uniform(-0.3, 0.4), 1)),
                "atmosphere_ratings": str(round(base_rating + random.uniform(-0.4, 0.5), 1)),
                "cleanliness_ratings": str(round(base_rating + random.uniform(-0.2, 0.3), 1)),
                "safety_ratings": str(round(base_rating + random.uniform(-0.3, 0.4), 1)),
                "dogs_allowed": "true" if random.choice([True, False]) else "false",
                "nursing_care_ratings": str(round(base_rating + random.uniform(0.1, 0.6), 1)),
            }
            nursing_homes_data.append(nursing_home)

    # If no doctors available from API, create sample data from departments API
    if not nursing_homes_data and departments_data and "results" in departments_data:
        departments_list = departments_data["results"]

        for dept in departments_list[:6]:
            base_rating = round(random.uniform(3.8, 4.6), 1)
            nursing_home = {
                "title": f"{dept['name']} Rehabilitation Center",
                "img": "https://via.placeholder.com/400x300?text=Medical+Facility",
                "details": dept.get("description", "Comprehensive healthcare facility"),
                "bar": "green" if base_rating >= 4.2 else "yellow" if base_rating >= 3.9 else "red",
                "ratings": str(base_rating),
                "location": "35.6000, -82.3500",  # Default location
                "address": "Kellcare Medical Center - Location Data Coming Soon",
                "food_ratings": str(round(base_rating + random.uniform(-0.3, 0.2), 1)),
                "staff_ratings": str(round(base_rating + random.uniform(-0.2, 0.3), 1)),
                "atmosphere_ratings": str(round(base_rating + random.uniform(-0.3, 0.4), 1)),
                "cleanliness_ratings": str(round(base_rating + random.uniform(-0.1, 0.3), 1)),
                "safety_ratings": str(round(base_rating + random.uniform(-0.2, 0.3), 1)),
                "dogs_allowed": "true" if random.choice([True, False]) else "false",
                "nursing_care_ratings": str(round(base_rating + random.uniform(0.2, 0.5), 1)),
            }
            nursing_homes_data.append(nursing_home)

    context = {
        "nursing_homes": nursing_homes_data[:6],  # Limit to 6 facilities
        "api_source": "Django REST Framework API + Geocoding API",  # Show data source
    }
    return render(request, "kellcare/nursing_homes.html", context)


def pet_care(request):
    """Pet Care Facilities page view - fully consuming Django REST Framework API"""
    from .api_client import fetch_doctors, fetch_departments

    # Consume API endpoints directly
    doctors_data = fetch_doctors(request)
    departments_data = fetch_departments(request)

    # Process API response
    total_vets = 0
    total_pet_facilities = 8  # Default value
    api_doctors = []

    # Count departments that could be pet-related facilities
    if departments_data and "results" in departments_data:
        departments_list = departments_data["results"]
        total_pet_facilities = len(departments_list) + 3  # Add some pet-specific facilities
        print(f"DEBUG: Found {len(departments_list)} departments, total_pet_facilities = {total_pet_facilities}")

    if doctors_data and "results" in doctors_data:
        all_doctors = doctors_data["results"]
        print(f"DEBUG: Found {len(all_doctors)} total doctors")

        # Filter for veterinary doctors (general practitioners)
        veterinary_doctors = [doc for doc in all_doctors if doc.get("specialization") == "general"]
        print(f"DEBUG: Found {len(veterinary_doctors)} general practitioners")

        total_vets = len(veterinary_doctors)
        api_doctors = veterinary_doctors[:5]  # First 5 veterinary doctors

        # If no general practitioners, count all doctors as potential vets
        if total_vets == 0:
            total_vets = len(all_doctors)
            api_doctors = all_doctors[:5]
            print(f"DEBUG: No general practitioners, using all {total_vets} doctors")

    print(f"DEBUG: Final values - total_pet_facilities: {total_pet_facilities}, certified_vets: {total_vets}")

    context = {
        "featured_pet": "Dexter",
        "featured_pet2": "Burt",
        "pet_services": ["Veterinary Care", "Pet Grooming", "Pet Boarding", "Dog Training", "Pet Therapy", "Emergency Pet Care"],
        "total_pet_facilities": total_pet_facilities,  # Now dynamic from API
        "certified_vets": total_vets,  # From API
        "api_doctors": api_doctors,  # From API
        "api_example_url": request.build_absolute_uri("/api/doctors/"),
        "api_source": "Django REST Framework API",  # Show data source
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
