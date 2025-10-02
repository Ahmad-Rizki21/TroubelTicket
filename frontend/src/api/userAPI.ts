import api from './apiConfig';

export interface Permission {
  id: number;
  name: string;
}

export interface Role {
  id: number;
  name: string;
  permissions: Permission[];
}

export interface User {
  id: number;
  username: string;
  role_id: number;
  created_at: string;
  role: Role;
}

export interface UserCreate {
  username: string;
  password?: string; // Optional for create if backend handles default
  role_id: number;
}

export interface UserUpdate {
  username?: string;
  password?: string;
  role_id?: number;
}

const userAPI = {
  getAllUsers: (skip: number = 0, limit: number = 100) => {
    return api.get<User[]>(`/users/`, { params: { skip, limit } });
  },

  getUserById: (id: number) => {
    return api.get<User>(`/users/${id}`);
  },

  createUser: (userData: UserCreate) => {
    return api.post<User>(`/users/`, userData);
  },

  updateUser: (id: number, userData: UserUpdate) => {
    return api.put<User>(`/users/${id}`, userData);
  },

  getMe: () => {
    return api.get<User>('/users/me');
  },

  deleteUser: (id: number) => {
    return api.delete(`/users/${id}`);
  }
};

export { userAPI };
