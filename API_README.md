# Kellcare Django REST API

A comprehensive healthcare management system backend API built with Django REST Framework and documented with Swagger/OpenAPI.

## 🚀 Features

- **Complete Healthcare API**: Manage departments, doctors, patients, appointments, and contact messages
- **RESTful Design**: Full CRUD operations with standard HTTP methods
- **Interactive Documentation**: Swagger UI and ReDoc for API exploration
- **Advanced Filtering**: Search, filter, and sort across all endpoints
- **Pagination**: Efficient data loading with configurable page sizes
- **Permission System**: Role-based access control for different user types
- **Data Validation**: Comprehensive serialization and validation
- **Sample Data**: Pre-populated database for testing and development

## 📋 Prerequisites

- Python 3.8+
- Django 5.2+
- Virtual environment (recommended)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd kellcare-django
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   # Windows
   .\.venv\Scripts\activate
   # Linux/Mac
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create sample data (optional)**
   ```bash
   python manage.py shell < create_sample_data.py
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

## 📚 API Documentation

### Interactive Documentation
- **Swagger UI**: http://127.0.0.1:8000/api/docs/
- **ReDoc**: http://127.0.0.1:8000/api/redoc/
- **OpenAPI Schema**: http://127.0.0.1:8000/api/schema/

### Authentication
- **Admin Panel**: http://127.0.0.1:8000/admin/ (admin/admin123)
- **API Authentication**: http://127.0.0.1:8000/api-auth/

## 🔗 API Endpoints

### Base URL: `http://127.0.0.1:8000/api/`

| Resource | Endpoint | Methods | Description |
|----------|----------|---------|-------------|
| **Departments** | `/departments/` | GET, POST, PUT, PATCH, DELETE | Hospital departments |
| **Doctors** | `/doctors/` | GET, POST, PUT, PATCH, DELETE | Doctor profiles and management |
| **Patients** | `/patients/` | GET, POST, PUT, PATCH, DELETE | Patient records |
| **Appointments** | `/appointments/` | GET, POST, PUT, PATCH, DELETE | Appointment scheduling |
| **Contact Messages** | `/contact-messages/` | GET, POST, PUT, PATCH, DELETE | Contact form submissions |
| **Users** | `/users/` | GET | User management (read-only) |

## 🔍 Advanced Features

### Custom Actions

#### Doctors
- `GET /api/doctors/available/` - Get only available doctors
- `GET /api/doctors/by_specialization/?spec=cardiology` - Filter by specialization
- `GET /api/doctors/{id}/appointments/` - Get doctor's appointments

#### Patients
- `GET /api/patients/{id}/appointments/` - Get patient's appointments
- `GET /api/patients/{id}/medical_history/` - Get medical history

#### Appointments
- `GET /api/appointments/today/` - Today's appointments
- `GET /api/appointments/upcoming/` - Upcoming appointments
- `GET /api/appointments/by_status/?status=scheduled` - Filter by status
- `PATCH /api/appointments/{id}/update_status/` - Update appointment status
- `PATCH /api/appointments/{id}/add_prescription/` - Add prescription

#### Contact Messages
- `GET /api/contact-messages/unread/` - Get unread messages
- `PATCH /api/contact-messages/{id}/mark_read/` - Mark as read

### Filtering & Search

All list endpoints support:
- **Search**: `?search=keyword`
- **Filtering**: `?field=value`
- **Ordering**: `?ordering=field` or `?ordering=-field` (descending)
- **Pagination**: `?page=1&page_size=20`

#### Examples:
```bash
# Search doctors by name or specialization
GET /api/doctors/?search=cardiology

# Filter available doctors
GET /api/doctors/?is_available=true

# Get appointments for specific doctor
GET /api/appointments/?doctor=1

# Search patients by name
GET /api/patients/?search=john

# Order appointments by date (newest first)
GET /api/appointments/?ordering=-appointment_date
```

## 🏥 Data Models

### Department
- Name, description, head of department
- Contact information (phone, email)
- Creation timestamp

### Doctor
- User profile integration
- License number and specialization
- Department association
- Consultation fees and availability
- Experience and bio information

### Patient
- User profile integration
- Unique patient ID
- Medical information (blood group, allergies, medications)
- Emergency contacts and insurance details
- Medical history tracking

### Appointment
- Patient and doctor relationships
- Date/time scheduling with duration
- Status tracking (scheduled, confirmed, completed, etc.)
- Reason, notes, and prescription fields
- Follow-up date support

### Contact Message
- Public contact form submissions
- Read/unread status tracking
- Subject and message content

## 🔐 Permissions

- **Public**: Contact message creation
- **Authenticated**: Most read operations
- **Staff/Admin**: Full CRUD operations
- **Patient Data**: Restricted access for sensitive information

## 🛡️ Security Features

- CORS configuration for frontend integration
- Authentication required for sensitive endpoints
- Input validation and sanitization
- Permission-based access control

## 🧪 Sample Data

The system includes sample data for testing:
- 5 Departments (Cardiology, Neurology, Pediatrics, etc.)
- 5 Doctors with different specializations
- 3 Patients with varied medical histories
- Multiple appointments in different states
- Contact messages for testing

## 🚀 Deployment

### Production Considerations

1. **Environment Variables**
   ```python
   # Use environment variables for sensitive settings
   SECRET_KEY = os.environ.get('SECRET_KEY')
   DEBUG = False
   ALLOWED_HOSTS = ['your-domain.com']
   ```

2. **Database**
   ```python
   # Use PostgreSQL in production
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           # ... other settings
       }
   }
   ```

3. **Static Files**
   ```bash
   python manage.py collectstatic
   ```

4. **CORS Settings**
   ```python
   # Configure CORS for your frontend domain
   CORS_ALLOWED_ORIGINS = [
       "https://your-frontend-domain.com",
   ]
   ```

## 📦 Dependencies

```
django>=4.2.0,<5.0.0
python-decouple>=3.8
Pillow>=10.0.0
djangorestframework>=3.14.0
drf-spectacular>=0.27.0
django-cors-headers>=4.3.0
django-filter>=23.0.0
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 📞 Support

For issues and questions:
- Create an issue in the repository
- Contact: admin@kellcare.com

---

**Happy coding! 🎉**