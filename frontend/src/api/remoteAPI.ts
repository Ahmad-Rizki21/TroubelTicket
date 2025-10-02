import api from './apiConfig';

export interface Remote {
  id: number;
  site_id_poi: string | null;
  site_name: string;
  notes: string | null;
  latitude: number;
  longitude: number;
  origin_backbone: string | null;
  origin_bb: string | null;
  terminating_bb: string | null;
  link: string | null;
  jumlah_bts: number | null;
  bw: string | null;
  vlan: string | null;
}

export interface RemoteCreate {
  site_id_poi?: string | null;
  site_name: string;
  notes?: string | null;
  latitude: number;
  longitude: number;
  origin_backbone?: string | null;
  origin_bb?: string | null;
  terminating_bb?: string | null;
  link?: string | null;
  jumlah_bts?: number | null;
  bw?: string | null;
  vlan?: string | null;
}

export interface RemoteUpdate {
  site_id_poi?: string | null;
  site_name?: string;
  notes?: string | null;
  latitude?: number;
  longitude?: number;
  origin_backbone?: string | null;
  origin_bb?: string | null;
  terminating_bb?: string | null;
  link?: string | null;
  jumlah_bts?: number | null;
  bw?: string | null;
  vlan?: string | null;
}

const remoteAPI = {
  getAllRemotes: () => {
    return api.get<Remote[]>('/remotes/');
  },
  getRemoteById: (id: number) => {
    return api.get<Remote>(`/remotes/${id}`);
  },
  createRemote: (remoteData: RemoteCreate) => {
    return api.post<Remote>('/remotes/', remoteData);
  },
  updateRemote: (id: number, remoteData: RemoteUpdate) => {
    return api.put<Remote>(`/remotes/${id}`, remoteData);
  },
  deleteRemote: (id: number) => {
    return api.delete(`/remotes/${id}`);
  },
};

export { remoteAPI };
