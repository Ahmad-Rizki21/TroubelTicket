import api from './apiConfig';

export interface Permission {
  id: number;
  name: string;
}

export interface Role {
  id: number;
  name: string;
  created_at?: string;
  permissions: Permission[]; // Assuming permissions are nested
}

export interface RoleCreate {
  name: string;
}

export interface RoleUpdate {
  name?: string;
}

const roleAPI = {
  getAllRoles: (skip: number = 0, limit: number = 100) => {
    return api.get<Role[]>(`/roles/`, { params: { skip, limit } });
  },

  getRoleById: (id: number) => {
    return api.get<Role>(`/roles/${id}`);
  },

  createRole: (roleData: RoleCreate) => {
    return api.post<Role>(`/roles/`, roleData);
  },

  updateRole: (id: number, roleData: RoleUpdate) => {
    return api.put<Role>(`/roles/${id}`, roleData);
  },

  deleteRole: (id: number) => {
    return api.delete(`/roles/${id}`);
  },

  assignPermissionToRole: (roleId: number, permissionId: number) => {
    return api.post<Role>(`/roles/${roleId}/permissions/${permissionId}`);
  },

  removePermissionFromRole: (roleId: number, permissionId: number) => {
    return api.delete<Role>(`/roles/${roleId}/permissions/${permissionId}`);
  }
};

export { roleAPI };
