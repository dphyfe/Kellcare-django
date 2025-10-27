from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm


def home(request):
    """Home page view"""
    return render(request, "kellcare/home.html")


def bestsellers(request):
    """Bestsellers page view - now with dynamic context data"""
    from .api_client import fetch_doctors, fetch_departments

    # Fetch data from API endpoints
    doctors_data = fetch_doctors(request)
    departments_data = fetch_departments(request)

    # Dynamic service data
    bestseller_services = [
        {
            "rank": 1,
            "badge": "⭐ #1 Most Booked",
            "badge_class": "bg-primary text-white",
            "border_class": "border-primary",
            "btn_class": "btn-primary",
            "title": "General Health Checkup",
            "description": "Comprehensive health screening including blood tests, vital signs monitoring, and general physician consultation.",
            "satisfaction": 95,
            "current_price": 149,
            "original_price": 199,
            "duration": "45 minutes",
            "completed": "1,200+",
            "icon": "🩺",
        },
        {
            "rank": 2,
            "badge": "🏆 #2 Most Popular",
            "badge_class": "bg-warning text-dark",
            "border_class": "border-warning",
            "btn_class": "btn-warning",
            "title": "Cardiology Consultation",
            "description": "Expert heart health assessment with ECG, blood pressure monitoring, and specialist consultation.",
            "satisfaction": 98,
            "current_price": 299,
            "original_price": 349,
            "duration": "60 minutes",
            "completed": "850+",
            "icon": "❤️",
        },
        {
            "rank": 3,
            "badge": "🥉 #3 Rising Star",
            "badge_class": "bg-info text-white",
            "border_class": "border-info",
            "btn_class": "btn-info",
            "title": "Pediatric Care",
            "description": "Specialized healthcare for children including vaccinations, growth monitoring, and pediatric consultations.",
            "satisfaction": 96,
            "current_price": 199,
            "original_price": 249,
            "duration": "40 minutes",
            "completed": "650+",
            "icon": "👶",
        },
    ]

    # Dynamic doctor data - combine API data with ratings and experience
    top_doctors = []
    if doctors_data and "results" in doctors_data:
        api_doctors = doctors_data["results"]

        # Create enhanced doctor profiles
        doctor_enhancements = [
            {"emoji": "👨‍⚕️", "bg_class": "bg-primary", "rating": 4.9, "experience": "15+ years", "achievement": "500+ successful treatments"},
            {"emoji": "👩‍⚕️", "bg_class": "bg-success", "rating": 4.8, "experience": "12+ years", "achievement": "400+ successful treatments"},
            {"emoji": "👩‍⚕️", "bg_class": "bg-info", "rating": 4.9, "experience": "10+ years", "achievement": "800+ happy families"},
            {"emoji": "👨‍⚕️", "bg_class": "bg-warning", "rating": 4.7, "experience": "18+ years", "achievement": "600+ procedures"},
        ]

        for i, doctor in enumerate(api_doctors[:4]):  # Top 4 doctors
            enhancement = doctor_enhancements[i] if i < len(doctor_enhancements) else doctor_enhancements[0]

            enhanced_doctor = {
                "id": doctor.get("id"),
                "name": doctor.get("name", "Dr. Unknown"),
                "specialization": doctor.get("specialization", "").replace("_", " ").title(),
                "department": doctor.get("department_name", "General Medicine"),
                "emoji": enhancement["emoji"],
                "bg_class": enhancement["bg_class"],
                "rating": enhancement["rating"],
                "rating_stars": "⭐" * int(enhancement["rating"]),
                "experience": enhancement["experience"],
                "achievement": enhancement["achievement"],
                "consultation_fee": doctor.get("consultation_fee", "200.00"),
            }
            top_doctors.append(enhanced_doctor)

    # Fallback doctors if API fails
    if not top_doctors:
        top_doctors = [
            {"name": "Dr. Sarah Johnson", "specialization": "Cardiology", "department": "Cardiology", "emoji": "👨‍⚕️", "bg_class": "bg-primary", "rating": 4.9, "rating_stars": "⭐⭐⭐⭐⭐", "experience": "15+ years", "achievement": "500+ successful treatments"},
            {"name": "Dr. Kelly Norcutt", "specialization": "Neurology", "department": "Neurology", "emoji": "👩‍⚕️", "bg_class": "bg-success", "rating": 4.8, "rating_stars": "⭐⭐⭐⭐⭐", "experience": "12+ years", "achievement": "400+ successful treatments"},
        ]

    # Department stats
    department_stats = {"total_departments": 0, "total_doctors": 0, "patient_satisfaction": 97.2, "treatments_completed": "15,000+"}

    if departments_data and "results" in departments_data:
        department_stats["total_departments"] = len(departments_data["results"])
    if doctors_data and "results" in doctors_data:
        department_stats["total_doctors"] = len(doctors_data["results"])

    context = {
        "page_title": "Our Most Popular Services",
        "page_description": "Discover our most sought-after healthcare services and top-rated medical professionals trusted by thousands of patients.",
        "bestseller_services": bestseller_services,
        "top_doctors": top_doctors,
        "department_stats": department_stats,
        "api_source": "Django REST Framework API",
        "current_year": 2025,
        "hospital_name": "Kellcare Healthcare Network",
    }

    return render(request, "kellcare/bestsellers.html", context)


def locations(request):
    """Locations page view - now with dynamic context data"""
    from .api_client import fetch_doctors, fetch_departments
    import random

    # Fetch data from API endpoints
    doctors_data = fetch_doctors(request)
    departments_data = fetch_departments(request)

    # Dynamic location data
    healthcare_locations = [
        {
            "id": 1,
            "name": "Kellcare Main Medical Center",
            "type": "Main Hospital",
            "icon": "🏥",
            "header_class": "bg-primary text-white",
            "btn_class": "btn-primary",
            "btn_outline": "btn-outline-primary",
            "address": {"street": "1000 Medical Plaza Drive", "district": "Metropolitan Health District", "city": "New York", "state": "NY", "zip": "10001"},
            "phone": "(555) 123-4567",
            "hours": "24/7 Emergency Care",
            "parking": "Free 3-hour parking",
            "services": ["Emergency Care", "Surgery Center", "ICU"],
            "service_colors": ["bg-success", "bg-info", "bg-warning text-dark"],
            "features": ["24/7 Emergency", "Full Surgery Suite", "Advanced ICU", "Trauma Center"],
            "specialties": ["Emergency Medicine", "General Surgery", "Critical Care"],
        },
        {
            "id": 2,
            "name": "Kellcare Family Clinic",
            "type": "Outpatient Center",
            "icon": "🏢",
            "header_class": "bg-success text-white",
            "btn_class": "btn-success",
            "btn_outline": "btn-outline-success",
            "address": {"street": "456 Wellness Boulevard", "district": "Suburban Health Plaza", "city": "New York", "state": "NY", "zip": "10002"},
            "phone": "(555) 234-5678",
            "hours": "Mon-Fri 8AM-6PM",
            "parking": "Free parking available",
            "services": ["Family Medicine", "Pediatrics", "Lab Services"],
            "service_colors": ["bg-success", "bg-info", "bg-warning text-dark"],
            "features": ["Family Practice", "Pediatric Care", "On-site Lab", "Wellness Programs"],
            "specialties": ["Family Medicine", "Pediatrics", "Preventive Care"],
        },
        {
            "id": 3,
            "name": "Kellcare Specialty Institute",
            "type": "Specialty Center",
            "icon": "🔬",
            "header_class": "bg-info text-white",
            "btn_class": "btn-info",
            "btn_outline": "btn-outline-info",
            "address": {"street": "789 Research Drive", "district": "Medical Innovation Campus", "city": "New York", "state": "NY", "zip": "10003"},
            "phone": "(555) 345-6789",
            "hours": "Mon-Sat 7AM-7PM",
            "parking": "Valet parking available",
            "services": ["Cardiology", "Neurology", "Research"],
            "service_colors": ["bg-danger", "bg-primary", "bg-secondary"],
            "features": ["Advanced Diagnostics", "Clinical Research", "Specialist Care", "Research Programs"],
            "specialties": ["Cardiology", "Neurology", "Medical Research"],
        },
    ]

    # Add API-sourced doctors to locations
    if doctors_data and "results" in doctors_data:
        api_doctors = doctors_data["results"]
        for i, location in enumerate(healthcare_locations):
            # Assign doctors to locations based on specialization
            if i < len(api_doctors):
                doctor = api_doctors[i]
                location["featured_doctor"] = {"name": doctor.get("name", "Dr. Unknown"), "specialization": doctor.get("specialization", "").replace("_", " ").title(), "department": doctor.get("department_name", "General Medicine"), "consultation_fee": doctor.get("consultation_fee", "200.00")}

    # Dynamic department-based services
    location_services = []
    if departments_data and "results" in departments_data:
        departments_list = departments_data["results"]
        for dept in departments_list:
            service = {"name": dept.get("name", "General Services"), "description": dept.get("description", "Comprehensive healthcare services"), "head": dept.get("head_of_department", "Medical Director"), "phone": dept.get("phone", "(555) 000-0000"), "email": dept.get("email", "info@kellcare.com")}
            location_services.append(service)

    # Pet therapy information
    pet_therapy = {
        "dog_name": "Dexter",
        "dog_breed": "Golden Retriever",
        "dog_age": "3 years old",
        "dog_location": "Pet-Friendly Wellness Center",
        "therapy_days": ["Monday", "Wednesday", "Friday"],
        "program_description": "Our certified therapy dog program helps reduce patient anxiety and promotes healing through animal-assisted therapy.",
        "services": ["Patient Visits", "Stress Reduction", "Child Therapy", "Recovery Support"],
    }

    # Location statistics
    location_stats = {"total_locations": len(healthcare_locations), "total_services": len(location_services), "emergency_locations": 1, "parking_spaces": "500+", "accessibility_rating": "100% ADA Compliant", "patient_satisfaction": 96.8}

    # Operating hours for different location types
    hours_info = {"emergency": "24/7/365 Emergency Care", "outpatient": "Mon-Fri 8AM-6PM, Sat 9AM-2PM", "specialty": "Mon-Sat 7AM-7PM", "weekend": "Weekend hours available at select locations"}

    context = {
        "page_title": "Our Healthcare Locations",
        "page_description": "Find convenient Kellcare facilities near you. We're committed to providing accessible healthcare services across multiple locations.",
        # Legacy context for existing template compatibility
        "dog_name": pet_therapy["dog_name"],
        "dog_location": pet_therapy["dog_location"],
        # New dynamic context
        "healthcare_locations": healthcare_locations,
        "location_services": location_services,
        "pet_therapy": pet_therapy,
        "location_stats": location_stats,
        "hours_info": hours_info,
        "api_source": "Django REST Framework API",
        "current_year": 2025,
        "hospital_network": "Kellcare Healthcare Network",
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
