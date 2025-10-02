import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import Login from '../views/Login.vue';
import Dashboard from '../views/Dashboard.vue';
import ResetPassword from '../views/ResetPassword.vue';
import ChangePassword from '../views/ChangePassword.vue';
import SimplePasswordReset from '../views/SimplePasswordReset.vue';
import Tickets from '../views/Tickets.vue';
import CreateTicket from '../views/CreateTicket.vue';
import Reports from '../views/Reports.vue';
import Settings from '../views/Settings.vue';
import ActionTakenView from '../views/ActionTakenView.vue';
import AddRemoteView from '../views/AddRemoteView.vue';
import EditRemoteView from '../views/EditRemoteView.vue';

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
  },
  {
    path: '/reset-password',
    name: 'ResetPassword',
    component: ResetPassword,
  },
  {
    path: '/reset-password/:token',
    name: 'ResetPasswordWithToken',
    component: ResetPassword,
    props: true
  },
  {
    path: '/change-password',
    name: 'ChangePassword',
    component: ChangePassword,
  },
  {
    path: '/simple-reset-password',
    name: 'SimplePasswordReset',
    component: SimplePasswordReset,
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
  },
  {
    path: '/tickets',
    name: 'Tickets',
    component: Tickets,
    meta: { requiresAuth: true, permissions: ['ticket:read'] }
  },
  {
    path: '/tickets/create',
    name: 'CreateTicket',
    component: CreateTicket,
    meta: { requiresAuth: true, permissions: ['ticket:create'] }
  },
  {
    path: '/reports',
    name: 'Reports',
    component: Reports,
    meta: { requiresAuth: true, permissions: ['report:read'] }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Settings,
    meta: { requiresAuth: true, permissions: ['settings:read'] }
  },
  {
    path: '/tickets/:id/action-taken',
    name: 'ActionTaken',
    component: ActionTakenView,
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/users',
    name: 'Users',
    component: () => import('../views/UsersView.vue'), // Lazy load
    meta: { requiresAuth: true, permissions: ['user:read'] }
  },
  {
    path: '/roles-permissions',
    name: 'RolesAndPermissions',
    component: () => import('../views/RolesPermissionsView.vue'), // Lazy load
    meta: { requiresAuth: true, permissions: ['role:read', 'permission:read'] }
  },
  {
    path: '/remotes',
    name: 'Remotes',
    component: () => import('../views/RemotesView.vue'), // Lazy load
    meta: { requiresAuth: true, permissions: ['remote:read'] }
  },
  {
    path: '/remotes/add',
    name: 'AddRemote',
    component: AddRemoteView,
    meta: { requiresAuth: true, permissions: ['remote:create'] }
  },
  {
    path: '/remotes/:id/edit',
    name: 'EditRemote',
    component: EditRemoteView,
    props: true,
    meta: { requiresAuth: true, permissions: ['remote:update'] }
  },
  {
    path: '/',
    redirect: '/login',
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Global navigation guard
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  
  // Check authentication
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login');
    return;
  }
  
  // Check permissions if route requires specific permissions
  if (to.meta.permissions && to.meta.permissions.length > 0) {
    if (!authStore.isAuthenticated || !authStore.user) {
      next('/login');
      return;
    }
    
    // Check if user has all required permissions
    const requiredPermissions = to.meta.permissions as string[];
    const hasAllPermissions = requiredPermissions.every(permission => 
      authStore.hasPermission(permission)
    );
    
    if (!hasAllPermissions) {
      // Redirect to dashboard or show error page if user doesn't have required permissions
      alert(`You don't have required permissions to access this page. Required: ${requiredPermissions.join(', ')}`);
      next('/dashboard'); // Redirect to dashboard as fallback
      return;
    }
  }
  
  next();
});

export default router;