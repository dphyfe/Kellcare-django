"""
Geocoding API views for converting addresses to coordinates
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .utils.geocoding import address_to_coordinates, coordinates_to_address
from .models import Doctor, Patient


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def geocode_address(request):
    """
    Convert address to coordinates

    POST /api/geocode/address/
    {
        "address": "1600 Amphitheatre Parkway, Mountain View, CA",
        "service": "nominatim"  // optional: "nominatim" or "google"
    }
    """
    address = request.data.get("address")
    service = request.data.get("service", "nominatim")

    if not address:
        return Response({"error": "Address is required"}, status=status.HTTP_400_BAD_REQUEST)

    result = address_to_coordinates(address, service=service)

    if result["success"]:
        return Response(
            {
                "address": address,
                "latitude": result["latitude"],
                "longitude": result["longitude"],
                "formatted_address": result["formatted_address"],
                "service_used": service,
                "success": True,
            }
        )
    else:
        return Response({"address": address, "error": result["error"], "service_used": service, "success": False}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def reverse_geocode(request):
    """
    Convert coordinates to address

    POST /api/geocode/reverse/
    {
        "latitude": 37.4224764,
        "longitude": -122.0842499,
        "service": "nominatim"  // optional
    }
    """
    latitude = request.data.get("latitude")
    longitude = request.data.get("longitude")
    service = request.data.get("service", "nominatim")

    if latitude is None or longitude is None:
        return Response({"error": "Both latitude and longitude are required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        latitude = float(latitude)
        longitude = float(longitude)
    except (ValueError, TypeError):
        return Response({"error": "Latitude and longitude must be valid numbers"}, status=status.HTTP_400_BAD_REQUEST)

    result = coordinates_to_address(latitude, longitude, service=service)

    if result["success"]:
        return Response({"latitude": latitude, "longitude": longitude, "address": result["address"], "service_used": service, "success": True})
    else:
        return Response(
            {"latitude": latitude, "longitude": longitude, "error": result["error"], "service_used": service, "success": False}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_doctor_coordinates(request):
    """
    Update doctor's coordinates based on their address

    POST /api/geocode/doctor/update/
    {
        "doctor_id": 1,
        "service": "nominatim"  // optional
    }
    """
    doctor_id = request.data.get("doctor_id")
    service = request.data.get("service", "nominatim")

    if not doctor_id:
        return Response({"error": "doctor_id is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        doctor = Doctor.objects.get(id=doctor_id)
    except Doctor.DoesNotExist:
        return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)

    if not doctor.address:
        return Response({"error": "Doctor has no address to geocode"}, status=status.HTTP_400_BAD_REQUEST)

    result = address_to_coordinates(doctor.address, service=service)

    if result["success"]:
        doctor.latitude = result["latitude"]
        doctor.longitude = result["longitude"]
        doctor.save()

        return Response(
            {
                "doctor_id": doctor.id,
                "doctor_name": doctor.user.get_full_name(),
                "address": doctor.address,
                "latitude": result["latitude"],
                "longitude": result["longitude"],
                "formatted_address": result["formatted_address"],
                "service_used": service,
                "success": True,
                "message": "Doctor coordinates updated successfully",
            }
        )
    else:
        return Response(
            {
                "doctor_id": doctor.id,
                "doctor_name": doctor.user.get_full_name(),
                "address": doctor.address,
                "error": result["error"],
                "service_used": service,
                "success": False,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_patient_coordinates(request):
    """
    Update patient's coordinates based on their address

    POST /api/geocode/patient/update/
    {
        "patient_id": 1,
        "service": "nominatim"  // optional
    }
    """
    patient_id = request.data.get("patient_id")
    service = request.data.get("service", "nominatim")

    if not patient_id:
        return Response({"error": "patient_id is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        patient = Patient.objects.get(id=patient_id)
    except Patient.DoesNotExist:
        return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)

    if not patient.address:
        return Response({"error": "Patient has no address to geocode"}, status=status.HTTP_400_BAD_REQUEST)

    result = address_to_coordinates(patient.address, service=service)

    if result["success"]:
        patient.latitude = result["latitude"]
        patient.longitude = result["longitude"]
        patient.save()

        return Response(
            {
                "patient_id": patient.id,
                "patient_name": patient.user.get_full_name(),
                "address": patient.address,
                "latitude": result["latitude"],
                "longitude": result["longitude"],
                "formatted_address": result["formatted_address"],
                "service_used": service,
                "success": True,
                "message": "Patient coordinates updated successfully",
            }
        )
    else:
        return Response(
            {
                "patient_id": patient.id,
                "patient_name": patient.user.get_full_name(),
                "address": patient.address,
                "error": result["error"],
                "service_used": service,
                "success": False,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def bulk_update_coordinates(request):
    """
    Update coordinates for all doctors and patients

    POST /api/geocode/bulk-update/
    {
        "service": "nominatim",  // optional
        "update_doctors": true,  // optional, default true
        "update_patients": true  // optional, default true
    }
    """
    service = request.data.get("service", "nominatim")
    update_doctors = request.data.get("update_doctors", True)
    update_patients = request.data.get("update_patients", True)

    results = {"doctors": {"updated": 0, "failed": 0, "errors": []}, "patients": {"updated": 0, "failed": 0, "errors": []}, "service_used": service}

    # Update doctors
    if update_doctors:
        doctors = Doctor.objects.filter(address__isnull=False).exclude(address="")
        for doctor in doctors:
            result = address_to_coordinates(doctor.address, service=service)
            if result["success"]:
                doctor.latitude = result["latitude"]
                doctor.longitude = result["longitude"]
                doctor.save()
                results["doctors"]["updated"] += 1
            else:
                results["doctors"]["failed"] += 1
                results["doctors"]["errors"].append({"doctor_id": doctor.id, "doctor_name": doctor.user.get_full_name(), "error": result["error"]})

    # Update patients
    if update_patients:
        patients = Patient.objects.filter(address__isnull=False).exclude(address="")
        for patient in patients:
            result = address_to_coordinates(patient.address, service=service)
            if result["success"]:
                patient.latitude = result["latitude"]
                patient.longitude = result["longitude"]
                patient.save()
                results["patients"]["updated"] += 1
            else:
                results["patients"]["failed"] += 1
                results["patients"]["errors"].append({"patient_id": patient.id, "patient_name": patient.user.get_full_name(), "error": result["error"]})

    return Response({"message": "Bulk coordinate update completed", "results": results, "success": True})


@api_view(["GET"])
@permission_classes([])  # No authentication required
def geocoding_info(request):
    """
    Get information about available geocoding services

    GET /api/geocode/info/
    """
    from django.conf import settings

    google_api_key_configured = hasattr(settings, "GOOGLE_MAPS_API_KEY") and settings.GOOGLE_MAPS_API_KEY

    return Response(
        {
            "available_services": {
                "nominatim": {
                    "name": "Nominatim (OpenStreetMap)",
                    "cost": "Free",
                    "rate_limit": "1 request per second",
                    "accuracy": "Good",
                    "coverage": "Worldwide",
                    "available": True,
                },
                "google": {
                    "name": "Google Maps Geocoding API",
                    "cost": "Paid (with free tier)",
                    "rate_limit": "High",
                    "accuracy": "Excellent",
                    "coverage": "Worldwide",
                    "available": google_api_key_configured,
                    "requires_api_key": True,
                },
            },
            "default_service": "nominatim",
            "endpoints": {
                "geocode_address": "/api/geocode/address/",
                "reverse_geocode": "/api/geocode/reverse/",
                "update_doctor": "/api/geocode/doctor/update/",
                "update_patient": "/api/geocode/patient/update/",
                "bulk_update": "/api/geocode/bulk-update/",
            },
        }
    )
