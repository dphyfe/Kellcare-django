# 🗺️ Geocoding Feature Guide

## ✅ **Geocoding Library Added Successfully!**

Your Kellcare API now includes comprehensive geocoding functionality to convert addresses into coordinates (latitude/longitude) using the **Geopy** library.

## 🚀 **What's New:**

### **1. Database Updates**
- Added `latitude` and `longitude` fields to `Doctor` and `Patient` models
- Supports decimal coordinates with 6 decimal places precision
- Migration applied successfully

### **2. Geocoding Services**
- **Nominatim (OpenStreetMap)** - Free service (default)
- **Google Maps Geocoding API** - Premium service (requires API key)

### **3. New API Endpoints**
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/geocode/info/` | GET | Get geocoding service information |
| `/api/geocode/address/` | POST | Convert address to coordinates |
| `/api/geocode/reverse/` | POST | Convert coordinates to address |
| `/api/geocode/doctor/update/` | POST | Update doctor's coordinates |
| `/api/geocode/patient/update/` | POST | Update patient's coordinates |
| `/api/geocode/bulk-update/` | POST | Update all coordinates in bulk |

## 🧪 **Testing Examples**

### **1. Get Geocoding Info (No Auth Required)**
```bash
curl http://127.0.0.1:8000/api/geocode/info/
```

### **2. Convert Address to Coordinates**
```bash
curl -X POST http://127.0.0.1:8000/api/geocode/address/ \
     -H "Authorization: Token 326da3a3d5ba71afe00ec2cebe1682a32944c04f" \
     -H "Content-Type: application/json" \
     -d '{
       "address": "1600 Amphitheatre Parkway, Mountain View, CA",
       "service": "nominatim"
     }'
```

**Response:**
```json
{
  "address": "1600 Amphitheatre Parkway, Mountain View, CA",
  "latitude": 37.4224764,
  "longitude": -122.0842499,
  "formatted_address": "Google Building 40, 1600, Amphitheatre Parkway, Mountain View, Santa Clara County, California, 94043, United States",
  "service_used": "nominatim",
  "success": true
}
```

### **3. Convert Coordinates to Address**
```bash
curl -X POST http://127.0.0.1:8000/api/geocode/reverse/ \
     -H "Authorization: Token 326da3a3d5ba71afe00ec2cebe1682a32944c04f" \
     -H "Content-Type: application/json" \
     -d '{
       "latitude": 37.4224764,
       "longitude": -122.0842499
     }'
```

### **4. Update Doctor Coordinates**
```bash
curl -X POST http://127.0.0.1:8000/api/geocode/doctor/update/ \
     -H "Authorization: Token 326da3a3d5ba71afe00ec2cebe1682a32944c04f" \
     -H "Content-Type: application/json" \
     -d '{
       "doctor_id": 1,
       "service": "nominatim"
     }'
```

### **5. Bulk Update All Coordinates**
```bash
curl -X POST http://127.0.0.1:8000/api/geocode/bulk-update/ \
     -H "Authorization: Token 326da3a3d5ba71afe00ec2cebe1682a32944c04f" \
     -H "Content-Type: application/json" \
     -d '{
       "service": "nominatim",
       "update_doctors": true,
       "update_patients": true
     }'
```

## 💻 **Frontend Integration**

### **JavaScript Example**
```javascript
// Convert address to coordinates
const geocodeAddress = async (address) => {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/geocode/address/', {
      method: 'POST',
      headers: {
        'Authorization': 'Token 326da3a3d5ba71afe00ec2cebe1682a32944c04f',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        address: address,
        service: 'nominatim'
      }),
    });
    
    const data = await response.json();
    
    if (data.success) {
      console.log('Coordinates:', data.latitude, data.longitude);
      return {
        lat: data.latitude,
        lng: data.longitude,
        formatted: data.formatted_address
      };
    } else {
      console.error('Geocoding failed:', data.error);
      return null;
    }
  } catch (error) {
    console.error('Request failed:', error);
    return null;
  }
};

// Usage
geocodeAddress("123 Main Street, New York, NY")
  .then(coords => {
    if (coords) {
      console.log('Location found:', coords);
      // Use coordinates for maps, distance calculations, etc.
    }
  });
```

### **React Hook Example**
```javascript
import { useState, useEffect } from 'react';

const useGeocoding = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const geocodeAddress = async (address) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('http://127.0.0.1:8000/api/geocode/address/', {
        method: 'POST',
        headers: {
          'Authorization': 'Token 326da3a3d5ba71afe00ec2cebe1682a32944c04f',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ address, service: 'nominatim' }),
      });
      
      const data = await response.json();
      setLoading(false);
      
      if (data.success) {
        return data;
      } else {
        setError(data.error);
        return null;
      }
    } catch (err) {
      setLoading(false);
      setError(err.message);
      return null;
    }
  };

  return { geocodeAddress, loading, error };
};

// Usage in component
const DoctorLocationForm = () => {
  const { geocodeAddress, loading, error } = useGeocoding();
  const [address, setAddress] = useState('');
  const [coordinates, setCoordinates] = useState(null);

  const handleGeocode = async () => {
    const result = await geocodeAddress(address);
    if (result) {
      setCoordinates({
        lat: result.latitude,
        lng: result.longitude
      });
    }
  };

  return (
    <div>
      <input 
        value={address}
        onChange={(e) => setAddress(e.target.value)}
        placeholder="Enter address..."
      />
      <button onClick={handleGeocode} disabled={loading}>
        {loading ? 'Geocoding...' : 'Get Coordinates'}
      </button>
      {error && <p style={{color: 'red'}}>Error: {error}</p>}
      {coordinates && (
        <p>Coordinates: {coordinates.lat}, {coordinates.lng}</p>
      )}
    </div>
  );
};
```

## 🔧 **Python Usage in Your Views**

```python
# In your Django views or management commands
from kellcare.utils.geocoding import address_to_coordinates, coordinates_to_address

# Convert address to coordinates
def update_doctor_location(doctor_id):
    doctor = Doctor.objects.get(id=doctor_id)
    result = address_to_coordinates(doctor.address)
    
    if result['success']:
        doctor.latitude = result['latitude']
        doctor.longitude = result['longitude']
        doctor.save()
        print(f"Updated {doctor.user.get_full_name()}'s coordinates")
    else:
        print(f"Geocoding failed: {result['error']}")

# Find nearby doctors (example)
def find_nearby_doctors(patient_lat, patient_lng, radius_km=10):
    from django.db.models import Q
    from math import radians, cos, sin, asin, sqrt
    
    # Simple distance calculation (for more precision, use PostGIS)
    doctors = Doctor.objects.filter(
        latitude__isnull=False,
        longitude__isnull=False,
        is_available=True
    )
    
    nearby_doctors = []
    for doctor in doctors:
        distance = calculate_distance(
            patient_lat, patient_lng,
            float(doctor.latitude), float(doctor.longitude)
        )
        if distance <= radius_km:
            nearby_doctors.append((doctor, distance))
    
    # Sort by distance
    nearby_doctors.sort(key=lambda x: x[1])
    return nearby_doctors

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points using Haversine formula"""
    # Convert to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers
    return c * r
```

## ⚙️ **Google Maps API Setup (Optional)**

To use Google Maps geocoding (more accurate but requires API key):

### **1. Get Google Maps API Key**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project or select existing
3. Enable "Geocoding API"
4. Create credentials (API Key)
5. Restrict the key to your domain

### **2. Add to Django Settings**
```python
# In settings.py
GOOGLE_MAPS_API_KEY = 'your-google-maps-api-key-here'
```

### **3. Use Google Service**
```bash
curl -X POST http://127.0.0.1:8000/api/geocode/address/ \
     -H "Authorization: Token 326da3a3d5ba71afe00ec2cebe1682a32944c04f" \
     -H "Content-Type: application/json" \
     -d '{
       "address": "123 Main St, New York, NY",
       "service": "google"
     }'
```

## 📊 **Use Cases**

### **Healthcare Applications**
1. **Find Nearest Doctors** - Help patients find doctors nearby
2. **Emergency Services** - Route ambulances to closest hospitals
3. **Service Area Mapping** - Show which areas doctors serve
4. **Appointment Logistics** - Calculate travel time for appointments
5. **Resource Planning** - Optimize placement of medical facilities

### **Example: Doctor Finder**
```javascript
// Find doctors within 5km of patient location
const findNearbyDoctors = async (patientAddress, specialization) => {
  // First, geocode patient address
  const patientCoords = await geocodeAddress(patientAddress);
  if (!patientCoords) return [];
  
  // Get all doctors with coordinates
  const response = await fetch('http://127.0.0.1:8000/api/doctors/', {
    headers: {
      'Authorization': 'Token 326da3a3d5ba71afe00ec2cebe1682a32944c04f'
    }
  });
  const doctors = await response.json();
  
  // Calculate distances and filter
  const nearbyDoctors = doctors.results
    .filter(doctor => doctor.latitude && doctor.longitude)
    .filter(doctor => !specialization || doctor.specialization === specialization)
    .map(doctor => ({
      ...doctor,
      distance: calculateDistance(
        patientCoords.lat, patientCoords.lng,
        doctor.latitude, doctor.longitude
      )
    }))
    .filter(doctor => doctor.distance <= 5)
    .sort((a, b) => a.distance - b.distance);
  
  return nearbyDoctors;
};
```

## 🎉 **Success!**

Your Kellcare API now includes:
- ✅ **Address to coordinates conversion**
- ✅ **Reverse geocoding (coordinates to address)**
- ✅ **Bulk coordinate updates**
- ✅ **Integration with doctor and patient models**
- ✅ **Multiple geocoding service support**
- ✅ **Comprehensive API endpoints**

**Your geocoding system is ready to use!** 🗺️