from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from django.db.models import Q
from datetime import datetime

from .models import Department, Doctor, Patient, Appointment, ContactMessage
from .serializers import (
    DepartmentSerializer,
    DoctorSerializer,
    DoctorCreateSerializer,
    DoctorListSerializer,
    PatientSerializer,
    PatientCreateSerializer,
    PatientListSerializer,
    AppointmentSerializer,
    AppointmentCreateSerializer,
    AppointmentListSerializer,
    ContactMessageSerializer,
    UserSerializer,
)


class DepartmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing hospital departments
    """

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name", "description", "head_of_department"]
    ordering_fields = ["name", "created_at"]
    ordering = ["name"]


class DoctorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing doctors
    """

    queryset = Doctor.objects.select_related("user", "department").all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ["user__first_name", "user__last_name", "specialization", "department__name"]
    ordering_fields = ["user__first_name", "specialization", "consultation_fee", "experience_years"]
    ordering = ["user__first_name"]
    filterset_fields = ["specialization", "department", "is_available"]

    def get_serializer_class(self):
        if self.action == "create":
            return DoctorCreateSerializer
        elif self.action == "list":
            return DoctorListSerializer
        return DoctorSerializer

    @action(detail=False, methods=["get"])
    def available(self, request):
        """Get only available doctors"""
        available_doctors = self.queryset.filter(is_available=True)
        serializer = DoctorListSerializer(available_doctors, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def by_specialization(self, request):
        """Get doctors grouped by specialization"""
        specialization = request.query_params.get("spec", None)
        if specialization:
            doctors = self.queryset.filter(specialization=specialization, is_available=True)
            serializer = DoctorListSerializer(doctors, many=True)
            return Response(serializer.data)

        # Return all specializations with doctor counts
        from django.db.models import Count

        specializations = Doctor.objects.values("specialization").annotate(count=Count("id"), available_count=Count("id", filter=Q(is_available=True)))
        return Response(specializations)

    @action(detail=True, methods=["get"])
    def appointments(self, request, pk=None):
        """Get appointments for a specific doctor"""
        doctor = self.get_object()
        appointments = Appointment.objects.filter(doctor=doctor).order_by("-appointment_date")
        serializer = AppointmentListSerializer(appointments, many=True)
        return Response(serializer.data)


class PatientViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing patients
    """

    queryset = Patient.objects.select_related("user").all()
    permission_classes = [permissions.IsAuthenticated]  # Patients data is sensitive
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ["user__first_name", "user__last_name", "patient_id", "phone"]
    ordering_fields = ["user__first_name", "created_at", "date_of_birth"]
    ordering = ["user__first_name"]
    filterset_fields = ["gender", "blood_group"]

    def get_serializer_class(self):
        if self.action == "create":
            return PatientCreateSerializer
        elif self.action == "list":
            return PatientListSerializer
        return PatientSerializer

    @action(detail=True, methods=["get"])
    def appointments(self, request, pk=None):
        """Get appointments for a specific patient"""
        patient = self.get_object()
        appointments = Appointment.objects.filter(patient=patient).order_by("-appointment_date")
        serializer = AppointmentListSerializer(appointments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def medical_history(self, request, pk=None):
        """Get medical history for a patient"""
        patient = self.get_object()
        return Response(
            {
                "patient_id": patient.patient_id,
                "medical_history": patient.medical_history,
                "allergies": patient.allergies,
                "current_medications": patient.current_medications,
                "blood_group": patient.blood_group,
            }
        )


class AppointmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing appointments
    """

    queryset = Appointment.objects.select_related("patient__user", "doctor__user").all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ["patient__user__first_name", "patient__user__last_name", "doctor__user__first_name", "doctor__user__last_name", "reason"]
    ordering_fields = ["appointment_date", "created_at", "status"]
    ordering = ["-appointment_date"]
    filterset_fields = ["status", "doctor", "patient"]

    def get_serializer_class(self):
        if self.action == "create":
            return AppointmentCreateSerializer
        elif self.action == "list":
            return AppointmentListSerializer
        return AppointmentSerializer

    @action(detail=False, methods=["get"])
    def today(self, request):
        """Get today's appointments"""
        today = datetime.now().date()
        appointments = self.queryset.filter(appointment_date__date=today)
        serializer = AppointmentListSerializer(appointments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def upcoming(self, request):
        """Get upcoming appointments"""
        now = datetime.now()
        upcoming = self.queryset.filter(appointment_date__gte=now, status__in=["scheduled", "confirmed"])
        serializer = AppointmentListSerializer(upcoming, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def by_status(self, request):
        """Get appointments by status"""
        status_param = request.query_params.get("status", None)
        if status_param:
            appointments = self.queryset.filter(status=status_param)
            serializer = AppointmentListSerializer(appointments, many=True)
            return Response(serializer.data)

        # Return appointment counts by status
        from django.db.models import Count

        status_counts = Appointment.objects.values("status").annotate(count=Count("id"))
        return Response(status_counts)

    @action(detail=True, methods=["patch"])
    def update_status(self, request, pk=None):
        """Update appointment status"""
        appointment = self.get_object()
        new_status = request.data.get("status")

        if new_status not in dict(Appointment.STATUS_CHOICES):
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

        appointment.status = new_status
        appointment.save()

        serializer = self.get_serializer(appointment)
        return Response(serializer.data)

    @action(detail=True, methods=["patch"])
    def add_prescription(self, request, pk=None):
        """Add prescription to appointment"""
        appointment = self.get_object()
        prescription = request.data.get("prescription")
        notes = request.data.get("notes", "")

        if not prescription:
            return Response({"error": "Prescription is required"}, status=status.HTTP_400_BAD_REQUEST)

        appointment.prescription = prescription
        if notes:
            appointment.notes = notes
        appointment.status = "completed"
        appointment.save()

        serializer = self.get_serializer(appointment)
        return Response(serializer.data)


class ContactMessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing contact messages
    """

    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ["name", "email", "subject", "message"]
    ordering_fields = ["created_at", "name", "is_read"]
    ordering = ["-created_at"]
    filterset_fields = ["is_read"]

    def get_permissions(self):
        """
        Allow anyone to create contact messages, but only authenticated users to view/edit
        """
        if self.action == "create":
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=["get"])
    def unread(self, request):
        """Get unread messages"""
        unread_messages = self.queryset.filter(is_read=False)
        serializer = self.get_serializer(unread_messages, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["patch"])
    def mark_read(self, request, pk=None):
        """Mark message as read"""
        message = self.get_object()
        message.is_read = True
        message.save()

        serializer = self.get_serializer(message)
        return Response(serializer.data)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing users (read-only)
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["username", "first_name", "last_name", "email"]
    ordering_fields = ["username", "first_name", "last_name", "date_joined"]
    ordering = ["first_name"]
