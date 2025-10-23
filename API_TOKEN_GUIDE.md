# 🔑 Kellcare API Authentication Guide

## Your API Token
```
Token: 326da3a3d5ba71afe00ec2cebe1682a32944c04f
User: admin
```

## 🚀 Quick Start

### 1. Test API Access (No Auth Required - Read Only)
```bash
curl http://127.0.0.1:8000/api/departments/
```

### 2. Test API Access (With Token - Full Access)
```bash
curl -H "Authorization: Token 326da3a3d5ba71afe00ec2cebe1682a32944c04f" \
     http://127.0.0.1:8000/api/appointments/
```

## 🔐 Authentication Methods

### Method 1: Using Your Existing Token
```bash
# Add this header to all requests:
Authorization: Token 326da3a3d5ba71afe00ec2cebe1682a32944c04f
```

### Method 2: Get New Token via API
```bash
# POST to get token
curl -X POST http://127.0.0.1:8000/api/auth/token/ \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "admin123"}'
```

### Method 3: Create Token via Command Line
```bash
# Create/get existing token
python manage.py create_api_token --username your_username

# Force refresh token (creates new one)
python manage.py refresh_api_token --username your_username
```

## 📋 API Endpoints

### Authentication Endpoints
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/token/` | Get authentication token | No |
| POST | `/api/auth/refresh-token/` | Refresh your token | Yes |
| GET | `/api/auth/user/` | Get user info | Yes |

### Data Endpoints
| Resource | Endpoint | Methods | Auth for Read | Auth for Write |
|----------|----------|---------|---------------|----------------|
| Departments | `/api/departments/` | GET, POST, PUT, DELETE | No | Yes |
| Doctors | `/api/doctors/` | GET, POST, PUT, DELETE | No | Yes |
| Patients | `/api/patients/` | GET, POST, PUT, DELETE | Yes | Yes |
| Appointments | `/api/appointments/` | GET, POST, PUT, DELETE | No | Yes |
| Contact Messages | `/api/contact-messages/` | GET, POST, PUT, DELETE | POST: No, Others: Yes | Yes |

## 🧪 Testing Examples

### 1. Get Authentication Token
```bash
curl -X POST http://127.0.0.1:8000/api/auth/token/ \
     -H "Content-Type: application/json" \
     -d '{
       "username": "admin",
       "password": "admin123"
     }'
```

**Response:**
```json
{
  "token": "326da3a3d5ba71afe00ec2cebe1682a32944c04f",
  "user_id": 1,
  "username": "admin",
  "message": "Token retrieved"
}
```

### 2. Get All Doctors (No Auth Required)
```bash
curl http://127.0.0.1:8000/api/doctors/
```

### 3. Get Specific Doctor (With Auth)
```bash
curl -H "Authorization: Token 326da3a3d5ba71afe00ec2cebe1682a32944c04f" \
     http://127.0.0.1:8000/api/doctors/1/
```

### 4. Create New Appointment (Auth Required)
```bash
curl -X POST http://127.0.0.1:8000/api/appointments/ \
     -H "Authorization: Token 326da3a3d5ba71afe00ec2cebe1682a32944c04f" \
     -H "Content-Type: application/json" \
     -d '{
       "patient": 1,
       "doctor": 1,
       "appointment_date": "2025-10-25T10:00:00Z",
       "reason": "Regular checkup"
     }'
```

### 5. Get Today's Appointments
```bash
curl -H "Authorization: Token 326da3a3d5ba71afe00ec2cebe1682a32944c04f" \
     http://127.0.0.1:8000/api/appointments/today/
```

### 6. Search Doctors
```bash
curl "http://127.0.0.1:8000/api/doctors/?search=cardiology"
```

### 7. Filter Available Doctors
```bash
curl "http://127.0.0.1:8000/api/doctors/available/"
```

## 🌐 Frontend Integration

### JavaScript/Fetch Example
```javascript
// Get token
const response = await fetch('http://127.0.0.1:8000/api/auth/token/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    username: 'admin',
    password: 'admin123'
  })
});

const data = await response.json();
const token = data.token;

// Use token for authenticated requests
const doctorsResponse = await fetch('http://127.0.0.1:8000/api/doctors/', {
  headers: {
    'Authorization': `Token ${token}`
  }
});

const doctors = await doctorsResponse.json();
```

### React/Axios Example
```javascript
import axios from 'axios';

// Set up axios with token
const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/',
  headers: {
    'Authorization': 'Token 326da3a3d5ba71afe00ec2cebe1682a32944c04f'
  }
});

// Use the API
const doctors = await api.get('doctors/');
const appointments = await api.get('appointments/today/');
```

## 🔧 Postman Setup

1. **Create new request**
2. **Add Authorization Header:**
   - Key: `Authorization`
   - Value: `Token 326da3a3d5ba71afe00ec2cebe1682a32944c04f`
3. **Set Content-Type for POST/PUT:**
   - Key: `Content-Type`
   - Value: `application/json`

## 🛡️ Security Notes

- **Token Security**: Keep your token secure and don't expose it in client-side code
- **HTTPS**: Use HTTPS in production
- **Token Rotation**: Refresh tokens periodically using `/api/auth/refresh-token/`
- **Permissions**: Different endpoints have different permission requirements

## 📊 Response Formats

### Success Response
```json
{
  "count": 123,
  "next": "http://127.0.0.1:8000/api/doctors/?page=2",
  "previous": null,
  "results": [...]
}
```

### Error Response
```json
{
  "detail": "Authentication credentials were not provided."
}
```

## 🔗 Interactive Documentation

- **Swagger UI**: http://127.0.0.1:8000/api/docs/
- **ReDoc**: http://127.0.0.1:8000/api/redoc/

## 🆘 Troubleshooting

### 403 Forbidden Error
- **Solution**: Add the Authorization header with your token
- **Example**: `Authorization: Token 326da3a3d5ba71afe00ec2cebe1682a32944c04f`

### 401 Unauthorized Error
- **Solution**: Check if your token is valid or refresh it
- **Command**: `python manage.py refresh_api_token --username admin`

### Token Not Working
1. Verify token format: `Token <your-token>`
2. Check if user exists and is active
3. Refresh the token using the refresh endpoint

---

**Your API is ready! 🎉**

Use the token `326da3a3d5ba71afe00ec2cebe1682a32944c04f` to access all authenticated endpoints.