# 🔧 CORS Fix Guide for Kellcare API

## ✅ **CORS Issue Resolved!**

The CORS error has been fixed with comprehensive CORS configuration. Your API now supports cross-origin requests from web browsers and frontend applications.

## 🧪 **Test CORS Configuration**

### Quick CORS Test
```bash
# Test from command line
curl -H "Origin: http://localhost:3000" \
     -H "Access-Control-Request-Method: GET" \
     -H "Access-Control-Request-Headers: authorization" \
     -X OPTIONS \
     http://127.0.0.1:8000/api/cors-test/
```

### Browser Test
Open your browser console and run:
```javascript
fetch('http://127.0.0.1:8000/api/cors-test/')
  .then(response => response.json())
  .then(data => console.log('CORS working:', data))
  .catch(error => console.error('CORS error:', error));
```

## 🌐 **Supported Origins**

Your API now accepts requests from:
- `http://localhost:3000` (React default)
- `http://127.0.0.1:3000`
- `http://localhost:8080` (Vue default)
- `http://127.0.0.1:8080`
- `http://localhost:5173` (Vite default)
- `http://127.0.0.1:5173`
- `http://localhost:4200` (Angular default)
- `http://127.0.0.1:4200`
- **All origins in development** (`CORS_ALLOW_ALL_ORIGINS = True`)

## 🚀 **Frontend Integration Examples**

### React/JavaScript
```javascript
// Using fetch with token
const apiCall = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/doctors/', {
      method: 'GET',
      headers: {
        'Authorization': 'Token bbbd1a564f28b11b482b3d6bb8176e02a61aa3ff',
        'Content-Type': 'application/json',
      },
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    console.log('Doctors:', data);
  } catch (error) {
    console.error('API Error:', error);
  }
};

apiCall();
```

### Axios Configuration
```javascript
import axios from 'axios';

// Create axios instance with default config
const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/',
  headers: {
    'Authorization': 'Token bbbd1a564f28b11b482b3d6bb8176e02a61aa3ff',
    'Content-Type': 'application/json',
  },
});

// Use the API
const getDoctors = async () => {
  try {
    const response = await api.get('doctors/');
    console.log('Doctors:', response.data);
  } catch (error) {
    console.error('API Error:', error.response?.data || error.message);
  }
};

getDoctors();
```

### Vue.js Example
```javascript
// In your Vue component
export default {
  data() {
    return {
      doctors: [],
      loading: false,
      error: null
    }
  },
  async created() {
    await this.fetchDoctors();
  },
  methods: {
    async fetchDoctors() {
      this.loading = true;
      try {
        const response = await fetch('http://127.0.0.1:8000/api/doctors/', {
          headers: {
            'Authorization': 'Token bbbd1a564f28b11b482b3d6bb8176e02a61aa3ff'
          }
        });
        
        if (!response.ok) throw new Error('Failed to fetch');
        
        const data = await response.json();
        this.doctors = data.results || data;
      } catch (error) {
        this.error = error.message;
      } finally {
        this.loading = false;
      }
    }
  }
}
```

## 🛠️ **CORS Configuration Details**

The following CORS settings have been applied:

```python
# CORS settings in settings.py
CORS_ALLOW_ALL_ORIGINS = True  # For development only
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',  # Important for token auth
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
```

## 🔍 **Troubleshooting**

### Still Getting CORS Errors?

1. **Check your request URL**
   - Use `http://127.0.0.1:8000` not `http://localhost:8000`
   - Or use `http://localhost:8000` consistently

2. **Verify Authorization Header**
   ```javascript
   headers: {
     'Authorization': 'Token bbbd1a564f28b11b482b3d6bb8176e02a61aa3ff'
   }
   ```

3. **Check Network Tab**
   - Look for preflight OPTIONS requests
   - Verify response headers include `Access-Control-Allow-Origin`

4. **Test CORS Endpoint**
   ```javascript
   fetch('http://127.0.0.1:8000/api/cors-test/')
     .then(r => r.json())
     .then(data => console.log(data));
   ```

### Browser Console Debugging
```javascript
// Test basic connectivity
fetch('http://127.0.0.1:8000/api/cors-test/')
  .then(response => {
    console.log('Status:', response.status);
    console.log('Headers:', [...response.headers.entries()]);
    return response.json();
  })
  .then(data => console.log('Data:', data))
  .catch(error => console.error('Error:', error));
```

## 🔐 **Authentication with CORS**

### Getting Token via CORS
```javascript
// Get authentication token
const getToken = async (username, password) => {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/auth/token/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password }),
    });
    
    const data = await response.json();
    
    if (response.ok) {
      localStorage.setItem('apiToken', data.token);
      return data.token;
    } else {
      throw new Error(data.error || 'Authentication failed');
    }
  } catch (error) {
    console.error('Auth error:', error);
    throw error;
  }
};

// Usage
getToken('admin', 'admin123')
  .then(token => console.log('Token:', token))
  .catch(error => console.error('Failed to get token:', error));
```

### Using Stored Token
```javascript
// Get token from storage and use it
const apiRequest = async (endpoint, options = {}) => {
  const token = localStorage.getItem('apiToken');
  
  const defaultOptions = {
    headers: {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Token ${token}` }),
    },
  };
  
  const mergedOptions = {
    ...defaultOptions,
    ...options,
    headers: {
      ...defaultOptions.headers,
      ...options.headers,
    },
  };
  
  const response = await fetch(`http://127.0.0.1:8000/api/${endpoint}`, mergedOptions);
  
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
  }
  
  return response.json();
};

// Usage examples
apiRequest('doctors/').then(data => console.log('Doctors:', data));
apiRequest('appointments/today/').then(data => console.log('Today:', data));
```

## 🎉 **Success!**

Your API now supports:
- ✅ Cross-origin requests
- ✅ Token authentication via CORS
- ✅ All HTTP methods (GET, POST, PUT, DELETE, etc.)
- ✅ Custom headers including Authorization
- ✅ Preflight OPTIONS requests

**Your frontend can now communicate with the API without CORS errors!**