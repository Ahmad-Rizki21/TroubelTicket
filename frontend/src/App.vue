<template>
  <div id="app">
    <div v-if="authStore.isAuthenticated && !$route.meta.hideSidebar" class="app-layout">
      <!-- Sidebar Navigation -->
      <aside class="sidebar">
        <div class="sidebar-header">
          <div class="logo">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM12 6V12L16 14" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span class="logo-text">{{ settingsStore.siteName }}</span>
          </div>
        </div>

        <nav class="sidebar-nav">
          <ul class="nav-list">
            <template v-for="(item, index) in navigationMenu" :key="index">
              <!-- Category Header -->
              <li v-if="item.isHeader" class="nav-header">
                <span>{{ item.title }}</span>
              </li>

              <!-- Menu Item -->
              <li v-else class="nav-item">
                <router-link :to="item.to" class="nav-link" :class="{ 'is-child': item.isChild }" active-class="active">
                  <component :is="item.icon" class="nav-icon" />
                  <span>{{ item.title }}</span>
                </router-link>
              </li>
            </template>
          </ul>
        </nav>

        <div class="sidebar-footer">
          <div class="user-info">
            <div class="user-avatar">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M20 21V19C20 16.24 16.42 14 12 14C7.58 14 4 16.24 4 19V21M12 14C14.76 14 17.3 15.2 19 17M12 14C9.24 14 6.7 15.2 5 17M16 7C16 9.21 14.21 11 12 11C9.79 11 8 9.21 8 7C8 4.79 9.79 3 12 3C14.21 3 16 4.79 16 7Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </div>
            <div class="user-details">
              <span class="user-name">{{ authStore.user?.username || 'User' }}</span>
              <span class="user-role">{{ authStore.user?.role?.name || 'Administrator' }}</span>
            </div>
          </div>
          <button class="logout-button" @click="handleLogout">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M9 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V5C3 4.46957 3.21071 3.96086 3.58579 3.58579C3.96086 3.21071 4.46957 3 5 3H9M16 17L21 12M21 12L16 7M21 12H9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
            <span>Logout</span>
          </button>
        </div>
      </aside>

      <main class="main-content">
        <router-view />
        <footer class="app-footer">
          <p>&copy; 2025 PT. Artacomindo Jejaring Nusa. All Rights Reserved.</p>
        </footer>
      </main>
    </div>

    <div v-else>
      <router-view />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from './stores/auth';
import { useSettingsStore } from './stores/settings';
import { useRouter } from 'vue-router';
import { onMounted, markRaw, computed } from 'vue';

// Import Icon Components
import DashboardIcon from './components/icons/DashboardIcon.vue';
import TiketIcon from './components/icons/TiketIcon.vue';
import LaporanChildIcon from './components/icons/LaporanChildIcon.vue';
import RemoteIcon from './components/icons/RemoteIcon.vue';
import UserIcon from './components/icons/UserIcon.vue';
import PeranIcon from './components/icons/PeranIcon.vue';
import PengaturanIcon from './components/icons/PengaturanIcon.vue';

// --- STORES & ROUTER ---
const authStore = useAuthStore();
const settingsStore = useSettingsStore();
const router = useRouter();

// --- TYPES ---
type NavItem = {
  title: string;
  isHeader?: false;
  to: string;
  icon: any;
  isChild?: boolean;
};

type NavHeader = {
  title: string;
  isHeader: true;
};

type NavigationMenuItem = NavItem | NavHeader;

// --- PERMISSION-BASED NAVIGATION MENU ---
const navigationMenu = computed(() => {
  const allNavigationItems: NavigationMenuItem[] = [
    { title: 'Dashboard', to: '/dashboard', icon: markRaw(DashboardIcon) },
    { title: 'Reports', isHeader: true },
    { title: 'Tickets', to: '/tickets', icon: markRaw(TiketIcon), isChild: true },
    { title: 'Reports', to: '/reports', icon: markRaw(LaporanChildIcon), isChild: true },
    { title: 'Services', isHeader: true },
    { title: 'Remote', to: '/remotes', icon: markRaw(RemoteIcon), isChild: true },
    { title: 'System', isHeader: true },
    { title: 'Users', to: '/users', icon: markRaw(UserIcon), isChild: true },
    { title: 'Roles & Permissions', to: '/roles-permissions', icon: markRaw(PeranIcon), isChild: true },
    { title: 'Settings', to: '/settings', icon: markRaw(PengaturanIcon), isChild: true },
  ];
  
  // Define permissions required for each route
  const routePermissions: Record<string, string[]> = {
    '/users': ['user:read'],
    '/roles-permissions': ['role:read', 'permission:read'],
    '/tickets': ['ticket:read'],
    '/reports': ['report:read'],
    '/remotes': ['remote:read'],
    '/settings': ['settings:read']
  };

  // Filter navigation items based on user permissions
  if (!authStore.isAuthenticated || !authStore.user) {
    return allNavigationItems;
  }
  
  return allNavigationItems.filter(item => {
    if ('isHeader' in item && item.isHeader) {
      return true; // Always show headers
    }
    
    if (!('to' in item)) {
      return true; // If no 'to' property (not a route), show it
    }
    
    const requiredPermissions = routePermissions[item.to];
    if (!requiredPermissions || requiredPermissions.length === 0) {
      return true; // If no specific permissions required, show it
    }
    
    // Check if user has all the required permissions
    return requiredPermissions.every(permission => authStore.hasPermission(permission));
  });
});

// --- LOGOUT & AUTH ---
const handleLogout = () => {
  authStore.clearToken();
  router.push('/login');
};

onMounted(() => {
  if (authStore.isAuthenticated) {
    authStore.fetchUser();
  }
});
</script>

<style>
/* Global styles */
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f8f9fa; color: #1e293b; overflow-x: hidden; }
#app { height: 100vh; width: 100vw; display: flex; }

/* App Layout */
.app-layout { display: flex; flex: 1; height: 100%; }

/* Sidebar */
.sidebar { width: 260px; background: linear-gradient(180deg, #6a0000 0%, #3d0000 100%); color: white; display: flex; flex-direction: column; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06); z-index: 100; transition: all 0.3s ease; }
.sidebar-header { padding: 24px 20px; border-bottom: 1px solid rgba(255, 255, 255, 0.1); }
.logo { display: flex; align-items: center; gap: 12px; }
.logo svg { color: #ff6b6b; }
.logo-text { font-size: 20px; font-weight: 700; letter-spacing: -0.5px; }

.sidebar-nav { flex: 1; padding: 16px 0; overflow-y: auto; }
.nav-list { list-style: none; }

.nav-header {
    padding: 20px 24px 8px 24px;
    font-size: 12px;
    font-weight: 700;
    color: rgba(255, 255, 255, 0.6);
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.nav-item .nav-link {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px 24px;
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  font-size: 15px;
  font-weight: 500;
  transition: all 0.2s ease;
  border-left: 3px solid transparent;
  margin: 2px 12px;
  border-radius: 8px;
}

.nav-link.is-child {
    padding-left: 24px;
}

.nav-link:hover { background: rgba(255, 255, 255, 0.1); color: white; }
.nav-link.active { background: rgba(255, 255, 255, 0.2); color: white; border-left-color: #ff6b6b; font-weight: 600; }
.nav-icon { flex-shrink: 0; width: 20px; height: 20px; }

.sidebar-footer { padding: 24px 20px; border-top: 1px solid rgba(250, 250, 250, 0.1); }
.user-info { display: flex; align-items: center; gap: 12px; margin-bottom: 20px; }
.user-avatar { width: 40px; height: 40px; border-radius: 50%; background: rgba(255, 255, 255, 0.1); display: flex; align-items: center; justify-content: center; }
.user-details { display: flex; flex-direction: column; }
.user-name { font-weight: 600; font-size: 15px; }
.user-role { font-size: 13px; opacity: 0.7; }
.logout-button { width: 100%; background: rgba(255, 255, 255, 0.1); border: none; border-radius: 8px; padding: 12px 16px; color: rgba(255, 255, 255, 0.9); display: flex; align-items: center; gap: 12px; font-size: 15px; font-weight: 500; cursor: pointer; transition: all 0.2s ease; }
.logout-button:hover { background: rgba(255, 255, 255, 0.2); color: white; }

/* Main Content */
.main-content { flex: 1; height: 100%; overflow-y: auto; background: #f8f9fa; display: flex; flex-direction: column; }

/* Footer Credit */
.app-footer { background: linear-gradient(180deg, #6a0000 0%, #3d0000 100%); color: white; text-align: center; padding: 15px 20px; margin-top: auto; font-size: 0.875rem; border-top: 1px solid rgba(255, 255, 255, 0.2); }
.app-footer p { margin: 0; color: #ffffff !important; font-weight: 600; text-shadow: 0 1px 2px rgba(0,0,0,0.1); }

/* Responsive Design */
@media (max-width: 1024px) {
  .sidebar { width: 80px; }
  .logo-text, .nav-link span, .user-name, .user-role, .logout-button span, .nav-header { display: none; }
  .logo { justify-content: center; }
  .nav-link { justify-content: center; padding: 16px; margin: 0 8px; }
  .nav-link.is-child { padding-left: 16px; }
  .user-info { justify-content: center; }
  .user-avatar { margin-bottom: 0; }
  .sidebar-footer { padding: 24px 8px; }
  .logout-button { justify-content: center; padding: 12px; }
}

@media (max-width: 768px) {
  .app-layout { flex-direction: column; }
  .sidebar { width: 100%; height: 60px; flex-direction: row; position: fixed; bottom: 0; left: 0; border-top: 1px solid rgba(255, 255, 255, 0.1); border-bottom: none; padding: 0 20px; }
  .sidebar-header, .sidebar-footer, .nav-header { display: none; }
  .sidebar-nav { padding: 0; display: flex; align-items: center; justify-content: center; }
  .nav-list { display: flex; gap: 20px; }
  .nav-item { margin: 0; }
  .nav-link { padding: 16px 12px; border-left: none; border-top: 3px solid transparent; margin: 0; }
  .nav-link.active { border-left: none; border-top-color: #ff6b6b; }
  .main-content { margin-bottom: 60px; padding-bottom: 20px; }
}

/* Footer */
.app-footer { background: linear-gradient(180deg, #6a0000 0%, #3d0000 100%); color: white; text-align: center; padding: 15px 20px; margin-top: auto; font-size: 0.875rem; }
.app-footer p { margin: 0; opacity: 0.8; }
</style>
