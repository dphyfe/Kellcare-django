from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Department, Doctor, Patient, Appointment, ContactMessage


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "date_joined"]
        read_only_fields = ["id", "date_joined"]


class DepartmentSerializer(serializers.ModelSerializer):
    """Serializer for Department model"""

    class Meta:
        model = Department
        fields = "__all__"
        read_only_fields = ["id", "created_at"]


class DoctorSerializer(serializers.ModelSerializer):
    """Serializer for Doctor model"""

    user = UserSerializer(read_only=True)
    department_name = serializers.CharField(source="department.name", read_only=True)

    class Meta:
        model = Doctor
        fields = "__all__"
        read_only_fields = ["id", "created_at"]


class DoctorCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating Doctor with User"""

    user_data = UserSerializer()

    class Meta:
        model = Doctor
        fields = [
            "user_data",
            "license_number",
            "specialization",
            "department",
            "phone",
            "address",
            "experience_years",
            "consultation_fee",
            "is_available",
            "bio",
            "photo",
        ]

    def create(self, validated_data):
        user_data = validated_data.pop("user_data")
        user = User.objects.create_user(**user_data)
        doctor = Doctor.objects.create(user=user, **validated_data)
        return doctor


class PatientSerializer(serializers.ModelSerializer):
    """Serializer for Patient model"""

    user = UserSerializer(read_only=True)
    age = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = "__all__"
        read_only_fields = ["id", "created_at"]

    def get_age(self, obj):
        from datetime import date

        today = date.today()
        return today.year - obj.date_of_birth.year - ((today.month, today.day) < (obj.date_of_birth.month, obj.date_of_birth.day))


class PatientCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating Patient with User"""

    user_data = UserSerializer()

    class Meta:
        model = Patient
        fields = [
            "user_data",
            "patient_id",
            "date_of_birth",
            "gender",
            "blood_group",
            "phone",
            "emergency_contact",
            "emergency_phone",
            "address",
            "medical_history",
            "allergies",
            "current_medications",
            "insurance_provider",
            "insurance_number",
        ]

    def create(self, validated_data):
        user_data = validated_data.pop("user_data")
        user = User.objects.create_user(**user_data)
        patient = Patient.objects.create(user=user, **validated_data)
        return patient


class AppointmentSerializer(serializers.ModelSerializer):
    """Serializer for Appointment model"""

    patient_name = serializers.CharField(source="patient.user.get_full_name", read_only=True)
    doctor_name = serializers.CharField(source="doctor.user.get_full_name", read_only=True)
    patient_id = serializers.CharField(source="patient.patient_id", read_only=True)
    doctor_specialization = serializers.CharField(source="doctor.specialization", read_only=True)

    class Meta:
        model = Appointment
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class AppointmentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating appointments"""

    class Meta:
        model = Appointment
        fields = ["patient", "doctor", "appointment_date", "duration", "reason"]


class ContactMessageSerializer(serializers.ModelSerializer):
    """Serializer for ContactMessage model"""

    class Meta:
        model = ContactMessage
        fields = "__all__"
        read_only_fields = ["id", "created_at"]


# Specialized serializers for different use cases
class DoctorListSerializer(serializers.ModelSerializer):
    """Simplified serializer for doctor lists"""

    name = serializers.CharField(source="user.get_full_name", read_only=True)
    department_name = serializers.CharField(source="department.name", read_only=True)

    class Meta:
        model = Doctor
        fields = ["id", "name", "specialization", "department_name", "consultation_fee", "is_available", "photo"]


class PatientListSerializer(serializers.ModelSerializer):
    """Simplified serializer for patient lists"""

    name = serializers.CharField(source="user.get_full_name", read_only=True)
    age = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = ["id", "name", "patient_id", "gender", "age", "phone"]

    def get_age(self, obj):
        from datetime import date

        today = date.today()
        return today.year - obj.date_of_birth.year - ((today.month, today.day) < (obj.date_of_birth.month, obj.date_of_birth.day))


class AppointmentListSerializer(serializers.ModelSerializer):
    """Simplified serializer for appointment lists"""

    patient_name = serializers.CharField(source="patient.user.get_full_name", read_only=True)
    doctor_name = serializers.CharField(source="doctor.user.get_full_name", read_only=True)

    class Meta:
        model = Appointment
        fields = ["id", "patient_name", "doctor_name", "appointment_date", "status", "reason"]
