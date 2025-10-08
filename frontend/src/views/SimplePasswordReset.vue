<template>
  <div class="login-container">
    <!-- Animated Background -->
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
      <!-- Logo Notch -->
      <div class="logo-notch">
        <div class="logo-wrapper-3d">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM12 6V12L16 14" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <div class="logo-glow-3d"></div>
        </div>
      </div>

      <div class="login-card">
        <!-- Header Section -->
        <div class="brand-section">
          <h1>Reset Password</h1>
          <p class="subtitle">Masukkan username dan password baru Anda</p>
        </div>
        
        <!-- Reset Password Form -->
        <form @submit.prevent="handlePasswordReset" class="login-form">
          <div class="form-group">
            <label for="username" class="form-label">Username</label>
            <div class="input-wrapper">
              <svg class="input-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M20 21V19C20 16.24 16.42 14 12 14M12 14C7.58 14 4 16.24 4 19V21M12 14C14.76 14 17.3 15.2 19 17M12 14C9.24 14 6.7 15.2 5 17M16 7C16 9.21 14.21 11 12 11C9.79 11 8 9.21 8 7C8 4.79 9.79 3 12 3C14.21 3 16 4.79 16 7Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <input type="text" class="form-input" id="username" v-model="username" placeholder="Enter your username" required>
            </div>
          </div>

          <div class="form-group">
            <label for="newPassword" class="form-label">New Password</label>
            <div class="input-wrapper">
              <svg class="input-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M19 11H5C3.89543 11 3 11.8954 3 13V20C3 21.1046 3.89543 22 5 22H19C20.1046 22 21 21.1046 21 20V13C21 11.8954 20.1046 11 19 11Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M7 11V7C7 5.67392 7.52678 4.40215 8.46447 3.46447C9.40215 2.52678 10.6739 2 12 2C13.3261 2 14.5979 2.52678 15.5355 3.46447C16.4732 4.40215 17 5.67392 17 7V11" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
              <input :type="showPassword ? 'text' : 'password'" class="form-input" id="newPassword" v-model="newPassword" placeholder="Enter new password" required>
              <button type="button" class="password-toggle" @click="togglePasswordVisibility" aria-label="Toggle password visibility">
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
          <div class="form-group">
            <label for="confirmPassword" class="form-label">Confirm New Password</label>
            <div class="input-wrapper">
              <svg class="input-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M19 11H5C3.89543 11 3 11.8954 3 13V20C3 21.1046 3.89543 22 5 22H19C20.1046 22 21 21.1046 21 20V13C21 11.8954 20.1046 11 19 11Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M7 11V7C7 5.67392 7.52678 4.40215 8.46447 3.46447C9.40215 2.52678 10.6739 2 12 2C13.3261 2 14.5979 2.52678 15.5355 3.46447C16.4732 4.40215 17 5.67392 17 7V11" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
              <input :type="showPassword ? 'text' : 'password'" class="form-input" id="confirmPassword" v-model="confirmPassword" placeholder="Confirm new password" required>
               <button type="button" class="password-toggle" @click="togglePasswordVisibility" aria-label="Toggle password visibility">
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
          <button type="submit" class="login-button" :disabled="isLoading">
            <span v-if="!isLoading">Reset Password</span>
            <span v-else class="loading-spinner">
              <svg class="animate-spin" width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 2V6M12 18V22M6 12H2M22 12H18M19.0784 19.0784L16.25 16.25M16.25 7.75L19.0784 4.92157M4.92157 4.92157L7.75 7.75M7.75 16.25L4.92157 19.0784" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </span>
          </button>
        </form>

        <!-- Messages -->
        <div v-if="message" class="success-message">{{ message }}</div>
        <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>

        <!-- Footer -->
        <div class="form-footer">
          <router-link to="/login" class="back-to-login">← Kembali ke Login</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { passwordResetAPI } from '../api/passwordResetAPI';

// State management
const username = ref('');
const newPassword = ref('');
const confirmPassword = ref('');
const errorMessage = ref('');
const message = ref('');
const showPassword = ref(false);
const isLoading = ref(false);

const router = useRouter();

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value;
};

// Perform password reset
const handlePasswordReset = async () => {
  if (!username.value.trim()) {
    errorMessage.value = 'Please enter your username';
    return;
  }
  if (newPassword.value.length < 6) {
    errorMessage.value = 'Password must be at least 6 characters long';
    return;
  }
  if (newPassword.value !== confirmPassword.value) {
    errorMessage.value = 'Passwords do not match';
    return;
  }

  isLoading.value = true;
  errorMessage.value = '';
  message.value = '';

  try {
    // Make a direct API call to reset password (this requires the backend endpoint to exist)
    // We'll try the change-password endpoint first
    const response = await passwordResetAPI.changePassword(
      username.value,
      newPassword.value,
      confirmPassword.value
    );
    
    message.value = response.data.message || 'Password reset successfully';
    username.value = '';
    newPassword.value = '';
    confirmPassword.value = '';
    
    // Setelah sukses, arahkan ke halaman login setelah 2 detik
    setTimeout(() => {
      router.push('/login');
    }, 2000);
    
  } catch (error: any) {
    console.error('Password reset error:', error);
    if (error.response && error.response.status === 404) {
      errorMessage.value = 'Forgot password feature is not available. Please contact your system administrator.';
    } else if (error.response && error.response.status === 400) {
      // Jika username tidak ditemukan atau validasi gagal
      errorMessage.value = error.response.data.detail || 'Username tidak ditemukan atau terjadi kesalahan.';
    } else if (error.response && error.response.data && error.response.data.detail) {
      errorMessage.value = error.response.data.detail;
    } else {
      errorMessage.value = 'An error occurred. Please try again.';
    }
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

.light-pulse {
  position: absolute;
  width: 4px;
  height: 4px;
  background: #ffcccc;
  border-radius: 50%;
  animation: pulse 2s ease-in-out infinite;
  box-shadow: 0 0 20px rgba(255, 150, 150, 0.5);
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

/* Wrapper for the form and notch */
.login-form-wrapper {
  position: relative;
  width: 100%;
  max-width: 480px;
  margin-top: 50px;
}

/* Main Login Card styling */
.login-card {
  width: 100%;
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  padding: 60px 40px 40px 40px;
  z-index: 1;
  transform-style: preserve-3d;
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
}

.logo-notch svg {
  color: #ff6b6b;
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
  color: #111827;
  background-color: #f9fafb;
  transition: all 0.2s ease;
  box-sizing: border-box;
}

.form-input:focus {
  outline: none;
  border-color: #ff6b6b;
  box-shadow: 0 0 0 3px rgba(255, 107, 107, 0.2);
  background-color: #fff;
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
}

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
}

.login-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(255, 107, 107, 0.4);
}

.login-button:disabled {
  background: #e5e7eb;
  cursor: not-allowed;
}

.loading-spinner {
  display: flex;
  justify-content: center;
}

.animate-spin {
  animation: spin 1s linear infinite;
}

.error-message, .success-message {
  padding: 12px;
  border-radius: 8px;
  margin-top: 16px;
  font-size: 14px;
  text-align: center;
}

.error-message {
  background-color: #fee2e2;
  color: #dc2626;
  border: 1px solid #fecaca;
}

.success-message {
  background-color: #d1fae5;
  color: #065f46;
  border: 1px solid #a7f3d0;
}

.form-footer {
  text-align: center;
  margin-top: 24px;
}

.back-to-login {
  color: #ff6b6b;
  text-decoration: none;
  font-weight: 500;
}

.back-to-login:hover {
  text-decoration: underline;
}

@keyframes gradientAnimation {
  0% { background-position: 0% 0%; }
  50% { background-position: 100% 100%; }
  100% { background-position: 0% 0%; }
}

@keyframes textureAnimation {
  0% { transform: translate(-50%, -50%) rotate(0deg); }
  100% { transform: translate(-50%, -50%) rotate(360deg); }
}

@keyframes fiberFlow {
  0% { transform: translateY(-100%); }
  100% { transform: translateY(100%); }
}

@keyframes pulse {
  0%, 100% { opacity: 0; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.5); }
}

@keyframes float {
  0% { transform: translateY(0) rotate(0deg); opacity: 1; }
  100% { transform: translateY(-100vh) rotate(360deg); opacity: 0; }
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>