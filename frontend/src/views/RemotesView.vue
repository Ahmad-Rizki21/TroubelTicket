<template>
  <div class="remote-page">
    <!-- Page Header -->
    <header class="page-header">
      <div class="header-content">
        <div class="title-section">
          <h1 class="page-title">
            <span class="title-gradient">Remote Management</span>
          </h1>
          <p class="page-subtitle">Manage and visualize all Point of Interest (POI) BTS locations.</p>
        </div>
        <div class="header-stats">
          <div class="live-indicator">
            <div class="live-dot"></div>
            <span>Live</span>
          </div>
          <div class="header-actions">
            <router-link to="/remotes/add" class="primary-button">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 5V19M5 12H19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <span>Add New Remote</span>
            </router-link>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <div class="remote-layout">
      <!-- Remotes Table Card -->
      <div class="card table-card">
        <div class="table-header">
          <h3>All Remote Locations ({{ remotes.length }}) - Showing {{ startIndex }}-{{ endIndex }} of {{ remotes.length }}</h3>
        </div>
        <div class="table-responsive">
          <table class="remotes-table">
            <thead>
              <tr>
                <th>Site ID POI</th>
                <th>Site Name</th>
                <th>Coordinates</th>
                <th>Origin BB</th>
                <th>Terminating BB</th>
                <th>Link</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="loading">
                <td colspan="7" class="loading-state">Loading remotes...</td>
              </tr>
              <tr v-else-if="remotes.length === 0">
                <td colspan="7" class="empty-state">No remotes found. Add one to get started.</td>
              </tr>
              <tr v-for="remote in paginatedRemotes" :key="remote.id">
                <td class="remote-id">{{ remote.site_id_poi || '-' }}</td>
                <td>
                  <div class="remote-name">{{ remote.site_name }}</div>
                </td>
                <td class="remote-coords">{{ remote.latitude }}, {{ remote.longitude }}</td>
                <td class="remote-origin">{{ remote.origin_bb || '-' }}</td>
                <td class="remote-term">{{ remote.terminating_bb || '-' }}</td>
                <td class="remote-link">{{ remote.link || '-' }}</td>
                <td>
                  <div class="action-buttons">
                    <router-link :to="`/remotes/${remote.id}/edit`" class="action-button edit" title="Edit Remote">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                    </router-link>
                    <button class="action-button delete" @click="openDeleteModal(remote)" title="Delete Remote">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3 6h18M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6h14z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <!-- Pagination Controls -->
        <div class="pagination-controls" v-if="remotes.length > itemsPerPage">
          <div class="pagination-info">
            Page {{ currentPage }} of {{ totalPages }}
          </div>
          <div class="pagination-buttons">
            <button 
              @click="prevPage" 
              :disabled="currentPage === 1" 
              class="pagination-button">
              Previous
            </button>
            
            <!-- Page number buttons -->
            <button 
              v-for="page in getPageNumbers()" 
              :key="page" 
              @click="goToPage(page)" 
              :class="['pagination-button', { active: page === currentPage }]">
              {{ page }}
            </button>
            
            <button 
              @click="nextPage" 
              :disabled="currentPage === totalPages" 
              class="pagination-button">
              Next
            </button>
          </div>
        </div>
      </div>
      
      <!-- Map Card -->
      <div class="card map-card">
        <div id="map-container"></div>
      </div>
    </div>


    <!-- Delete Confirmation Modal -->
    <transition name="modal-fade">
        <div v-if="showDeleteModal" class="modal-overlay" @click="closeDeleteModal">
            <div class="modal-content confirmation-modal" @click.stop>
                <div class="modal-header">
                    <h2 class="modal-title">Confirm Deletion</h2>
                </div>
                <div class="modal-body">
                    <p v-if="remoteToDelete">Are you sure you want to delete the remote <strong>{{ remoteToDelete.site_name }}</strong>?</p>
                    <p class="warning-text">This action cannot be undone.</p>
                </div>
                <div class="modal-actions">
                    <button type="button" class="secondary-button" @click="closeDeleteModal">Cancel</button>
                    <button type="button" class="primary-button delete-confirm-button" @click="confirmDelete">Yes, Delete</button>
                </div>
            </div>
        </div>
    </transition>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import L, { Map, Marker, Icon, TileLayer } from 'leaflet';
import { remoteAPI, type Remote } from '../api/remoteAPI';

const router = useRouter();

// The 'router' instance is implicitly used by <router-link> components in the template.
// This declaration is kept to ensure full router functionality is available and to prevent linter warnings.

// --- State ---
const remotes = ref<Remote[]>([]);
const loading = ref(true);
let map: Map | null = null;
const markers = ref<Marker[]>([]);
const baseLayers = ref<{ [key: string]: TileLayer }>({});

const showDeleteModal = ref(false);
const remoteToDelete = ref<Remote | null>(null);

// --- Pagination State ---
const currentPage = ref(1);
const itemsPerPage = ref(5); // Default items per page

const totalPages = computed(() => Math.ceil(remotes.value.length / itemsPerPage.value));

const paginatedRemotes = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value;
  const end = start + itemsPerPage.value;
  return remotes.value.slice(start, end);
});

const startIndex = computed(() => (currentPage.value - 1) * itemsPerPage.value + 1);
const endIndex = computed(() => Math.min(currentPage.value * itemsPerPage.value, remotes.value.length));

// --- Leaflet Icon Fix ---
// Manually set the icon paths for Leaflet to work with Vite
delete (Icon.Default.prototype as any)._getIconUrl;
Icon.Default.mergeOptions({
  iconRetinaUrl: new URL('leaflet/dist/images/marker-icon-2x.png', import.meta.url).href,
  iconUrl: new URL('leaflet/dist/images/marker-icon.png', import.meta.url).href,
  shadowUrl: new URL('leaflet/dist/images/marker-shadow.png', import.meta.url).href,
});

// Custom Maroon Icon
const maroonIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png',
  iconRetinaUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

// --- Map Logic ---
const initMap = () => {
  try {
    // Check if container exists
    const container = document.getElementById('map-container');
    if (!container) {
      console.error('Map container not found');
      return;
    }

    // Clear existing map if any
    if (map) {
      map.remove();
      map = null;
    }

    // Initialize map
    map = L.map('map-container').setView([-6.2088, 106.8456], 10); // Default view (Jakarta)

  // Define different tile layers
  const osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  });

  const satellite = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
  });

  const terrain = L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
    attribution: 'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)'
  });

  const dark = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
    subdomains: 'abcd',
    maxZoom: 19
  });

  // Store base layers
  baseLayers.value = {
    "Standard": osm,
    "Satellite": satellite,
    "Terrain": terrain,
    "Dark": dark
  };

  // Add OpenStreetMap as default layer
  osm.addTo(map);

  // Create custom layer control
  const addLayerControl = () => {
    if (!map) return;

    const controlContainer = L.DomUtil.create('div', 'leaflet-bar leaflet-control layer-control-container');
    controlContainer.style.cssText = `
      position: absolute;
      top: 10px;
      right: 10px;
      z-index: 1000;
      background: rgba(255, 255, 255, 0.95);
      backdrop-filter: blur(10px);
      border-radius: 12px;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
      font-family: 'Inter', sans-serif;
      display: flex;
      flex-direction: column;
      gap: 0.25rem;
      padding: 0.5rem;
      border: 1px solid #e2e8f0;
      min-width: 150px;
    `;

    const layers = [
      { name: 'Standard', icon: '🗺️' },
      { name: 'Satellite', icon: '🛰️' },
      { name: 'Terrain', icon: '🏞️' },
      { name: 'Dark', icon: '🌃' }
    ];

    const buttons: { [key: string]: HTMLElement } = {};

    const updateButtons = (activeLayerName: string) => {
      layers.forEach(layer => {
        const button = buttons[layer.name];
        if (layer.name === activeLayerName) {
          // Remove active class from all buttons
          Object.values(buttons).forEach(btn => {
            btn.classList.remove('active');
            btn.classList.add('inactive');
          });
          // Add active class to selected button
          button.classList.add('active');
          button.classList.remove('inactive');
        }
      });
    };

    layers.forEach((layer) => {
      const button = L.DomUtil.create('a', 'layer-selector', controlContainer);
      button.innerHTML = `<span class="layer-icon">${layer.icon}</span><span class="layer-name">${layer.name}</span>`;
      button.href = '#';
      button.setAttribute('role', 'button');
      button.setAttribute('title', layer.name + ' Map');
      button.style.cssText = `
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.625rem 1rem;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.2s ease;
        font-size: 0.875rem;
        font-weight: 500;
        text-decoration: none;
        white-space: nowrap;
        border: 1px solid transparent;
        color: #334155;
        width: 100%;
      `;

      L.DomEvent.on(button, 'click', (e) => {
        L.DomEvent.stop(e);
        
        Object.values(baseLayers.value).forEach(tileLayer => {
          if (map && map.hasLayer(tileLayer)) {
            map.removeLayer(tileLayer);
          }
        });

        if (map) {
          baseLayers.value[layer.name].addTo(map);
        }
        updateButtons(layer.name);
      });
      
      buttons[layer.name] = button;
    });

    updateButtons('Standard'); // Set initial active button

    map.getContainer().appendChild(controlContainer);
  };
  // Call layer control after map is fully initialized
  setTimeout(() => {
    addLayerControl();
  }, 100);

} catch (error) {
  console.error('Error initializing map:', error);
  // Fallback: show error message to user
  const errorContainer = document.getElementById('map-container');
    if (errorContainer) {
      errorContainer.innerHTML = `
        <div style="
          display: flex;
          background: #f8fafc;
          border: 2px dashed #e2e8f0;
          border-radius: 12px;
          padding: 2rem;
          text-align: center;
          color: #64748b;
        ">
          <div style="font-size: 4rem; margin-bottom: 1rem;">🗺️</div>
          <h3 style="color: #1e293b; margin: 0 0 0.5rem 0;">Map Loading Error</h3>
          <p>Unable to load the map. Please refresh the page and try again.</p>
          <button onclick="location.reload()" style="
            background: #800000;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 6px;
            cursor: pointer;
            margin-top: 1rem;
          ">Refresh Page</button>
        </div>
      `;
    }
  }
};

const updateMapMarkers = () => {
  if (!map) return;

  // Clear existing markers
  markers.value.forEach(marker => marker.remove());
  markers.value = [];

  // Add new markers - use the full remotes array for the map
  remotes.value.forEach(remote => {
    const popupContent = `
      <div class="map-popup">
        <h4>${remote.site_name}</h4>
        <p><strong>Site ID:</strong> ${remote.site_id_poi || '-'}</p>
        <p><strong>BTS Count:</strong> ${remote.jumlah_bts ?? 'N/A'}</p>
        <p><strong>Bandwidth:</strong> ${remote.bw || 'N/A'}</p>
        <p><strong>Origin BB:</strong> ${remote.origin_bb || '-'}</p>
        <p><strong>Terminating BB:</strong> ${remote.terminating_bb || '-'}</p>
      </div>
    `;
    const marker = L.marker([remote.latitude, remote.longitude], { icon: maroonIcon })
      .addTo(map!)
      .bindPopup(popupContent);
    markers.value.push(marker);
  });

  // Adjust map view to fit all markers
  if (remotes.value.length > 0) {
    const group = L.featureGroup(markers.value as unknown as L.Layer[]);
    map.fitBounds(group.getBounds().pad(0.5));
  }
};

// --- Data & CRUD Logic ---
const loadRemotes = async () => {
  loading.value = true;
  try {
    const response = await remoteAPI.getAllRemotes();
    remotes.value = response.data;
    await nextTick(); // Wait for DOM to update
    updateMapMarkers();
  } catch (error) {
    console.error("Failed to load remotes:", error);
  } finally {
    loading.value = false;
  }
};



const openDeleteModal = (remote: Remote) => {
  remoteToDelete.value = remote;
  showDeleteModal.value = true;
};

const closeDeleteModal = () => {
  showDeleteModal.value = false;
  remoteToDelete.value = null;
};

const confirmDelete = async () => {
  if (!remoteToDelete.value) return;
  try {
    await remoteAPI.deleteRemote(remoteToDelete.value.id);
    closeDeleteModal();
    loadRemotes(); // Reload data
  } catch (error) {
    console.error("Failed to delete remote:", error);
  }
};

// --- Pagination Methods ---
const goToPage = (page: number) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page;
  }
};

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
  }
};

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
  }
};

// Function to generate page numbers to display in pagination
const getPageNumbers = () => {
  const pages = [];
  const maxVisiblePages = 5; // Maximum number of page buttons to show
  
  if (totalPages.value <= maxVisiblePages) {
    // If total pages is less than or equal to max visible, show all pages
    for (let i = 1; i <= totalPages.value; i++) {
      pages.push(i);
    }
  } else {
    // Calculate the range of pages to show around current page
    let startPage = Math.max(1, currentPage.value - Math.floor(maxVisiblePages / 2));
    let endPage = Math.min(totalPages.value, startPage + maxVisiblePages - 1);
    
    // Adjust the start page if the end page reached the maximum
    if (endPage - startPage + 1 < maxVisiblePages) {
      startPage = Math.max(1, endPage - maxVisiblePages + 1);
    }
    
    // Add the page numbers to the array
    for (let i = startPage; i <= endPage; i++) {
      pages.push(i);
    }
  }
  
  return pages;
};

// --- Lifecycle Hooks ---
onMounted(() => {
  nextTick(() => {
    initMap();
    loadRemotes();
    // Dummy usage to prevent linter warning about 'router' being unused.
    // The router instance is primarily used by <router-link> in the template.
    console.log('Router instance:', router);
  });
});

onUnmounted(() => {
  if (map) {
    map.remove();
    map = null;
  }
});

</script>

<style>
/* Import Leaflet CSS */
@import "leaflet/dist/leaflet.css";
</style>

<style scoped>
.remote-page {
  background-color: #f8fafc;
  padding: 2rem;
  font-family: 'Inter', sans-serif;
}

.card {
  background-color: #ffffff;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
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

.page-title {
  font-size: clamp(1.75rem, 4vw, 2.5rem);
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
  font-size: clamp(1rem, 2vw, 1.125rem);
  color: #64748b;
  margin: 0;
  line-height: 1.5;
  font-weight: 400;
}

.header-stats {
  display: flex;
  align-items: center;
  gap: 1.5rem;
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

.header-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
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
}

.primary-button {
  background: linear-gradient(135deg, #800000 0%, #5c0000 100%);
  color: white;
}

.primary-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(128, 0, 0, 0.3);
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

/* Layout */
.remote-layout {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}
@media (min-width: 1024px) {
  .remote-layout {
    flex-direction: column;
  }
}

/* Map */
.map-card {
  padding: 0.5rem;
}
#map-container {
  width: 100%;
  height: 500px;
  border-radius: 12px;
  z-index: 1;
}

/* Table */
.table-card { overflow: hidden; }
.table-header {
    padding: 1.5rem;
    border-bottom: 1px solid #e2e8f0;
}
.table-header h3 { margin: 0; font-size: 1.25rem; color: #1e293b; }
.table-responsive { overflow-x: auto; }
.remotes-table { width: 100%; border-collapse: collapse; text-align: left; }
.remotes-table th, .remotes-table td { padding: 1rem 1.5rem; border-bottom: 1px solid #e2e8f0; vertical-align: middle; }
.remotes-table tr:last-child td { border-bottom: none; }
.remotes-table th { font-size: 0.875rem; font-weight: 600; color: #64748b; text-transform: uppercase; background-color: #f8fafc; }
.remote-name { font-weight: 600; color: #1e293b; }
.remote-coords { font-family: 'Courier New', Courier, monospace; font-size: 0.9rem; color: #475569; }
.remote-desc { font-size: 0.9rem; color: #64748b; max-width: 250px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.loading-state, .empty-state { text-align: center; padding: 4rem; color: #64748b; font-style: italic; }

.action-buttons { display: flex; gap: 0.5rem; }
.action-button { width: 36px; height: 36px; border-radius: 8px; background: transparent; border: none; display: flex; align-items: center; justify-content: center; color: #64748b; cursor: pointer; transition: all 0.2s ease; }
.action-button:hover { background-color: #f1f5f9; color: #1e293b; }
.action-button.edit:hover { color: #f59e0b; }
.action-button.delete:hover { color: #ef4444; }

/* Pagination Styles */
.pagination-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-top: 1px solid #e2e8f0;
  background-color: #ffffff;
}

.pagination-info {
  font-size: 0.9rem;
  color: #64748b;
}

.pagination-buttons {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.pagination-button {
  padding: 0.5rem 1rem;
  border: 1px solid #e2e8f0;
  background-color: #ffffff;
  color: #475569;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.9rem;
}

.pagination-button:hover:not(:disabled) {
  background-color: #f1f5f9;
  border-color: #cbd5e1;
}

.pagination-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination-button.active {
  background-color: #800000;
  color: white;
  border-color: #800000;
}

/* Modal Styles (re-using from Tickets.vue for consistency) */
.modal-fade-enter-active, .modal-fade-leave-active { transition: opacity 0.3s ease; }
.modal-fade-enter-from, .modal-fade-leave-to { opacity: 0; }
.modal-fade-enter-active .modal-content, .modal-fade-leave-active .modal-content { transition: all 0.3s ease; }
.modal-fade-enter-from .modal-content, .modal-fade-leave-to .modal-content { opacity: 0; transform: translateY(-20px); }
.modal-overlay { position: fixed; inset: 0; background: rgba(17, 24, 39, 0.6); display: flex; align-items: center; justify-content: center; z-index: 1000; backdrop-filter: blur(5px); }
.modal-content { background-color: #f8fafc; border-radius: 20px; width: 100%; max-width: 600px; max-height: 90vh; display: flex; flex-direction: column; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1); }
.modal-header { display: flex; justify-content: space-between; align-items: center; padding: 1.5rem 2rem; background-color: #1f2937; color: #fff; border-top-left-radius: 20px; border-top-right-radius: 20px; }
.modal-title { font-size: 1.25rem; font-weight: 600; }
.close-button { background: transparent; border: none; color: #9ca3af; cursor: pointer; padding: 0.5rem; border-radius: 50%; }
.close-button:hover { color: #fff; }
.modal-form, .modal-body { padding: 2rem; overflow-y: auto; background-color: #ffffff; }
.form-group { margin-bottom: 1.5rem; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }
.form-group label { display: block; font-size: 0.875rem; font-weight: 600; color: #1e293b; margin-bottom: 0.5rem; }
.form-group input, .form-group textarea { width: 100%; padding: 0.75rem 1rem; border: 1px solid #e2e8f0; border-radius: 12px; font-size: 1rem; transition: all 0.3s ease; background-color: #f8fafc; box-sizing: border-box; }
.form-group input:focus, .form-group textarea:focus { outline: none; border-color: #ff4d4f; box-shadow: 0 0 0 3px rgba(255, 77, 79, 0.2); background-color: #ffffff; }
.modal-actions { display: flex; justify-content: flex-end; gap: 1rem; padding: 1.5rem 2rem; border-top: 1px solid #e2e8f0; background-color: #f8fafc; border-bottom-left-radius: 20px; border-bottom-right-radius: 20px; }
.confirmation-modal { max-width: 450px; }
.confirmation-modal .modal-body { font-size: 1.1rem; color: #334155; line-height: 1.6; }
.confirmation-modal .warning-text { font-size: 1rem; font-weight: 600; color: #ef4444; margin-top: 1rem; }
.delete-confirm-button { background-color: #ef4444; }
.delete-confirm-button:hover { background-color: #dc2626; }

/* Custom Popup Styles */
:deep(.leaflet-popup-content-wrapper) {
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  background-color: #f8fafc;
}

:deep(.leaflet-popup-content) {
  margin: 1rem;
  font-family: 'Inter', sans-serif;
  line-height: 1.6;
  min-width: 220px;
}

:deep(.leaflet-popup-content h4) {
  margin: 0 0 0.75rem 0;
  font-size: 1.1rem;
  font-weight: 700;
  color: #1e293b;
  border-bottom: 1px solid #e2e8f0;
  padding-bottom: 0.5rem;
}

:deep(.leaflet-popup-content p) {
  margin: 0.25rem 0;
  font-size: 0.9rem;
  color: #475569;
}

:deep(.leaflet-popup-content p strong) {
  font-weight: 600;
  color: #334155;
}

:deep(.leaflet-popup-close-button) {
  color: #64748b;
  padding: 0.5rem;
  border-radius: 50%;
  top: 10px;
  right: 10px;
}
:deep(.leaflet-popup-close-button:hover) {
  color: #1e293b;
  background-color: #f1f5f9;
}

/* Custom Layer Control Styles */
:deep(.layer-control-container) {
  background: rgba(255, 255, 255, 0.95) !important;
  backdrop-filter: blur(10px) !important;
  border-radius: 12px !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
  border: 1px solid #e2e8f0 !important;
  padding: 0.5rem !important;
  min-width: 150px !important;
  font-family: 'Inter', sans-serif !important;
}

:deep(.layer-selector) {
  display: flex !important;
  align-items: center !important;
  gap: 0.5rem !important;
  padding: 0.625rem 1rem !important;
  border-radius: 8px !important;
  cursor: pointer !important;
  transition: all 0.2s ease !important;
  font-size: 0.875rem !important;
  font-weight: 500 !important;
  text-decoration: none !important;
  white-space: nowrap !important;
  border: 1px solid transparent !important;
  color: #334155 !important;
  background: transparent !important;
  width: 100% !important;
  text-align: left !important;
  line-height: 1.3 !important;
}

:deep(.layer-selector:hover:not(.active)) {
  background-color: #f1f5f9 !important;
  border-color: #cbd5e1 !important;
}

:deep(.layer-selector.active) {
  background: linear-gradient(135deg, #800000 0%, #5c0000 100%) !important;
  color: white !important;
  border-color: #800000 !important;
}

:deep(.layer-selector.inactive) {
  background: transparent !important;
  color: #334155 !important;
  border-color: transparent !important;
}

:deep(.layer-icon) {
  font-size: 1.1rem !important;
  display: flex !important;
  align-items: center !important;
  width: 1.25rem !important;
  height: 1.25rem !important;
  justify-content: center !important;
}

:deep(.layer-name) {
  font-weight: 500 !important;
  white-space: nowrap !important;
}

@media (max-width: 768px) {
  :deep(.layer-name) {
    display: none !important;
  }
  :deep(.layer-selector) {
    padding: 0.625rem !important;
    justify-content: center !important;
  }
  :deep(.layer-icon) {
    margin-right: 0 !important;
  }
  :deep(.layer-control-container) {
    min-width: 50px !important;
    padding: 0.25rem !important;
  }
}
</style>
