<template>
  <div class="add-remote-page">
    <!-- Page Header -->
    <header class="page-header">
      <div class="header-content">
        <h1 class="page-title">Add New Remote</h1>
        <p class="page-subtitle">Fill in the details for the new remote location.</p>
      </div>
    </header>

    <!-- Main Content -->
    <div class="remote-form-wrapper">
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
  padding: 2rem 1rem;
  font-family: 'Inter', sans-serif;
}

@media (min-width: 768px) {
  .add-remote-page {
    padding: 2rem;
  }
}

.remote-form-wrapper {
  max-width: 100%;
  margin: 0 auto;
  width: 100%;
  padding: 0 1rem;
  box-sizing: border-box;
}

@media (min-width: 768px) {
  .remote-form-wrapper {
    padding: 0 2rem;
  }
}

@media (min-width: 1024px) {
  .remote-form-wrapper {
    padding: 0 3rem;
  }
}

@media (min-width: 1400px) {
  .remote-form-wrapper {
    max-width: 90%;
    margin: 0 auto;
  }
}

.remote-form {
  background-color: #ffffff;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
  padding: 2rem;
  margin-top: 1rem;
  width: 100%;
  box-sizing: border-box;
}

/* Adjust page padding for desktop */
@media (min-width: 1024px) {
  .add-remote-page {
    padding: 1rem 1rem;
  }
}

@media (min-width: 1280px) {
  .add-remote-page {
    padding: 1rem 1rem;
  }
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
  font-size: 2rem; 
  font-weight: 800; 
  color: #1e293b; 
  margin: 0; 
}
.page-subtitle { 
  font-size: 1.1rem; 
  color: #64748b; 
  margin-top: 0.25rem; 
}

/* Buttons */
.primary-button, .secondary-button {
  display: inline-flex; 
  align-items: center; 
  gap: 0.5rem; 
  padding: 0.75rem 1.5rem;
  border-radius: 12px; 
  font-size: 1rem; 
  font-weight: 600; 
  cursor: pointer; 
  transition: all 0.3s ease; 
  border: 1px solid transparent;
  text-decoration: none;
}
.primary-button { 
  background-color: #ff4d4f; 
  color: white; 
}
.primary-button:hover:not(:disabled) { 
  background-color: #d9363e; 
}
.primary-button:disabled {
  background-color: #cbd5e1;
  cursor: not-allowed;
}
.secondary-button { 
  background: #ffffff; 
  color: #475569; 
  border-color: #e2e8f0; 
}
.secondary-button:hover { 
  background-color: #f1f5f9; 
  border-color: #cbd5e1; 
}



/* Form Styles */
.remote-form {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.form-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-section h3 {
  font-size: 1.25rem;
  color: #1e293b;
  margin: 0 0 1rem 0;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #e2e8f0;
}

.form-row { 
  display: grid; 
  grid-template-columns: 1fr 1fr; 
  gap: 1.5rem; 
}

.form-group { 
  margin-bottom: 1.5rem; 
}
.form-group label { 
  display: block; 
  font-size: 0.875rem; 
  font-weight: 600; 
  color: #1e293b; 
  margin-bottom: 0.5rem; 
}
.form-group input, 
.form-group textarea { 
  width: 100%; 
  padding: 0.75rem 1rem; 
  border: 1px solid #e2e8f0; 
  border-radius: 12px; 
  font-size: 1rem; 
  transition: all 0.3s ease; 
  background-color: #f8fafc; 
  box-sizing: border-box; 
}
.form-group input:focus, 
.form-group textarea:focus { 
  outline: none; 
  border-color: #ff4d4f; 
  box-shadow: 0 0 0 3px rgba(255, 77, 79, 0.2); 
  background-color: #ffffff; 
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0;
  margin-top: 1rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .add-remote-page {
    padding: 1rem;
  }
  
  .form-row { 
    grid-template-columns: 1fr; 
  }
}
</style>