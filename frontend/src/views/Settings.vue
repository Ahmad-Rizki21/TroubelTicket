<template>
  <div class="settings-container">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">Pengaturan Sistem</h1>
        <p class="page-subtitle">Kelola konfigurasi dan preferensi sistem</p>
      </div>
    </div>

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
                v-model="generalSettings.siteName" 
                class="form-input"
              >
            </div>
            
            <div class="form-group">
              <label for="timezone">Zona Waktu</label>
              <select id="timezone" v-model="generalSettings.timezone" class="form-select">
                <option value="Asia/Jakarta">Asia/Jakarta (UTC+7)</option>
                <option value="Asia/Makassar">Asia/Makassar (UTC+8)</option>
                <option value="Asia/Jayapura">Asia/Jayapura (UTC+9)</option>
              </select>
            </div>
            
            <div class="form-group">
              <label for="language">Bahasa</label>
              <select id="language" v-model="generalSettings.language" class="form-select">
                <option value="id">Bahasa Indonesia</option>
                <option value="en">English</option>
              </select>
            </div>
            
            <div class="form-group checkbox-group">
              <label class="checkbox-label">
                <input 
                  type="checkbox" 
                  v-model="generalSettings.maintenanceMode"
                  class="form-checkbox"
                >
                <span class="checkbox-text">Mode Pemeliharaan</span>
              </label>
              <p class="help-text">Aktifkan mode pemeliharaan untuk membatasi akses pengguna</p>
            </div>
          </div>
          
          <div class="form-actions">
            <button class="save-button" @click="saveGeneralSettings">Simpan Perubahan</button>
          </div>
        </div>

        <!-- Email Settings -->
        <div v-if="activeSection === 'email'" class="settings-section">
          <div class="section-header">
            <h2 class="section-title">Pengaturan Email</h2>
            <p class="section-description">Konfigurasi server email untuk notifikasi</p>
          </div>
          
          <div class="settings-form">
            <div class="form-group">
              <label for="smtpHost">SMTP Host</label>
              <input 
                type="text" 
                id="smtpHost" 
                v-model="emailSettings.smtpHost" 
                class="form-input"
                placeholder="smtp.example.com"
              >
            </div>
            
            <div class="form-row">
              <div class="form-group">
                <label for="smtpPort">Port</label>
                <input 
                  type="number" 
                  id="smtpPort" 
                  v-model="emailSettings.smtpPort" 
                  class="form-input"
                  placeholder="587"
                >
              </div>
              
              <div class="form-group">
                <label for="encryption">Enkripsi</label>
                <select id="encryption" v-model="emailSettings.encryption" class="form-select">
                  <option value="tls">TLS</option>
                  <option value="ssl">SSL</option>
                  <option value="none">None</option>
                </select>
              </div>
            </div>
            
            <div class="form-group">
              <label for="emailUsername">Username</label>
              <input 
                type="text" 
                id="emailUsername" 
                v-model="emailSettings.username" 
                class="form-input"
                placeholder="username@example.com"
              >
            </div>
            
            <div class="form-group">
              <label for="emailPassword">Password</label>
              <input 
                type="password" 
                id="emailPassword" 
                v-model="emailSettings.password" 
                class="form-input"
                placeholder="••••••••"
              >
            </div>
            
            <div class="form-group">
              <label for="senderEmail">Email Pengirim</label>
              <input 
                type="email" 
                id="senderEmail" 
                v-model="emailSettings.senderEmail" 
                class="form-input"
                placeholder="noreply@example.com"
              >
            </div>
            
            <div class="form-group">
              <label for="senderName">Nama Pengirim</label>
              <input 
                type="text" 
                id="senderName" 
                v-model="emailSettings.senderName" 
                class="form-input"
                placeholder="Trouble Ticket System"
              >
            </div>
          </div>
          
          <div class="form-actions">
            <button class="test-button" @click="testEmailConnection">Uji Koneksi</button>
            <button class="save-button" @click="saveEmailSettings">Simpan Perubahan</button>
          </div>
        </div>

        <!-- Notification Settings -->
        <div v-if="activeSection === 'notifications'" class="settings-section">
          <div class="section-header">
            <h2 class="section-title">Notifikasi</h2>
            <p class="section-description">Atur jenis notifikasi yang dikirim ke pengguna</p>
          </div>
          
          <div class="settings-form">
            <div class="notification-group">
              <h3 class="group-title">Notifikasi Tiket</h3>
              
              <div class="form-group checkbox-group">
                <label class="checkbox-label">
                  <input 
                    type="checkbox" 
                    v-model="notificationSettings.ticketCreated"
                    class="form-checkbox"
                  >
                  <span class="checkbox-text">Tiket Dibuat</span>
                </label>
                <p class="help-text">Kirim notifikasi saat tiket baru dibuat</p>
              </div>
              
              <div class="form-group checkbox-group">
                <label class="checkbox-label">
                  <input 
                    type="checkbox" 
                    v-model="notificationSettings.ticketAssigned"
                    class="form-checkbox"
                  >
                  <span class="checkbox-text">Tiket Ditugaskan</span>
                </label>
                <p class="help-text">Kirim notifikasi saat tiket ditugaskan ke teknisi</p>
              </div>
              
              <div class="form-group checkbox-group">
                <label class="checkbox-label">
                  <input 
                    type="checkbox" 
                    v-model="notificationSettings.ticketUpdated"
                    class="form-checkbox"
                  >
                  <span class="checkbox-text">Tiket Diperbarui</span>
                </label>
                <p class="help-text">Kirim notifikasi saat tiket diperbarui</p>
              </div>
              
              <div class="form-group checkbox-group">
                <label class="checkbox-label">
                  <input 
                    type="checkbox" 
                    v-model="notificationSettings.ticketResolved"
                    class="form-checkbox"
                  >
                  <span class="checkbox-text">Tiket Diselesaikan</span>
                </label>
                <p class="help-text">Kirim notifikasi saat tiket diselesaikan</p>
              </div>
            </div>
            
            <div class="notification-group">
              <h3 class="group-title">Notifikasi Pengguna</h3>
              
              <div class="form-group checkbox-group">
                <label class="checkbox-label">
                  <input 
                    type="checkbox" 
                    v-model="notificationSettings.userRegistered"
                    class="form-checkbox"
                  >
                  <span class="checkbox-text">Pengguna Terdaftar</span>
                </label>
                <p class="help-text">Kirim notifikasi saat pengguna baru mendaftar</p>
              </div>
              
              <div class="form-group checkbox-group">
                <label class="checkbox-label">
                  <input 
                    type="checkbox" 
                    v-model="notificationSettings.passwordReset"
                    class="form-checkbox"
                  >
                  <span class="checkbox-text">Reset Password</span>
                </label>
                <p class="help-text">Kirim notifikasi saat pengguna mereset password</p>
              </div>
            </div>
          </div>
          
          <div class="form-actions">
            <button class="save-button" @click="saveNotificationSettings">Simpan Perubahan</button>
          </div>
        </div>

        <!-- User Management -->
        <div v-if="activeSection === 'users'" class="settings-section">
          <div class="section-header">
            <h2 class="section-title">Manajemen Pengguna</h2>
            <p class="section-description">Kelola pengguna dan hak akses sistem</p>
          </div>
          
          <div class="settings-form">
            <div class="form-group">
              <label for="defaultRole">Role Default</label>
              <select id="defaultRole" v-model="userSettings.defaultRole" class="form-select">
                <option value="user">Pengguna</option>
                <option value="technician">Teknisi</option>
                <option value="admin">Administrator</option>
              </select>
            </div>
            
            <div class="form-group checkbox-group">
              <label class="checkbox-label">
                <input 
                  type="checkbox" 
                  v-model="userSettings.requireEmailVerification"
                  class="form-checkbox"
                >
                <span class="checkbox-text">Verifikasi Email Wajib</span>
              </label>
              <p class="help-text">Pengguna harus memverifikasi email sebelum dapat login</p>
            </div>
            
            <div class="form-group checkbox-group">
              <label class="checkbox-label">
                <input 
                  type="checkbox" 
                  v-model="userSettings.allowSelfRegistration"
                  class="form-checkbox"
                >
                <span class="checkbox-text">Izinkan Registrasi Mandiri</span>
              </label>
              <p class="help-text">Pengguna dapat mendaftar akun sendiri</p>
            </div>
            
            <div class="form-group">
              <label for="sessionTimeout">Timeout Sesi (menit)</label>
              <input 
                type="number" 
                id="sessionTimeout" 
                v-model="userSettings.sessionTimeout" 
                class="form-input"
                min="1"
                max="1440"
              >
              <p class="help-text">Durasi maksimal sesi pengguna sebelum harus login ulang</p>
            </div>
          </div>
          
          <div class="form-actions">
            <button class="save-button" @click="saveUserSettings">Simpan Perubahan</button>
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
                <h3 class="info-title">Versi Sistem</h3>
                <div class="info-icon">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M14 2H6C5.46957 2 4.96086 2.21071 4.58579 2.58579C4.21071 2.96086 4 3.46957 4 4V20C4 20.5304 4.21071 21.0391 4.58579 21.4142C4.96086 21.7893 5.46957 22 6 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V8L14 2ZM18 20H6V4H13V9H18V20Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
              </div>
              <div class="info-content">
                <p class="info-value">v2.1.0</p>
                <p class="info-label">Trouble Ticket System</p>
              </div>
            </div>
            
            <div class="info-card">
              <div class="info-header">
                <h3 class="info-title">Database</h3>
                <div class="info-icon">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 3C16.9706 3 21 7.02944 21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3ZM12 17C14.7614 17 17 14.7614 17 12C17 9.23858 14.7614 7 12 7C9.23858 7 7 9.23858 7 12C7 14.7614 9.23858 17 12 17ZM12 14C13.1046 14 14 13.1046 14 12C14 10.8954 13.1046 10 12 10C10.8954 10 10 10.8954 10 12C10 13.1046 10.8954 14 12 14Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
              </div>
              <div class="info-content">
                <p class="info-value">PostgreSQL 13.4</p>
                <p class="info-label">Connected</p>
              </div>
            </div>
            
            <div class="info-card">
              <div class="info-header">
                <h3 class="info-title">Server</h3>
                <div class="info-icon">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M20 7L4 7C2.89543 7 2 7.89543 2 9L2 15C2 16.1046 2.89543 17 4 17L20 17C21.1046 17 22 16.1046 22 15L22 9C22 7.89543 21.1046 7 20 7ZM20 7L20 5C20 3.89543 19.1046 3 18 3L6 3C4.89543 3 4 3.89543 4 5L4 7M20 7L20 9M4 7L4 9M8 13H8.01M12 13H12.01M16 13H16.01" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
              </div>
              <div class="info-content">
                <p class="info-value">Ubuntu 20.04 LTS</p>
                <p class="info-label">Production Server</p>
              </div>
            </div>
            
            <div class="info-card">
              <div class="info-header">
                <h3 class="info-title">Status</h3>
                <div class="info-icon">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22ZM12 18C15.3137 18 18 15.3137 18 12C18 8.68629 15.3137 6 12 6C8.68629 6 6 8.68629 6 12C6 15.3137 8.68629 18 12 18ZM12 15C13.6569 15 15 13.6569 15 12C15 10.3431 13.6569 9 12 9C10.3431 9 9 10.3431 9 12C9 13.6569 10.3431 15 12 15Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
              </div>
              <div class="info-content">
                <p class="info-value success">Operasional</p>
                <p class="info-label">Uptime: 99.98%</p>
              </div>
            </div>
          </div>
          
          <div class="system-actions">
            <button class="action-button primary" @click="backupDatabase">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 12V18M8 16H16M16 8C16 6.93913 15.5786 5.92172 14.8284 5.17157C14.0783 4.42143 13.0609 4 12 4C10.9391 4 9.92172 4.42143 9.17157 5.17157C8.42143 5.92172 8 6.93913 8 8M12 4V8H16" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <span>Backup Database</span>
            </button>
            
            <button class="action-button secondary" @click="clearCache">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M21 4H3M20 8L16 4M4 8L8 4M16 4L14 14M8 4L10 14M14 14L12 20L10 14M14 14H10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <span>Bersihkan Cache</span>
            </button>
            
            <button class="action-button danger" @click="restartServer">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M21 12C21 13.1819 20.7672 14.3522 20.3141 15.4442C19.861 16.5361 19.1971 17.5282 18.3608 18.3645C17.5245 19.2008 16.5324 19.8647 15.4405 20.3178C14.3485 20.7709 13.1782 21 12 21C10.8218 21 9.65152 20.7709 8.55957 20.3178C7.46763 19.8647 6.47553 19.2008 5.6392 18.3645C4.80288 17.5282 4.13898 16.5361 3.68588 15.4442C3.23279 14.3522 3.00003 13.1819 3 12C3.00003 10.8181 3.23279 9.64781 3.68588 8.55585C4.13898 7.4639 4.80288 6.4718 5.6392 5.63547C6.47553 4.79915 7.46763 4.13525 8.55957 3.68216C9.65152 3.22907 10.8218 3 12 3C13.1782 3 14.3485 3.22907 15.4405 3.68216C16.5324 4.13525 17.5245 4.79915 18.3608 5.63547C19.1971 6.4718 19.861 7.4639 20.3141 8.55585C20.7672 9.64781 20.9999 10.8181 21 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <span>Mulai Ulang Server</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';

// State management
const activeSection = ref('general');

// Settings sections
const settingsSections = ref([
  {
    id: 'general',
    title: 'Umum',
    icon: 'GeneralIcon'
  },
  {
    id: 'email',
    title: 'Email',
    icon: 'EmailIcon'
  },
  {
    id: 'notifications',
    title: 'Notifikasi',
    icon: 'NotificationIcon'
  },
  {
    id: 'users',
    title: 'Pengguna',
    icon: 'UserIcon'
  },
  {
    id: 'system',
    title: 'Sistem',
    icon: 'SystemIcon'
  }
]);

// Settings data
const generalSettings = ref({
  siteName: 'Trouble Ticket System',
  timezone: 'Asia/Jakarta',
  language: 'id',
  maintenanceMode: false
});

const emailSettings = ref({
  smtpHost: 'smtp.example.com',
  smtpPort: 587,
  encryption: 'tls',
  username: 'noreply@example.com',
  password: '',
  senderEmail: 'noreply@example.com',
  senderName: 'Trouble Ticket System'
});

const notificationSettings = ref({
  ticketCreated: true,
  ticketAssigned: true,
  ticketUpdated: true,
  ticketResolved: true,
  userRegistered: true,
  passwordReset: true
});

const userSettings = ref({
  defaultRole: 'user',
  requireEmailVerification: true,
  allowSelfRegistration: false,
  sessionTimeout: 30
});

// Icon components
const GeneralIcon = {
  template: `
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M4 6H20M4 12H20M4 18H16" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  `
};

const EmailIcon = {
  template: `
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M3 8L10.89 13.26C11.2134 13.4762 11.5928 13.5915 11.9825 13.5919C12.3722 13.5924 12.7553 13.4779 13.0865 13.2621L21 8M5 19H19C20.1046 19 21 18.1046 21 17V7C21 5.89543 20.1046 5 19 5H5C3.89543 5 3 5.89543 3 7V17C3 18.1046 3.89543 19 5 19Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  `
};

const NotificationIcon = {
  template: `
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M18 8C18 6.4087 17.3679 4.88258 16.2426 3.75736C15.1174 2.63214 13.5913 2 12 2C10.4087 2 8.88258 2.63214 7.75736 3.75736C6.63214 4.88258 6 6.4087 6 8C6 15 3 17 3 17H21C21 17 18 15 18 8ZM13.73 21C13.5542 21.147 13.345 21.2477 13.1213 21.2929C12.8976 21.3381 12.6666 21.3264 12.45 21.2589C12.2333 21.1915 12.0382 21.0705 11.8835 20.9076C11.7289 20.7447 11.6198 20.5453 11.5669 20.33C11.5141 20.1147 11.5193 19.8892 11.5822 19.6763C11.645 19.4634 11.7634 19.2706 11.9253 19.1177C12.0872 18.9647 12.2868 18.8572 12.504 18.8059C12.7211 18.7546 12.9482 18.7614 13.1623 18.8256C13.3764 18.8898 13.5701 19.0092 13.7236 19.1715C13.8772 19.3338 13.9851 19.5332 14.036 19.749C14.0868 19.9648 14.0788 20.189 14.0133 20.3978C13.9478 20.6065 13.8274 20.792 13.665 20.9345C13.5025 21.077 13.305 21.1705 13.095 21.195C12.885 21.2195 12.6714 21.1733 12.475 21.06C12.2786 20.9467 12.1064 20.7706 11.975 20.55C11.8436 20.3294 11.7575 20.0713 11.725 19.8C11.6925 19.5287 11.7147 19.25 11.79 18.99C11.8653 18.73 12.005 18.49 12.2 18.3C12.394 18.109 12.628 17.962 12.885 17.87C13.142 17.778 13.416 17.742 13.686 17.765C13.956 17.788 14.215 17.87 14.445 17.999C14.675 18.128 14.87 18.303 15.015 18.51C15.16 18.717 15.25 18.95 15.28 19.19C15.31 19.43 15.279 19.67 15.189 19.89C15.099 20.11 14.952 20.304 14.76 20.457C14.568 20.61 14.336 20.718 14.085 20.77C13.834 20.822 13.572 20.817 13.32 20.755C13.068 20.693 12.833 20.576 12.635 20.413C12.437 20.25 12.282 20.045 12.185 19.815C12.088 19.585 12.052 19.335 12.08 19.085C12.108 18.835 12.2 18.6 12.345 18.4C12.49 18.2 12.685 18.04 12.915 17.93C13.145 17.82 13.405 17.765 13.67 17.77C13.935 17.775 14.195 17.84 14.43 17.96C14.665 18.08 14.87 18.255 15.03 18.475C15.19 18.695 15.3 18.955 15.355 19.235C15.41 19.515 15.408 19.805 15.348 20.085C15.288 20.365 15.172 20.625 15 20.85C14.828 21.075 14.615 21.255 14.375 21.385C14.135 21.515 13.875 21.59 13.61 21.605C13.345 21.62 13.085 21.575 12.84 21.47C12.595 21.365 12.375 21.205 12.195 21C12.015 20.795 11.885 20.555 11.815 20.295C11.745 20.035 11.735 19.76 11.785 19.5C11.835 19.24 11.945 19 12.11 18.79C12.275 18.58 12.49 18.41 12.74 18.29C12.99 18.17 13.27 18.105 13.56 18.1C13.85 18.095 14.14 18.15 14.41 18.26C14.68 18.37 14.925 18.535 15.13 18.745C15.335 18.955 15.495 19.205 15.6 19.48C15.705 19.755 15.75 20.05 15.735 20.35C15.72 20.65 15.645 20.95 15.51 21.225C15.375 21.5 15.185 21.745 14.95 21.945C14.715 22.145 14.44 22.295 14.14 22.385C13.84 22.475 13.52 22.505 13.2 22.475C12.88 22.445 12.565 22.355 12.275 22.21C11.985 22.065 11.725 21.865 11.51 21.62C11.295 21.375 11.13 21.09 11.02 20.785C10.91 20.48 10.86 20.16 10.87 19.84C10.88 19.52 10.95 19.205 11.08 18.915C11.21 18.625 11.395 18.365 11.625 18.15C11.855 17.935 12.125 17.77 12.42 17.665C12.715 17.56 13.03 17.515 13.345 17.535C13.66 17.555 13.965 17.64 14.245 17.785C14.525 17.93 14.775 18.13 14.98 18.375C15.185 18.62 15.34 18.905 15.44 19.215C15.54 19.525 15.58 19.855 15.56 20.185C15.54 20.515 15.46 20.84 15.32 21.145C15.18 21.45 14.985 21.725 14.745 21.955C14.505 22.185 14.225 22.365 13.92 22.485C13.615 22.605 13.29 22.665 12.96 22.665C12.63 22.665 12.305 22.605 12 22.485C11.695 22.365 11.415 22.185 11.175 21.955C10.935 21.725 10.74 21.45 10.6 21.145C10.46 20.84 10.38 20.515 10.36 20.185C10.34 19.855 10.38 19.525 10.48 19.215C10.58 18.905 10.735 18.62 10.94 18.375C11.145 18.13 11.395 17.93 11.675 17.785C11.955 17.64 12.26 17.555 12.575 17.535C12.89 17.515 13.205 17.56 13.5 17.665" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
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

// Methods
const saveGeneralSettings = () => {
  alert('Pengaturan umum berhasil disimpan!');
};

const saveEmailSettings = () => {
  alert('Pengaturan email berhasil disimpan!');
};

const testEmailConnection = () => {
  alert('Menguji koneksi email...');
};

const saveNotificationSettings = () => {
  alert('Pengaturan notifikasi berhasil disimpan!');
};

const saveUserSettings = () => {
  alert('Pengaturan pengguna berhasil disimpan!');
};

const backupDatabase = () => {
  if (confirm('Apakah Anda yakin ingin membuat backup database?')) {
    alert('Proses backup database dimulai...');
  }
};

const clearCache = () => {
  if (confirm('Apakah Anda yakin ingin membersihkan cache sistem?')) {
    alert('Cache sistem berhasil dibersihkan!');
  }
};

const restartServer = () => {
  if (confirm('Apakah Anda yakin ingin merestart server? Sistem akan tidak tersedia untuk beberapa menit.')) {
    alert('Server restart dimulai...');
  }
};

// Lifecycle hook
onMounted(() => {
  // Load settings from API in a real app
  console.log('Loading settings...');
});
</script>

<style scoped>
.settings-container {
  padding: 24px;
  width: 100%;
  box-sizing: border-box;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
  flex-wrap: wrap;
  gap: 16px;
}

.header-content {
  flex: 1;
}

.page-title {
  font-size: 28px;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 8px 0;
}

.page-subtitle {
  font-size: 16px;
  color: #64748b;
  margin: 0;
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
  background: #eff6ff;
  color: #3b82f6;
  border-left-color: #3b82f6;
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
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
  background-color: #fff;
}

.checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
}

.form-checkbox {
  width: 18px;
  height: 18px;
  accent-color: #3b82f6;
  cursor: pointer;
}

.checkbox-text {
  font-size: 16px;
  font-weight: 500;
  color: #111827;
}

.help-text {
  font-size: 14px;
  color: #64748b;
  margin: 0;
}

.notification-group {
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 1px solid #e5e7eb;
}

.group-title {
  font-size: 18px;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 16px 0;
}

.form-actions {
  display: flex;
  gap: 16px;
  margin-top: 32px;
  flex-wrap: wrap;
}

.save-button {
  padding: 12px 24px;
  background: linear-gradient(90deg, #3b82f6, #60a5fa);
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
  box-shadow: 0 5px 15px rgba(59, 130, 246, 0.4);
}

.test-button {
  padding: 12px 24px;
  background: #e5e7eb;
  color: #374151;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.test-button:hover {
  background: #d1d5db;
}

.system-info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
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

.system-actions {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.action-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-button.primary {
  background: linear-gradient(90deg, #3b82f6, #60a5fa);
  color: white;
}

.action-button.secondary {
  background: #e5e7eb;
  color: #374151;
}

.action-button.danger {
  background: #fee2e2;
  color: #dc2626;
}

.action-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
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
    border-bottom-color: #3b82f6;
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
  
  .system-actions {
    flex-direction: column;
  }
  
  .action-button {
    width: 100%;
    justify-content: center;
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