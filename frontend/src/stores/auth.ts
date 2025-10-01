interface User {
  id: number;
  username: string;
  role?: {
    name: string;
  };
}

import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    isAuthenticated: !!localStorage.getItem('token'),
    user: null as User | null,
  }),
  actions: {
    setToken(token: string) {
      this.token = token;
      this.isAuthenticated = true;
      localStorage.setItem('token', token);
    },
    setUser(user: User) {
      this.user = user;
    },
    clearToken() {
      this.token = null;
      this.isAuthenticated = false;
      this.user = null;
      localStorage.removeItem('token');
    },
  },
});
