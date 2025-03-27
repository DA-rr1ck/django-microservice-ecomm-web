import axios from 'axios';

// Base API gateway URL
const API_URL = process.env.REACT_APP_API_GATEWAY || 'http://localhost:8000/api';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  },
  timeout: 10000 // 10 seconds timeout
});

// Add auth token to requests
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

// Handle common response errors
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response) {
      // Global error handling
      switch (error.response.status) {
        case 401:
          // Unauthorized - clear auth and redirect to login
          localStorage.removeItem('token');
          window.location = '/login';
          break;
        case 503:
          // Service unavailable - show maintenance message
          console.error('Service temporarily unavailable');
          break;
        default:
          // Other errors
          break;
      }
    }
    return Promise.reject(error);
  }
);

// Create service-specific APIs
export const customerService = {
  register: (userData) => api.post('/customers/register/', userData),
  login: (credentials) => api.post('/customers/login/', credentials),
  getProfile: () => api.get('/customers/profile/'),
  updateProfile: (data) => api.put('/customers/profile/', data),
  // Add more customer-related endpoints as needed
};

// Export the base api for other services to use later
export default api;