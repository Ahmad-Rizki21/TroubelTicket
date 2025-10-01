<template>
  <div id="app">
    <div v-if="authStore.isAuthenticated" class="app-layout">
      <!-- Sidebar Navigation -->
      <aside class="sidebar">
        <div class="sidebar-header">
          <div class="logo">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM12 6V12L16 14" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span class="logo-text">Trouble Ticket</span>
          </div>
        </div>
        
        <nav class="sidebar-nav">
          <ul class="nav-list">
            <li class="nav-item">
              <router-link to="/dashboard" class="nav-link" active-class="active">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M3 9L12 2L21 9V20C21 20.5304 20.7893 21.0391 20.4142 21.4142C20.0391 21.7893 19.5304 22 19 22H5C4.46957 22 3.96086 21.7893 3.58579 21.4142C3.21071 21.0391 3 20.5304 3 20V9Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M9 22V12H15V22" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <span>Dashboard</span>
              </router-link>
            </li>
            <li class="nav-item">
              <router-link to="/tickets" class="nav-link" active-class="active">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M21 11.5C21.0034 12.8199 20.6951 14.1219 20.1 15.3C19.5 16.5 18.5 17.5 17.3 18.1C16.122 18.6951 14.82 19.0034 13.5 19H11.5C10.1801 19.0034 8.87812 18.6951 7.7 18.1C6.5 17.5 5.5 16.5 4.9 15.3C4.30493 14.1219 3.99656 12.8199 4 11.5V11.5C3.99656 10.1801 4.30493 8.87812 4.9 7.7C5.5 6.5 6.5 5.5 7.7 4.9C8.87812 4.30493 10.1801 3.99656 11.5 4H13.5C14.8199 3.99656 16.1219 4.30493 17.3 4.9C18.5 5.5 19.5 6.5 20.1 7.7C20.6951 8.87812 21.0034 10.1801 21 11.5V11.5Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M12 8V12L15 14" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <span>Tiket</span>
              </router-link>
            </li>
            <li class="nav-item">
              <router-link to="/reports" class="nav-link" active-class="active">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M9 17V11M9 7V7.01M15 17V11M15 7V7.01M21 11C21 11.5304 20.7893 12.0391 20.4142 12.4142C20.0391 12.7893 19.5304 13 19 13H17V17C17 17.5304 16.7893 18.0391 16.4142 18.4142C16.0391 18.7893 15.5304 19 15 19H9C8.46957 19 7.96086 18.7893 7.58579 18.4142C7.21071 18.0391 7 17.5304 7 17V13H5C4.46957 13 3.96086 12.7893 3.58579 12.4142C3.21071 12.0391 3 11.5304 3 11V5C3 4.46957 3.21071 3.96086 3.58579 3.58579C3.96086 3.21071 4.46957 3 5 3H19C19.5304 3 20.0391 3.21071 20.4142 3.58579C20.7893 3.96086 21 4.46957 21 5V11Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <span>Laporan</span>
              </router-link>
            </li>
            <li class="nav-item">
              <router-link to="/users" class="nav-link" active-class="active">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M20 21V19C20 16.24 16.42 14 12 14C7.58 14 4 16.24 4 19V21M12 14C14.76 14 17.3 15.2 19 17M12 14C9.24 14 6.7 15.2 5 17M16 7C16 9.21 14.21 11 12 11C9.79 11 8 9.21 8 7C8 4.79 9.79 3 12 3C14.21 3 16 4.79 16 7Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <span>Pengguna</span>
              </router-link>
            </li>
            <li class="nav-item">
              <router-link to="/roles-permissions" class="nav-link" active-class="active">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M15 7H9C7.89543 7 7 7.89543 7 9V15C7 16.1046 7.89543 17 9 17H15C16.1046 17 17 16.1046 17 15V9C17 7.89543 16.1046 7 15 7Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M12 17V22M12 2V7M17 12H22M2 12H7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <span>Peran & Izin</span>
              </router-link>
            </li>
            <li class="nav-item">
              <router-link to="/settings" class="nav-link" active-class="active">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12 15C13.6569 15 15 13.6569 15 12C15 10.3431 13.6569 9 12 9C10.3431 9 9 10.3431 9 12C9 13.6569 10.3431 15 12 15Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M19.4 15C19.2667 15.2833 19.1333 15.5333 19 15.75C18.5991 16.5517 18.0156 17.2492 17.2981 17.7848C16.5807 18.3204 15.7503 18.6785 14.877 18.8284C14.0038 18.9784 13.1138 18.9159 12.2836 18.6463C11.4535 18.3767 10.7084 17.9083 10.114 17.283C9.88068 17.033 9.65402 16.7763 9.434 16.513M19.4 15C20.2 15.2 21 15.4333 21.75 15.75C21.9 15.8 22.0333 15.8667 22.15 15.95M19.4 15C19.6 14.2 19.7667 13.3667 19.9 12.5M19.9 12.5C19.9667 12.1667 20 11.8333 20 11.5C20 11.1667 19.9667 10.8333 19.9 10.5M19.9 12.5C19.7667 11.6333 19.6 10.8 19.4 10M19.4 10C19.2667 9.71667 19.1333 9.46667 19 9.25C18.5991 8.44831 18.0156 7.75075 17.2981 7.21517C16.5807 6.67959 15.7503 6.32153 14.877 6.17157C14.0038 6.02161 13.1138 6.08414 12.2836 6.35374C11.4535 6.62334 10.7084 7.09171 10.114 7.717C9.88068 7.967 9.65402 8.22367 9.434 8.487M19.4 10C20.2 9.8 21 9.56667 21.75 9.25C21.9 9.2 22.0333 9.13333 22.15 9.05M9.434 8.487C8.63317 9.08757 8.01562 9.90029 7.64193 10.8457C7.26825 11.7911 7.15113 12.8369 7.30367 13.865C7.45621 14.8931 7.87327 15.8615 8.50799 16.6613C9.14271 17.461 9.96928 18.0595 10.888 18.385M9.434 8.487C9.21398 8.75033 8.98732 9.007 8.754 9.257M8.754 9.257C8.15388 9.8574 7.73673 10.616 7.55 11.446M8.754 9.257C8.554 9.48367 8.36067 9.717 8.174 9.957M8.174 9.957C7.78732 10.4837 7.46065 11.0603 7.2 11.679M7.2 11.679C7.06668 12.1123 6.96668 12.5657 6.9 13.032M6.9 13.032C6.83332 13.4987 6.83332 13.9653 6.9 14.432M6.9 14.432C6.96668 14.8987 7.06668 15.352 7.2 15.7853M7.2 15.7853C7.46065 16.4047 7.78732 16.9813 8.174 17.508M8.174 17.508C8.36067 17.748 8.554 17.9813 8.754 18.208M8.754 18.208C8.98732 18.458 9.21398 18.7147 9.434 18.978M9.434 18.978C9.65402 19.2413 9.88068 19.498 10.114 19.748M10.114 19.748C10.7084 20.3733 11.4535 20.8417 12.2836 21.1113C13.1138 21.3809 14.0038 21.4434 14.877 21.2934C15.7503 21.1435 16.5807 20.7854 17.2981 20.2498C18.0156 19.7142 18.5991 19.0167 19 18.215C19.1333 17.9983 19.2667 17.7483 19.4 17.465M10.114 19.748C10.864 20.065 11.664 20.265 12.5 20.3M12.5 20.3C13.336 20.265 14.136 20.065 14.886 19.748M14.886 19.748C15.636 19.431 16.314 18.9983 16.9 18.465M16.9 18.465C17.486 17.9317 17.964 17.2983 18.3 16.5983M18.3 16.5983C18.636 15.8983 18.814 15.1483 18.8 14.3983M18.8 14.3983C18.786 13.6483 18.586 12.915 18.2 12.2317M18.2 12.2317C17.814 11.5483 17.264 10.9317 16.6 10.415M16.6 10.415C15.936 9.89833 15.186 9.5 14.4 9.25M14.4 9.25C13.614 9 12.814 8.95 12 9M12 9C11.186 8.95 10.386 9 9.6 9.25M9.6 9.25C8.814 9.5 8.064 9.89833 7.4 10.415M7.4 10.415C6.736 10.9317 6.186 11.5483 5.8 12.2317M5.8 12.2317C5.414 12.915 5.214 13.6483 5.2 14.3983M5.2 14.3983C5.186 15.1483 5.364 15.8983 5.7 16.5983M5.7 16.5983C6.036 17.2983 6.514 17.9317 7.1 18.465M7.1 18.465C7.686 18.9983 8.436 19.4317 9.3 19.748M9.3 19.748C10.164 20.065 11.064 20.265 12 20.3M12 20.3C12.936 20.265 13.836 20.065 14.7 19.748M14.7 19.748C15.564 19.4317 16.314 18.9983 16.9 18.465" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <span>Pengaturan</span>
              </router-link>
            </li>
          </ul>
        </nav>
        
        <div class="sidebar-footer">
          <div class="user-info">
            <div class="user-avatar">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M20 21V19C20 16.24 16.42 14 12 14C7.58 14 4 16.24 4 19V21M12 14C14.76 14 17.3 15.2 19 17M12 14C9.24 14 6.7 15.2 5 17M16 7C16 9.21 14.21 11 12 11C9.79 11 8 9.21 8 7C8 4.79 9.79 3 12 3C14.21 3 16 4.79 16 7Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <div class="user-details">
              <span class="user-name">{{ authStore.user?.username || 'User' }}</span>
              <span class="user-role">{{ authStore.user?.role?.name || 'Administrator' }}</span>
            </div>
          </div>
          <button class="logout-button" @click="handleLogout">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M9 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V5C3 4.46957 3.21071 3.96086 3.58579 3.58579C3.96086 3.21071 4.46957 3 5 3H9M16 17L21 12M21 12L16 7M21 12H9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>Keluar</span>
          </button>
        </div>
      </aside>
      
      <!-- Main Content -->
      <main class="main-content">
        <router-view />
      </main>
    </div>
    
    <!-- Login/Non-authenticated pages -->
    <div v-else>
      <router-view />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from './stores/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();

const handleLogout = () => {
  authStore.clearToken();
  router.push('/login');
};
</script>

<style>
/* Global styles */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f8f9fa;
  color: #1e293b;
  overflow-x: hidden;
}

#app {
  height: 100vh;
  width: 100vw;
  display: flex;
}

/* App Layout */
.app-layout {
  display: flex;
  flex: 1;
  height: 100%;
}

/* Sidebar */
.sidebar {
  width: 260px;
  background: linear-gradient(180deg, #6a0000 0%, #3d0000 100%);
  color: white;
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  z-index: 100;
  transition: all 0.3s ease;
}

.sidebar-header {
  padding: 24px 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo svg {
  color: #ff6b6b;
}

.logo-text {
  font-size: 20px;
  font-weight: 700;
  letter-spacing: -0.5px;
}

.sidebar-nav {
  flex: 1;
  padding: 24px 0;
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
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  font-size: 16px;
  font-weight: 500;
  transition: all 0.2s ease;
  border-left: 3px solid transparent;
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border-left-color: rgba(255, 255, 255, 0.3);
}

.nav-link.active {
  background: rgba(255, 255, 255, 0.15);
  color: white;
  border-left-color: #ff6b6b;
}

.nav-link svg {
  flex-shrink: 0;
}

.sidebar-footer {
  padding: 24px 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-details {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-weight: 600;
  font-size: 15px;
}

.user-role {
  font-size: 13px;
  opacity: 0.7;
}

.logout-button {
  width: 100%;
  background: rgba(255, 255, 255, 0.1);
  border: none;
  border-radius: 8px;
  padding: 12px 16px;
  color: rgba(255, 255, 255, 0.9);
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.logout-button:hover {
  background: rgba(255, 255, 255, 0.2);
  color: white;
}

/* Main Content */
.main-content {
  flex: 1;
  height: 100%;
  overflow-y: auto;
  background: #f8f9fa;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .sidebar {
    width: 80px;
  }
  
  .logo-text,
  .nav-link span,
  .user-name,
  .user-role,
  .logout-button span {
    display: none;
  }
  
  .logo {
    justify-content: center;
  }
  
  .nav-link {
    justify-content: center;
    padding: 16px;
  }
  
  .user-info {
    justify-content: center;
  }
  
  .user-avatar {
    margin-bottom: 0;
  }
  
  .sidebar-footer {
    padding: 24px 8px;
  }
  
  .logout-button {
    justify-content: center;
    padding: 12px;
  }
}

@media (max-width: 768px) {
  .app-layout {
    flex-direction: column;
  }
  
  .sidebar {
    width: 100%;
    height: 60px;
    flex-direction: row;
    position: fixed;
    bottom: 0;
    left: 0;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    border-bottom: none;
    padding: 0 20px;
  }
  
  .sidebar-header {
    display: none;
  }
  
  .sidebar-nav {
    padding: 0;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .nav-list {
    display: flex;
    gap: 20px;
  }
  
  .nav-item {
    margin: 0;
  }
  
  .nav-link {
    padding: 16px 12px;
    border-left: none;
    border-top: 3px solid transparent;
  }
  
  .nav-link.active {
    border-left: none;
    border-top-color: #ff6b6b;
  }
  
  .sidebar-footer {
    display: none;
  }
  
  .main-content {
    margin-bottom: 60px;
    padding-bottom: 20px;
  }
}
</style>
