import api from './apiConfig';

export interface Remote {
  id: number;
  site_name: string;
  site_id_poi?: string;
  notes?: string;
  latitude: number;
  longitude: number;
  origin_backbone?: string;
  origin_bb?: string;
  terminating_bb?: string;
  link?: string;
  jumlah_bts?: number;
  bw?: string;
  vlan?: string;
}

const remotesAPI = {
  // Get all remotes
  getAllRemotes: (skip: number = 0, limit: number = 100) => {
    return api.get<Remote[]>(`/remotes/`, { params: { skip, limit } });
  },

  // Get a single remote by ID
  getRemoteById: (id: number) => {
    return api.get<Remote>(`/remotes/${id}`);
  },

  // Create a new remote
  createRemote: (remoteData: Omit<Remote, 'id' | 'created_at'>) => {
    return api.post<Remote>('/remotes/', remoteData);
  },

  // Update a remote
  updateRemote: (id: number, remoteData: Partial<Omit<Remote, 'id' | 'created_at'>>) => {
    return api.put<Remote>(`/remotes/${id}`, remoteData);
  },

  // Delete a remote
  deleteRemote: (id: number) => {
    return api.delete(`/remotes/${id}`);
  }
};

export { remotesAPI };