import axios from 'axios';
import { useAuthStore } from '../stores/auth';

// Create an axios instance with base configuration
// Use relative path in development (will be proxied) or configured base URL
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || (import.meta.env.DEV ? '/api' : 'http://127.0.0.1:8000'),
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

// Flag to prevent multiple refresh attempts
let isRefreshing = false;
let failedQueue: Array<{ resolve: (value: any) => void; reject: (reason?: any) => void }> = [];

const processQueue = (error: any, token: string | null = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });

  failedQueue = [];
};

// Response interceptor for handling responses globally
api.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;

    // If error is 401 and we haven't tried to refresh token yet
    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        // If already refreshing, add to queue and wait
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        }).then(token => {
          originalRequest.headers.Authorization = `Bearer ${token}`;
          return api(originalRequest);
        }).catch(err => {
          return Promise.reject(err);
        });
      }

      originalRequest._retry = true;
      isRefreshing = true;

      try {
        // Get auth store and try to refresh token
        const authStore = useAuthStore();
        const newToken = await authStore.refreshAccessToken();

        // Update Authorization header
        api.defaults.headers.common['Authorization'] = `Bearer ${newToken}`;
        originalRequest.headers.Authorization = `Bearer ${newToken}`;

        // Process any queued requests
        processQueue(null, newToken);

        // Retry the original request
        return api(originalRequest);
      } catch (refreshError) {
        // If refresh fails, process queue with error and redirect to login
        processQueue(refreshError, null);

        // Check if we're not already on login page to prevent redirect loops
        if (window.location.pathname !== '/login') {
          window.location.href = '/login';
        }
        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }

    // For other errors or if refresh fails, just reject
    return Promise.reject(error);
  }
);

export default api;