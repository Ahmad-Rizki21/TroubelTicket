import api from './api';

export const authAPI = {
  login: (username: string, password: string) => {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);
    
    // Use the base URL directly since /token is handled by the proxy
    return api.post('/token', formData.toString(), {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      }
    });
  },
  
  refreshToken: () => {
    return api.post('/refresh');
  },
  
  logout: () => {
    // In a real implementation, you might want to call a backend logout endpoint
    // For now, we just remove the token from local storage
    localStorage.removeItem('token');
  }
};