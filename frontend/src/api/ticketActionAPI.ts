import api from './apiConfig';

export interface TicketAction {
  id: number;
  ticket_id: number;
  user_id: number;
  role_id?: number;
  action_description: string;
  action_image_url?: string;
  created_at: string;
  user: any; // Using any for now, can be typed more specifically later
  role?: any; // Using any for now, can be typed more specifically later
}

export interface TicketActionCreate {
  action_description: string;
  action_image_url?: string;
  user_id?: number; // Optional - will use authenticated user if not provided
  role_id?: number; // Optional
  new_status?: string; // New status for the ticket
  summary_problem?: string; // Summary of the problem when closing ticket
  summary_action?: string; // Summary of the action taken when closing ticket
}

const ticketActionAPI = {
  // Get all actions for a specific ticket
  getTicketActions: (ticketId: number) => {
    return api.get<TicketAction[]>(`/tickets/${ticketId}/actions/`);
  },

  // Create a new action for a ticket
  createTicketAction: (ticketId: number, actionData: FormData) => {
    return api.post<TicketAction>(`/tickets/${ticketId}/actions/`, actionData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },

  // Update an existing ticket action
  updateTicketAction: (ticketId: number, actionId: number, actionData: FormData) => {
    return api.put<TicketAction>(`/tickets/${ticketId}/actions/${actionId}/`, actionData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
};

export { ticketActionAPI };