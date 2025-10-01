<template>
  <div class="login-container">
    <!-- Maintenance Banner (adapted from your DefaultLayout.vue) -->
    <div v-if="maintenanceMode" class="maintenance-banner">
      <svg class="banner-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M12 2L2 12H5V21H19V12H22L12 2ZM12 15C10.9 15 10 14.1 10 13C10 11.9 10.9 11 12 11C13.1 11 14 11.9 14 13C14 14.1 13.1 15 12 15Z" fill="currentColor"/>
      </svg>
      <span>{{ maintenanceMessage }}</span>
    </div>

    <!-- Enhanced Fiber Optic Background Animation (from your LoginView.vue) -->
    <div class="fiber-bg">
      <div class="fiber-strand" v-for="i in 12" :key="i" :style="{
        left: `${Math.random() * 100}%`,
        animationDelay: `${Math.random() * 3}s`,
        animationDuration: `${3 + Math.random() * 2}s`
      }"></div>
      <div class="light-pulse" v-for="i in 10" :key="`pulse-${i}`" :style="{
        left: `${Math.random() * 100}%`,
        top: `${Math.random() * 100}%`,
        animationDelay: `${Math.random() * 4}s`
      }"></div>
      
      <!-- Floating Particles -->
      <div class="floating-particles">
        <div class="particle" v-for="i in 15" :key="`particle-${i}`" :style="{
          left: `${Math.random() * 100}%`,
          top: `${Math.random() * 100}%`,
          animationDelay: `${Math.random() * 10}s`,
          animationDuration: `${8 + Math.random() * 4}s`
        }"></div>
      </div>
    </div>
    
    <div class="login-form-wrapper">
      <!-- "Poni" Logo -->
      <div class="logo-notch">
        <div class="logo-wrapper-3d">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM12 6V12L16 14" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <div class="logo-glow-3d"></div>
        </div>
      </div>

      <div class="login-card">
        <!-- Brand section text -->
        <div class="brand-section">
          <h1>Trouble Ticket</h1>
          <p class="subtitle">Sign in to your account</p>
        </div>
        
        <!-- Login form -->
        <form @submit.prevent="handleLogin" class="login-form">
          <div class="form-group">
            <label for="username" class="form-label">Username</label>
            <div class="input-wrapper">
              <svg class="input-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M20 21V19C20 16.24 16.42 14 12 14M12 14C7.58 14 4 16.24 4 19V21M12 14C14.76 14 17.3 15.2 19 17M12 14C9.24 14 6.7 15.2 5 17M16 7C16 9.21 14.21 11 12 11C9.79 11 8 9.21 8 7C8 4.79 9.79 3 12 3C14.21 3 16 4.79 16 7Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <input 
                type="text" 
                class="form-input" 
                id="username" 
                v-model="username" 
                placeholder="Enter your username"
                autocomplete="username"
                required
              >
            </div>
          </div>
          
          <div class="form-group">
            <label for="password" class="form-label">Password</label>
            <div class="input-wrapper">
              <svg class="input-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M19 11H5C3.89543 11 3 11.8954 3 13V20C3 21.1046 3.89543 22 5 22H19C20.1046 22 21 21.1046 21 20V13C21 11.8954 20.1046 11 19 11Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M7 11V7C7 5.67392 7.52678 4.40215 8.46447 3.46447C9.40215 2.52678 10.6739 2 12 2C13.3261 2 14.5979 2.52678 15.5355 3.46447C16.4732 4.40215 17 5.67392 17 7V11" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <input 
                :type="showPassword ? 'text' : 'password'" 
                class="form-input" 
                id="password" 
                v-model="password" 
                placeholder="Enter your password"
                autocomplete="current-password"
                required
              >
              <button 
                type="button" 
                class="password-toggle" 
                @click="togglePasswordVisibility"
                aria-label="Toggle password visibility"
              >
                <svg v-if="showPassword" width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <line x1="1" y1="1" x2="23" y2="23" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                </svg>
                <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </button>
            </div>
          </div>
          
          <div class="form-options">
            <div class="remember-me">
              <input type="checkbox" id="remember" v-model="rememberMe">
              <label for="remember">Remember me</label>
            </div>
            <router-link to="/simple-reset-password" class="forgot-password">Forgot password?</router-link>
          </div>
          
          <button 
            type="submit" 
            class="login-button"
            :disabled="isLoading"
          >
            <span v-if="!isLoading">Sign In</span>
            <span v-else class="loading-spinner">
              <svg class="animate-spin" width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2V6M12 18V22M6 12H2M22 12H18M19.0784 19.0784L16.25 16.25M16.25 7.75L19.0784 4.92157M4.92157 4.92157L7.75 7.75M7.75 16.25L4.92157 19.0784" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </span>
          </button>
          
          <div v-if="errorMessage" class="error-message">
            {{ errorMessage }}
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import { authAPI } from '../api/authAPI';

const username = ref('');
const password = ref('');
const errorMessage = ref('');
const showPassword = ref(false);
const rememberMe = ref(false);
const isLoading = ref(false);
const maintenanceMode = ref(false); // Set to true if in maintenance
const maintenanceMessage = ref('System under maintenance. Please try again later.');

const router = useRouter();
const authStore = useAuthStore();

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value;
};

const handleLogin = async () => {
  if (!username.value.trim() || !password.value.trim()) {
    errorMessage.value = 'Please enter both username and password';
    return;
  }
  
  isLoading.value = true;
  errorMessage.value = '';
  
  try {
    // Send login request to backend API using auth service
    const response = await authAPI.login(username.value, password.value);

    if (response.data && response.data.access_token) {
      // Store the token using the auth store
      authStore.setToken(response.data.access_token);
      
      if (rememberMe.value) {
        localStorage.setItem('rememberMe', 'true');
        localStorage.setItem('username', username.value);
      } else {
        localStorage.removeItem('rememberMe');
        localStorage.removeItem('username');
      }
      
      // Redirect to dashboard
      router.push('/dashboard');
    } else {
      errorMessage.value = 'Invalid response from server';
    }
  } catch (error: any) {
    if (error.response && error.response.data && error.response.data.detail) {
      errorMessage.value = error.response.data.detail;
    } else if (error.response) {
      errorMessage.value = `Login failed: ${error.response.status} ${error.response.statusText}`;
    } else if (error.request) {
      // Network error
      errorMessage.value = 'Unable to connect to the server. Please check your connection.';
    } else {
      errorMessage.value = 'An unexpected error occurred.';
    }
    console.error('Login error:', error);
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
/* Main container with maroon gradient background */
.login-container {
  position: fixed;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #6a0000, #3d0000); /* Maroon Gradient */
  background-size: 200% 200%;
  animation: gradientAnimation 15s ease infinite;
  padding: 20px;
  overflow: hidden;
  font-family: system-ui, Avenir, Helvetica, Arial, sans-serif;
}

.login-container::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0) 70%);
  animation: textureAnimation 20s linear infinite;
}

/* Maintenance banner styles */
.maintenance-banner {
  position: fixed;
  top: 0;
  left:0;
  width: 100%;
  background: #ffcc00;
  color: #333;
  padding: 10px;
  text-align: center;
  font-weight: bold;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.banner-icon {
  color: #333;
}

/* Background animations matching maroon theme */
.fiber-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  pointer-events: none;
}

.fiber-strand {
  position: absolute;
  width: 2px;
  height: 100%;
  background: linear-gradient(to bottom, transparent, rgba(255, 180, 180, 0.3), transparent);
  animation: fiberFlow 5s linear infinite;
}

@keyframes fiberFlow {
  0% { transform: translateY(-100%); }
  100% { transform: translateY(100%); }
}

.light-pulse {
  position: absolute;
  width: 4px;
  height: 4px;
  background: #ffcccc;
  border-radius: 50%;
  animation: pulse 2s ease-in-out infinite;
  box-shadow: 0 0 20px rgba(255, 150, 150, 0.5);
}

@keyframes pulse {
  0%, 100% { opacity: 0; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.5); }
}

.floating-particles {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.particle {
  position: absolute;
  width: 3px;
  height: 3px;
  background: rgba(255, 200, 200, 0.3);
  border-radius: 50%;
  animation: float 10s linear infinite;
}

@keyframes float {
  0% { transform: translateY(0) rotate(0deg); opacity: 1; }
  100% { transform: translateY(-100vh) rotate(360deg); opacity: 0; }
}

/* New wrapper for the form and notch */
.login-form-wrapper {
  position: relative;
  width: 100%;
  max-width: 480px;
  margin-top: 50px; /* Space for the notch to appear */
}

/* Main Login Card styling */
.login-card {
  width: 100%;
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  padding: 60px 40px 40px 40px; /* Increased top padding */
  z-index: 1;
  transform-style: preserve-3d;
  transition: transform 0.3s;
  box-sizing: border-box;
}

/* "Poni" Logo container */
.logo-notch {
  position: absolute;
  top: 0;
  left: 50%;
  transform: translate(-50%, -50%);
  background: #fff;
  border-radius: 50%;
  padding: 15px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2;
}

.logo-wrapper-3d {
  position: relative;
  perspective: 1000px;
}

.logo-glow-3d {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle, rgba(255, 107, 107, 0.4) 0%, transparent 70%);
  transform: translate(-50%, -50%) translateZ(-20px);
  filter: blur(20px);
  opacity: 0.7;
}

/* Brand and title section */
.brand-section {
  text-align: center;
  margin-bottom: 24px;
}

.brand-section h1 {
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 8px 0;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.1);
}

.logo-notch svg {
  color: #ff6b6b; /* Warna merah */
}

.subtitle {
  color: #64748b;
  font-size: 16px;
  margin: 0;
}

/* Form elements styling */
.form-group {
  margin-bottom: 20px;
}

.form-label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: #334155;
  margin-bottom: 8px;
}

.input-wrapper {
  position: relative;
}

.input-icon {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  color: #94a3b8;
  pointer-events: none;
}

.form-input {
  width: 100%;
  padding: 14px 14px 14px 44px;
  border: 1px solid #d1d5db;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 400;
  color: #111827;
  background-color: #f9fafb;
  transition: all 0.2s ease;
  box-sizing: border-box;
}

.form-input:focus {
  outline: none;
  border-color: #ff6b6b;
  box-shadow: 0 0 0 3px rgba(255, 107, 107, 0.2);
  transform: translateZ(5px);
  background-color: #fff;
}

.form-input::placeholder {
  color: #9ca3af;
  font-weight: 400;
}

.password-toggle {
  position: absolute;
  right: 14px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  color: #94a3b8;
  padding: 4px;
  border-radius: 4px;
  transition: color 0.2s ease;
}

.password-toggle:hover {
  color: #ff6b6b;
}

/* Form options (remember me, forgot password) */
.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  font-size: 14px;
  color: #4b5563;
}

.remember-me {
  display: flex;
  align-items: center;
  gap: 8px;
}

.remember-me input {
  margin: 0;
  accent-color: #ff6b6b;
}

.forgot-password {
  color: #ff6b6b;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s ease;
}

.forgot-password:hover {
  text-decoration: underline;
  color: #ff8e53;
}

/* Login Button styling */
.login-button {
  width: 100%;
  padding: 14px;
  background: linear-gradient(90deg, #ff6b6b, #ff8e53);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  position: relative;
  overflow: hidden;
  transform-style: preserve-3d;
}

.login-button::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  transition: width 0.6s ease, height 0.6s ease;
}

.login-button:hover::before {
  width: 300px;
  height: 300px;
}

.login-button:hover:not(:disabled) {
  transform: translateY(-2px) translateZ(10px);
  box-shadow: 0 5px 15px rgba(255, 107, 107, 0.4);
}

.login-button:disabled {
  background: #e5e7eb;
  color: #9ca3af;
  cursor: not-allowed;
}

.loading-spinner {
  display: flex;
  align-items: center;
  justify-content: center;
}

.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.error-message {
  background-color: #fee2e2;
  color: #dc2626;
  padding: 12px;
  border-radius: 8px;
  margin-top: 16px;
  font-size: 14px;
  border: 1px solid #fecaca;
  text-align: center;
}

/* Media Queries for Responsiveness */
@media (max-width: 767px) {
  .login-container {
    padding: 15px;
    align-items: flex-start;
    padding-top: 60px;
  }
  
  .login-form-wrapper {
    margin-top: 50px;
    width: 100%;
  }

  .login-card {
    padding: 60px 24px 32px 24px;
  }
  
  .form-options {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
}

@media (max-width: 480px) {
  .login-card {
    padding: 60px 20px 28px 20px;
  }
  
  .brand-section h1 {
    font-size: 22px;
  }
}

@media (prefers-reduced-motion: reduce) {
  .fiber-strand, .light-pulse, .particle, .login-card, .login-button {
    animation: none;
    transition: none;
  }
}

/* Background animation keyframes */
@keyframes gradientAnimation {
  0% { background-position: 0% 0%; }
  50% { background-position: 100% 100%; }
  100% { background-position: 0% 0%; }
}

@keyframes textureAnimation {
  0% { transform: translate(-50%, -50%) rotate(0deg); }
  100% { transform: translate(-50%, -50%) rotate(360deg); }
}
</style>

