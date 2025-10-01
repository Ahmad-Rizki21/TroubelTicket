import api from './apiConfig';

export interface Ticket {
  id: number;
  ticket_code: string;
  title: string;
  description?: string;
  status: string;
  priority: string;
  reporter_name: string;
  reporter_contact?: string;
  assignee_id?: number;
  created_at: string;
  closed_at?: string;
  downtime?: string;
  summary_problem?: string;
  summary_action?: string;
  actions: any[]; // Using any for now, can be typed more specifically later
  assignee?: any; // Using any for now, can be typed more specifically later
}

export interface TicketCreate {
  title: string;
  description?: string;
  priority: string;
  reporter_name: string;
  reporter_contact?: string;
  ticket_code: string;
}

export interface TicketUpdate {
  title?: string;
  description?: string;
  status?: string;
  priority?: string;
  reporter_contact?: string;
  assignee_id?: number;
  summary_problem?: string;
  summary_action?: string;
}

const ticketAPI = {
  // Get all tickets
  getAllTickets: (skip: number = 0, limit: number = 100) => {
    return api.get<Ticket[]>(`/tickets/`, { params: { skip, limit } });
  },

  // Get a single ticket by ID
  getTicketById: (id: number) => {
    return api.get<Ticket>(`/tickets/${id}`);
  },

  // Create a new ticket
  createTicket: (ticketData: TicketCreate) => {
    return api.post<Ticket>('/tickets/', ticketData);
  },

  // Update a ticket
  updateTicket: (id: number, ticketData: TicketUpdate) => {
    return api.put<Ticket>(`/tickets/${id}`, ticketData);
  },

  // Delete a ticket
  deleteTicket: (id: number) => {
    return api.delete(`/tickets/${id}`);
  }
};

export { ticketAPI };