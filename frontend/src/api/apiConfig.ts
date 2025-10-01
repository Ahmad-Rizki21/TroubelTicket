import axios from 'axios';

// Create an axios instance with base configuration
// Use relative path in development (will be proxied) or configured base URL
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || (import.meta.env.DEV ? '/api' : 'http://127.0.0.1:8000'),
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add token to requests (when available)
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for handling responses globally (optional)
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Handle global error responses here if needed
    // e.g., redirect to login if token is expired
    if (error.response?.status === 401) {
      // Remove token and redirect to login
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;