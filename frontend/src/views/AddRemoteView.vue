<template>
  <div class="add-remote-page">
    <!-- Page Header -->
    <header class="page-header">
      <div class="header-content">
        <div class="title-section">
          <div class="breadcrumb">
            <router-link to="/remotes" class="breadcrumb-link">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M15 18L9 12L15 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              Back to Remotes
            </router-link>
          </div>
          <h1 class="page-title">
            <span class="title-gradient">Add New Remote</span>
          </h1>
          <p class="page-subtitle">Fill in the details for the new remote location.</p>
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
        <form @submit.prevent="createRemote" class="remote-form">
        <div class="form-section">
          <h3>Basic Information</h3>
          <div class="form-row">
            <div class="form-group">
              <label for="site_id_poi">Site ID POI</label>
              <input type="text" id="site_id_poi" v-model="remoteData.site_id_poi" placeholder="e.g., ID001">
            </div>
            <div class="form-group">
              <label for="site_name">Site Name *</label>
              <input type="text" id="site_name" v-model="remoteData.site_name" required placeholder="e.g., BTS Tower Central">
            </div>
          </div>
          <div class="form-group">
            <label for="notes">Notes</label>
            <textarea id="notes" v-model="remoteData.notes" rows="3" placeholder="e.g., Additional information..."></textarea>
          </div>
        </div>



        <div class="form-section">
          <h3>Network Information</h3>
          <div class="form-row">
            <div class="form-group">
              <label for="origin_backbone">Origin Backbone</label>
              <input type="text" id="origin_backbone" v-model="remoteData.origin_backbone" placeholder="e.g., Backbone Site A">
            </div>
            <div class="form-group">
              <label for="origin_bb">Origin BB</label>
              <input type="text" id="origin_bb" v-model="remoteData.origin_bb" placeholder="e.g., BBA001">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label for="terminating_bb">Terminating BB</label>
              <input type="text" id="terminating_bb" v-model="remoteData.terminating_bb" placeholder="e.g., TBB001">
            </div>
            <div class="form-group">
              <label for="link">Link</label>
              <input type="text" id="link" v-model="remoteData.link" placeholder="e.g., Link Type">
            </div>
          </div>
        </div>

        <div class="form-section">
          <h3>Technical Information</h3>
          <div class="form-row">
            <div class="form-group">
              <label for="latitude">Latitude *</label>
              <input type="number" step="any" id="latitude" v-model.number="remoteData.latitude" required placeholder="e.g., -6.2088">
            </div>
            <div class="form-group">
              <label for="longitude">Longitude *</label>
              <input type="number" step="any" id="longitude" v-model.number="remoteData.longitude" required placeholder="e.g., 106.8456">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label for="jumlah_bts">Jumlah BTS</label>
              <input type="number" id="jumlah_bts" v-model.number="remoteData.jumlah_bts" placeholder="e.g., 5">
            </div>
            <div class="form-group">
              <label for="bw">Bandwidth (BW)</label>
              <input type="text" id="bw" v-model="remoteData.bw" placeholder="e.g., 100 Mbps">
            </div>
          </div>
          <div class="form-group">
            <label for="vlan">VLAN</label>
            <input type="text" id="vlan" v-model="remoteData.vlan" placeholder="e.g., VLAN100">
          </div>
        </div>

        <div class="form-actions">
          <router-link to="/remotes" class="secondary-button">
            <span>Cancel</span>
          </router-link>
          <button type="submit" class="primary-button" :disabled="loading">
            <span v-if="!loading">Create Remote</span>
            <span v-else>Creating...</span>
          </button>
        </div>
      </form>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { remoteAPI, type RemoteCreate } from '../api/remoteAPI';

// --- State ---
const router = useRouter();
const loading = ref(false);
const remoteData = ref<RemoteCreate>({ 
  site_id_poi: '', 
  site_name: '', 
  notes: '', 
  latitude: 0, 
  longitude: 0, 
  origin_backbone: '',
  origin_bb: '',
  terminating_bb: '',
  link: '',
  jumlah_bts: null,
  bw: '',
  vlan: ''
});

// --- Form Submission ---
const createRemote = async () => {
  if (!remoteData.value.site_name || remoteData.value.latitude === 0 || remoteData.value.longitude === 0) {
    alert('Site Name, Latitude, and Longitude are required.');
    return;
  }

  loading.value = true;
  try {
    await remoteAPI.createRemote(remoteData.value);
    router.push('/remotes'); // Redirect to remotes list after successful creation
  } catch (error) {
    console.error("Failed to create remote:", error);
    // Show user-friendly error message
    alert(`Failed to create remote: ${error instanceof Error ? error.message : 'Unknown error'}`);
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.add-remote-page {
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
  padding: 2rem;
  border-top: 4px solid transparent;
  background: linear-gradient(white, white) padding-box,
              linear-gradient(135deg, #800000, #5c0000) border-box;
  flex: 1;
  display: flex;
  flex-direction: column;
}

/* Buttons */
.primary-button, .secondary-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid transparent;
  text-decoration: none;
  height: 40px;
}
.primary-button {
  background: linear-gradient(135deg, #800000 0%, #5c0000 100%);
  color: white;
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
  background: #ffffff;
  color: #64748b;
  border-color: #e2e8f0;
}
.secondary-button:hover {
  border-color: #800000;
  color: #800000;
  background: linear-gradient(135deg, rgba(128, 0, 0, 0.05) 0%, rgba(92, 0, 0, 0.05) 100%);
}



/* Form Styles */
.remote-form {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  flex: 1;
  align-items: start;
}

.remote-form > .form-section:nth-child(1) {
  grid-column: 1 / -1; /* Full width for first section */
}

.remote-form > .form-section:nth-child(2) {
  grid-column: 1; /* Left column */
}

.remote-form > .form-section:nth-child(3) {
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
  min-height: 180px;
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

.form-section h3 {
  font-size: 1rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 0.25rem 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
.form-group label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}
.form-group input,
.form-group textarea {
  width: 100%;
  padding: 1rem 1.125rem;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 1rem;
  color: #374151;
  transition: all 0.3s ease;
  background-color: #f8fafc;
  box-sizing: border-box;
  font-family: 'Inter', sans-serif;
}
.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #800000;
  box-shadow: 0 0 0 3px rgba(128, 0, 0, 0.1);
  background-color: #ffffff;
}

.form-group textarea {
  resize: none;
  height: 80px;
  line-height: 1.5;
}

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

/* Tablet Responsive */
@media (max-width: 1024px) {
  .add-remote-page {
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
    min-height: 160px;
  }

  .remote-form {
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
  .add-remote-page {
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
  .remote-form {
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

  .form-group input,
  .form-group textarea {
    padding: 0.875rem 1rem;
    font-size: 0.9rem;
  }

  .form-group textarea {
    height: 70px;
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
  .add-remote-page {
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

  .form-group input,
  .form-group textarea {
    padding: 0.75rem 0.875rem;
    font-size: 0.875rem;
  }

  .form-group textarea {
    height: 60px;
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

  .form-section h3 {
    font-size: 0.9rem;
  }

  .form-group label {
    font-size: 0.8rem;
  }
}
</style>