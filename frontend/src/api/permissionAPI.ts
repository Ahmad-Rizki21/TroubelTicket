import api from './apiConfig';

export interface Permission {
  id: number;
  name: string;
  created_at?: string;
}

export interface PermissionCreate {
  name: string;
}

export interface PermissionUpdate {
  name?: string;
}

const permissionAPI = {
  getAllPermissions: (skip: number = 0, limit: number = 100) => {
    return api.get<Permission[]>(`/permissions/`, { params: { skip, limit } });
  },

  getPermissionById: (id: number) => {
    return api.get<Permission>(`/permissions/${id}`);
  },

  createPermission: (permissionData: PermissionCreate) => {
    return api.post<Permission>(`/permissions/`, permissionData);
  },

  updatePermission: (id: number, permissionData: PermissionUpdate) => {
    return api.put<Permission>(`/permissions/${id}`, permissionData);
  },

  deletePermission: (id: number) => {
    return api.delete(`/permissions/${id}`);
  }
};

export { permissionAPI };
