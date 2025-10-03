export interface ReportSummary {
  total_tickets: number;
  resolved_tickets: number;
  open_tickets: number;
  avg_resolution_time: string;
  satisfaction_rate: number;
}

export interface ReportTicket {
  id: number;
  ticket_code: string;
  title: string;
  description: string;
  status: string;
  priority: string;
  category: string;
  reporter_name: string;
  reporter_contact: string;
  assignee: string;
  created_at: string;
  closed_at: string;
  resolution_time: number;
  summary_problem?: string;
  summary_action?: string;
}

export interface ReportFilters {
  startDate?: string;
  endDate?: string;
  category?: string;
  priority?: string;
  status?: string;
  search?: string;
  page?: number;
  limit?: number;
}

export interface ReportData {
  summary: ReportSummary;
  tickets: ReportTicket[];
  pagination: {
    current_page: number;
    total_pages: number;
    total_items: number;
    items_per_page: number;
  };
}

export interface CategoryStats {
  category: string;
  count: number;
  percentage: number;
}

export interface PriorityStats {
  priority: string;
  count: number;
  percentage: number;
}

export interface StatusStats {
  status: string;
  count: number;
  percentage: number;
}

export interface TechnicianPerformance {
  technician: string;
  resolved_tickets: number;
  avg_resolution_time: string;
  rating: number;
}

import api from './apiConfig';

const reportsAPI = {
  getReportsData: (filters: ReportFilters = {}) => {
    return api.get<ReportData>('/reports/', { params: filters });
  },

  exportAllTickets: (filters: ReportFilters = {}) => {
    return api.get('/tickets/export/excel', {
      params: filters,
      responseType: 'blob'
    });
  },

  exportTicketPDF: (ticketId: number) => {
    return api.get(`/tickets/${ticketId}/export/pdf`, {
      responseType: 'blob'
    });
  },

  getCategoryStats: (filters: ReportFilters = {}) => {
    return api.get<CategoryStats[]>('/reports/categories', { params: filters });
  },

  getPriorityStats: (filters: ReportFilters = {}) => {
    return api.get<PriorityStats[]>('/reports/priorities', { params: filters });
  },

  getStatusStats: (filters: ReportFilters = {}) => {
    return api.get<StatusStats[]>('/reports/statuses', { params: filters });
  },

  getTechnicianPerformance: (filters: ReportFilters = {}) => {
    return api.get<TechnicianPerformance[]>('/reports/technicians', { params: filters });
  }
};

export { reportsAPI };