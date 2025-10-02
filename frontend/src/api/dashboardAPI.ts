export interface DashboardStats {
  total_tickets: number;
  open_tickets: number;
  completed_tickets: number;
  avg_resolution_time: string;
  total_remotes: number;
}

export interface TicketStatusData {
  status: string;
  count: number;
}

export interface TicketPriorityData {
  priority: string;
  count: number;
}

export interface RecentTicket {
  id: number;
  ticket_code: string;
  title: string;
  status: string;
  priority: string;
  created_at: string;
}

export interface TicketCategoryData {
  name: string;
  count: number;
  percentage: number;
}

export interface DashboardData {
  stats: DashboardStats;
  status_distribution: TicketStatusData[];
  priority_distribution: TicketPriorityData[];
  recent_tickets: RecentTicket[];
  top_categories: TicketCategoryData[];
}

import api from './apiConfig';

const dashboardAPI = {
  getDashboardData: (period: string = 'week') => {
    return api.get<DashboardData>(`/dashboard/`, { params: { period } });
  }
};

export { dashboardAPI };