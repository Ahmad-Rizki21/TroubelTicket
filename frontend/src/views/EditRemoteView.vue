<template>
  <div class="edit-remote-page">
    <!-- Page Header -->
    <header class="page-header">
      <div class="header-content">
        <h1 class="page-title">Edit Remote</h1>
        <p class="page-subtitle">Update the details for this remote location.</p>
      </div>
    </header>

    <!-- Main Content -->
    <div class="remote-form-wrapper" v-if="remote">
      <form @submit.prevent="updateRemote" class="remote-form">
        <div class="form-section">
          <h3>Basic Information</h3>
          <div class="form-row">
            <div class="form-group">
              <label for="site_id_poi">Site ID POI</label>
              <input type="text" id="site_id_poi" v-model="remote.site_id_poi" placeholder="e.g., ID001">
            </div>
            <div class="form-group">
              <label for="site_name">Site Name *</label>
              <input type="text" id="site_name" v-model="remote.site_name" required placeholder="e.g., BTS Tower Central">
            </div>
          </div>
          <div class="form-group">
            <label for="notes">Notes</label>
            <textarea id="notes" v-model="remote.notes" rows="3" placeholder="e.g., Additional information..."></textarea>
          </div>
        </div>



        <div class="form-section">
          <h3>Network Information</h3>
          <div class="form-row">
            <div class="form-group">
              <label for="origin_backbone">Origin Backbone</label>
              <input type="text" id="origin_backbone" v-model="remote.origin_backbone" placeholder="e.g., Backbone Site A">
            </div>
            <div class="form-group">
              <label for="origin_bb">Origin BB</label>
              <input type="text" id="origin_bb" v-model="remote.origin_bb" placeholder="e.g., BBA001">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label for="terminating_bb">Terminating BB</label>
              <input type="text" id="terminating_bb" v-model="remote.terminating_bb" placeholder="e.g., TBB001">
            </div>
            <div class="form-group">
              <label for="link">Link</label>
              <input type="text" id="link" v-model="remote.link" placeholder="e.g., Link Type">
            </div>
          </div>
        </div>

        <div class="form-section">
          <h3>Technical Information</h3>
          <div class="form-row">
            <div class="form-group">
              <label for="latitude">Latitude *</label>
              <input type="number" step="any" id="latitude" v-model.number="remote.latitude" required placeholder="e.g., -6.2088">
            </div>
            <div class="form-group">
              <label for="longitude">Longitude *</label>
              <input type="number" step="any" id="longitude" v-model.number="remote.longitude" required placeholder="e.g., 106.8456">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label for="jumlah_bts">Jumlah BTS</label>
              <input type="number" id="jumlah_bts" v-model.number="remote.jumlah_bts" placeholder="e.g., 5">
            </div>
            <div class="form-group">
              <label for="bw">Bandwidth (BW)</label>
              <input type="text" id="bw" v-model="remote.bw" placeholder="e.g., 100 Mbps">
            </div>
          </div>
          <div class="form-group">
            <label for="vlan">VLAN</label>
            <input type="text" id="vlan" v-model="remote.vlan" placeholder="e.g., VLAN100">
          </div>
        </div>

        <div class="form-actions">
          <router-link to="/remotes" class="secondary-button">
            <span>Cancel</span>
          </router-link>
          <button type="submit" class="primary-button" :disabled="loading">
            <span v-if="!loading">Save Changes</span>
            <span v-else>Saving...</span>
          </button>
        </div>
      </form>
    </div>
    <div v-else class="loading-container">
      <p>Loading remote data...</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { remoteAPI, type Remote } from '../api/remoteAPI';

// --- State ---
const router = useRouter();
const route = useRoute();
const loading = ref(false);
const remote = ref<Remote | null>(null);

// --- Lifecycle ---
onMounted(() => {
  loadRemote();
});

// --- Data Fetching ---
const loadRemote = async () => {
  try {
    const id = parseInt(route.params.id as string);
    const response = await remoteAPI.getRemoteById(id);
    remote.value = response.data;
  } catch (error) {
    console.error("Failed to load remote:", error);
    // Redirect to remotes list if not found
    router.push('/remotes');
  }
};

// --- Form Submission ---
const updateRemote = async () => {
  if (!remote.value?.site_name || remote.value?.latitude === 0 || remote.value?.longitude === 0) {
    alert('Site Name, Latitude, and Longitude are required.');
    return;
  }

  loading.value = true;
  try {
    await remoteAPI.updateRemote(remote.value.id, {
      site_id_poi: remote.value.site_id_poi,
      site_name: remote.value.site_name,
      notes: remote.value.notes,
      latitude: remote.value.latitude,
      longitude: remote.value.longitude,
      origin_backbone: remote.value.origin_backbone,
      origin_bb: remote.value.origin_bb,
      terminating_bb: remote.value.terminating_bb,
      link: remote.value.link,
      jumlah_bts: remote.value.jumlah_bts,
      bw: remote.value.bw,
      vlan: remote.value.vlan,
    });
    router.push('/remotes'); // Redirect to remotes list after successful update
  } catch (error) {
    console.error("Failed to update remote:", error);
    // Show user-friendly error message
    alert(`Failed to update remote: ${error instanceof Error ? error.message : 'Unknown error'}`);
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.edit-remote-page {
  background-color: #f8fafc;
  padding: 2rem 1rem;
  font-family: 'Inter', sans-serif;
}

@media (min-width: 768px) {
  .edit-remote-page {
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
  .edit-remote-page {
    padding: 1rem 1rem;
  }
}

@media (min-width: 1280px) {
  .edit-remote-page {
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
  .edit-remote-page {
    padding: 1rem;
  }
  
  .form-row { 
    grid-template-columns: 1fr; 
  }
}

.loading-container {
  background-color: #ffffff;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
  padding: 2rem;
  margin-top: 1rem;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1.2rem;
  color: #64748b;
}
</style>