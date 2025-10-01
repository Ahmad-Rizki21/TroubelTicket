<template>
  <div class="tickets-page">
    <!-- Page Header -->
    <header class="page-header">
      <div class="header-content">
        <h1 class="page-title">Ticket Management</h1>
        <p class="page-subtitle">Manage, track, and resolve all issue tickets here.</p>
      </div>
      <div class="header-actions">
        <button class="primary-button" @click="openCreateModal">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 5V19M5 12H19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span>Create New Ticket</span>
        </button>
      </div>
    </header>

    <!-- Filters and Search Section -->
    <div class="card filters-card">
      <div class="search-box">
        <svg class="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M21 21L15 15M17 10C17 13.866 13.866 17 10 17C6.13401 17 3 13.866 3 10C3 6.13401 6.13401 3 10 3C13.866 3 17 6.13401 17 10Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="Search by ID, title..." 
          class="search-input"
          @input="filterTickets"
        >
      </div>
      
      <div class="filters">
        <select v-model="statusFilter" class="filter-select" @change="filterTickets">
          <option value="">All Statuses</option>
          <option value="Open">Open</option>
          <option value="In Progress">In Progress</option>
          <option value="Closed">Closed</option>
          <option value="On Hold">On Hold</option>
        </select>
        
        <select v-model="priorityFilter" class="filter-select" @change="filterTickets">
          <option value="">All Priorities</option>
          <option value="High">High</option>
          <option value="Medium">Medium</option>
          <option value="Low">Low</option>
        </select>
      </div>
    </div>

    <!-- Tickets Table -->
    <div class="card tickets-table-card">
      <div class="table-responsive">
        <table class="tickets-table">
          <thead>
            <tr>
              <th>Ticket ID</th>
              <th>Title</th>
              <th>Status</th>
              <th>Priority</th>
              <th>Reporter</th>
              <th>Date Created</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="filteredTickets.length === 0">
              <td colspan="7" class="empty-state">
                <p>No tickets match your criteria.</p>
              </td>
            </tr>
            <tr v-for="ticket in filteredTickets" :key="ticket.id">
              <td class="ticket-id">{{ ticket.ticket_code }}</td>
              <td>
                <div class="ticket-title">{{ ticket.title }}</div>
                <div class="ticket-updated">Updated: {{ formatDate(ticket.closed_at || ticket.created_at) }}</div>
              </td>
              <td>
                <span class="status-badge" :class="`status-${ticket.status.toLowerCase().replace(' ', '-')}`">
                  {{ ticket.status }}
                </span>
              </td>
              <td>
                <span class="priority-badge" :class="`priority-${ticket.priority.toLowerCase()}`">
                  {{ ticket.priority }}
                </span>
              </td>
              <td>{{ ticket.reporter_name }}</td>
              <td>{{ formatDate(ticket.created_at) }}</td>
              <td>
                <div class="action-buttons">
                  <button class="action-button view" @click="viewTicket(ticket)" title="View Details">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M1 12C1 12 5 4 12 4C19 4 23 12 23 12C23 12 19 20 12 20C5 20 1 12 1 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M12 15C13.6569 15 15 13.6569 15 12C15 10.3431 13.6569 9 12 9C10.3431 9 9 10.3431 9 12C9 13.6569 10.3431 15 12 15Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                  </button>
                  <button class="action-button edit" @click="editTicket(ticket)" title="Edit Ticket">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M11 4H4C3.46957 4 2.96086 4.21071 2.58579 4.58579C2.21071 4.96086 2 5.46957 2 6V20C2 20.5304 2.21071 21.0391 2.58579 21.4142C2.96086 21.7893 3.46957 22 4 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V13M18.5 2.5L21.5 5.5M17.5 1.5L9 10V13H12L20.5 4.5L17.5 1.5Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                  </button>
                  <button class="action-button delete" @click="deleteTicket(ticket)" title="Delete Ticket">
                   <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3 6H5H21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M8 6V4C8 3.46957 8.21071 2.96086 8.58579 2.58579C8.96086 2.21071 9.46957 2 10 2H14C14.5304 2 15.0391 2.21071 15.4142 2.58579C15.7893 2.96086 16 3.46957 16 4V6M19 6V20C19 20.5304 18.7893 21.0391 18.4142 21.4142C18.0391 21.7893 17.5304 22 17 22H7C6.46957 22 5.96086 21.7893 5.58579 21.4142C5.21071 21.0391 5 20.5304 5 20V6H19Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M10 11V17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M14 11V17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
       <!-- Pagination -->
      <div class="pagination">
        <button class="pagination-button" :disabled="currentPage === 1" @click="prevPage">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M15 18L9 12L15 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span>Previous</span>
        </button>
        <span class="pagination-info">Page {{ currentPage }} of {{ totalPages }}</span>
        <button class="pagination-button" :disabled="currentPage === totalPages" @click="nextPage">
          <span>Next</span>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M9 18L15 12L9 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
      </div>
    </div>
  </div>

  <!-- Create/Edit Ticket Modal -->
  <transition name="modal-fade">
    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2 class="modal-title">{{ isEditing ? 'Edit Ticket' : 'Create New Ticket' }}</h2>
          <button class="close-button" @click="closeModal">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
        </div>
        <form @submit.prevent="saveTicket" class="modal-form">
          <div class="form-group">
            <label for="title">Ticket Title</label>
            <input type="text" id="title" v-model="currentTicket.title" required placeholder="e.g., Slow internet connection">
          </div>
          <div class="form-group">
            <label for="description">Description</label>
            <textarea id="description" v-model="currentTicket.description" rows="4" placeholder="Describe the issue in detail..."></textarea>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label for="reporter_name">Reporter Name</label>
              <input type="text" id="reporter_name" v-model="currentTicket.reporter_name" required placeholder="Enter reporter's name">
            </div>
            <div class="form-group">
              <label for="reporter_contact">Reporter Contact</label>
              <input type="text" id="reporter_contact" v-model="currentTicket.reporter_contact" placeholder="Enter reporter's contact info">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label for="category">Category</label>
              <select id="category" v-model="currentTicket.category">
                <option value="Network">Network</option>
                <option value="Hardware">Hardware</option>
                <option value="Software">Software</option>
                <option value="Other">Other</option>
              </select>
            </div>
            <div class="form-group">
              <label for="priority">Priority</label>
              <select id="priority" v-model="currentTicket.priority" disabled>
                <option value="Low">Low</option>
                <option value="Medium">Medium</option>
                <option value="High">High</option>
              </select>
            </div>
          </div>
          <div class="form-group">
            <label for="assigned_to">Assigned To</label>
            <select id="assigned_to" v-model="currentTicket.assigned_to">
              <option value="">Select technician</option>
              <option value="1">Technician A</option>
              <option value="2">Technician B</option>
              <option value="3">Technician C</option>
            </select>
          </div>
          <div class="modal-actions">
            <button type="button" class="secondary-button" @click="closeModal">Cancel</button>
            <button type="submit" class="primary-button save-button">{{ isEditing ? 'Save Changes' : 'Create Ticket' }}</button>
          </div>
        </form>
      </div>
    </div>
  </transition>

  <!-- View Ticket Detail Modal -->
  <transition name="modal-fade">
    <div v-if="showDetailModal" class="modal-overlay" @click="closeDetailModal">
      <div class="modal-content detail-modal-content" @click.stop>
        <div class="modal-header">
          <h2 class="modal-title">Ticket Details #{{ selectedTicket.id }}</h2>
          <button class="close-button" @click="closeDetailModal">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
          </button>
        </div>
        <div class="ticket-detail">
          <div class="detail-grid">
              <div class="detail-item">
                <span class="detail-label">Title</span>
                <span class="detail-value">{{ selectedTicket.title }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Status</span>
                <span class="status-badge" :class="`status-${selectedTicket.status.toLowerCase().replace(' ', '-')}`">{{ selectedTicket.status }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Priority</span>
                <span class="priority-badge" :class="`priority-${selectedTicket.priority.toLowerCase()}`">{{ selectedTicket.priority }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Category</span>
                <span class="detail-value">{{ selectedTicket.category }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Reporter Name</span>
                <span class="detail-value">{{ selectedTicket.reporter_name }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Reporter Contact</span>
                <span class="detail-value">{{ selectedTicket.reporter_contact || 'N/A' }}</span>
              </div>
          </div>
          <div class="detail-item description">
              <span class="detail-label">Description</span>
              <p class="detail-value">{{ selectedTicket.description }}</p>
          </div>
          <div class="detail-grid">
              <div class="detail-item">
                <span class="detail-label">Created At</span>
                <span class="detail-value">{{ formatDate(selectedTicket.created_at) }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Last Updated</span>
                <span class="detail-value">{{ formatDate(selectedTicket.closed_at || selectedTicket.created_at) }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Assigned To</span>
                <span class="detail-value">{{ selectedTicket.assigned_to || 'Not assigned' }}</span>
              </div>
          </div>
        </div>
      </div>
    </div>
  </transition>
  
    <!-- Delete Confirmation Modal -->
  <transition name="modal-fade">
    <div v-if="showDeleteModal" class="modal-overlay" @click="closeDeleteModal">
      <div class="modal-content confirmation-modal" @click.stop>
        <div class="modal-header">
          <h2 class="modal-title">Confirm Ticket Deletion</h2>
        </div>
        <div class="modal-body">
          <p v-if="ticketToDelete">
            Are you sure you want to delete ticket <strong>{{ ticketToDelete.ticket_code }} - {{ ticketToDelete.title }}</strong>?
          </p>
          <p class="warning-text">This action cannot be undone.</p>
        </div>
        <div class="modal-actions">
          <button type="button" class="secondary-button" @click="closeDeleteModal">Cancel</button>
          <button type="button" class="primary-button delete-confirm-button" @click="confirmDelete">Yes, Delete</button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import type { Ticket, TicketCreate, TicketUpdate } from '../api/ticketAPI';
import { ticketAPI } from '../api/ticketAPI';

// State management
const showModal = ref(false);
const showDetailModal = ref(false);
const showDeleteModal = ref(false);
const ticketToDelete = ref<Ticket | null>(null);
const isEditing = ref(false);
const searchQuery = ref('');
const statusFilter = ref('');
const priorityFilter = ref('');
const currentPage = ref(1);
const itemsPerPage = ref(10);
const totalItems = ref(0);
const loading = ref(false);
interface ExtendedTicket extends Ticket {
  category?: string; // For UI compatibility - doesn't exist in backend
  assigned_to?: string; // For UI compatibility - doesn't exist in backend (use assignee_id instead)
  reporter_contact?: string; // Add reporter_contact for UI compatibility
}

const selectedTicket = ref<ExtendedTicket>({
  id: 0,
  ticket_code: '',
  title: '',
  description: '',
  status: 'Open',
  priority: 'Medium',
  reporter_name: '',
  reporter_contact: '',
  assignee_id: undefined,
  created_at: '',
  closed_at: undefined,
  downtime: undefined,
  summary_problem: undefined,
  summary_action: undefined,
  actions: [],
  assignee: undefined,
  category: 'Network', // For UI compatibility
  assigned_to: '', // For UI compatibility
});

// Define a type that includes all possible fields needed for the form, including UI-only fields
interface FormTicket {
  title: string;
  description?: string;
  priority: string;
  reporter_name: string;
  reporter_contact?: string; // Add reporter_contact
  category?: string; // For UI compatibility - doesn't exist in backend
  ticket_code?: string; // Only for create
  status?: string; // Only for update
  assignee_id?: number; // Only for update
  assigned_to?: string; // For UI compatibility - doesn't exist in backend (use assignee_id instead)
  summary_problem?: string; // Only for update 
  summary_action?: string; // Only for update
}

const currentTicket = ref<FormTicket>({
  title: '',
  description: '',
  priority: 'High',
  reporter_name: '',
  reporter_contact: '',
  category: 'Network', // Default for UI compatibility
  ticket_code: ''
});

// Tickets data from API
const allTickets = ref<Ticket[]>([]);
const filteredTickets = ref<Ticket[]>([]);

// Computed properties
const totalPages = computed(() => Math.ceil(filteredTickets.value.length / itemsPerPage.value));

const formatDate = (dateString: string | undefined) => {
  if (!dateString) return '-';
  // Make sure it's a valid date string before processing
  const date = new Date(dateString);
  if (isNaN(date.getTime())) {
    return '-'; // Return a default value if the date string is invalid
  }
  return date.toLocaleDateString('en-US', { day: '2-digit', month: 'long', year: 'numeric' });
};

// Methods
const applyFilters = () => {
  let filtered = [...allTickets.value];
  
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(ticket => 
      (ticket.title || '').toLowerCase().includes(query) || 
      (ticket.ticket_code || '').toLowerCase().includes(query)
    );
  }
  
  if (statusFilter.value) {
    filtered = filtered.filter(ticket => ticket.status === statusFilter.value);
  }
  
  if (priorityFilter.value) {
    filtered = filtered.filter(ticket => ticket.priority === priorityFilter.value);
  }
  
  // Store all filtered tickets
  filteredTickets.value = filtered;
  
  // Reset to first page when filters change
  currentPage.value = 1;
};

const filterTickets = () => {
  applyFilters();
};

const openCreateModal = () => {
  isEditing.value = false;
  currentTicket.value = { 
    title: '', 
    description: '', 
    priority: 'High', // Changed to High as default
    reporter_name: '', 
    reporter_contact: '', // Initialize reporter_contact
    category: 'Network', // For UI compatibility
    ticket_code: generateTicketCode(),
    assigned_to: '', // For UI compatibility
    status: 'Open' // Default status
  };
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
};

const closeDetailModal = () => {
  showDetailModal.value = false;
};

const saveTicket = async () => {
  try {
    if (isEditing.value) {
      // Update existing ticket
      const ticketId = selectedTicket.value.id;
      const updateData: TicketUpdate = {
        title: currentTicket.value.title,
        description: currentTicket.value.description,
        status: currentTicket.value.status,
        priority: currentTicket.value.priority,
        reporter_contact: currentTicket.value.reporter_contact, // Include reporter_contact
        assignee_id: currentTicket.value.assignee_id,
        summary_problem: currentTicket.value.summary_problem,
        summary_action: currentTicket.value.summary_action
      };
      // Only include fields that have values, but explicitly allow empty string for reporter_contact
      Object.keys(updateData).forEach(key => {
        if (key !== 'reporter_contact' && (updateData[key as keyof TicketUpdate] === undefined || updateData[key as keyof TicketUpdate] === '')) {
          delete updateData[key as keyof TicketUpdate];
        }
      });
      
      await ticketAPI.updateTicket(ticketId, updateData);
    } else {
      // Create new ticket
      const createData: TicketCreate = {
        title: currentTicket.value.title,
        description: currentTicket.value.description || '',
        priority: currentTicket.value.priority,
        reporter_name: currentTicket.value.reporter_name,
        reporter_contact: currentTicket.value.reporter_contact, // Send undefined if empty, not ''
        ticket_code: currentTicket.value.ticket_code || generateTicketCode()
      };
      
      await ticketAPI.createTicket(createData);
    }
    
    // Reload tickets after save
    await loadTickets();
    closeModal();
  } catch (error) {
    console.error('Error saving ticket:', error);
    // In a real app, you might want to show an error message to the user
  }
};

const viewTicket = async (ticket: Ticket) => {
  try {
    // If we already have the full ticket data, just display it
    if (allTickets.value.some(t => t.id === ticket.id)) {
      selectedTicket.value = { 
        ...ticket, 
        category: 'Network', // Add UI compatibility field
        assigned_to: ticket.assignee_id ? `${ticket.assignee_id}` : '', // Add UI compatibility field
        reporter_contact: ticket.reporter_contact, // Populate reporter_contact
      };
    } else {
      // Otherwise, fetch the full ticket details from the API
      const response = await ticketAPI.getTicketById(ticket.id);
      selectedTicket.value = { 
        ...response.data,
        category: 'Network', // Add UI compatibility field
        assigned_to: response.data.assignee_id ? `${response.data.assignee_id}` : '', // Add UI compatibility field
        reporter_contact: response.data.reporter_contact, // Populate reporter_contact
      };
    }
    showDetailModal.value = true;
  } catch (error) {
    console.error('Error loading ticket details:', error);
    // In a real app, you might want to show an error message to the user
  }
};

const editTicket = (ticket: Ticket) => {
  currentTicket.value = { 
    title: ticket.title, 
    description: ticket.description || '', 
    priority: 'High',
    reporter_name: ticket.reporter_name,
    reporter_contact: ticket.reporter_contact || '', // Populate reporter_contact
    category: 'Network', // For UI compatibility
    status: ticket.status, // For updates
    assignee_id: ticket.assignee_id, // For updates
    assigned_to: ticket.assignee_id ? `${ticket.assignee_id}` : '', // For UI compatibility
    summary_problem: ticket.summary_problem, // For updates
    summary_action: ticket.summary_action // For updates
  };
  selectedTicket.value = { 
    ...ticket,
    category: 'Network', // Add UI compatibility field
    assigned_to: ticket.assignee_id ? `${ticket.assignee_id}` : '', // Add UI compatibility field
    reporter_contact: ticket.reporter_contact, // Populate reporter_contact
  }; // Keep a reference to the ticket being edited
  isEditing.value = true;
  showModal.value = true;
};

const deleteTicket = (ticket: Ticket) => {
  ticketToDelete.value = ticket;
  showDeleteModal.value = true;
};

const closeDeleteModal = () => {
  showDeleteModal.value = false;
  ticketToDelete.value = null;
};

const confirmDelete = async () => {
  if (!ticketToDelete.value) return;

  try {
    await ticketAPI.deleteTicket(ticketToDelete.value.id);
    await loadTickets();
  } catch (error: any) {
    console.error('Error deleting ticket:', error);
  } finally {
    closeDeleteModal();
  }
};

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
    // Update filteredTickets to reflect the new page (if we implement true pagination later)
    applyFilters();
  }
};

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
    // Update filteredTickets to reflect the new page (if we implement true pagination later)
    applyFilters();
  }
};

const loadTickets = async () => {
  loading.value = true;
  try {
    console.log('Attempting to load tickets from API...');
    // We need to load all tickets to properly filter them on the frontend
    // For a real application, you'd want to implement backend filtering
    const response = await ticketAPI.getAllTickets(0, 100); // Getting more tickets to ensure we have them all for filtering
    
    console.log('API Response:', response); // Log the full response
    
    // The response should be an array of tickets
    allTickets.value = response.data;
    totalItems.value = response.data.length;
    
    console.log('Loaded tickets:', response.data); // For debugging
    console.log('Number of tickets loaded:', response.data.length);
    
    // Apply filtering to the loaded data
    applyFilters();
  } catch (error: any) {
    console.error('Error loading tickets:', error);
    console.error('Error details:', error?.response?.data || error?.message);
    // In a real app, you might want to show a notification to the user
  } finally {
    loading.value = false;
  }
};

// Generate a ticket code in the format AG-0000001 based on the next available sequence
const generateTicketCode = (): string => {
  // Determine the next sequence number based on current tickets
  if (allTickets.value.length === 0) {
    return 'AG-0000001';
  }
  
  // Find the highest numbered ticket that follows the AG-XXXXXX pattern
  let maxNumber = 0;
  const ticketPattern = /^AG-(\d+)$/;
  
  allTickets.value.forEach(ticket => {
    const match = ticket.ticket_code.match(ticketPattern);
    if (match && match[1]) {
      const number = parseInt(match[1], 10);
      if (number > maxNumber) {
        maxNumber = number;
      }
    }
  });
  
  // The next number should be maxNumber + 1
  const nextNumber = maxNumber + 1;
  const paddedNumber = nextNumber.toString().padStart(7, '0');
  
  return `AG-${paddedNumber}`;
};

onMounted(async () => {
  await loadTickets();
});

// Watch for filter changes and reload filtered data
import { watch } from 'vue';
watch([searchQuery, statusFilter, priorityFilter], () => {
  applyFilters();
});
</script>

<style scoped>
.tickets-page {
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

/* Header */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}
.page-title {
  font-size: 2.25rem;
  font-weight: 800;
  color: #1e293b;
  margin: 0;
}
.page-subtitle {
  font-size: 1.125rem;
  color: #64748b;
  margin-top: 0.25rem;
}

/* Buttons */
.primary-button {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background-color: #ff4d4f;
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}
.primary-button:hover {
  background-color: #d9363e;
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}
.secondary-button {
  padding: 0.75rem 1.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  background: #ffffff;
  color: #64748b;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}
.secondary-button:hover {
  background-color: #f1f5f9;
  border-color: #cbd5e1;
}

/* Filters */
.filters-card {
  display: flex;
  padding: 1.5rem;
  gap: 1.5rem;
  flex-wrap: wrap;
}
.search-box {
  position: relative;
  flex-grow: 1;
}
.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #64748b;
}
.search-input, .filter-select {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 2.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  font-size: 1rem;
  color: #1e293b;
  background-color: #f8fafc;
  transition: all 0.3s ease;
  box-sizing: border-box;
}
.search-input:focus, .filter-select:focus {
  outline: none;
  border-color: #ff4d4f;
  box-shadow: 0 0 0 3px rgba(255, 77, 79, 0.2);
  background-color: #ffffff;
}
.filters {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}
.filter-select {
  padding: 0.75rem 1rem;
  min-width: 180px;
}

/* Table */
.tickets-table-card {
  overflow: hidden;
}
.table-responsive {
  overflow-x: auto;
}
.tickets-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}
.tickets-table th, .tickets-table td {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}
.tickets-table th {
  font-size: 0.875rem;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  background-color: #f8fafc;
}
.tickets-table tr:last-child td {
  border-bottom: none;
}
.ticket-id {
  font-weight: 600;
  color: #d9363e;
}
.ticket-title {
  font-weight: 600;
  color: #1e293b;
}
.ticket-updated {
  font-size: 0.875rem;
  color: #64748b;
  margin-top: 0.25rem;
}

/* Badges */
.status-badge, .priority-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  display: inline-block;
}
.status-open { background-color: #fee2e2; color: #dc2626; }
.status-in-progress { background-color: #fef3c7; color: #d97706; }
.status-closed { background-color: #d1fae5; color: #059669; }
.status-on-hold { background-color: #e5e7eb; color: #374151; }

.priority-high { background-color: #fecaca; color: #b91c1c; }
.priority-medium { background-color: #fed7aa; color: #c2410c; }
.priority-low { background-color: #bfdbfe; color: #1d4ed8; }

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
.action-button.view:hover { color: #3b82f6; }
.action-button.edit:hover { color: #f59e0b; }
.action-button.delete:hover { color: #ef4444; }

/* Empty State */
.empty-state {
  text-align: center;
  padding: 4rem;
  color: #64748b;
}

/* Pagination */
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}
.pagination-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background: #ffffff;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s ease;
}
.pagination-button:hover:not(:disabled) {
  border-color: #ff4d4f;
  color: #ff4d4f;
}
.pagination-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.pagination-info {
  font-size: 1rem;
  font-weight: 500;
  color: #1e293b;
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
.modal-form, .ticket-detail, .modal-body {
  padding: 2rem;
  overflow-y: auto;
  background-color: #ffffff;
}
.form-group {
  margin-bottom: 1.5rem;
}
.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}
.form-group label {
  display: block;
  font-size: 0.875rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 0.5rem;
}
.form-group input, .form-group textarea, .form-group select {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background-color: #f8fafc;
  box-sizing: border-box;
}
.form-group input:focus, .form-group textarea:focus, .form-group select:focus {
  outline: none;
  border-color: #ff4d4f;
  box-shadow: 0 0 0 3px rgba(255, 77, 79, 0.2);
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

/* Detail Modal */
.detail-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid #e2e8f0;
    margin-bottom: 1.5rem;
}
.detail-grid:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}
.detail-item {
    display: flex;
    flex-direction: column;
}
.detail-item.description {
    grid-column: 1 / -1;
}
.detail-label {
    font-size: 0.875rem;
    font-weight: 600;
    color: #64748b;
    margin-bottom: 0.5rem;
}
.detail-value {
    font-size: 1rem;
    color: #1e293b;
    line-height: 1.6;
}

/* Responsive */
@media (max-width: 768px) {
  .tickets-page {
    padding: 1rem;
  }
  .page-header {
    flex-direction: column;
    align-items: flex-start;
  }
  .filters-card {
    flex-direction: column;
  }
  .form-row {
    grid-template-columns: 1fr;
  }
  .tickets-table th:nth-child(5), .tickets-table td:nth-child(5) {
      display: none; /* Hide date on smaller screens */
  }
}
@media (max-width: 480px) {
  .page-title {
    font-size: 1.75rem;
  }
  .modal-content {
      margin: 1rem;
      max-height: calc(100vh - 2rem);
  }
  .modal-form, .ticket-detail {
    padding: 1.5rem;
  }
}
</style>

