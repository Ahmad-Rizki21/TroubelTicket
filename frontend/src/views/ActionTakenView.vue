<template>
  <div class="action-taken-page">
    <!-- Page Header -->
    <header class="page-header">
      <div class="header-content">
        <h1 class="page-title">Action Taken for Ticket #{{ ticketId }}: {{ ticket?.title }}</h1>
        <p class="page-subtitle">Track all actions taken on this ticket.</p>
      </div>
      <div class="header-actions">
        <button class="secondary-button" @click="goBack">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M19 12H5M12 19L5 12L12 5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span>Back to Tickets</span>
        </button>
      </div>
    </header>

    <!-- Ticket Info Card -->
    <div class="card ticket-info-card">
      <div class="ticket-info-grid">
        <div class="info-item">
          <span class="info-label">Ticket ID</span>
          <span class="info-value">{{ ticket?.ticket_code }}</span>
        </div>
        <div class="info-item">
          <span class="info-label">Status</span>
          <span v-if="ticket?.status" class="status-badge" :class="`status-${ticket.status.toLowerCase().replace(' ', '-')}`">
            {{ ticket.status }}
          </span>
        </div>
        <div class="info-item">
          <span class="info-label">Priority</span>
          <span v-if="ticket?.priority" class="priority-badge" :class="`priority-${ticket.priority.toLowerCase()}`">
            {{ ticket.priority }}
          </span>
        </div>
        <div class="info-item">
          <span class="info-label">Reporter</span>
          <span class="info-value">{{ ticket?.reporter_name }}</span>
        </div>
        <div class="info-item">
          <span class="info-label">Created</span>
          <span class="info-value">{{ formatDate(ticket?.created_at) }}</span>
        </div>
        <div class="info-item" v-if="ticket?.closed_at">
          <span class="info-label">Closed</span>
          <span class="info-value">{{ formatDate(ticket?.closed_at) }}</span>
        </div>
      </div>
    </div>

    <div class="action-layout">
      <div class="left-column">
        <!-- Add/Edit Action Form -->
        <div class="card add-action-card" ref="formCard">
          <h3>{{ isEditingAction ? 'Edit Action' : 'Add New Action' }}</h3>
          <form @submit.prevent="submitAction" class="add-action-form">
            <div class="form-group">
              <label for="action-description">Action Description *</label>
              <textarea 
                id="action-description" 
                v-model="currentAction.description" 
                rows="3" 
                placeholder="Describe the action taken..."
                required
                class="form-input"
              ></textarea>
            </div>
            
            <div class="form-group">
              <label for="action-user">Re-assign Ticket To (Optional)</label>
              <select 
                id="action-user" 
                v-model="currentAction.assignee_id"
                class="form-input"
              >
                <option :value="undefined">Select a user</option>
                <option v-for="user in users" :key="user.id" :value="user.id">
                  {{ user.username }}
                </option>
              </select>
            </div>
            
            <div v-if="ticket?.status !== 'Closed' && !isEditingAction" class="form-row">
              <div class="form-group">
                <label for="new-status">Change Ticket Status (Optional)</label>
                <select 
                  id="new-status" 
                  v-model="currentAction.new_status"
                  class="form-input"
                >
                  <option value="">Keep current status</option>
                  <option value="Open">Open</option>
                  <option value="Closed">Closed</option>
                </select>
              </div>
            </div>
            
            <div v-if="currentAction.new_status === 'Closed'" class="summary-fields">
              <div class="form-group">
                <label for="summary-problem">Summary Problem *</label>
                <textarea 
                  id="summary-problem" 
                  v-model="currentAction.summary_problem" 
                  rows="2" 
                  placeholder="Describe the problem that was resolved..."
                  class="form-input"
                  required
                ></textarea>
              </div>
              <div class="form-group">
                <label for="summary-action">Summary Action *</label>
                <textarea 
                  id="summary-action" 
                  v-model="currentAction.summary_action" 
                  rows="2" 
                  placeholder="Describe the action taken to resolve the problem..."
                  class="form-input"
                  required
                ></textarea>
              </div>
            </div>
            
            <div class="form-group">
              <label>Evidence File (Optional)</label>
              <label for="action-image" class="file-upload-button">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><polyline points="17 8 12 3 7 8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><line x1="12" y1="3" x2="12" y2="15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                  <span>{{ currentAction.image ? 'Change file' : 'Upload a file' }}</span>
              </label>
              <input 
                type="file" 
                id="action-image" 
                accept="image/*,.txt,.log,.json" 
                @change="onImageChange"
                class="file-upload-input"
              />
              <div v-if="fileName" class="selected-file">
                Selected: {{ fileName }}
              </div>
            </div>
            
            <div class="form-group">
              <label for="action-text">Text Evidence (Optional)</label>
              <textarea 
                id="action-text" 
                v-model="currentAction.text_content" 
                rows="4" 
                placeholder="Paste command output or other text evidence here..."
                class="form-input"
              ></textarea>
            </div>
            
            <div class="form-actions">
              <button v-if="isEditingAction" type="button" class="secondary-button" @click="cancelEditAction">Cancel</button>
              <button 
                type="submit"
                class="primary-button"
                :disabled="!currentAction.description.trim() || (currentAction.new_status === 'Closed' && (!currentAction.summary_problem.trim() || !currentAction.summary_action.trim()))"
              >
                {{ isEditingAction ? 'Update Action' : 'Add Action' }}
              </button>
            </div>
          </form>
        </div>

        <!-- Downtime Timer Card -->
        <div class="card downtime-card">
          <h4>TICKET DOWNTIME</h4>
          <div class="timer-display">
            <div class="time-segment">
              <span class="time-value">{{ downtime.days }}</span>
              <span class="time-label">Days</span>
            </div>
            <div class="time-separator">:</div>
            <div class="time-segment">
              <span class="time-value">{{ downtime.hours }}</span>
              <span class="time-label">Hours</span>
            </div>
            <div class="time-separator">:</div>
            <div class="time-segment">
              <span class="time-value">{{ downtime.minutes }}</span>
              <span class="time-label">Minutes</span>
            </div>
            <div class="time-separator">:</div>
            <div class="time-segment">
              <span class="time-value">{{ downtime.seconds }}</span>
              <span class="time-label">Seconds</span>
            </div>
          </div>
          <div class="timer-status-label">
            <span v-if="ticket?.status !== 'Closed'">Ticket is currently open</span>
            <span v-else>Total time until closed</span>
          </div>
        </div>
      </div>

      <!-- Actions History -->
      <div class="card actions-history-card">
        <h3>Action History ({{ currentTicketActions.length }})</h3>
        <div v-if="loading" class="loading-state">
          Loading actions...
        </div>
        <div v-else-if="currentTicketActions.length === 0" class="no-actions">
          No actions recorded for this ticket yet.
        </div>
        <div v-else class="action-list">
          <div 
            v-for="action in currentTicketActions" 
            :key="action.id" 
            class="action-item"
          >
            <div class="action-header">
              <div class="action-user">
                <strong>{{ action.user?.username || 'Unknown User' }}</strong>
                <span v-if="action.role && action.role.name" class="action-role">({{ action.role.name }})</span>
              </div>
              <div class="action-controls">
                <button class="control-button edit" @click="startEditAction(action)" title="Edit Action">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M11 4H4C3.46957 4 2.96086 4.21071 2.58579 4.58579C2.21071 4.96086 2 5.46957 2 6V20C2 20.5304 2.21071 21.0391 2.58579 21.4142C2.96086 21.7893 3.46957 22 4 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                </button>
                <div class="action-date">
                  {{ formatDate(action.created_at) }}
                </div>
              </div>
            </div>
            <div class="action-description">
              {{ action.action_description }}
            </div>
            <div v-if="action.action_image_url" class="action-evidence">
              <img 
                v-if="isImageFile(action.action_image_url)" 
                :src="getImageUrl(action.action_image_url)" 
                alt="Action evidence" 
                class="action-evidence-image"
                @click="openImageModal(getImageUrl(action.action_image_url))"
              >
              <div v-else class="action-evidence-text">
                <div class="text-evidence-header">
                  <span>Text Evidence</span>
                  <a :href="getImageUrl(action.action_image_url)" target="_blank" download class="download-link">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M21 15V19C21 19.5304 20.7893 20.0391 20.4142 20.4142C20.0391 20.7893 19.5304 21 19 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M7 10L12 15L17 10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M12 15V3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                  </a>
                </div>
                <button class="view-text-button" @click="viewTextContent(getImageUrl(action.action_image_url))">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><polyline points="14 2 14 8 20 8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><line x1="16" y1="13" x2="8" y2="13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><line x1="16" y1="17" x2="8" y2="17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><polyline points="10 9 8 9 8 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                  <span>View Text Content</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Text Content Modal -->
  <transition name="modal-fade">
    <div v-if="showTextModal" class="modal-overlay" @click="showTextModal = false">
      <div class="modal-content text-modal" @click.stop style="max-width: 800px; width: 90%; max-height: 80vh;">
        <div class="modal-header">
          <h2 class="modal-title">Text Evidence Content</h2>
          <button class="close-button" @click="showTextModal = false">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
          </button>
        </div>
        <div class="text-content-display">
          <pre>{{ textContent }}</pre>
        </div>
      </div>
    </div>
  </transition>

  <!-- Image Viewer Modal -->
  <transition name="modal-fade">
    <div v-if="showImageModal" class="modal-overlay image-overlay" @click="showImageModal = false">
        <img :src="imageModalSrc" class="enlarged-image" @click.stop/>
        <button class="close-button modal-close-btn" @click="showImageModal = false">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </button>
    </div>
  </transition>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { ticketAPI, type Ticket, type TicketUpdate } from '../api/ticketAPI';
import { ticketActionAPI, type TicketAction } from '../api/ticketActionAPI';
import { userAPI, type User } from '../api/userAPI';
import { roleAPI, type Role } from '../api/roleAPI';

const route = useRoute();
const router = useRouter();

const ticketId = ref<number>(parseInt(route.params.id as string, 10));

// State
const ticket = ref<Ticket | null>(null);
const currentTicketActions = ref<TicketAction[]>([]);
const users = ref<User[]>([]);
const roles = ref<Role[]>([]);
const loading = ref(false);
const showTextModal = ref(false);
const textContent = ref('');
const showImageModal = ref(false);
const imageModalSrc = ref('');
const formCard = ref<HTMLElement | null>(null);

// Downtime Timer State
const downtime = ref({ days: '0', hours: '00', minutes: '00', seconds: '00' });
const downtimeInterval = ref<number | null>(null);

// Editing State
const isEditingAction = ref(false);
const actionToEdit = ref<TicketAction | null>(null);

const currentAction = ref({
  description: '',
  image: null as File | null,
  text_content: '',
  assignee_id: undefined as number | undefined,
  new_status: undefined as string | undefined,
  summary_problem: '',
  summary_action: ''
});

const fileName = computed(() => {
    if (currentAction.value.image) {
        return currentAction.value.image.name;
    }
    if (isEditingAction.value && actionToEdit.value?.action_image_url) {
        return actionToEdit.value.action_image_url.split('/').pop();
    }
    return '';
});

// --- Methods ---

const loadTicketAndActions = async () => {
  loading.value = true;
  try {
    const [ticketResponse, actionsResponse] = await Promise.all([
        ticketAPI.getTicketById(ticketId.value),
        ticketActionAPI.getTicketActions(ticketId.value)
    ]);
    ticket.value = ticketResponse.data;
    currentTicketActions.value = actionsResponse.data.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());
  } catch (error) {
    console.error('Error loading ticket or actions:', error);
  } finally {
    loading.value = false;
  }
};

const loadUsersAndRoles = async () => {
  try {
    const [usersResponse, rolesResponse] = await Promise.all([
      userAPI.getAllUsers(),
      roleAPI.getAllRoles()
    ]);
    users.value = usersResponse.data;
    roles.value = rolesResponse.data;
  } catch (error) {
    console.error('Error loading users or roles:', error);
  }
};

const onImageChange = (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files[0]) {
    currentAction.value.image = target.files[0];
  }
};

const resetForm = () => {
    currentAction.value = {
        description: '',
        image: null,
        text_content: '',
        assignee_id: undefined,
        new_status: undefined,
        summary_problem: '',
        summary_action: ''
    };
    isEditingAction.value = false;
    actionToEdit.value = null;

    const fileInput = document.getElementById('action-image') as HTMLInputElement;
    if(fileInput) fileInput.value = '';
};

const submitAction = async () => {
  if (!currentAction.value.description.trim()) return;
  
  const formData = new FormData();
  formData.append('action_description', currentAction.value.description);

  if (currentAction.value.assignee_id) formData.append('assignee_id', String(currentAction.value.assignee_id));

  if (currentAction.value.image) {
    formData.append('action_image', currentAction.value.image);
  } else if (currentAction.value.text_content) {
    const textBlob = new Blob([currentAction.value.text_content], { type: 'text/plain' });
    formData.append('action_image', textBlob, 'evidence.txt');
  }

  try {
    if (isEditingAction.value && actionToEdit.value) {
        const updatedAction = await ticketActionAPI.updateTicketAction(ticketId.value, actionToEdit.value.id, formData);
        const index = currentTicketActions.value.findIndex(a => a.id === actionToEdit.value!.id);
        if (index !== -1) {
            currentTicketActions.value[index] = updatedAction.data;
        }
    } else {
        const newActionResponse = await ticketActionAPI.createTicketAction(ticketId.value, formData);
        currentTicketActions.value.unshift(newActionResponse.data);

        if (currentAction.value.new_status && ticket.value) {
            const updateData: Partial<TicketUpdate> = { status: currentAction.value.new_status };
            if (currentAction.value.new_status === 'Closed') {
                updateData.summary_problem = currentAction.value.summary_problem;
                updateData.summary_action = currentAction.value.summary_action;
            }
            const updatedTicket = await ticketAPI.updateTicket(ticket.value.id, updateData);
            ticket.value = updatedTicket.data;
        }
    }

    if (currentAction.value.assignee_id || currentAction.value.new_status) {
        const ticketResponse = await ticketAPI.getTicketById(ticketId.value);
        ticket.value = ticketResponse.data;
    }
    resetForm();
  } catch (error) {
    console.error('Error submitting action:', error);
  }
};

const startEditAction = (action: TicketAction) => {
    isEditingAction.value = true;
    actionToEdit.value = action;

    currentAction.value = {
        description: action.action_description,
        image: null,
        text_content: '',
        assignee_id: undefined,
        new_status: undefined,
        summary_problem: '',
        summary_action: ''
    };

    formCard.value?.scrollIntoView({ behavior: 'smooth', block: 'center' });
};

const cancelEditAction = () => {
    resetForm();
}

// --- Timer Logic ---
const formatDuration = (ms: number) => {
    if (ms < 0) ms = 0;
    const totalSeconds = Math.floor(ms / 1000);
    const days = Math.floor(totalSeconds / 86400);
    const hours = Math.floor((totalSeconds % 86400) / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    const seconds = totalSeconds % 60;

    return {
        days: String(days),
        hours: String(hours).padStart(2, '0'),
        minutes: String(minutes).padStart(2, '0'),
        seconds: String(seconds).padStart(2, '0'),
    };
};

const startOrUpdateDowntimeTimer = () => {
    if (downtimeInterval.value) {
        clearInterval(downtimeInterval.value);
        downtimeInterval.value = null;
    }
    if (!ticket.value) return;

    const startTime = new Date(ticket.value.created_at).getTime();

    const updateDisplay = () => {
        const endTime = ticket.value?.status === 'Closed' && ticket.value.closed_at 
            ? new Date(ticket.value.closed_at).getTime() 
            : new Date().getTime();
        downtime.value = formatDuration(endTime - startTime);
    };

    updateDisplay();

    if (ticket.value.status !== 'Closed') {
        downtimeInterval.value = window.setInterval(updateDisplay, 1000);
    }
};

// --- Utility Methods ---
const formatDate = (dateString: string | undefined) => {
  if (!dateString) return '-';
  const date = new Date(dateString);
  return isNaN(date.getTime()) ? '-' : date.toLocaleDateString('en-US', { day: '2-digit', month: 'long', year: 'numeric' });
};

const getImageUrl = (path: string) => {
  if (!path || path.startsWith('http')) return path;
  const baseUrl = (import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000').replace(/\/$/, '');
  const imagePath = path.replace(/^\//, '');
  return `${baseUrl}/${imagePath}`;
};

const isImageFile = (url: string) => {
  if (!url) return false;
  return /\.(jpg|jpeg|png|gif|bmp|webp|svg)$/i.test(url.toLowerCase());
};

const viewTextContent = async (url: string) => {
  try {
    const response = await fetch(url);
    if (response.ok) {
      textContent.value = await response.text();
      showTextModal.value = true;
    } else {
      textContent.value = "Unable to load text content.";
      showTextModal.value = true;
    }
  } catch (error) {
    console.error('Error loading text content:', error);
    textContent.value = "An error occurred while loading the content.";
    showTextModal.value = true;
  }
};

const openImageModal = (src: string) => {
    imageModalSrc.value = src;
    showImageModal.value = true;
}

const goBack = () => {
  router.push({ name: 'Tickets' });
};

// --- Lifecycle Hooks ---
onMounted(async () => {
  await loadTicketAndActions();
  await loadUsersAndRoles();
});

onUnmounted(() => {
    if (downtimeInterval.value) {
        clearInterval(downtimeInterval.value);
    }
});

watch(ticket, (newTicket) => {
    if (newTicket) {
        startOrUpdateDowntimeTimer();
    }
}, { deep: true });

</script>

<style scoped>
/* Main Page Layout */
.action-taken-page {
  background-color: #f8fafc;
  padding: 2rem;
  font-family: 'Inter', sans-serif;
}

.card {
  background-color: #ffffff;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
  margin-bottom: 1.5rem;
  overflow: hidden;
}

/* Header */
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem; flex-wrap: wrap; gap: 1rem; }
.page-title { font-size: 2rem; font-weight: 800; color: #1e293b; margin: 0; }
.page-subtitle { font-size: 1.1rem; color: #64748b; margin-top: 0.25rem; }

/* Buttons */
.primary-button, .secondary-button {
  display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.75rem 1.5rem;
  border-radius: 12px; font-size: 1rem; font-weight: 600; cursor: pointer; transition: all 0.3s ease; border: 1px solid transparent;
}
.primary-button { background-color: #ff4d4f; color: white; }
.primary-button:hover { background-color: #d9363e; box-shadow: 0 4px 15px rgba(255, 77, 79, 0.2); }
.primary-button:disabled { opacity: 0.6; cursor: not-allowed; background-color: #fca5a5; }
.secondary-button { background: #ffffff; color: #475569; border-color: #e2e8f0; }
.secondary-button:hover { background-color: #f1f5f9; border-color: #cbd5e1; }

/* Ticket Info Card */
.ticket-info-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1.5rem; padding: 1.5rem; }
.info-item { display: flex; flex-direction: column; }
.info-label { font-size: 0.875rem; font-weight: 600; color: #64748b; margin-bottom: 0.5rem; }
.info-value { font-size: 1rem; color: #1e293b; }

/* Badges */
.status-badge, .priority-badge { padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; display: inline-block; }
.status-open { background-color: #fee2e2; color: #dc2626; }
.status-in-progress { background-color: #fef3c7; color: #d97706; }
.status-closed { background-color: #d1fae5; color: #059669; }
.status-on-hold { background-color: #e5e7eb; color: #374151; }
.priority-high { background-color: #fecaca; color: #b91c1c; }
.priority-medium { background-color: #fed7aa; color: #c2410c; }
.priority-low { background-color: #bfdbfe; color: #1d4ed8; }

/* Two-column Layout */
.action-layout {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
}
.left-column { display: flex; flex-direction: column; gap: 1.5rem; }

@media (min-width: 1024px) {
  .action-layout {
    grid-template-columns: minmax(450px, 1fr) 2fr;
    align-items: flex-start;
  }
}

/* Form & History Cards */
.add-action-card, .actions-history-card { padding: 1.5rem; }
.add-action-card h3, .actions-history-card h3 {
  color: #1e293b;
  font-size: 1.5rem; font-weight: 700; margin-top: 0; margin-bottom: 1.5rem;
  padding-bottom: 1rem; border-bottom: 1px solid #e2e8f0;
}

/* Form Styles */
.add-action-form { display: flex; flex-direction: column; gap: 1.25rem; }
.form-group { position: relative; }
.form-group label { font-size: 0.875rem; font-weight: 600; color: #334155; margin-bottom: 0.5rem; display: block; }
.form-input, .form-group select {
  width: 100%; padding: 0.75rem 1rem; border: 1px solid #d1d5db; border-radius: 12px;
  font-size: 1rem; transition: all 0.3s ease; background-color: #f9fafb; box-sizing: border-box;
}
.form-input:focus, .form-group select:focus { outline: none; border-color: #ff4d4f; box-shadow: 0 0 0 3px rgba(255, 77, 79, 0.2); background-color: #ffffff; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1.25rem; }
.form-actions { display: flex; justify-content: flex-end; gap: 1rem; margin-top: 1rem; }

/* Custom File Input */
.file-upload-input { display: none; }
.file-upload-button {
    display: inline-flex; align-items: center; gap: 0.75rem; padding: 0.75rem 1rem; border-radius: 12px;
    background-color: #f9fafb; border: 1px dashed #d1d5db; color: #475569; font-weight: 600;
    cursor: pointer; transition: all 0.2s ease-in-out; width: 100%; justify-content: center;
}
.file-upload-button:hover { background-color: #f1f5f9; border-color: #ff4d4f; color: #1e293b; }
.selected-file { margin-top: 0.75rem; font-size: 0.875rem; color: #4b5563; font-style: italic; }

.summary-fields { margin: 1rem 0; padding: 1rem; background-color: #fefce8; border-radius: 8px; border: 1px solid #fef08a; }

/* Downtime Card */
.downtime-card {
    padding: 1.5rem;
    text-align: center;
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
}
.downtime-card h4 {
    margin-top: 0;
    margin-bottom: 1.5rem;
    color: #1e293b;
    font-size: 1rem;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
}
.timer-display {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 0.5rem;
}
.time-segment {
    display: flex;
    flex-direction: column;
    align-items: center;
    background-color: #f8fafc;
    padding: 0.75rem 1rem;
    border-radius: 8px;
    border: 1px solid #e2e8f0;
    min-width: 70px;
}
.time-value {
    font-size: 2.5rem;
    font-weight: 700;
    color: #ff4d4f;
    font-family: 'Courier New', Courier, monospace;
}
.time-label {
    font-size: 0.75rem;
    color: #64748b;
    text-transform: uppercase;
}
.time-separator {
    font-size: 2rem;
    font-weight: 700;
    color: #cbd5e1;
    padding-bottom: 1.2rem; /* Align with numbers */
}
.timer-status-label {
    margin-top: 1.5rem;
    font-size: 0.875rem;
    color: #64748b;
    text-align: center;
}

/* Actions History */
.no-actions, .loading-state { text-align: center; padding: 3rem 1rem; color: #64748b; font-style: italic; }
.action-list { display: flex; flex-direction: column; gap: 1.5rem; }
.action-item { padding: 1.5rem; border: 1px solid #e2e8f0; border-radius: 12px; background-color: #fdfdff; }
.action-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; padding-bottom: 0.75rem; border-bottom: 1px solid #e2e8f0; }
.action-user { font-weight: 600; color: #1e293b; display: flex; align-items: center; gap: 0.5rem; }
.action-role { font-weight: normal; font-size: 0.875rem; background-color: #e5e7eb; padding: 0.125rem 0.5rem; border-radius: 9999px; color: #475569; }
.action-date { font-size: 0.875rem; color: #64748b; }
.action-controls { display: flex; align-items: center; gap: 1rem; }
.control-button { background: none; border: none; cursor: pointer; color: #9ca3af; padding: 0.25rem; }
.control-button:hover { color: #1e293b; }
.action-description { margin-bottom: 1rem; color: #334155; line-height: 1.6; white-space: pre-wrap; }

/* Evidence Styles */
.action-evidence { margin-top: 1rem; }
.action-evidence-image { max-width: 100%; height: auto; border-radius: 8px; border: 1px solid #e2e8f0; cursor: pointer; transition: transform 0.2s; }
.action-evidence-image:hover { transform: scale(1.02); }
.action-evidence-text { background-color: #f1f5f9; border: 1px solid #cbd5e1; border-radius: 8px; padding: 1rem; max-width: 100%; }
.text-evidence-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; padding-bottom: 0.5rem; border-bottom: 1px solid #cbd5e1; font-weight: 600; color: #1e293b; }
.download-link { color: #3b82f6; cursor: pointer; }
.view-text-button { display: inline-flex; align-items: center; gap: 0.5rem; width: 100%; justify-content: center; padding: 0.75rem 1rem; border: 1px solid #e2e8f0; border-radius: 12px; background: #f8fafc; color: #334155; font-weight: 600; cursor: pointer; transition: all 0.3s ease; margin-top: 0.75rem; }
.view-text-button:hover { background-color: #f1f5f9; border-color: #cbd5e1; color: #1e293b; }

/* Modal Styles */
.modal-fade-enter-active, .modal-fade-leave-active { transition: opacity 0.3s ease; }
.modal-fade-enter-from, .modal-fade-leave-to { opacity: 0; }
.modal-overlay { position: fixed; inset: 0; background: rgba(17, 24, 39, 0.7); display: flex; align-items: center; justify-content: center; z-index: 1000; backdrop-filter: blur(4px); }
.modal-content { background-color: #f8fafc; border-radius: 20px; width: 100%; max-width: 600px; max-height: 90vh; display: flex; flex-direction: column; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1); }
.modal-header { display: flex; justify-content: space-between; align-items: center; padding: 1.5rem 2rem; background-color: #1f2937; color: #fff; border-top-left-radius: 20px; border-top-right-radius: 20px; }
.modal-title { font-size: 1.25rem; font-weight: 600; }
.close-button { background: transparent; border: none; color: #9ca3af; cursor: pointer; padding: 0.5rem; transition: color 0.2s; }
.close-button:hover { color: #fff; }

/* Text Content Modal */
.text-content-display { padding: 1rem; background-color: #1e293b; border-radius: 0 0 16px 16px; overflow: auto; max-height: calc(80vh - 70px); }
.text-content-display pre {
  white-space: pre-wrap; word-wrap: break-word; margin: 0;
  font-family: 'Fira Code', 'Courier New', monospace;
  font-size: 0.9rem; line-height: 1.7;
  color: #d1d5db;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Image Viewer Modal */
.image-overlay { padding: 2rem; }
.enlarged-image { max-width: 95vw; max-height: 90vh; object-fit: contain; border-radius: 8px; box-shadow: 0 0 40px rgba(0,0,0,0.5); }
.modal-close-btn { position: absolute; top: 1rem; right: 1rem; color: white; background: rgba(0,0,0,0.3); border-radius: 50%; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; }
.modal-close-btn:hover { background: rgba(0,0,0,0.6); }

/* Responsive */
@media (max-width: 768px) {
  .action-taken-page { padding: 1rem; }
  .page-header { flex-direction: column; align-items: flex-start; }
  .form-row { grid-template-columns: 1fr; }
}
</style>
