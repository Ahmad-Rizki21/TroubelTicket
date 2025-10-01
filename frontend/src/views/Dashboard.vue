<template>
  <div class="dashboard-container">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">Dashboard</h1>
        <p class="page-subtitle">Selamat datang kembali! Berikut ringkasan aktivitas tiket Anda.</p>
      </div>
      <div class="header-actions">
        <div class="date-filter">
          <select v-model="selectedPeriod" class="period-selector" @change="updateDashboardData">
            <option value="today">Hari Ini</option>
            <option value="week">Minggu Ini</option>
            <option value="month">Bulan Ini</option>
            <option value="year">Tahun Ini</option>
          </select>
        </div>
        <button class="refresh-button" @click="refreshData">
          <svg v-if="!isRefreshing" width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M23 4V10H17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M1 20V14H7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M3.51 9C4.15325 7.99003 5.02055 7.14729 6.04414 6.53788C7.06773 5.92847 8.21931 5.56918 9.4068 5.48856C10.5943 5.40794 11.7844 5.60827 12.882 6.07351C13.9797 6.53875 14.9547 7.25616 15.73 8.17H23M1 4V10H7M20.49 15C19.8468 16.0099 18.9795 16.8527 17.9559 17.4621C16.9323 18.0715 15.7807 18.4308 14.5932 18.5114C13.4057 18.5921 12.2156 18.3917 11.118 17.9265C10.0203 17.4612 9.04534 16.7438 8.27 15.83H1" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <svg v-else class="animate-spin" width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2V6M12 18V22M6 12H2M22 12H18M19.0784 19.0784L16.25 16.25M16.25 7.75L19.0784 4.92157M4.92157 4.92157L7.75 7.75M7.75 16.25L4.92157 19.0784" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
      </div>
    </div>

    <!-- Stats Overview -->
    <div class="stats-grid">
      <div class="stat-card" v-for="stat in stats" :key="stat.title">
        <div class="stat-icon" :style="{ backgroundColor: stat.color + '20', color: stat.color }">
          <component :is="stat.icon" />
        </div>
        <div class="stat-content">
          <h3 class="stat-value">{{ stat.value }}</h3>
          <p class="stat-title">{{ stat.title }}</p>
        </div>
        <div class="stat-trend" :class="{ positive: stat.trend > 0, negative: stat.trend < 0 }">
          <svg v-if="stat.trend > 0" width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 19V5M5 12L12 5L19 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <svg v-else-if="stat.trend < 0" width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 5V19M19 12L12 19L5 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span>{{ Math.abs(stat.trend) }}%</span>
        </div>
      </div>
    </div>

    <!-- Charts and Tables Grid -->
    <div class="content-grid">
      <!-- Ticket Status Chart -->
      <div class="chart-card">
        <div class="card-header">
          <h2 class="card-title">Status Tiket</h2>
          <div class="card-actions">
            <button class="action-button">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 5V19M5 12H19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>
          </div>
        </div>
        <div class="chart-container">
          <canvas ref="statusChart"></canvas>
        </div>
      </div>

      <!-- Recent Tickets Table -->
      <div class="table-card">
        <div class="card-header">
          <h2 class="card-title">Tiket Terbaru</h2>
          <div class="card-actions">
            <button class="action-button">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 5V19M5 12H19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>
          </div>
        </div>
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Judul</th>
                <th>Status</th>
                <th>Prioritas</th>
                <th>Dibuat</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="ticket in recentTickets" :key="ticket.id">
                <td>#{{ ticket.id }}</td>
                <td>{{ ticket.title }}</td>
                <td>
                  <span class="status-badge" :class="ticket.status.toLowerCase()">
                    {{ ticket.status }}
                  </span>
                </td>
                <td>
                  <span class="priority-badge" :class="ticket.priority.toLowerCase()">
                    {{ ticket.priority }}
                  </span>
                </td>
                <td>{{ formatDate(ticket.created_at) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Priority Distribution Chart -->
      <div class="chart-card">
        <div class="card-header">
          <h2 class="card-title">Distribusi Prioritas</h2>
          <div class="card-actions">
            <button class="action-button">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 5V19M5 12H19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>
          </div>
        </div>
        <div class="chart-container">
          <canvas ref="priorityChart"></canvas>
        </div>
      </div>

      <!-- Top Categories -->
      <div class="categories-card">
        <div class="card-header">
          <h2 class="card-title">Kategori Teratas</h2>
          <div class="card-actions">
            <button class="action-button">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 5V19M5 12H19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>
          </div>
        </div>
        <div class="categories-list">
          <div class="category-item" v-for="category in topCategories" :key="category.name">
            <div class="category-info">
              <h3 class="category-name">{{ category.name }}</h3>
              <div class="category-progress">
                <div class="progress-bar">
                  <div class="progress-fill" :style="{ width: category.percentage + '%', backgroundColor: category.color }"></div>
                </div>
              </div>
            </div>
            <div class="category-stats">
              <span class="category-count">{{ category.count }}</span>
              <span class="category-percentage">{{ category.percentage }}%</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { Chart, registerables } from 'chart.js';

// Register Chart.js components
Chart.register(...registerables);

// State management
const selectedPeriod = ref('week');
const isRefreshing = ref(false);

// Icon components
const TicketIcon = {
  template: `
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M15 5V7M15 11V13M15 17V19M5 5C3.89543 5 3 5.89543 3 7V10C4.10457 10 5 10.8954 5 12C5 13.1046 4.10457 14 3 14V17C3 18.1046 3.89543 19 5 19H19C20.1046 19 21 18.1046 21 17V14C19.8954 14 19 13.1046 19 12C19 10.8954 19.8954 10 21 10V7C21 5.89543 20.1046 5 19 5H5Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  `
};

const OpenTicketIcon = {
  template: `
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M21 15C21 15.5304 20.7893 16.0391 20.4142 16.4142C20.0391 16.7893 19.5304 17 19 17H7L3 21V5C3 4.46957 3.21071 3.96086 3.58579 3.58579C3.96086 3.21071 4.46957 3 5 3H19C19.5304 3 20.0391 3.21071 20.4142 3.58579C20.7893 3.96086 21 4.46957 21 5V15Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  `
};

const CompletedTicketIcon = {
  template: `
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M9 12L11 14L15 10M21 12C21 13.1819 20.7672 14.3522 20.3141 15.4442C19.861 16.5361 19.1971 17.5282 18.3608 18.3645C17.5245 19.2008 16.5324 19.8647 15.4405 20.3178C14.3485 20.7709 13.1782 21 12 21C10.8218 21 9.65152 20.7709 8.55957 20.3178C7.46763 19.8647 6.47553 19.2008 5.6392 18.3645C4.80288 17.5282 4.13898 16.5361 3.68588 15.4442C3.23279 14.3522 3.00003 13.1819 3 12C3.00003 10.8181 3.23279 9.64781 3.68588 8.55585C4.13898 7.4639 4.80288 6.4718 5.6392 5.63547C6.47553 4.79915 7.46763 4.13525 8.55957 3.68216C9.65152 3.22907 10.8218 3 12 3C13.1782 3 14.3485 3.22907 15.4405 3.68216C16.5324 4.13525 17.5245 4.79915 18.3608 5.63547C19.1971 6.4718 19.861 7.4639 20.3141 8.55585C20.7672 9.64781 20.9999 10.8181 21 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  `
};

const TimeIcon = {
  template: `
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
      <path d="M12 6V12L16 14" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  `
};

// Mock data for demonstration
const stats = ref([
  {
    title: 'Total Tiket',
    value: '142',
    trend: 12,
    color: '#3b82f6',
    icon: TicketIcon
  },
  {
    title: 'Tiket Terbuka',
    value: '24',
    trend: -3,
    color: '#ef4444',
    icon: OpenTicketIcon
  },
  {
    title: 'Tiket Diselesaikan',
    value: '118',
    trend: 8,
    color: '#10b981',
    icon: CompletedTicketIcon
  },
  {
    title: 'Rata-rata Resolusi',
    value: '2.3 hari',
    trend: -5,
    color: '#8b5cf6',
    icon: TimeIcon
  }
]);

const recentTickets = ref([
  {
    id: '001',
    title: 'Internet Lambat di Ruang IT',
    status: 'Terbuka',
    priority: 'Tinggi',
    created_at: '2023-06-15T09:30:00Z'
  },
  {
    id: '002',
    title: 'Printer Tidak Merespon',
    status: 'Dalam Proses',
    priority: 'Sedang',
    created_at: '2023-06-14T14:15:00Z'
  },
  {
    id: '003',
    title: 'Software Accounting Error',
    status: 'Selesai',
    priority: 'Rendah',
    created_at: '2023-06-13T11:45:00Z'
  },
  {
    id: '004',
    title: 'Komputer Tidak Bisa Boot',
    status: 'Terbuka',
    priority: 'Tinggi',
    created_at: '2023-06-12T16:20:00Z'
  },
  {
    id: '005',
    title: 'Email Server Down',
    status: 'Dalam Proses',
    priority: 'Tinggi',
    created_at: '2023-06-11T08:10:00Z'
  }
]);

const topCategories = ref([
  {
    name: 'Jaringan',
    count: 42,
    percentage: 35,
    color: '#3b82f6'
  },
  {
    name: 'Hardware',
    count: 38,
    percentage: 32,
    color: '#ef4444'
  },
  {
    name: 'Software',
    count: 31,
    percentage: 26,
    color: '#10b981'
  },
  {
    name: 'Lainnya',
    count: 8,
    percentage: 7,
    color: '#8b5cf6'
  }
]);

// Chart references
const statusChart = ref<HTMLCanvasElement | null>(null);
const priorityChart = ref<HTMLCanvasElement | null>(null);
let statusChartInstance: Chart | null = null;
let priorityChartInstance: Chart | null = null;

// Methods
const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('id-ID', {
    day: '2-digit',
    month: 'short',
    year: 'numeric'
  });
};

const updateDashboardData = () => {
  console.log(`Updating dashboard data for period: ${selectedPeriod.value}`);
};

const refreshData = () => {
  isRefreshing.value = true;
  setTimeout(() => {
    isRefreshing.value = false;
  }, 1000);
};

// Initialize charts
const initCharts = () => {
  if (statusChart.value) {
    const ctx = statusChart.value.getContext('2d');
    if (ctx) {
      statusChartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: ['Terbuka', 'Dalam Proses', 'Selesai', 'Ditunda'],
          datasets: [{
            data: [24, 18, 118, 5],
            backgroundColor: [
              '#ef4444',
              '#f59e0b',
              '#10b981',
              '#6b7280'
            ],
            borderWidth: 0
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'bottom',
              labels: {
                padding: 20,
                usePointStyle: true,
                pointStyle: 'circle'
              }
            }
          },
          cutout: '70%'
        }
      });
    }
  }

  if (priorityChart.value) {
    const ctx = priorityChart.value.getContext('2d');
    if (ctx) {
      priorityChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun'],
          datasets: [
            {
              label: 'Tinggi',
              data: [12, 19, 15, 17, 14, 24],
              backgroundColor: '#ef4444',
              borderRadius: 4
            },
            {
              label: 'Sedang',
              data: [22, 28, 25, 30, 27, 38],
              backgroundColor: '#f59e0b',
              borderRadius: 4
            },
            {
              label: 'Rendah',
              data: [15, 18, 12, 20, 16, 25],
              backgroundColor: '#10b981',
              borderRadius: 4
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'top',
              labels: {
                usePointStyle: true,
                pointStyle: 'rectRounded'
              }
            }
          },
          scales: {
            x: {
              grid: {
                display: false
              }
            },
            y: {
              beginAtZero: true,
              grid: {
                color: 'rgba(0, 0, 0, 0.05)'
              }
            }
          }
        }
      });
    }
  }
};

// Lifecycle hooks
onMounted(() => {
  initCharts();
});

// Watch for theme changes or data updates
watch([stats, recentTickets, topCategories], () => {
  if (statusChartInstance) {
    statusChartInstance.update();
  }
  if (priorityChartInstance) {
    priorityChartInstance.update();
  }
});
</script>

<style scoped>
* {
  box-sizing: border-box;
}

.dashboard-container {
  width: 100%;
  min-height: 100vh;
  padding: 1rem;
  background-color: #f8fafc;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
  gap: 1rem;
  flex-wrap: wrap;
}

.header-content {
  flex: 1;
  min-width: 250px;
}

.page-title {
  font-size: clamp(1.5rem, 4vw, 2rem);
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
  line-height: 1.2;
}

.page-subtitle {
  font-size: clamp(0.875rem, 2vw, 1rem);
  color: #64748b;
  margin: 0;
  line-height: 1.4;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.period-selector {
  padding: 0.5rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  background-color: #fff;
  font-size: 0.875rem;
  color: #374151;
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 120px;
}

.period-selector:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
}

.refresh-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  height: 2.5rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  background-color: #fff;
  color: #374151;
  cursor: pointer;
  transition: all 0.2s ease;
}

.refresh-button:hover {
  border-color: #3b82f6;
  color: #3b82f6;
  background-color: #eff6ff;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: #ffffff;
  border-radius: 1rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  min-height: 120px;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0,0.05);
}

.stat-icon {
  width: 3.5rem;
  height: 3.5rem;
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-content {
  flex: 1;
  min-width: 0;
}

.stat-value {
  font-size: clamp(1.25rem, 3vw, 1.5rem);
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 0.25rem 0;
  line-height: 1.2;
}

.stat-title {
  font-size: 0.875rem;
  color: #64748b;
  margin: 0;
  line-height: 1.4;
}

.stat-trend {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.875rem;
  font-weight: 500;
  flex-shrink: 0;
}

.stat-trend.positive {
  color: #10b981;
}

.stat-trend.negative {
  color: #ef4444;
}

/* Content Grid */
.content-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 1.5rem;
}

.chart-card, .table-card, .categories-card {
  background: #ffffff;
  border-radius: 1rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  padding: 1.5rem;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  min-height: 400px;
}

.chart-card:hover, .table-card:hover, .categories-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  gap: 1rem;
}

.card-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
  line-height: 1.2;
}

.card-actions {
  display: flex;
  gap: 0.5rem;
  flex-shrink: 0;
}

.action-button {
  width: 2rem;
  height: 2rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
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
  width: 100%;
}

.table-container {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 500px;
}

.data-table th {
  text-align: left;
  padding: 0.75rem 1rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
  border-bottom: 2px solid #e5e7eb;
  white-space: nowrap;
}

.data-table td {
  padding: 0.75rem 1rem;
  font-size: 0.875rem;
  color: #374151;
  border-bottom: 1px solid #e5e7eb;
  white-space: nowrap;
}

.data-table tr:last-child td {
  border-bottom: none;
}

.data-table tr:hover td {
  background-color: #f9fafb;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 1.25rem;
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: uppercase;
  white-space: nowrap;
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

.priority-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 1.25rem;
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: uppercase;
  white-space: nowrap;
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

.categories-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.category-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.category-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  min-width: 0;
}

.category-name {
  font-size: 1rem;
  font-weight: 500;
  color: #1e293b;
  margin: 0;
  line-height: 1.2;
}

.category-progress {
  width: 100%;
}

.progress-bar {
  height: 0.5rem;
  background-color: #e5e7eb;
  border-radius: 0.25rem;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: 0.25rem;
  transition: width 0.3s ease;
}

.category-stats {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-shrink: 0;
}

.category-count {
  font-size: 1rem;
  font-weight: 600;
  color: #1e293b;
  white-space: nowrap;
}

.category-percentage {
  font-size: 0.875rem;
  color: #64748b;
  min-width: 2.5rem;
  text-align: right;
  white-space: nowrap;
}

/* Animations */
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.animate-spin {
  animation: spin 1s linear infinite;
}

/* Responsive Design */
@media (max-width: 1200px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
  
  .stats-grid {
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  }
}

@media (max-width: 768px) {
  .dashboard-container {
    padding: 0.75rem;
  }
  
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .header-actions {
    width: 100%;
    justify-content: space-between;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .stat-card {
    padding: 1rem;
    min-height: 100px;
  }
  
  .stat-icon {
    width: 3rem;
    height: 3rem;
  }
  
  .chart-card, .table-card, .categories-card {
    padding: 1rem;
    min-height: 350px;
  }
  
  .chart-container {
    height: 250px;
  }
  
  .content-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .category-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .category-stats {
    width: 100%;
    justify-content: space-between;
  }
}

@media (max-width: 480px) {
  .dashboard-container {
    padding: 0.5rem;
  }
  
  .page-title {
    font-size: 1.5rem;
  }
  
  .stat-card {
    flex-direction: column;
    text-align: center;
    gap: 0.75rem;
  }
  
  .stat-content {
    text-align: center;
  }
  
  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }
  
  .card-actions {
    align-self: flex-end;
  }
  
  .data-table th,
  .data-table td {
    padding: 0.5rem 0.75rem;
  }
}

/* Print styles */
@media print {
  .dashboard-container {
    background: white;
    padding: 1rem;
  }
  
  .header-actions {
    display: none;
  }
  
  .stat-card, .chart-card, .table-card, .categories-card {
    box-shadow: none;
    border: 1px solid #e5e7eb;
    break-inside: avoid;
  }
  
  .content-grid {
    display: block;
  }
  
  .chart-card, .table-card, .categories-card {
    margin-bottom: 2rem;
  }
}

/* High contrast mode */
@media (prefers-contrast: high) {
  .stat-card, .chart-card, .table-card, .categories-card {
    border: 2px solid #000;
  }
  
  .status-badge, .priority-badge {
    border: 1px solid #000;
  }
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
  .stat-card, .chart-card, .table-card, .categories-card {
    transition: none;
  }
  
  .animate-spin {
    animation: none;
  }
  
  .progress-fill {
    transition: none;
  }
}
</style>