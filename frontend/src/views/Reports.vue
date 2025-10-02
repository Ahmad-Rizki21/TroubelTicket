<template>
  <div class="reports-container">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">Laporan & Analitik</h1>
        <p class="page-subtitle">Analisis kinerja dan statistik trouble ticket</p>
      </div>
      <div class="header-actions">
        <button class="export-button" @click="exportReport">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 12L12 18M12 18L8 14M12 18L16 14M16 8L16 6C16 5.46957 15.7893 4.96086 15.4142 4.58579C15.0391 4.21071 14.5304 4 14 4H10C9.46957 4 8.96086 4.21071 8.58579 4.58579C8.21071 4.96086 8 5.46957 8 6L8 8M16 8L16 10M16 8H8M8 8L8 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span>Ekspor Laporan</span>
        </button>
      </div>
    </div>

    <!-- Date Range Filter -->
    <div class="date-filter-section">
      <div class="date-range-picker">
        <label for="startDate">Periode:</label>
        <input 
          type="date" 
          id="startDate" 
          v-model="startDate" 
          class="date-input"
        >
        <span>-</span>
        <input 
          type="date" 
          id="endDate" 
          v-model="endDate" 
          class="date-input"
        >
        <button class="apply-button" @click="applyDateFilter">Terapkan</button>
      </div>
      <div class="period-presets">
        <button 
          v-for="preset in periodPresets" 
          :key="preset.value"
          class="preset-button"
          :class="{ active: selectedPreset === preset.value }"
          @click="selectPreset(preset.value)"
        >
          {{ preset.label }}
        </button>
      </div>
    </div>

    <!-- Summary Cards -->
    <div class="summary-cards">
      <div class="summary-card" v-for="card in summaryCards" :key="card.title">
        <div class="card-icon" :style="{ backgroundColor: card.color + '20', color: card.color }">
          <component :is="card.icon" />
        </div>
        <div class="card-content">
          <h3 class="card-value">{{ card.value }}</h3>
          <p class="card-title">{{ card.title }}</p>
        </div>
        <div class="card-trend" :class="{ positive: card.trend > 0, negative: card.trend < 0 }">
          <svg v-if="card.trend > 0" width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 19V5M5 12L12 5L19 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <svg v-else-if="card.trend < 0" width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 5V19M19 12L12 19L5 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span>{{ Math.abs(card.trend) }}%</span>
        </div>
      </div>
    </div>

    <!-- Charts Grid -->
    <div class="charts-grid">
      <!-- Ticket Resolution Time Chart -->
      <div class="chart-card">
        <div class="card-header">
          <h2 class="card-title">Waktu Penyelesaian Tiket (Rata-rata)</h2>
          <div class="card-actions">
            <select v-model="resolutionTimePeriod" class="period-select">
              <option value="daily">Harian</option>
              <option value="weekly">Mingguan</option>
              <option value="monthly">Bulanan</option>
            </select>
          </div>
        </div>
        <div class="chart-container">
          <div class="chart-placeholder">
            <p>Chart akan segera tersedia</p>
          </div>
        </div>
      </div>

      <!-- Ticket Volume by Category Chart -->
      <div class="chart-card">
        <div class="card-header">
          <h2 class="card-title">Volume Tiket berdasarkan Kategori</h2>
          <div class="card-actions">
            <button class="action-button">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 5V19M5 12H19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>
          </div>
        </div>
        <div class="chart-container">
          <div class="chart-placeholder">
            <p>Chart akan segera tersedia</p>
          </div>
        </div>
      </div>

      <!-- Ticket Status Distribution Chart -->
      <div class="chart-card">
        <div class="card-header">
          <h2 class="card-title">Distribusi Status Tiket</h2>
          <div class="card-actions">
            <button class="action-button">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 5V19M5 12H19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>
          </div>
        </div>
        <div class="chart-container">
          <div class="chart-placeholder">
            <p>Chart akan segera tersedia</p>
          </div>
        </div>
      </div>

      <!-- Technician Performance Chart -->
      <div class="chart-card">
        <div class="card-header">
          <h2 class="card-title">Performa Teknisi</h2>
          <div class="card-actions">
            <select v-model="performanceMetric" class="period-select">
              <option value="tickets">Tiket Diselesaikan</option>
              <option value="time">Waktu Rata-rata</option>
              <option value="rating">Rating</option>
            </select>
          </div>
        </div>
        <div class="chart-container">
          <div class="chart-placeholder">
            <p>Chart akan segera tersedia</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Detailed Reports Table -->
    <div class="reports-table-container">
      <div class="table-header">
        <h2 class="table-title">Laporan Detail Tiket</h2>
        <div class="table-filters">
          <select v-model="reportCategory" class="filter-select">
            <option value="">Semua Kategori</option>
            <option value="Jaringan">Jaringan</option>
            <option value="Hardware">Hardware</option>
            <option value="Software">Software</option>
            <option value="Lainnya">Lainnya</option>
          </select>
          <select v-model="reportPriority" class="filter-select">
            <option value="">Semua Prioritas</option>
            <option value="Tinggi">Tinggi</option>
            <option value="Sedang">Sedang</option>
            <option value="Rendah">Rendah</option>
          </select>
        </div>
      </div>
      <div class="table-container">
        <table class="reports-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Judul</th>
              <th>Kategori</th>
              <th>Prioritas</th>
              <th>Status</th>
              <th>Dibuat</th>
              <th>Selesai</th>
              <th>Waktu Resolusi</th>
              <th>Teknisi</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="report in filteredReports" :key="report.id">
              <td>#{{ report.id }}</td>
              <td>{{ report.title }}</td>
              <td>{{ report.category }}</td>
              <td>
                <span class="priority-badge" :class="report.priority.toLowerCase()">
                  {{ report.priority }}
                </span>
              </td>
              <td>
                <span class="status-badge" :class="report.status.toLowerCase().replace(' ', '-')">
                  {{ report.status }}
                </span>
              </td>
              <td>{{ formatDate(report.created_at || '') }}</td>
              <td>{{ formatDate(report.completed_at || '') }}</td>
              <td>{{ formatResolutionTime(report.resolution_time || 0) }}</td>
              <td>{{ report.technician || '-' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="pagination">
        <button class="pagination-button" :disabled="currentPage === 1" @click="prevPage">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M15 18L9 12L15 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
        <span class="pagination-info">Halaman {{ currentPage }} dari {{ totalPages }}</span>
        <button class="pagination-button" :disabled="currentPage === totalPages" @click="nextPage">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M9 18L15 12L9 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';

// State management
const startDate = ref('');
const endDate = ref('');
const selectedPreset = ref('7days');
const resolutionTimePeriod = ref('daily');
const performanceMetric = ref('tickets');
const reportCategory = ref('');
const reportPriority = ref('');
const currentPage = ref(1);
const totalPages = ref(10);

// Period presets
const periodPresets = ref([
  { label: '7 Hari', value: '7days' },
  { label: '30 Hari', value: '30days' },
  { label: '3 Bulan', value: '3months' },
  { label: '1 Tahun', value: '1year' }
]);

// Summary cards
const summaryCards = ref([
  {
    title: 'Total Tiket',
    value: '1,248',
    trend: 12,
    color: '#3b82f6',
    icon: 'TicketIcon'
  },
  {
    title: 'Tiket Diselesaikan',
    value: '1,102',
    trend: 8,
    color: '#10b981',
    icon: 'CompletedTicketIcon'
  },
  {
    title: 'Waktu Resolusi Rata-rata',
    value: '2.3 jam',
    trend: -5,
    color: '#8b5cf6',
    icon: 'TimeIcon'
  },
  {
    title: 'Kepuasan Pelanggan',
    value: '4.7/5',
    trend: 3,
    color: '#f59e0b',
    icon: 'SatisfactionIcon'
  }
]);

// Mock reports data
const allReports = ref([
  {
    id: '001',
    title: 'Internet Lambat di Ruang IT',
    category: 'Jaringan',
    priority: 'Tinggi',
    status: 'Selesai',
    created_at: '2023-06-15T09:30:00Z',
    completed_at: '2023-06-15T11:45:00Z',
    resolution_time: 135, // minutes
    technician: 'Teknisi A'
  },
  {
    id: '002',
    title: 'Printer Tidak Merespon',
    category: 'Hardware',
    priority: 'Sedang',
    status: 'Selesai',
    created_at: '2023-06-14T14:15:00Z',
    completed_at: '2023-06-14T16:20:00Z',
    resolution_time: 125, // minutes
    technician: 'Teknisi B'
  },
  {
    id: '003',
    title: 'Software Accounting Error',
    category: 'Software',
    priority: 'Rendah',
    status: 'Selesai',
    created_at: '2023-06-13T11:45:00Z',
    completed_at: '2023-06-14T10:30:00Z',
    resolution_time: 1365, // minutes
    technician: 'Teknisi C'
  },
  {
    id: '004',
    title: 'Komputer Tidak Bisa Boot',
    category: 'Hardware',
    priority: 'Tinggi',
    status: 'Dalam Proses',
    created_at: '2023-06-12T16:20:00Z',
    completed_at: null,
    resolution_time: null,
    technician: 'Teknisi A'
  },
  {
    id: '005',
    title: 'Email Server Down',
    category: 'Jaringan',
    priority: 'Tinggi',
    status: 'Selesai',
    created_at: '2023-06-11T08:10:00Z',
    completed_at: '2023-06-11T10:45:00Z',
    resolution_time: 155, // minutes
    technician: 'Teknisi B'
  }
]);

const filteredReports = ref([...allReports.value]);


// Methods
const formatDate = (dateString: string) => {
  if (!dateString) return '-';
  const date = new Date(dateString);
  return date.toLocaleDateString('id-ID', {
    day: '2-digit',
    month: 'short',
    year: 'numeric'
  });
};

const formatResolutionTime = (minutes: number) => {
  if (minutes === null || minutes === undefined) return '-';
  
  const hours = Math.floor(minutes / 60);
  const mins = minutes % 60;
  
  if (hours > 0) {
    return `${hours}j ${mins}m`;
  }
  return `${mins}m`;
};

const applyDateFilter = () => {
  // In a real app, this would filter the data based on the selected dates
  console.log(`Applying date filter: ${startDate.value} to ${endDate.value}`);
};

const selectPreset = (preset: string) => {
  selectedPreset.value = preset;
  // Apply preset logic here
  console.log(`Selected preset: ${preset}`);
};

const exportReport = () => {
  alert('Fitur ekspor laporan akan segera tersedia!');
};

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
  }
};

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
  }
};


// Lifecycle hooks
onMounted(() => {
  // Set default date range to last 30 days
  const today = new Date();
  const thirtyDaysAgo = new Date(today);
  thirtyDaysAgo.setDate(today.getDate() - 30);
  
  endDate.value = today.toISOString().split('T')[0];
  startDate.value = thirtyDaysAgo.toISOString().split('T')[0];
});
</script>

<style scoped>
.reports-container {
  padding: 24px;
  width: 100%;
  box-sizing: border-box;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
  flex-wrap: wrap;
  gap: 16px;
}

.header-content {
  flex: 1;
}

.page-title {
  font-size: 28px;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 8px 0;
}

.page-subtitle {
  font-size: 16px;
  color: #64748b;
  margin: 0;
}

.export-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: linear-gradient(90deg, #3b82f6, #60a5fa);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.export-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(59, 130, 246, 0.4);
}

.date-filter-section {
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  padding: 24px;
  margin-bottom: 32px;
}

.date-range-picker {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.date-range-picker label {
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
}

.date-input {
  padding: 12px 16px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 16px;
  color: #111827;
  background-color: #f9fafb;
  transition: all 0.2s ease;
}

.date-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
  background-color: #fff;
}

.apply-button {
  padding: 12px 24px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.apply-button:hover {
  background: #2563eb;
}

.period-presets {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.preset-button {
  padding: 8px 16px;
  border: 1px solid #d1d5db;
  border-radius: 20px;
  background: #fff;
  color: #374151;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.preset-button:hover,
.preset-button.active {
  background: #3b82f6;
  color: white;
  border-color: #3b82f6;
}

.summary-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.summary-card {
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.summary-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

.card-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.card-content {
  flex: 1;
}

.card-value {
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 4px 0;
}

.card-title {
  font-size: 14px;
  color: #64748b;
  margin: 0;
}

.card-trend {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
  font-weight: 500;
}

.card-trend.positive {
  color: #10b981;
}

.card-trend.negative {
  color: #ef4444;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.chart-card {
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  padding: 24px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.chart-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  flex-wrap: wrap;
  gap: 16px;
}

.card-title {
  font-size: 20px;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.card-actions {
  display: flex;
  gap: 8px;
}

.period-select {
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  background-color: #fff;
  font-size: 14px;
  color: #374151;
  cursor: pointer;
  transition: all 0.2s ease;
}

.period-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
}

.action-button {
  width: 32px;
  height: 32px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  background: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #374151;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-button:hover {
  border-color: #3b82f6;
  color: #3b82f6;
  background-color: #eff6ff;
}

.chart-container {
  height: 300px;
  position: relative;
}

.chart-placeholder {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8fafc;
  border: 2px dashed #e2e8f0;
  border-radius: 8px;
  color: #64748b;
  font-style: italic;
}

.reports-table-container {
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  overflow: hidden;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px;
  border-bottom: 1px solid #e5e7eb;
  flex-wrap: wrap;
  gap: 16px;
}

.table-title {
  font-size: 20px;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.table-filters {
  display: flex;
  gap: 12px;
}

.filter-select {
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  background-color: #fff;
  font-size: 14px;
  color: #374151;
  cursor: pointer;
  transition: all 0.2s ease;
}

.filter-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
}

.table-container {
  overflow-x: auto;
}

.reports-table {
  width: 100%;
  border-collapse: collapse;
}

.reports-table th {
  text-align: left;
  padding: 12px 16px;
  font-size: 14px;
  font-weight: 600;
  color: #374151;
  border-bottom: 2px solid #e5e7eb;
  white-space: nowrap;
}

.reports-table td {
  padding: 12px 16px;
  font-size: 14px;
  color: #374151;
  border-bottom: 1px solid #e5e7eb;
  white-space: nowrap;
}

.reports-table tr:last-child td {
  border-bottom: none;
}

.reports-table tr:hover td {
  background-color: #f9fafb;
}

.priority-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
  text-transform: uppercase;
}

.priority-badge.tinggi {
  background-color: #fee2e2;
  color: #dc2626;
}

.priority-badge.sedang {
  background-color: #fef3c7;
  color: #d97706;
}

.priority-badge.rendah {
  background-color: #d1fae5;
  color: #059669;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
  text-transform: uppercase;
}

.status-badge.terbuka {
  background-color: #fee2e2;
  color: #dc2626;
}

.status-badge.dalam-proses {
  background-color: #fef3c7;
  color: #d97706;
}

.status-badge.selesai {
  background-color: #d1fae5;
  color: #059669;
}

.status-badge.ditunda {
  background-color: #e5e7eb;
  color: #374151;
}

.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  padding: 24px;
}

.pagination-button {
  width: 40px;
  height: 40px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  background: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #374151;
  cursor: pointer;
  transition: all 0.2s ease;
}

.pagination-button:hover:not(:disabled) {
  border-color: #3b82f6;
  color: #3b82f6;
  background-color: #eff6ff;
}

.pagination-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination-info {
  font-size: 16px;
  font-weight: 500;
  color: #374151;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .charts-grid {
    grid-template-columns: 1fr;
  }
  
  .summary-cards {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .reports-container {
    padding: 16px;
  }
  
  .page-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .header-actions {
    width: 100%;
    justify-content: flex-end;
  }
  
  .date-filter-section {
    padding: 16px;
  }
  
  .date-range-picker {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .summary-cards {
    grid-template-columns: 1fr;
  }
  
  .table-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
  
  .table-filters {
    width: 100%;
    justify-content: space-between;
  }
  
  .reports-table {
    min-width: 800px;
  }
  
  .pagination {
    flex-direction: column;
    gap: 12px;
  }
}

@media (max-width: 480px) {
  .reports-container {
    padding: 12px;
  }
  
  .page-title {
    font-size: 24px;
  }
  
  .export-button {
    width: 100%;
    justify-content: center;
  }
  
  .period-presets {
    flex-wrap: wrap;
  }
  
  .preset-button {
    flex: 1;
    text-align: center;
  }
}
</style>