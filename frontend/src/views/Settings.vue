<template>
  <div class="settings-container">
    <!-- Page Header -->
    <header class="page-header">
      <div class="header-content">
        <div class="title-section">
          <h1 class="page-title">
            <span class="title-gradient">Pengaturan Sistem</span>
          </h1>
          <p class="page-subtitle">Kelola konfigurasi dan preferensi sistem</p>
        </div>
        <div class="header-stats">
          <div class="live-indicator">
            <div class="live-dot"></div>
            <span>Active</span>
          </div>
        </div>
      </div>
    </header>

    <!-- Settings Navigation -->
    <div class="settings-layout">
      <nav class="settings-sidebar">
        <ul class="nav-list">
          <li class="nav-item" v-for="section in settingsSections" :key="section.id">
            <button 
              class="nav-link" 
              :class="{ active: activeSection === section.id }"
              @click="activeSection = section.id"
            >
              <component :is="section.icon" />
              <span>{{ section.title }}</span>
            </button>
          </li>
        </ul>
      </nav>

      <!-- Settings Content -->
      <div class="settings-content">
        <!-- General Settings -->
        <div v-if="activeSection === 'general'" class="settings-section">
          <div class="section-header">
            <h2 class="section-title">Pengaturan Umum</h2>
            <p class="section-description">Konfigurasi dasar sistem trouble ticket</p>
          </div>
          
          <div class="settings-form">
            <div class="form-group">
              <label for="siteName">Nama Situs</label>
              <input 
                type="text" 
                id="siteName" 
                v-model="settingsStore.siteName" 
                class="form-input"
              >
            </div>
            
            <div class="form-group">
              <label for="timezone">Zona Waktu</label>
              <select id="timezone" v-model="settingsStore.timezone" class="form-select">
                <option value="Asia/Jakarta">Asia/Jakarta (UTC+7)</option>
                <option value="Asia/Makassar">Asia/Makassar (UTC+8)</option>
                <option value="Asia/Jayapura">Asia/Jayapura (UTC+9)</option>
              </select>
            </div>
            
            <div class="form-group">
              <label for="language">Bahasa</label>
              <select id="language" v-model="settingsStore.language" class="form-select">
                <option value="id">Bahasa Indonesia</option>
                <option value="en">English</option>
              </select>
            </div>
          </div>
          
          <div class="form-actions">
            <button class="save-button" @click="saveGeneralSettings">Simpan Perubahan</button>
          </div>
        </div>

        <!-- Account Settings -->
        <div v-if="activeSection === 'account'" class="settings-section">
          <div class="section-header">
            <h2 class="section-title">Akun Saya</h2>
            <p class="section-description">Kelola nama pengguna Anda</p>
          </div>
          
          <div class="settings-form">
            <div class="form-group">
              <label for="username">Nama Pengguna</label>
              <input 
                type="text" 
                id="username" 
                v-model="accountSettings.username" 
                class="form-input"
                placeholder="Nama pengguna Anda"
              >
            </div>
          </div>
          
          <div class="form-actions">
            <button class="save-button" @click="saveAccountSettings">Simpan Nama Pengguna</button>
          </div>
        </div>

        <!-- System Information -->
        <div v-if="activeSection === 'system'" class="settings-section">
          <div class="section-header">
            <h2 class="section-title">Informasi Sistem</h2>
            <p class="section-description">Detail teknis dan status sistem</p>
          </div>
          
          <div class="system-info-grid">
            <div class="info-card">
              <div class="info-header">
                <h3 class="info-title">Versi Aplikasi</h3>
                <div class="info-icon">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M14 2v6h6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                </div>
              </div>
              <div class="info-content">
                <p class="info-value">v{{ appVersion }}</p>
                <p class="info-label">Frontend Version</p>
              </div>
            </div>
            
            <div class="info-card">
              <div class="info-header">
                <h3 class="info-title">Database</h3>
                <div class="info-icon">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 3v18m-9-9h18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                </div>
              </div>
              <div class="info-content">
                <p class="info-value">MySQL / MariaDB</p>
                <p class="info-label">Status: Connected</p>
              </div>
            </div>
            
            <div class="info-card">
              <div class="info-header">
                <h3 class="info-title">Server</h3>
                <div class="info-icon">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="2" y="2" width="20" height="20" rx="2" ry="2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><line x1="2" y1="8" x2="22" y2="8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><line x1="8" y1="2" x2="8" y2="22" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                </div>
              </div>
              <div class="info-content">
                <p class="info-value">Production</p>
                <p class="info-label">Environment</p>
              </div>
            </div>
            
            <div class="info-card">
              <div class="info-header">
                <h3 class="info-title">API Status</h3>
                <div class="info-icon">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M22 12h-4l-3 9L9 3l-3 9H2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                </div>
              </div>
              <div class="info-content">
                <p class="info-value success">Operasional</p>
                <p class="info-label">Uptime: 99.9%</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, markRaw } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useSettingsStore } from '../stores/settings';
import { version as appVersion } from '../../package.json';

// State management
const activeSection = ref('general');
const authStore = useAuthStore();
const settingsStore = useSettingsStore();

// Define Icon components first
const GeneralIcon = {
  template: `
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M4 6H20M4 12H20M4 18H16" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  `
};

const UserIcon = {
  template: `
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M20 21V19C20 16.24 16.42 14 12 14C7.58 14 4 16.24 4 19V21M12 14C14.76 14 17.3 15.2 19 17M12 14C9.24 14 6.7 15.2 5 17M16 7C16 9.21 14.21 11 12 11C9.79 11 8 9.21 8 7C8 4.79 9.79 3 12 3C14.21 3 16 4.79 16 7Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  `
};

const SystemIcon = {
  template: `
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22ZM12 18C15.3137 18 18 15.3137 18 12C18 8.68629 15.3137 6 12 6C8.68629 6 6 8.68629 6 12C6 15.3137 8.68629 18 12 18ZM12 15C13.6569 15 15 13.6569 15 12C15 10.3431 13.6569 9 12 9C10.3431 9 9 10.3431 9 12C9 13.6569 10.3431 15 12 15Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  `
};

// Settings sections with direct component references
const settingsSections = ref([
  {
    id: 'general',
    title: 'Umum',
    icon: markRaw(GeneralIcon)
  },
  {
    id: 'account',
    title: 'Akun Saya',
    icon: markRaw(UserIcon)
  },
  {
    id: 'system',
    title: 'Sistem',
    icon: markRaw(SystemIcon)
  }
]);

// Account settings data
const accountSettings = ref({
  username: ''
});

// Methods
const saveGeneralSettings = () => {
  settingsStore.setSiteName(settingsStore.siteName);
  settingsStore.setTimezone(settingsStore.timezone);
  settingsStore.setLanguage(settingsStore.language);
  alert('Pengaturan umum berhasil disimpan!');
};

const saveAccountSettings = () => {
  // Here you would typically call an API to update the username
  // e.g., userAPI.updateUser(authStore.user.id, { username: accountSettings.value.username })
  alert(`Nama pengguna berhasil disimpan menjadi: ${accountSettings.value.username}`)
};

// Lifecycle hook
onMounted(() => {
  if (authStore.user) {
    accountSettings.value.username = authStore.user.username;
  }
});
</script>

<style scoped>
.settings-container {
  background-color: #f8fafc;
  padding: 2rem;
  font-family: 'Inter', sans-serif;
}

/* Header Styles - Similar to Dashboard */
.page-header {
  background: #ffffff;
  border-radius: 1rem;
  padding: 2rem;
  margin-bottom: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 1px solid #e5e7eb;
  flex-shrink: 0;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  width: 100%;
}

.title-section {
  flex: 1;
}

.page-title {
  font-size: clamp(1.75rem, 4vw, 2.5rem);
  font-weight: 800;
  margin: 0 0 0.5rem 0;
  line-height: 1.1;
}

.title-gradient {
  background: linear-gradient(135deg, #800000 0%, #5c0000 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.page-subtitle {
  font-size: clamp(1rem, 2vw, 1.125rem);
  color: #64748b;
  margin: 0;
  line-height: 1.5;
  font-weight: 400;
}

.header-stats {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.live-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: rgba(128, 0, 0, 0.1);
  border-radius: 2rem;
  color: #800000;
  font-size: 0.875rem;
  font-weight: 500;
  border: 1px solid rgba(128, 0, 0, 0.2);
}

.live-dot {
  width: 8px;
  height: 8px;
  background: #800000;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.settings-layout {
  display: flex;
  gap: 24px;
  height: calc(100vh - 180px);
}

.settings-sidebar {
  width: 280px;
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  padding: 24px 0;
  flex-shrink: 0;
}

.nav-list {
  list-style: none;
}

.nav-item {
  margin-bottom: 8px;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 14px 24px;
  width: 100%;
  border: none;
  background: transparent;
  text-align: left;
  font-size: 16px;
  font-weight: 500;
  color: #374151;
  cursor: pointer;
  transition: all 0.2s ease;
  border-left: 3px solid transparent;
}

.nav-link:hover {
  background: #f9fafb;
  color: #1e293b;
}

.nav-link.active {
  background: rgba(128, 0, 0, 0.1);
  color: #800000;
  border-left-color: #800000;
}

.settings-content {
  flex: 1;
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  padding: 32px;
  overflow-y: auto;
}

.section-header {
  margin-bottom: 32px;
}

.section-title {
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 8px 0;
}

.section-description {
  font-size: 16px;
  color: #64748b;
  margin: 0;
}

.settings-form {
  max-width: 600px;
}

.form-group {
  margin-bottom: 24px;
}

.form-row {
  display: flex;
  gap: 16px;
}

.form-group label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: #334155;
  margin-bottom: 8px;
}

.form-input,
.form-select {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 16px;
  color: #111827;
  background-color: #f9fafb;
  transition: all 0.2s ease;
  box-sizing: border-box;
}

.form-input:focus,
.form-select:focus {
  outline: none;
  border-color: #800000;
  box-shadow: 0 0 0 3px rgba(128, 0, 0, 0.1);
  background-color: #fff;
}

.form-actions {
  display: flex;
  gap: 16px;
  margin-top: 32px;
  flex-wrap: wrap;
}

.save-button {
  padding: 12px 24px;
  background: linear-gradient(135deg, #800000 0%, #5c0000 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.save-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(128, 0, 0, 0.3);
}

.system-info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 24px;
}

.info-card {
  background: #f9fafb;
  border-radius: 12px;
  padding: 24px;
  border: 1px solid #e5e7eb;
  transition: all 0.2s ease;
}

.info-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.info-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.info-title {
  font-size: 16px;
  font-weight: 600;
  color: #374151;
  margin: 0;
}

.info-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #374151;
}

.info-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-value {
  font-size: 20px;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.info-value.success {
  color: #10b981;
}

.info-label {
  font-size: 14px;
  color: #64748b;
  margin: 0;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .settings-layout {
    flex-direction: column;
    height: auto;
  }
  
  .settings-sidebar {
    width: 100%;
  }
  
  .nav-list {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
  }
  
  .nav-item {
    margin-bottom: 0;
  }
  
  .nav-link {
    border-left: none;
    border-bottom: 3px solid transparent;
    border-radius: 8px;
  }
  
  .nav-link.active {
    border-left: none;
    border-bottom-color: #800000;
  }
  
  .form-row {
    flex-direction: column;
    gap: 16px;
  }
}

@media (max-width: 768px) {
  .settings-container {
    padding: 16px;
  }
  
  .page-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .settings-content {
    padding: 24px;
  }
}

@media (max-width: 480px) {
  .settings-container {
    padding: 12px;
  }
  
  .page-title {
    font-size: 24px;
  }
  
  .settings-content {
    padding: 16px;
  }
  
  .system-info-grid {
    grid-template-columns: 1fr;
  }
}
</style>