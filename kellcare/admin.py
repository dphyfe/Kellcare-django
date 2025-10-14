from django.contrib import admin
from .models import Department, Doctor, Patient, Appointment, ContactMessage


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["name", "head_of_department", "phone", "email"]
    list_filter = ["created_at"]
    search_fields = ["name", "head_of_department"]


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ["user", "license_number", "specialization", "department", "is_available"]
    list_filter = ["specialization", "department", "is_available", "created_at"]
    search_fields = ["user__first_name", "user__last_name", "license_number"]
    list_editable = ["is_available"]


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ["user", "patient_id", "gender", "blood_group", "phone"]
    list_filter = ["gender", "blood_group", "created_at"]
    search_fields = ["user__first_name", "user__last_name", "patient_id", "phone"]


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ["patient", "doctor", "appointment_date", "status", "created_at"]
    list_filter = ["status", "appointment_date", "doctor__specialization"]
    search_fields = ["patient__user__first_name", "patient__user__last_name", "doctor__user__first_name", "doctor__user__last_name"]
    list_editable = ["status"]
    date_hierarchy = "appointment_date"


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "subject", "is_read", "created_at"]
    list_filter = ["is_read", "created_at"]
    search_fields = ["name", "email", "subject"]
    list_editable = ["is_read"]
    readonly_fields = ["created_at"]
