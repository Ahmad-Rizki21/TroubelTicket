interface User {
  id: number;
  username: string;
  role_id: number;
  created_at: string;
  role: {
    id: number;
    name: string;
    permissions: {
      id: number;
      name: string;
    }[];
  };
}

import { defineStore } from 'pinia';
import { userAPI } from '../api/userAPI';
import { authAPI } from '../api/authAPI';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    refreshToken: localStorage.getItem('refreshToken') || null,
    isAuthenticated: !!localStorage.getItem('token'),
    user: null as User | null,
  }),
  getters: {
    userPermissions: (state) => {
      if (!state.user || !state.user.role || !state.user.role.permissions) {
        return [];
      }
      return state.user.role.permissions.map(perm => perm.name);
    },
    hasPermission: (state) => {
      return (permission: string) => {
        if (!state.user || !state.user.role || !state.user.role.permissions) {
          return false;
        }
        return state.user.role.permissions.some(perm => perm.name === permission);
      };
    }
  },
  actions: {
    async setToken(token: string, refreshToken?: string) {
      this.token = token;
      this.refreshToken = refreshToken || null;
      this.isAuthenticated = true;
      localStorage.setItem('token', token);
      if (refreshToken) {
        localStorage.setItem('refreshToken', refreshToken);
      }
      // Immediately fetch user data after setting the token
      await this.fetchUser();
    },
    setUser(user: User) {
      this.user = user;
    },
    clearToken() {
      this.token = null;
      this.refreshToken = null;
      this.isAuthenticated = false;
      this.user = null;
      localStorage.removeItem('token');
      localStorage.removeItem('refreshToken');
    },
    async fetchUser() {
      if (this.token) {
        try {
          const response = await userAPI.getMe();
          console.log("User data fetched:", response.data); // Debug log
          this.setUser(response.data);
        } catch (error) {
          console.error("Failed to fetch user:", error);
          // If fetching user fails (e.g. invalid token), clear session
          this.clearToken();
        }
      }
    },
    async refreshAccessToken() {
      if (!this.refreshToken) {
        throw new Error('No refresh token available');
      }

      try {
        const response = await authAPI.refreshToken();
        const { access_token, refresh_token } = response.data;

        this.setToken(access_token, refresh_token);
        return access_token;
      } catch (error) {
        console.error('Failed to refresh token:', error);
        this.clearToken();
        throw error;
      }
    },
  },
});
