"""
Sample data creation script for Kellcare API
Run this with: python manage.py shell < create_sample_data.py
"""

from django.contrib.auth.models import User
from kellcare.models import Department, Doctor, Patient, Appointment, ContactMessage
from datetime import datetime, timedelta, date

# Create superuser if it doesn't exist
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@kellcare.com", "admin123")
    print("Created superuser: admin/admin123")

# Create departments
departments_data = [
    {
        "name": "Cardiology",
        "description": "Heart and cardiovascular system care",
        "head_of_department": "Dr. Sarah Johnson",
        "phone": "555-0101",
        "email": "cardiology@kellcare.com",
    },
    {
        "name": "Neurology",
        "description": "Brain and nervous system care",
        "head_of_department": "Dr. Michael Chen",
        "phone": "555-0102",
        "email": "neurology@kellcare.com",
    },
    {
        "name": "Pediatrics",
        "description": "Children and adolescent healthcare",
        "head_of_department": "Dr. Emily Davis",
        "phone": "555-0103",
        "email": "pediatrics@kellcare.com",
    },
    {
        "name": "Orthopedics",
        "description": "Bone, joint, and muscle care",
        "head_of_department": "Dr. Robert Wilson",
        "phone": "555-0104",
        "email": "orthopedics@kellcare.com",
    },
    {
        "name": "General Medicine",
        "description": "Primary healthcare and general medical care",
        "head_of_department": "Dr. Lisa Anderson",
        "phone": "555-0105",
        "email": "general@kellcare.com",
    },
]

departments = []
for dept_data in departments_data:
    dept, created = Department.objects.get_or_create(name=dept_data["name"], defaults=dept_data)
    departments.append(dept)
    if created:
        print(f"Created department: {dept.name}")

# Create doctors
doctors_data = [
    {
        "user_data": {"username": "dr_johnson", "email": "sarah.johnson@kellcare.com", "first_name": "Sarah", "last_name": "Johnson"},
        "license_number": "MD001234",
        "specialization": "cardiology",
        "department": departments[0],  # Cardiology
        "phone": "555-1001",
        "address": "123 Medical Plaza, Suite 100",
        "experience_years": 15,
        "consultation_fee": 200.00,
        "bio": "Experienced cardiologist specializing in heart disease prevention and treatment.",
    },
    {
        "user_data": {"username": "dr_chen", "email": "michael.chen@kellcare.com", "first_name": "Michael", "last_name": "Chen"},
        "license_number": "MD001235",
        "specialization": "neurology",
        "department": departments[1],  # Neurology
        "phone": "555-1002",
        "address": "123 Medical Plaza, Suite 200",
        "experience_years": 12,
        "consultation_fee": 250.00,
        "bio": "Neurologist with expertise in brain disorders and neurological conditions.",
    },
    {
        "user_data": {"username": "dr_davis", "email": "emily.davis@kellcare.com", "first_name": "Emily", "last_name": "Davis"},
        "license_number": "MD001236",
        "specialization": "pediatrics",
        "department": departments[2],  # Pediatrics
        "phone": "555-1003",
        "address": "123 Medical Plaza, Suite 300",
        "experience_years": 8,
        "consultation_fee": 150.00,
        "bio": "Pediatrician dedicated to providing comprehensive healthcare for children.",
    },
    {
        "user_data": {"username": "dr_wilson", "email": "robert.wilson@kellcare.com", "first_name": "Robert", "last_name": "Wilson"},
        "license_number": "MD001237",
        "specialization": "orthopedics",
        "department": departments[3],  # Orthopedics
        "phone": "555-1004",
        "address": "123 Medical Plaza, Suite 400",
        "experience_years": 20,
        "consultation_fee": 300.00,
        "bio": "Orthopedic surgeon specializing in joint replacement and sports injuries.",
    },
    {
        "user_data": {"username": "dr_anderson", "email": "lisa.anderson@kellcare.com", "first_name": "Lisa", "last_name": "Anderson"},
        "license_number": "MD001238",
        "specialization": "general",
        "department": departments[4],  # General Medicine
        "phone": "555-1005",
        "address": "123 Medical Plaza, Suite 500",
        "experience_years": 10,
        "consultation_fee": 120.00,
        "bio": "General practitioner providing primary healthcare and preventive medicine.",
    },
]

doctors = []
for doctor_data in doctors_data:
    user_data = doctor_data.pop("user_data")

    # Create or get user
    user, user_created = User.objects.get_or_create(username=user_data["username"], defaults=user_data)

    # Create or get doctor
    doctor, created = Doctor.objects.get_or_create(user=user, defaults=doctor_data)
    doctors.append(doctor)
    if created:
        print(f"Created doctor: Dr. {user.get_full_name()}")

# Create patients
patients_data = [
    {
        "user_data": {"username": "john_doe", "email": "john.doe@email.com", "first_name": "John", "last_name": "Doe"},
        "patient_id": "PAT001",
        "date_of_birth": date(1985, 3, 15),
        "gender": "M",
        "blood_group": "O+",
        "phone": "555-2001",
        "emergency_contact": "Jane Doe",
        "emergency_phone": "555-2002",
        "address": "456 Oak Street, Apt 2B",
        "medical_history": "No significant medical history",
        "allergies": "None known",
        "insurance_provider": "HealthFirst Insurance",
        "insurance_number": "HF123456789",
    },
    {
        "user_data": {"username": "jane_smith", "email": "jane.smith@email.com", "first_name": "Jane", "last_name": "Smith"},
        "patient_id": "PAT002",
        "date_of_birth": date(1992, 7, 22),
        "gender": "F",
        "blood_group": "A-",
        "phone": "555-2003",
        "emergency_contact": "Mike Smith",
        "emergency_phone": "555-2004",
        "address": "789 Pine Avenue, Unit 5",
        "medical_history": "Asthma diagnosed in childhood",
        "allergies": "Penicillin",
        "current_medications": "Albuterol inhaler as needed",
        "insurance_provider": "CareFirst Insurance",
        "insurance_number": "CF987654321",
    },
    {
        "user_data": {"username": "bob_johnson", "email": "bob.johnson@email.com", "first_name": "Bob", "last_name": "Johnson"},
        "patient_id": "PAT003",
        "date_of_birth": date(1978, 11, 5),
        "gender": "M",
        "blood_group": "B+",
        "phone": "555-2005",
        "emergency_contact": "Alice Johnson",
        "emergency_phone": "555-2006",
        "address": "321 Elm Drive, House 12",
        "medical_history": "High blood pressure, diabetes type 2",
        "allergies": "Shellfish",
        "current_medications": "Metformin, Lisinopril",
        "insurance_provider": "Medicare",
        "insurance_number": "MC555666777",
    },
]

patients = []
for patient_data in patients_data:
    user_data = patient_data.pop("user_data")

    # Create or get user
    user, user_created = User.objects.get_or_create(username=user_data["username"], defaults=user_data)

    # Create or get patient
    patient, created = Patient.objects.get_or_create(user=user, defaults=patient_data)
    patients.append(patient)
    if created:
        print(f"Created patient: {user.get_full_name()} ({patient.patient_id})")

# Create appointments
base_date = datetime.now()
appointments_data = [
    {
        "patient": patients[0],
        "doctor": doctors[0],  # Cardiology
        "appointment_date": base_date + timedelta(days=1, hours=9),
        "reason": "Chest pain evaluation",
        "status": "scheduled",
    },
    {
        "patient": patients[1],
        "doctor": doctors[2],  # Pediatrics
        "appointment_date": base_date + timedelta(days=2, hours=14),
        "reason": "Annual physical examination",
        "status": "confirmed",
    },
    {
        "patient": patients[2],
        "doctor": doctors[4],  # General Medicine
        "appointment_date": base_date + timedelta(days=3, hours=10),
        "reason": "Diabetes follow-up",
        "status": "scheduled",
    },
    {
        "patient": patients[0],
        "doctor": doctors[1],  # Neurology
        "appointment_date": base_date + timedelta(days=5, hours=11),
        "reason": "Headache consultation",
        "status": "scheduled",
    },
    {
        "patient": patients[1],
        "doctor": doctors[3],  # Orthopedics
        "appointment_date": base_date - timedelta(days=7, hours=-8),
        "reason": "Knee pain examination",
        "status": "completed",
        "notes": "Minor strain, recommended rest and physiotherapy",
        "prescription": "Ibuprofen 400mg twice daily for 7 days",
    },
]

for apt_data in appointments_data:
    appointment, created = Appointment.objects.get_or_create(
        patient=apt_data["patient"], doctor=apt_data["doctor"], appointment_date=apt_data["appointment_date"], defaults=apt_data
    )
    if created:
        print(f"Created appointment: {appointment}")

# Create contact messages
contact_messages_data = [
    {
        "name": "Alice Williams",
        "email": "alice.williams@email.com",
        "phone": "555-3001",
        "subject": "Insurance Question",
        "message": "I would like to know if my insurance is accepted at your facility.",
        "is_read": False,
    },
    {
        "name": "Tom Brown",
        "email": "tom.brown@email.com",
        "phone": "555-3002",
        "subject": "Appointment Scheduling",
        "message": "I need to schedule an urgent consultation. Please contact me as soon as possible.",
        "is_read": True,
    },
    {
        "name": "Mary Davis",
        "email": "mary.davis@email.com",
        "subject": "Feedback",
        "message": "Excellent service! The staff was very professional and caring.",
        "is_read": False,
    },
]

for msg_data in contact_messages_data:
    message, created = ContactMessage.objects.get_or_create(email=msg_data["email"], subject=msg_data["subject"], defaults=msg_data)
    if created:
        print(f"Created contact message: {message}")

print("\nSample data creation completed!")
print("\nAPI Endpoints available:")
print("- http://127.0.0.1:8000/api/ (API Root)")
print("- http://127.0.0.1:8000/api/docs/ (Swagger UI)")
print("- http://127.0.0.1:8000/api/redoc/ (ReDoc)")
print("- http://127.0.0.1:8000/api/departments/")
print("- http://127.0.0.1:8000/api/doctors/")
print("- http://127.0.0.1:8000/api/patients/")
print("- http://127.0.0.1:8000/api/appointments/")
print("- http://127.0.0.1:8000/api/contact-messages/")
print("\nAdmin access: http://127.0.0.1:8000/admin/ (admin/admin123)")
