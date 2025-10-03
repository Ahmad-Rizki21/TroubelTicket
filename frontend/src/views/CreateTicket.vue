<template>
  <div class="create-ticket-page">
    <!-- Page Header -->
    <header class="page-header">
      <div class="header-content">
        <div class="title-section">
          <div class="breadcrumb">
            <router-link to="/tickets" class="breadcrumb-link">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M15 18L9 12L15 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              Back to Tickets
            </router-link>
          </div>
          <h1 class="page-title">
            <span class="title-gradient">Create New Ticket</span>
          </h1>
          <p class="page-subtitle">Submit a new support ticket for assistance</p>
        </div>
        <div class="header-stats">
          <div class="live-indicator">
            <div class="live-dot"></div>
            <span>Ready</span>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="main-content">
      <div class="card form-card">
        <form @submit.prevent="saveTicket" class="ticket-form">
          <!-- Basic Information Section -->
          <div class="form-section">
            <h2 class="section-title">Basic Information</h2>
            <div class="section-divider"></div>

            <div class="form-group">
              <label for="site_name">Site Name *</label>
              <select
                id="site_name"
                v-model="currentTicket.selected_site_id"
                @change="onSiteChange"
                required
                class="form-select"
                :disabled="isLoadingRemotes"
              >
                <option value="">Select a site</option>
                <option
                  v-for="remote in remotes"
                  :key="remote.id"
                  :value="remote.id"
                >
                  {{ remote.site_name }} ({{ remote.site_id_poi || 'No ID' }})
                </option>
              </select>
              <small class="form-help">
                {{ isLoadingRemotes ? 'Loading sites...' : 'Select the site where the issue occurred' }}
              </small>
              <!-- Hidden field to store the title for API submission -->
              <input type="hidden" v-model="currentTicket.title" required>
            </div>

            <div class="form-group">
              <label for="description">Description</label>
              <textarea
                id="description"
                v-model="currentTicket.description"
                rows="6"
                placeholder="Describe the issue in detail, including any error messages, steps to reproduce, and affected systems..."
                class="form-textarea"
              ></textarea>
              <small class="form-help">Provide as much detail as possible to help us resolve your issue faster</small>
            </div>
          </div>

          <!-- Reporter Information Section -->
          <div class="form-section">
            <h2 class="section-title">Reporter Information</h2>
            <div class="section-divider"></div>

            <div class="form-row">
              <div class="form-group">
                <label for="reporter_name">Reporter Name *</label>
                <input
                  type="text"
                  id="reporter_name"
                  v-model="currentTicket.reporter_name"
                  required
                  placeholder="Enter your full name"
                  class="form-input"
                >
              </div>

              <div class="form-group">
                <label for="reporter_contact">Contact Information</label>
                <input
                  type="text"
                  id="reporter_contact"
                  v-model="currentTicket.reporter_contact"
                  placeholder="Email address or phone number"
                  class="form-input"
                >
                <small class="form-help">How we can reach you for updates</small>
              </div>
            </div>
          </div>

          <!-- Classification Section -->
          <div class="form-section">
            <h2 class="section-title">Ticket Classification</h2>
            <div class="section-divider"></div>

            <div class="form-row">
              <div class="form-group">
                <label for="category">Category *</label>
                <select id="category" v-model="currentTicket.category" required class="form-select">
                  <option value="">Select a category</option>
                  <option value="Network">Network Issues</option>
                  <option value="Hardware">Hardware Problems</option>
                  <option value="Software">Software Issues</option>
                  
                </select>
              </div>

              <div class="form-group">
                <label for="priority">Priority Level</label>
                <div class="priority-display">
                  <div class="priority-badge high">
                    <span class="priority-icon">🔥</span>
                    HIGH PRIORITY
                  </div>
                  <small class="form-help">All tickets are marked as High priority for immediate attention</small>
                </div>
                <!-- Hidden field to ensure HIGH priority is always submitted -->
                <input type="hidden" v-model="currentTicket.priority" value="High">
              </div>
            </div>

            <div class="form-group">
              <label for="assigned_to">Assign To (Optional)</label>
              <select id="assigned_to" v-model="currentTicket.assigned_to" class="form-select">
                <option value="">Auto-assign technician</option>
                <option value="1">Technician A</option>
                <option value="2">Technician B</option>
                <option value="3">Technician C</option>
              </select>
              <small class="form-help">Request a specific technician if needed</small>
            </div>
          </div>

          <!-- Form Actions -->
          <div class="form-actions">
            <router-link to="/tickets" class="secondary-button">
              Cancel
            </router-link>
            <button type="submit" class="primary-button" :disabled="isSubmitting">
              <div v-if="isSubmitting" class="loading-spinner"></div>
              <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 5V19M5 12H19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <span>{{ isSubmitting ? 'Creating Ticket...' : 'Create Ticket' }}</span>
            </button>
          </div>
        </form>
      </div>
    </main>

    <!-- Success Modal -->
    <transition name="modal-fade">
      <div v-if="showSuccessModal" class="modal-overlay" @click="closeSuccessModal">
        <div class="modal-content success-modal" @click.stop>
          <div class="success-icon">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z" fill="#10b981"/>
            </svg>
          </div>
          <h2 class="modal-title">Ticket Created Successfully!</h2>
          <p class="modal-message">
            Your ticket <strong>{{ createdTicketCode }}</strong> has been submitted successfully.
            You will receive updates at your provided contact information.
          </p>
          <div class="modal-actions">
            <router-link to="/tickets" class="primary-button">
              View All Tickets
            </router-link>
            <button @click="createAnotherTicket" class="secondary-button">
              Create Another Ticket
            </button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import type { TicketCreate } from '../api/ticketAPI';
import { ticketAPI } from '../api/ticketAPI';
import { remotesAPI, type Remote } from '../api/remotesAPI';

const router = useRouter();

// State management
const isSubmitting = ref(false);
const showSuccessModal = ref(false);
const createdTicketCode = ref('');
const remotes = ref<Remote[]>([]);
const isLoadingRemotes = ref(false);

interface FormTicket {
  title: string;
  description?: string;
  priority: string;
  reporter_name: string;
  reporter_contact?: string;
  category?: string;
  status?: string;
  assignee_id?: number;
  assigned_to?: string;
  selected_site_id?: number;
}

const currentTicket = ref<FormTicket>({
  title: '',
  description: '',
  priority: 'High',
  reporter_name: '',
  reporter_contact: '',
  category: '',
  assigned_to: '',
  status: 'Open',
  selected_site_id: undefined
});


const fetchRemotes = async () => {
  isLoadingRemotes.value = true;
  try {
    const response = await remotesAPI.getAllRemotes();
    remotes.value = response.data;
  } catch (error) {
    console.error('Error fetching remotes:', error);
    alert('Error loading site names. Please refresh the page.');
  } finally {
    isLoadingRemotes.value = false;
  }
};

const onSiteChange = () => {
  const selectedRemote = remotes.value.find(remote => remote.id === currentTicket.value.selected_site_id);
  if (selectedRemote) {
    currentTicket.value.title = selectedRemote.site_name;
  } else {
    currentTicket.value.title = '';
  }
};

const saveTicket = async () => {
  isSubmitting.value = true;

  try {
    const createData: TicketCreate = {
      title: currentTicket.value.title,
      description: currentTicket.value.description || '',
      priority: currentTicket.value.priority,
      reporter_name: currentTicket.value.reporter_name,
      reporter_contact: currentTicket.value.reporter_contact,
      category: currentTicket.value.category
    };

    const response = await ticketAPI.createTicket(createData);
    createdTicketCode.value = response.data.ticket_code;

    // Show success modal
    showSuccessModal.value = true;

  } catch (error) {
    console.error('Error creating ticket:', error);
    // You could add error handling here, like showing a toast or error message
    alert('Error creating ticket. Please try again.');
  } finally {
    isSubmitting.value = false;
  }
};

const closeSuccessModal = () => {
  showSuccessModal.value = false;
  router.push('/tickets');
};

const createAnotherTicket = () => {
  // Reset form
  currentTicket.value = {
    title: '',
    description: '',
    priority: 'High',
    reporter_name: '',
    reporter_contact: '',
    category: '',
    assigned_to: '',
    status: 'Open',
    selected_site_id: undefined
  };

  showSuccessModal.value = false;
};

onMounted(async () => {
  // Fetch remotes data
  await fetchRemotes();
});
</script>

<style scoped>
.create-ticket-page {
  background-color: #f8fafc;
  min-height: 100vh;
  font-family: 'Inter', sans-serif;
  padding: 1rem;
  width: 100%;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
}

/* Header Styles - Similar to Dashboard */
.page-header {
  background: #ffffff;
  border-radius: 1rem;
  padding: 2rem;
  margin-bottom: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 1px solid #e5e7eb;
  flex-shrink: 0;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  width: 100%;
}

.title-section {
  flex: 1;
}

.breadcrumb {
  margin-bottom: 1rem;
}

.breadcrumb-link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: #800000;
  text-decoration: none;
  font-weight: 500;
  font-size: 0.875rem;
  transition: color 0.2s ease;
}

.breadcrumb-link:hover {
  color: #5c0000;
}

.page-title {
  font-size: clamp(1.5rem, 3vw, 2rem);
  font-weight: 800;
  margin: 0 0 0.5rem 0;
  line-height: 1.1;
}

.title-gradient {
  background: linear-gradient(135deg, #800000 0%, #5c0000 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.page-subtitle {
  font-size: clamp(0.875rem, 1.5vw, 1rem);
  color: #64748b;
  margin: 0;
  line-height: 1.5;
  font-weight: 400;
}

.header-stats {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.live-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: rgba(128, 0, 0, 0.1);
  border-radius: 2rem;
  color: #800000;
  font-size: 0.875rem;
  font-weight: 500;
  border: 1px solid rgba(128, 0, 0, 0.2);
}

.live-dot {
  width: 8px;
  height: 8px;
  background: #800000;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

/* Main Content */
.main-content {
  width: 100%;
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 0 2rem;
}

.card {
  background-color: #ffffff;
  border-radius: 16px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  border: 1px solid #e2e8f0;
}

.form-card {
  padding: 2rem; /* Increased padding for more space */
  border-top: 4px solid transparent;
  background: linear-gradient(white, white) padding-box,
              linear-gradient(135deg, #800000, #5c0000) border-box;
  flex: 1;
  display: flex;
  flex-direction: column;
}

/* Form Styles */
.ticket-form {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  flex: 1;
  align-items: start;
}

.ticket-form > .form-section:nth-child(1) {
  grid-column: 1 / -1; /* Full width for first section */
}

.ticket-form > .form-section:nth-child(2) {
  grid-column: 1; /* Left column */
}

.ticket-form > .form-section:nth-child(3) {
  grid-column: 2; /* Right column */
}

.form-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  animation: fadeInUp 0.6s ease-out;
  animation-fill-mode: both;
  padding: 1.5rem;
  background-color: #f8fafc;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  min-height: 160px;
}

.form-section:nth-child(1) { animation-delay: 0.1s; }
.form-section:nth-child(2) { animation-delay: 0.2s; }
.form-section:nth-child(3) { animation-delay: 0.3s; }

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.section-title {
  font-size: 1rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 0.25rem 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.section-divider {
  height: 2px;
  background: linear-gradient(135deg, #800000 0%, #5c0000 100%);
  border-radius: 1px;
  opacity: 0.2;
  margin-bottom: 1rem;
  display: none; /* Hidden since we have section backgrounds now */
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.form-group label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.form-input,
.form-textarea,
.form-select {
  width: 100%;
  padding: 1rem 1.125rem;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 1rem;
  color: #374151;
  background-color: #f8fafc;
  transition: all 0.3s ease;
  box-sizing: border-box;
  font-family: 'Inter', sans-serif;
}

.form-input:focus,
.form-textarea:focus,
.form-select:focus {
  outline: none;
  border-color: #800000;
  box-shadow: 0 0 0 3px rgba(128, 0, 0, 0.1);
  background-color: #ffffff;
}

.form-textarea {
  resize: none;
  height: 100px;
  line-height: 1.5;
}

.form-select {
  cursor: pointer;
}

/* Priority Badge Styles */
.priority-display {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.priority-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  font-weight: 700;
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border: 2px solid;
}

.priority-badge.high {
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(220, 38, 38, 0.1) 100%);
  color: #dc2626;
  border-color: #dc2626;
  box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.1);
}

.priority-icon {
  font-size: 1rem;
  animation: flicker 2s infinite;
}

@keyframes flicker {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

.form-help {
  font-size: 0.75rem;
  color: #64748b;
  margin: 0;
  line-height: 1.4;
  margin-top: 0.25rem;
}

/* Buttons */
.form-actions {
  grid-column: 1 / -1; /* Full width */
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding: 1rem 2rem;
  border-top: 1px solid #e2e8f0;
  margin-top: auto;
  background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
  border-radius: 0 0 16px 16px;
  flex-shrink: 0; /* Don't shrink actions */
}

.primary-button {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #800000 0%, #5c0000 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
  height: 40px;
}

.primary-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(128, 0, 0, 0.3);
}

.primary-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.secondary-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  background: #ffffff;
  color: #64748b;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
  height: 40px;
  font-size: 0.9rem;
}

.secondary-button:hover {
  border-color: #800000;
  color: #800000;
  background: linear-gradient(135deg, rgba(128, 0, 0, 0.05) 0%, rgba(92, 0, 0, 0.05) 100%);
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid #ffffff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Success Modal */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

.modal-fade-enter-active .modal-content,
.modal-fade-leave-active .modal-content {
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.modal-fade-enter-from .modal-content,
.modal-fade-leave-to .modal-content {
  opacity: 0;
  transform: scale(0.9) translateY(20px);
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(17, 24, 39, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(8px);
}

.success-modal {
  background-color: #ffffff;
  border-radius: 16px;
  width: 100%;
  max-width: 500px;
  text-align: center;
  padding: 3rem 2rem;
  border: 1px solid #e2e8f0;
}

.success-icon {
  margin-bottom: 1.5rem;
  display: flex;
  justify-content: center;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 1rem 0;
}

.modal-message {
  font-size: 1rem;
  color: #64748b;
  line-height: 1.6;
  margin: 0 0 2rem 0;
}

.success-modal .modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  padding: 0;
  border: none;
  margin: 0;
}

/* Desktop Layout Improvements */
@media (min-width: 1024px) {
  .create-ticket-page {
    padding: 1.5rem 0 2rem 0; /* Compact padding for desktop */
  }

  .main-content {
    padding: 0 2rem;
  }

  .form-card {
    padding: 1.5rem 1.5rem 0 1.5rem;
  }

  .form-section {
    gap: 1rem;
    padding: 1.25rem;
    min-height: 180px; /* Optimized height for desktop */
  }

  .form-row {
    gap: 1.5rem;
  }

  .ticket-form {
    gap: 1.5rem;
  }

  .form-actions {
    padding: 1rem 1.5rem;
  }

  /* Ensure grid layout works on desktop */
  .ticket-form {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
  }

  .form-input,
  .form-textarea,
  .form-select {
    padding: 0.75rem 0.875rem;
    font-size: 0.9rem;
  }

  .primary-button,
  .secondary-button {
    padding: 0.625rem 1.25rem;
    font-size: 0.875rem;
    height: 36px;
  }
}

/* Tablet Responsive */
@media (max-width: 1024px) {
  .create-ticket-page {
    padding: 1rem 0.5rem;
  }

  .page-header {
    padding: 1.5rem;
    margin-bottom: 1rem;
  }

  .main-content {
    padding: 0 1rem;
  }

  .form-card {
    padding: 1.5rem;
  }

  .form-section {
    padding: 1.25rem;
    min-height: 140px;
  }

  .ticket-form {
    gap: 1.25rem;
  }

  .form-row {
    gap: 1rem;
  }

  .page-title {
    font-size: 1.5rem;
  }

  .page-subtitle {
    font-size: 0.875rem;
  }
}

/* Mobile Responsive */
@media (max-width: 768px) {
  .create-ticket-page {
    padding: 0.75rem 0;
    padding-bottom: 2rem; /* Space for mobile */
  }

  .page-header {
    padding: 1.25rem;
    margin-bottom: 1rem;
    flex-direction: column;
    gap: 1rem;
  }

  .header-content {
    flex-direction: column;
    gap: 1rem;
  }

  .header-stats {
    align-self: flex-start;
  }

  .main-content {
    padding: 0 0.75rem;
  }

  .form-card {
    padding: 1.25rem;
  }

  /* Reset to single column layout on mobile */
  .ticket-form {
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
  }

  .form-section {
    padding: 1.25rem;
    min-height: auto; /* Remove fixed height on mobile */
  }

  .form-row {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .form-group {
    gap: 0.625rem;
  }

  .form-input,
  .form-textarea,
  .form-select {
    padding: 0.875rem 1rem;
    font-size: 0.9rem;
  }

  .form-textarea {
    height: 80px;
  }

  .form-help {
    font-size: 0.7rem;
  }

  .form-actions {
    flex-direction: column;
    padding: 1.25rem;
    gap: 0.75rem;
  }

  .primary-button,
  .secondary-button {
    width: 100%;
    justify-content: center;
    padding: 0.875rem 1.25rem;
    font-size: 0.9rem;
  }

  .page-title {
    font-size: 1.375rem;
  }

  .page-subtitle {
    font-size: 0.8rem;
  }

  .breadcrumb {
    margin-bottom: 0.75rem;
  }

  .breadcrumb-link {
    font-size: 0.8rem;
  }

  .live-indicator {
    padding: 0.5rem 1rem;
    font-size: 0.8rem;
  }
}

/* Small Mobile */
@media (max-width: 480px) {
  .create-ticket-page {
    padding: 0.5rem 0;
  }

  .page-header {
    padding: 1rem;
  }

  .main-content {
    padding: 0 0.5rem;
  }

  .form-card {
    padding: 1rem;
    border-radius: 12px;
  }

  .form-section {
    padding: 1rem;
    border-radius: 8px;
  }

  .form-row {
    gap: 0.75rem;
  }

  .form-group {
    gap: 0.5rem;
  }

  .form-input,
  .form-textarea,
  .form-select {
    padding: 0.75rem 0.875rem;
    font-size: 0.875rem;
  }

  .form-textarea {
    height: 70px;
  }

  .form-actions {
    padding: 1rem;
    gap: 0.625rem;
  }

  .primary-button,
  .secondary-button {
    padding: 0.75rem 1rem;
    font-size: 0.875rem;
    height: 44px;
  }

  .page-title {
    font-size: 1.25rem;
  }

  .page-subtitle {
    font-size: 0.75rem;
  }

  .section-title {
    font-size: 0.9rem;
  }

  .form-group label {
    font-size: 0.8rem;
  }

  .form-help {
    font-size: 0.65rem;
  }
}
</style>