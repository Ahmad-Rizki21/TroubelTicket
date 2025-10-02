<template>
  <div class="roles-permissions-page">
    <header class="page-header">
      <div class="header-content">
        <div class="title-section">
          <h1 class="page-title">
            <span class="title-gradient">Manajemen Peran & Izin</span>
          </h1>
          <p class="page-subtitle">Atur peran pengguna dan izin akses sistem.</p>
        </div>
        <div class="header-stats">
          <div class="live-indicator">
            <div class="live-dot"></div>
            <span>Live</span>
          </div>
          <div class="header-actions">
            <button class="primary-button" @click="openCreateRoleModal">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 5V19M5 12H19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <span>Tambah Peran</span>
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Tabs for Roles and Permissions -->
    <div class="tabs">
      <button 
        :class="['tab-button', { active: activeTab === 'roles' }]" 
        @click="activeTab = 'roles'"
      >
        Peran (Roles)
      </button>
      <button 
        :class="['tab-button', { active: activeTab === 'permissions' }]" 
        @click="activeTab = 'permissions'"
      >
        Izin (Permissions)
      </button>
    </div>

    <!-- Roles Tab -->
    <div v-if="activeTab === 'roles'" class="tab-content">
      <div class="card roles-card">
        <div class="table-responsive">
          <table class="roles-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Nama Peran</th>
                <th>Izin Terkait</th>
                <th>Aksi</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="roles.length === 0">
                <td colspan="4" class="empty-state">Tidak ada peran yang ditemukan.</td>
              </tr>
              <tr v-for="role in roles" :key="role.id">
                <td class="role-id">#{{ role.id }}</td>
                <td class="role-name">{{ role.name }}</td>
                <td>
                  <div class="permissions-list">
                    <span v-for="permission in role.permissions.slice(0, 5)" :key="permission.id" class="permission-tag" :title="permission.name">{{ permission.name }}</span>
                    <span v-if="role.permissions.length > 5" class="permission-tag more" title="Dan lainnya">+{{ role.permissions.length - 5 }}</span>
                  </div>
                </td>
                <td>
                  <div class="action-buttons">
                    <button class="action-button edit" @click="openEditRoleModal(role)" title="Edit Peran">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M11 4H4C3.46957 4 2.96086 4.21071 2.58579 4.58579C2.21071 4.96086 2 5.46957 2 6V20C2 20.5304 2.21071 21.0391 2.58579 21.4142C2.96086 21.7893 3.46957 22 4 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V13M18.5 2.5L21.5 5.5M17.5 1.5L9 10V13H12L20.5 4.5L17.5 1.5Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                    </button>
                    <button class="action-button delete" @click="confirmDeleteRole(role)" title="Hapus Peran">
                     <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3 6H5H21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M8 6V4C8 3.46957 8.21071 2.96086 8.58579 2.58579C8.96086 2.21071 9.46957 2 10 2H14C14.5304 2 15.0391 2.21071 15.4142 2.58579C15.7893 2.96086 16 2.96957 16 3.5V6M19 6V20C19 20.5304 18.7893 21.0391 18.4142 21.4142C18.0391 21.7893 17.5304 22 17 22H7C6.46957 22 5.96086 21.7893 5.58579 21.4142C5.21071 21.0391 5 20.5304 5 20V6H19Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M10 11V17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M14 11V17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Permissions Tab -->
    <div v-if="activeTab === 'permissions'" class="tab-content">
      <div class="card permissions-card">
        <div class="table-responsive">
          <div class="table-actions">
            <button class="primary-button" @click="openCreatePermissionModal">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 5V19M5 12H19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <span>Tambah Izin</span>
            </button>
          </div>
          <table class="permissions-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Nama Izin</th>
                <th>Dibuat Pada</th>
                <th>Aksi</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="permissions.length === 0">
                <td colspan="4" class="empty-state">Tidak ada izin yang ditemukan.</td>
              </tr>
              <tr v-for="permission in permissions" :key="permission.id">
                <td class="permission-id">#{{ permission.id }}</td>
                <td class="permission-name">{{ permission.name }}</td>
                <td>{{ formatDate(permission.created_at) }}</td>
                <td>
                  <div class="action-buttons">
                    <button class="action-button edit" @click="openEditPermissionModal(permission)" title="Edit Izin">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M11 4H4C3.46957 4 2.96086 4.21071 2.58579 4.58579C2.21071 4.96086 2 5.46957 2 6V20C2 20.5304 2.21071 21.0391 2.58579 21.4142C2.96086 21.7893 3.46957 22 4 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V13M18.5 2.5L21.5 5.5M17.5 1.5L9 10V13H12L20.5 4.5L17.5 1.5Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                    </button>
                    <button class="action-button delete" @click="confirmDeletePermission(permission)" title="Hapus Izin">
                     <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3 6H5H21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M8 6V4C8 3.46957 8.21071 2.96086 8.58579 2.58579C8.96086 2.21071 9.46957 2 10 2H14C14.5304 2 15.0391 2.21071 15.4142 2.58579C15.7893 2.96086 16 2.96957 16 3.5V6M19 6V20C19 20.5304 18.7893 21.0391 18.4142 21.4142C18.0391 21.7893 17.5304 22 17 22H7C6.46957 22 5.96086 21.7893 5.58579 21.4142C5.21071 21.0391 5 20.5304 5 20V6H19Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M10 11V17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M14 11V17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>

  <!-- Create/Edit Role Modal -->
  <transition name="modal-fade">
    <div v-if="showRoleModal" class="modal-overlay" @click="closeRoleModal">
      <div v-if="currentRole" class="modal-content" @click.stop>
        <div class="modal-header">
          <h2 class="modal-title">{{ isEditingRole ? 'Edit Peran' : 'Tambah Peran' }}</h2>
          <button class="close-button" @click="closeRoleModal">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
        </div>
        <form @submit.prevent="saveRole" class="modal-form">
          <div class="form-group">
            <label for="roleName">Nama Peran</label>
            <input type="text" id="roleName" v-model="currentRole.name" required>
          </div>
          <div class="form-group">
            <label>Izin</label>
            <div class="permissions-header">
              <button type="button" class="secondary-button small" @click="selectAllPermissions">Pilih Semua</button>
              <button type="button" class="secondary-button small" @click="deselectAllPermissions">Hapus Semua</button>
            </div>
            <div class="permissions-checkbox-group">
              <div v-for="perm in availablePermissions" :key="perm.id" class="checkbox-item">
                <input type="checkbox" :id="`perm-${perm.id}`" :value="perm.id" v-model="selectedPermissions">
                <label :for="`perm-${perm.id}`">{{ perm.name }}</label>
              </div>
            </div>
          </div>
          <div class="modal-actions">
            <button type="button" class="secondary-button" @click="closeRoleModal">Batal</button>
            <button type="submit" class="primary-button">{{ isEditingRole ? 'Simpan Perubahan' : 'Tambah Peran' }}</button>
          </div>
        </form>
      </div>
    </div>
  </transition>

  <!-- Delete Role Confirmation Modal -->
  <transition name="modal-fade">
    <div v-if="showDeleteRoleModal" class="modal-overlay" @click="closeDeleteRoleModal">
      <div class="modal-content confirmation-modal" @click.stop>
        <div class="modal-header">
          <h2 class="modal-title">Konfirmasi Penghapusan Peran</h2>
        </div>
        <div class="modal-body">
          <p v-if="roleToDelete">
            Apakah Anda yakin ingin menghapus peran <strong>{{ roleToDelete.name }}</strong>?
          </p>
          <p class="warning-text">Tindakan ini tidak dapat dibatalkan.</p>
        </div>
        <div class="modal-actions">
          <button type="button" class="secondary-button" @click="closeDeleteRoleModal">Batal</button>
          <button type="button" class="primary-button delete-confirm-button" @click="deleteRole">Ya, Hapus</button>
        </div>
      </div>
    </div>
  </transition>

  <!-- Create/Edit Permission Modal -->
  <transition name="modal-fade">
    <div v-if="showPermissionModal" class="modal-overlay" @click="closePermissionModal">
      <div v-if="currentPermission" class="modal-content" @click.stop>
        <div class="modal-header">
          <h2 class="modal-title">{{ isEditingPermission ? 'Edit Izin' : 'Tambah Izin' }}</h2>
          <button class="close-button" @click="closePermissionModal">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
        </div>
        <form @submit.prevent="savePermission" class="modal-form">
          <div class="form-group">
            <label for="permissionName">Nama Izin</label>
            <input type="text" id="permissionName" v-model="currentPermission.name" required>
          </div>
          <div class="modal-actions">
            <button type="button" class="secondary-button" @click="closePermissionModal">Batal</button>
            <button type="submit" class="primary-button">{{ isEditingPermission ? 'Simpan Perubahan' : 'Tambah Izin' }}</button>
          </div>
        </form>
      </div>
    </div>
  </transition>

  <!-- Delete Permission Confirmation Modal -->
  <transition name="modal-fade">
    <div v-if="showDeletePermissionModal" class="modal-overlay" @click="closeDeletePermissionModal">
      <div class="modal-content confirmation-modal" @click.stop>
        <div class="modal-header">
          <h2 class="modal-title">Konfirmasi Penghapusan Izin</h2>
        </div>
        <div class="modal-body">
          <p v-if="permissionToDelete">
            Apakah Anda yakin ingin menghapus izin <strong>{{ permissionToDelete.name }}</strong>?
          </p>
          <p class="warning-text">Tindakan ini tidak dapat dibatalkan.</p>
        </div>
        <div class="modal-actions">
          <button type="button" class="secondary-button" @click="closeDeletePermissionModal">Batal</button>
          <button type="button" class="primary-button delete-confirm-button" @click="deletePermission">Ya, Hapus</button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { roleAPI, type Role, type RoleCreate } from '../api/roleAPI';
import { permissionAPI, type Permission, type PermissionCreate } from '../api/permissionAPI';

const activeTab = ref('roles');

const roles = ref<Role[]>([]);
const permissions = ref<Permission[]>([]);
const availablePermissions = ref<Permission[]>([]); // All permissions for role assignment

// Role Modals
const showRoleModal = ref(false);
const isEditingRole = ref(false);
const currentRole = ref<RoleCreate | Role | null>(null);
const selectedPermissions = ref<number[]>([]); // For permissions assigned to a role

// Permission Modals
const showPermissionModal = ref(false);
const isEditingPermission = ref(false);
const currentPermission = ref<PermissionCreate | Permission | null>(null);

// Delete Modals
const showDeleteRoleModal = ref(false);
const roleToDelete = ref<Role | null>(null);
const showDeletePermissionModal = ref(false);
const permissionToDelete = ref<Permission | null>(null);

const formatDate = (dateString?: string) => {
  if (!dateString) return '-';
  const date = new Date(dateString);
  return date.toLocaleDateString('id-ID', {
    day: '2-digit',
    month: 'short',
    year: 'numeric'
  });
};

// --- Role Management ---
const loadRoles = async () => {
  try {
    const response = await roleAPI.getAllRoles();
    roles.value = response.data;
  } catch (error) {
    console.error('Error loading roles:', error);
  }
};

const openCreateRoleModal = () => {
  isEditingRole.value = false;
  currentRole.value = { name: '' };
  selectedPermissions.value = [];
  showRoleModal.value = true;
};

const openEditRoleModal = (role: Role) => {
  isEditingRole.value = true;
  currentRole.value = { ...role };
  selectedPermissions.value = role.permissions ? role.permissions.map(p => p.id) : [];
  showRoleModal.value = true;
};

const closeRoleModal = () => {
  showRoleModal.value = false;
  currentRole.value = null;
  selectedPermissions.value = [];
};

const saveRole = async () => {
  if (!currentRole.value) return;

  try {
    let savedRole: Role;
    if (isEditingRole.value && (currentRole.value as Role).id) {
      savedRole = (await roleAPI.updateRole((currentRole.value as Role).id, { name: currentRole.value.name })).data;
    } else {
      savedRole = (await roleAPI.createRole({ name: currentRole.value.name })).data;
    }

    // Update permissions for the role
    // Get the current role with its permissions to compare
    const updatedRole = await roleAPI.getRoleById(savedRole.id);
    const existingPermissions = updatedRole.data.permissions || [];
    const existingPermissionIds = new Set(existingPermissions.map(p => p.id));
    const permissionsToAdd = selectedPermissions.value.filter(id => !existingPermissionIds.has(id));
    const permissionsToRemove = existingPermissions.filter(p => !selectedPermissions.value.includes(p.id)).map(p => p.id);

    for (const permId of permissionsToAdd) {
      await roleAPI.assignPermissionToRole(savedRole.id, permId);
    }
    for (const permId of permissionsToRemove) {
      await roleAPI.removePermissionFromRole(savedRole.id, permId);
    }

    // Perbarui role yang sedang ditampilkan dengan permission terbaru
    await loadRoles();
    closeRoleModal();
  } catch (error) {
    console.error('Error saving role:', error);
  }
};

const confirmDeleteRole = (role: Role) => {
  roleToDelete.value = role;
  showDeleteRoleModal.value = true;
};

const deleteRole = async () => {
  if (!roleToDelete.value) return;
  try {
    await roleAPI.deleteRole(roleToDelete.value.id);
    await loadRoles();
  } catch (error) {
    console.error('Error deleting role:', error);
  } finally {
    closeDeleteRoleModal();
  }
};

const closeDeleteRoleModal = () => {
  showDeleteRoleModal.value = false;
  roleToDelete.value = null;
};

// --- Permission Management ---
const loadPermissions = async () => {
  try {
    const response = await permissionAPI.getAllPermissions();
    permissions.value = response.data;
    availablePermissions.value = response.data; // Also populate available permissions for role assignment
  } catch (error) {
    console.error('Error loading permissions:', error);
  }
};

const openCreatePermissionModal = () => {
  isEditingPermission.value = false;
  currentPermission.value = { name: '' };
  showPermissionModal.value = true;
};

const openEditPermissionModal = (permission: Permission) => {
  isEditingPermission.value = true;
  currentPermission.value = { ...permission };
  showPermissionModal.value = true;
};

const closePermissionModal = () => {
  showPermissionModal.value = false;
  currentPermission.value = null;
};

const savePermission = async () => {
  if (!currentPermission.value) return;

  try {
    if (isEditingPermission.value && (currentPermission.value as Permission).id) {
      await permissionAPI.updatePermission((currentPermission.value as Permission).id, { name: currentPermission.value.name });
    } else {
      await permissionAPI.createPermission({ name: currentPermission.value.name });
    }
    await loadPermissions();
    closePermissionModal();
  } catch (error) {
    console.error('Error saving permission:', error);
  }
};

const confirmDeletePermission = (permission: Permission) => {
  permissionToDelete.value = permission;
  showDeletePermissionModal.value = true;
};

const deletePermission = async () => {
  if (!permissionToDelete.value) return;
  try {
    await permissionAPI.deletePermission(permissionToDelete.value.id);
    await loadPermissions();
  } catch (error) {
    console.error('Error deleting permission:', error);
  } finally {
    closeDeletePermissionModal();
  }
};

const closeDeletePermissionModal = () => {
  showDeletePermissionModal.value = false;
  permissionToDelete.value = null;
};

// Fungsi untuk memilih semua permission
const selectAllPermissions = () => {
  selectedPermissions.value = availablePermissions.value.map(perm => perm.id);
};

// Fungsi untuk menghapus semua pilihan permission
const deselectAllPermissions = () => {
  selectedPermissions.value = [];
};

// Lifecycle hooks
onMounted(async () => {
  await loadRoles();
  await loadPermissions();
});

// Watch for tab changes to reload data if necessary
watch(activeTab, (newTab) => {
  if (newTab === 'roles') {
    loadRoles();
  } else {
    loadPermissions();
  }
});
</script>

<style scoped>
.roles-permissions-page {
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

/* Tabs */
.tabs {
  display: flex;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}
.tab-button {
  padding: 0.75rem 1.5rem;
  background: transparent;
  border: none;
  border-bottom: 2px solid transparent;
  font-size: 1rem;
  font-weight: 600;
  color: #64748b;
  cursor: pointer;
  transition: all 0.3s ease;
}
.tab-button:hover {
  color: #1e293b;
}
.tab-button.active {
  color: #3b82f6;
  border-bottom: 2px solid #3b82f6;
}
.tab-content {
  margin-top: 1.5rem;
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

/* Table */
.table-responsive {
  overflow-x: auto;
}
.roles-table, .permissions-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}
.roles-table th, .roles-table td, .permissions-table th, .permissions-table td {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}
.roles-table th, .permissions-table th {
  font-size: 0.875rem;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  background-color: #f8fafc;
}
.roles-table tr:last-child td, .permissions-table tr:last-child td {
  border-bottom: none;
}
.role-id, .permission-id {
  font-weight: 600;
  color: #800000;
}
.role-name, .permission-name {
  font-weight: 600;
  color: #1e293b;
}
.permission-desc {
  color: #64748b;
}

/* Permissions tags */
.permissions-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  max-height: 60px;
  overflow-y: auto;
  padding: 0.25rem 0;
}
.permission-tag {
  padding: 0.25rem 0.5rem;
  background-color: #e0e7ff;
  color: #4f46e5;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
  white-space: nowrap;
  max-width: 120px;
  overflow: hidden;
  text-overflow: ellipsis;
}
.permission-tag.more {
  background-color: #cbd5e1;
  color: #475569;
  cursor: help;
}

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
.action-button.edit:hover { color: #f59e0b; }
.action-button.delete:hover { color: #ef4444; }

/* Responsive */
@media (max-width: 768px) {
  .roles-permissions-page {
    padding: 1rem;
  }
  .page-header {
    flex-direction: column;
    align-items: flex-start;
  }
  .tabs {
    overflow-x: auto;
    justify-content: flex-start;
  }
  .tab-button {
    white-space: nowrap;
  }
}
@media (max-width: 480px) {
  .page-title {
    font-size: 1.75rem;
  }
  .roles-table th:nth-child(3), .roles-table td:nth-child(3),
  .permissions-table th:nth-child(3), .permissions-table td:nth-child(3) {
    display: none; /* Hide description on smaller screens */
  }
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
.modal-form, .modal-body {
  padding: 2rem;
  overflow-y: auto;
  background-color: #ffffff;
}
.form-group {
  margin-bottom: 1.5rem;
}
.form-group label {
  display: block;
  font-size: 0.875rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 0.5rem;
}
.form-group input, .form-group select {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background-color: #f8fafc;
  box-sizing: border-box;
}
.form-group input:focus, .form-group select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
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

/* Confirmation Modal Specifics */
.confirmation-modal {
  max-width: 450px;
}
.confirmation-modal .modal-body {
  font-size: 1.1rem;
  color: #334155;
  line-height: 1.6;
}
.confirmation-modal .warning-text {
  font-size: 1rem;
  font-weight: 600;
  color: #ef4444;
  margin-top: 1rem;
}
.delete-confirm-button {
  background-color: #ef4444;
}
.delete-confirm-button:hover {
  background-color: #dc2626;
}

/* Permissions Checkbox Group */
.permissions-checkbox-group {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 0.75rem;
  padding: 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  background-color: #f8fafc;
}

.checkbox-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.checkbox-item input[type="checkbox"] {
  width: 16px;
  height: 16px;
  accent-color: #3b82f6;
  cursor: pointer;
}

.checkbox-item label {
  margin-bottom: 0;
  font-weight: 400;
  color: #334155;
  cursor: pointer;
}

/* Table Actions for Permissions Tab */
.table-actions {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 1rem;
}

/* Permissions Header */
.permissions-header {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 2rem;
  color: #64748b;
}

/* Small buttons */
.secondary-button.small {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
}

/* Responsive */
@media (max-width: 768px) {
  .modal-content {
    margin: 1rem;
  }
  .form-group.permissions-checkbox-group {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .modal-form, .modal-body {
    padding: 1.5rem;
  }
  .modal-header {
    padding: 1rem 1.5rem;
  }
  .modal-actions {
    padding: 1rem 1.5rem;
  }
}
</style>