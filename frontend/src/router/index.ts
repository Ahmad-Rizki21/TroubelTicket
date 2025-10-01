import { createRouter, createWebHistory } from 'vue-router';
import Login from '../views/Login.vue';
import Dashboard from '../views/Dashboard.vue';
import ResetPassword from '../views/ResetPassword.vue';
import ChangePassword from '../views/ChangePassword.vue';
import SimplePasswordReset from '../views/SimplePasswordReset.vue';
import Tickets from '../views/Tickets.vue';
import Reports from '../views/Reports.vue';
import Settings from '../views/Settings.vue';

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
  },
  {
    path: '/reports',
    name: 'Reports',
    component: Reports,
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Settings,
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
    path: '/',
    redirect: '/login',
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
