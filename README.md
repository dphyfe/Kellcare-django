# Kellcare Django Application

A comprehensive healthcare management system built with Django.

## Features

- **Patient Management**: Complete patient registration and profile management
- **Doctor Management**: Doctor profiles with specializations and availability
- **Appointment Scheduling**: Online appointment booking system
- **Department Management**: Hospital department organization
- **Contact System**: Contact form for inquiries
- **Admin Interface**: Django admin for backend management

## Project Structure

```
kellcare-django/
├── kellcare_project/          # Main Django project
│   ├── settings.py           # Project settings
│   ├── urls.py              # Main URL configuration
│   └── wsgi.py              # WSGI configuration
├── kellcare/                 # Main application
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   ├── urls.py              # App URL patterns
│   ├── forms.py             # Django forms
│   ├── admin.py             # Admin configuration
│   ├── templates/           # HTML templates
│   │   └── kellcare/
│   │       ├── base.html
│   │       ├── home.html
│   │       ├── about.html
│   │       ├── services.html
│   │       └── contact.html
│   └── static/              # Static files
│       └── kellcare/
│           ├── css/
│           ├── js/
│           └── images/
├── media/                   # User uploaded files
├── static/                  # Collected static files
└── manage.py               # Django management script
```

## Models

### Patient
- User profile extension with medical information
- Patient ID, demographics, medical history
- Emergency contact information
- Insurance details

### Doctor
- User profile extension for medical staff
- License number, specialization, department
- Consultation fees, availability status
- Professional bio and photo

### Department
- Hospital departments (Cardiology, Surgery, etc.)
- Department head and contact information

### Appointment
- Patient-doctor appointments
- Scheduling, status tracking
- Notes and prescriptions
- Follow-up scheduling

### ContactMessage
- Contact form submissions
- Admin tracking and response management

## Installation & Setup

1. **Create Virtual Environment**:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   ```

2. **Install Dependencies**:
   ```bash
   pip install django>=4.2 python-decouple pillow
   ```

3. **Database Setup**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create Superuser**:
   ```bash
   python manage.py createsuperuser
   ```

5. **Run Development Server**:
   ```bash
   python manage.py runserver
   ```

## Usage

### Admin Interface
- Access: `http://localhost:8000/admin/`
- Manage patients, doctors, appointments, and departments
- View and respond to contact messages

### Public Pages
- Home: `http://localhost:8000/`
- About: `http://localhost:8000/about/`
- Services: `http://localhost:8000/services/`
- Contact: `http://localhost:8000/contact/`

## Next Steps

1. **User Authentication**: Implement patient/doctor login system
2. **Appointment Booking**: Online appointment scheduling for patients
3. **Medical Records**: Electronic health records management
4. **Billing System**: Patient billing and payment processing
5. **Reporting**: Generate medical reports and analytics
6. **Notifications**: Email/SMS notifications for appointments
7. **API Development**: REST API for mobile applications

## Technologies Used

- **Backend**: Django 4.2+
- **Database**: SQLite (development), PostgreSQL (production recommended)
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Static Files**: Django static files handling
- **File Uploads**: Django file handling for images

## License

This project is developed for educational and demonstration purposes.