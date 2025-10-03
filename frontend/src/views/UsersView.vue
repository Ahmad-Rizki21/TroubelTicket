<template>
  <div class="users-page">
    <header class="page-header">
      <div class="header-content">
        <div class="title-section">
          <h1 class="page-title">
            <span class="title-gradient">User Management</span>
          </h1>
          <p class="page-subtitle">Add, edit, and manage user accounts here.</p>
        </div>
        <div class="header-stats">
          <div class="live-indicator">
            <div class="live-dot"></div>
            <span>Live</span>
          </div>
          <div class="header-actions">
            <button class="primary-button" @click="openCreateModal">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 5V19M5 12H19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <span>Add User</span>
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Filters and Search Section -->
    <div class="card filters-card">
      <div class="search-box">
        <svg class="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M21 21L15 15M17 10C17 13.866 13.866 17 10 17C6.13401 17 3 13.866 3 10C3 6.13401 6.13401 3 10 3C13.866 3 17 6.13401 17 10Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <input 
          type="text" 
          placeholder="Search by name, username..." 
          class="search-input"
          v-model="searchQuery"
          @input="applyFilters"
        >
      </div>
      
      <div class="filters">
        <select class="filter-select" v-model="roleFilter" @change="applyFilters">
          <option value="">All Roles</option>
          <option v-for="role in roles" :key="role.id" :value="role.name">{{ role.name }}</option>
        </select>
      </div>
    </div>

    <!-- Users Table -->
    <div class="card users-table-card">
      <div class="table-responsive">
        <table class="users-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Username</th>
              <th>Role</th>
              <th>Status</th>
              <th>Created At</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="paginatedUsers.length === 0">
              <td colspan="6" class="empty-state">
                <p>No users found.</p>
              </td>
            </tr>
            <tr v-for="user in paginatedUsers" :key="user.id">
              <td class="user-id">#{{ user.id }}</td>
              <td>
                <div class="user-name">{{ user.username }}</div>
                <!-- Assuming email is not directly in User schema, or can be added later -->
                <!-- <div class="user-email">{{ user.email }}</div> -->
              </td>
              <td>
                <span class="role-badge" :style="getRoleStyle(user.role.name)">{{ user.role.name }}</span>
              </td>
              <td>
                <span class="status-badge status-active">Active</span> <!-- Placeholder for status -->
              </td>
              <td>{{ formatDate(user.created_at) }}</td>
              <td>
                <div class="action-buttons">
                  <button class="action-button edit" @click="openEditModal(user)" title="Edit User">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M11 4H4C3.46957 4 2.96086 4.21071 2.58579 4.58579C2.21071 4.96086 2 5.46957 2 6V20C2 20.5304 2.21071 21.0391 2.58579 21.4142C2.96086 21.7893 3.46957 22 4 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V13M18.5 2.5L21.5 5.5M17.5 1.5L9 10V13H12L20.5 4.5L17.5 1.5Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                  </button>
                  <button class="action-button delete" @click="confirmDelete(user)" title="Delete User">
                   <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3 6H5H21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M8 6V4C8 3.46957 8.21071 2.96086 8.58579 2.58579C8.96086 2.21071 9.46957 2 10 2H14C14.5304 2 15.0391 2.21071 15.4142 2.58579C15.7893 2.96086 16 2.96957 16 3.5V6M19 6V20C19 20.5304 18.7893 21.0391 18.4142 21.4142C18.0391 21.7893 17.5304 22 17 22H7C6.46957 22 5.96086 21.7893 5.58579 21.4142C5.21071 21.0391 5 20.5304 5 20V6H19Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M10 11V17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M14 11V17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <!-- Pagination -->
      <div class="pagination">
        <button class="pagination-button" :disabled="currentPage === 1" @click="prevPage">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M15 18L9 12L15 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span>Previous</span>
        </button>
        <span class="pagination-info">Page {{ currentPage }} of {{ totalPages }}</span>
        <button class="pagination-button" :disabled="currentPage === totalPages" @click="nextPage">
          <span>Next</span>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M9 18L15 12L9 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
      </div>
    </div>
  </div>

  <!-- Create/Edit User Modal -->
  <transition name="modal-fade">
    <div v-if="showCreateEditModal" class="modal-overlay" @click="closeCreateEditModal">
      <div v-if="currentUser" class="modal-content" @click.stop>
        <div class="modal-header">
          <h2 class="modal-title">{{ isEditing ? 'Edit User' : 'Add User' }}</h2>
          <button class="close-button" @click="closeCreateEditModal">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
        </div>
        <form @submit.prevent="saveUser" class="modal-form">
          <div class="form-group">
            <label for="username">Username</label>
            <input type="text" id="username" v-model="currentUser.username" required>
          </div>
          <div class="form-group" v-if="!isEditing">
            <label for="password">Password</label>
            <input type="password" id="password" v-model="currentUser.password" required>
          </div>
          <div class="form-group">
            <label for="role">Role</label>
            <select id="role" v-model="currentUser.role_id" required>
              <option v-for="role in roles" :key="role.id" :value="role.id">{{ role.name }}</option>
            </select>
          </div>
          <div class="modal-actions">
            <button type="button" class="secondary-button" @click="closeCreateEditModal">Cancel</button>
            <button type="submit" class="primary-button">{{ isEditing ? 'Save Changes' : 'Add User' }}</button>
          </div>
        </form>
      </div>
    </div>
  </transition>

  <!-- Delete Confirmation Modal -->
  <transition name="modal-fade">
    <div v-if="showDeleteModal" class="modal-overlay" @click="closeDeleteModal">
      <div class="modal-content confirmation-modal" @click.stop>
        <div class="modal-header">
          <h2 class="modal-title">Confirm User Deletion</h2>
        </div>
        <div class="modal-body">
          <p v-if="userToDelete">
            Are you sure you want to delete the user <strong>{{ userToDelete.username }}</strong>?
          </p>
          <p class="warning-text">This action cannot be undone.</p>
        </div>
        <div class="modal-actions">
          <button type="button" class="secondary-button" @click="closeDeleteModal">Cancel</button>
          <button type="button" class="primary-button delete-confirm-button" @click="deleteUser">Yes, Delete</button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue';
import type { User, UserCreate, UserUpdate } from '../api/userAPI';
import { userAPI } from '../api/userAPI';
import { roleAPI } from '../api/roleAPI';
import type { Role } from '../api/roleAPI';

// Extend User interface for form handling, including password for creation
interface UserForm extends User {
  password?: string;
}

// State management
const allUsers = ref<User[]>([]);
const filteredUsers = ref<User[]>([]);
const roles = ref<Role[]>([]);
const searchQuery = ref('');
const roleFilter = ref('');
const currentPage = ref(1);
const itemsPerPage = ref(10);
const loading = ref(false);

const showCreateEditModal = ref(false);
const isEditing = ref(false);
const currentUser = ref<UserForm | null>(null);

const showDeleteModal = ref(false);
const userToDelete = ref<User | null>(null);

// Computed properties
const totalPages = computed(() => Math.ceil(filteredUsers.value.length / itemsPerPage.value));
const paginatedUsers = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value;
  const end = start + itemsPerPage.value;
  return filteredUsers.value.slice(start, end);
});

// Methods
const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('id-ID', {
    day: '2-digit',
    month: 'short',
    year: 'numeric'
  });
};

// Fungsi untuk mendapatkan style berdasarkan nama role
const getRoleStyle = (roleName: string) => {
  // Jika nama role cocok dengan kelas yang sudah ada, gunakan style yang ditentukan
  const existingStyles: Record<string, [string, string]> = {
    'admin': ['#dbeafe', '#1d4ed8'],
    'teknisi': ['#fffbeb', '#b45309'],
    'user': ['#ecfdf5', '#047857']
  };
  
  const normalizedRoleName = roleName.toLowerCase();
  
  if (existingStyles[normalizedRoleName]) {
    const [bgColor, textColor] = existingStyles[normalizedRoleName];
    return {
      backgroundColor: bgColor,
      color: textColor
    };
  }
  
  // Jika tidak ada, buat warna berdasarkan hash nama role
  const hue = generateHueFromName(roleName);
  const bgColor = `hsl(${hue}, 70%, 90%)`;
  const textColor = `hsl(${hue}, 70%, 25%)`;
  
  return {
    backgroundColor: bgColor,
    color: textColor
  };
};

// Fungsi untuk membuat hue berdasarkan nama role untuk warna yang konsisten
const generateHueFromName = (name: string): number => {
  let hash = 0;
  for (let i = 0; i < name.length; i++) {
    hash = name.charCodeAt(i) + ((hash << 5) - hash);
  }
  return Math.abs(hash) % 360; // Nilai hue antara 0-360
};

const loadUsers = async () => {
  loading.value = true;
  try {
    const usersResponse = await userAPI.getAllUsers();
    allUsers.value = usersResponse.data;
    
    const rolesResponse = await roleAPI.getAllRoles();
    roles.value = rolesResponse.data;
    
    applyFilters();
  } catch (error) {
    console.error('Error loading users or roles:', error);
  } finally {
    loading.value = false;
  }
};

const applyFilters = () => {
  let tempUsers = [...allUsers.value];

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    tempUsers = tempUsers.filter(user => 
      user.username.toLowerCase().includes(query) ||
      user.role.name.toLowerCase().includes(query)
    );
  }

  if (roleFilter.value) {
    tempUsers = tempUsers.filter(user => user.role.name === roleFilter.value);
  }

  filteredUsers.value = tempUsers;
  currentPage.value = 1; // Reset to first page on filter change
};

const openCreateModal = () => {
  isEditing.value = false;
  currentUser.value = { 
    id: 0, 
    username: '', 
    password: '', // Initialize password for new user
    role_id: roles.value[0]?.id || 0, 
    created_at: new Date().toISOString(), 
    role: roles.value[0] || { id: 0, name: '' } 
  };
  showCreateEditModal.value = true;
};

const openEditModal = (user: User) => {
  isEditing.value = true;
  currentUser.value = { ...user }; // No password needed for editing
  showCreateEditModal.value = true;
};

const closeCreateEditModal = () => {
  showCreateEditModal.value = false;
  currentUser.value = null;
};

const saveUser = async () => {
  if (!currentUser.value) return;

  try {
    if (isEditing.value) {
      const userData: UserUpdate = { 
        username: currentUser.value.username, 
        role_id: currentUser.value.role_id 
      };
      await userAPI.updateUser(currentUser.value.id, userData);
    } else {
      const userData: UserCreate = { 
        username: currentUser.value.username, 
        password: currentUser.value.password || '', // Ensure password is provided for creation
        role_id: currentUser.value.role_id 
      };
      await userAPI.createUser(userData);
    }
    await loadUsers();
    closeCreateEditModal();
  } catch (error) {
    console.error('Error saving user:', error);
  }
};

const confirmDelete = (user: User) => {
  userToDelete.value = user;
  showDeleteModal.value = true;
};

const deleteUser = async () => {
  if (!userToDelete.value) return;
  try {
    await userAPI.deleteUser(userToDelete.value.id);
    await loadUsers();
  } catch (error) {
    console.error('Error deleting user:', error);
  } finally {
    closeDeleteModal();
  }
};

const closeDeleteModal = () => {
  showDeleteModal.value = false;
  userToDelete.value = null;
};

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
  }
};

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
  }
};

// Lifecycle hooks
onMounted(async () => {
  await loadUsers();
});

// Watch for filter changes
watch([searchQuery, roleFilter], () => {
  applyFilters();
});
</script>

<style scoped>
.users-page {
  background-color: #f8fafc;
  padding: 2rem;
  font-family: 'Inter', sans-serif;
  width: 100%;
  box-sizing: border-box;
}

.card {
  background-color: #ffffff;
  border-radius: 16px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  border: 1px solid #e2e8f0;
  margin-bottom: 1.5rem;
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

.header-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

/* Buttons */
.primary-button {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #800000 0%, #5c0000 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}
.primary-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(128, 0, 0, 0.3);
}

/* Filters */
.filters-card {
  display: flex;
  padding: 1.5rem;
  gap: 1.5rem;
  flex-wrap: wrap;
}
.search-box {
  position: relative;
  flex-grow: 1;
}
.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #64748b;
}
.search-input, .filter-select {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 2.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  font-size: 1rem;
  color: #1e293b;
  background-color: #f8fafc;
  transition: all 0.3s ease;
  box-sizing: border-box;
}
.search-input:focus, .filter-select:focus {
  outline: none;
  border-color: #800000;
  box-shadow: 0 0 0 3px rgba(128, 0, 0, 0.1);
  background-color: #ffffff;
}
.filters {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}
.filter-select {
  padding: 0.75rem 1rem;
  min-width: 180px;
}

/* Table */
.users-table-card {
  overflow: hidden;
}
.table-responsive {
  overflow-x: auto;
}
.users-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}
.users-table th, .users-table td {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}
.users-table th {
  font-size: 0.875rem;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  background-color: #f8fafc;
}
.users-table tr:last-child td {
  border-bottom: none;
}
.user-id {
  font-weight: 600;
  color: #3b82f6;
}
.user-name {
  font-weight: 600;
  color: #1e293b;
}
.user-email {
  font-size: 0.875rem;
  color: #64748b;
  margin-top: 0.25rem;
}

/* Badges */
.role-badge, .status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  display: inline-block;
}

/* Role badges yang sudah didefinisikan secara spesifik tetap menggunakan inline style */
.role-admin { background-color: #dbeafe; color: #1d4ed8; }
.role-teknisi { background-color: #fffbeb; color: #b45309; }
.role-user { background-color: #ecfdf5; color: #047857; }

/* Status badges */
.status-active { background-color: #d1fae5; color: #059669; }
.status-inactive { background-color: #fee2e2; color: #dc2626; }

/* Actions */
.action-buttons {
  display: flex;
  gap: 0.5rem;
}
.action-button {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background: transparent;
  border: 1px solid transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s ease;
}
.action-button:hover {
  background-color: #f1f5f9;
  color: #1e293b;
}
.action-button.view:hover { color: #800000; }
.action-button.edit:hover { color: #f59e0b; }
.action-button.delete:hover { color: #ef4444; }

/* Empty State */
.empty-state {
  text-align: center;
  padding: 4rem;
  color: #64748b;
}

/* Pagination */
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}
.pagination-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background: #ffffff;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s ease;
}
.pagination-button:hover:not(:disabled) {
  border-color: #800000;
  color: #800000;
}
.pagination-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.pagination-info {
  font-size: 1rem;
  font-weight: 500;
  color: #1e293b;
}

/* Modal Styles */
.modal-fade-enter-active, .modal-fade-leave-active {
  transition: opacity 0.3s ease;
}
.modal-fade-enter-from, .modal-fade-leave-to {
  opacity: 0;
}
.modal-fade-enter-active .modal-content, .modal-fade-leave-active .modal-content {
  transition: all 0.3s ease;
}
.modal-fade-enter-from .modal-content, .modal-fade-leave-to .modal-content {
  opacity: 0;
  transform: translateY(-20px);
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(17, 24, 39, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(5px);
}
.modal-content {
  background-color: #f8fafc;
  border-radius: 20px;
  width: 100%;
  max-width: 600px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1), 0 10px 10px -5px rgba(0,0,0,0.04);
}
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  background-color: #1f2937;
  color: #fff;
  border-top-left-radius: 20px;
  border-top-right-radius: 20px;
}
.modal-title {
  font-size: 1.25rem;
  font-weight: 600;
}
.close-button {
  background: transparent;
  border: none;
  color: #9ca3af;
  cursor: pointer;
  padding: 0.5rem;
}
.close-button:hover {
  color: #fff;
}
.modal-form, .user-detail {
  padding: 2rem;
  overflow-y: auto;
  background-color: #ffffff;
}
.form-group {
  margin-bottom: 1.5rem;
}
.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}
.form-group label {
  display: block;
  font-size: 0.875rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 0.5rem;
}
.form-group input, .form-group textarea, .form-group select {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background-color: #f8fafc;
  box-sizing: border-box;
}
.form-group input:focus, .form-group textarea:focus, .form-group select:focus {
  outline: none;
  border-color: #800000;
  box-shadow: 0 0 0 3px rgba(128, 0, 0, 0.1);
  background-color: #ffffff;
}
.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding: 1.5rem 2rem;
  border-top: 1px solid #e2e8f0;
  background-color: #f8fafc;
  border-bottom-left-radius: 20px;
  border-bottom-right-radius: 20px;
}

/* Detail Modal */
.detail-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid #e2e8f0;
    margin-bottom: 1.5rem;
}
.detail-grid:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}
.detail-item {
    display: flex;
    flex-direction: column;
}
.detail-item.description {
    grid-column: 1 / -1;
}
.detail-label {
    font-size: 0.875rem;
    font-weight: 600;
    color: #64748b;
    margin-bottom: 0.5rem;
}
.detail-value {
    font-size: 1rem;
    color: #1e293b;
    line-height: 1.6;
}

/* Responsive */
@media (max-width: 768px) {
  .users-page {
    padding: 1rem;
  }
  .page-header {
    flex-direction: column;
    align-items: flex-start;
  }
  .filters-card {
    flex-direction: column;
  }
  .form-row {
    grid-template-columns: 1fr;
  }
  .users-table th:nth-child(4), .users-table td:nth-child(4) {
      display: none; /* Hide date on smaller screens */
  }
}
@media (max-width: 480px) {
  .page-title {
    font-size: 1.75rem;
  }
  .modal-content {
      margin: 1rem;
      max-height: calc(100vh - 2rem);
  }
  .modal-form, .user-detail {
    padding: 1.5rem;
  }
}
</style>