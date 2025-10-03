<template>
  <div class="reports-container">
    <!-- Page Header -->
    <header class="page-header">
      <div class="header-content">
        <div class="title-section">
          <h1 class="page-title">
            <span class="title-gradient">Reports & Analytics</span>
          </h1>
          <p class="page-subtitle">Performance analysis and trouble ticket statistics</p>
        </div>
        <div class="header-stats">
          <div class="live-indicator">
            <div class="live-dot"></div>
            <span>Live</span>
          </div>
          <div class="header-actions">
            <button class="export-button" @click="exportReport" :disabled="isExporting">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 12L12 18M12 18L8 14M12 18L16 14M16 8L16 6C16 5.46957 15.7893 4.96086 15.4142 4.58579C15.0391 4.21071 14.5304 4 14 4H10C9.46957 4 8.96086 4.21071 8.58579 4.58579C8.21071 4.96086 8 5.46957 8 6L8 8M16 8L16 10M16 8H8M8 8L8 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <span>{{ isExporting ? 'Exporting...' : 'Export Report' }}</span>
            </button>
            <button class="refresh-button" @click="refreshData" :disabled="isRefreshing">
              <svg v-if="!isRefreshing" width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M23 4V10H17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M1 20V14H7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M3.51 9C4.15325 7.99003 5.02055 7.14729 6.04414 6.53788C7.06773 5.92847 8.21931 5.56918 9.4068 5.48856C10.5943 5.40794 11.7844 5.60827 12.882 6.07351C13.9797 6.53875 14.9547 7.25616 15.73 8.17H23M1 4V10H7M20.49 15C19.8468 16.0099 18.9795 16.8527 17.9559 17.4621C16.9323 18.0715 15.7807 18.4308 14.5932 18.5114C13.4057 18.5921 12.2156 18.3917 11.118 17.9265C10.0203 17.4612 9.04534 16.7438 8.27 15.83H1" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <svg v-else class="animate-spin" width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2V6M12 18V22M6 12H2M22 12H18M19.0784 19.0784L16.25 16.25M16.25 7.75L19.0784 4.92157M4.92157 4.92157L7.75 7.75M7.75 16.25L4.92157 19.0784" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <span class="refresh-text">Refresh</span>
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Loading State -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="loading-spinner">
        <div class="spinner"></div>
        <p>Loading report data...</p>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-state">
      <div class="error-icon">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
          <line x1="12" y1="8" x2="12" y2="12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          <line x1="12" y1="16" x2="12.01" y2="16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        </svg>
      </div>
      <h3>Unable to load reports</h3>
      <p>{{ error }}</p>
      <button @click="fetchReportsData" class="retry-button">Try Again</button>
    </div>

    <!-- Reports Content -->
    <div v-else class="reports-content">

      <!-- Date Range Filter -->
      <div class="card filters-card">
        <div class="filters-header">
          <h3 class="filters-title">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            Report Filters
          </h3>
        </div>

        <div class="filter-controls">
          <!-- Date Range Section -->
          <div class="filter-section">
            <div class="section-label">Date Range</div>
            <div class="date-filters">
              <div class="date-filter-group">
                <label for="date-from">From Date</label>
                <input
                  type="date"
                  id="date-from"
                  v-model="filters.startDate"
                  class="date-input"
                  @change="applyFilters"
                >
              </div>
              <div class="date-filter-group">
                <label for="date-to">To Date</label>
                <input
                  type="date"
                  id="date-to"
                  v-model="filters.endDate"
                  class="date-input"
                  @change="applyFilters"
                >
              </div>
            </div>
          </div>

          <!-- Quick Period Selection -->
          <div class="filter-section">
            <div class="section-label">Quick Period</div>
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

          <!-- Filter Options Section -->
          <div class="filter-section">
            <div class="section-label">Filter Details</div>
            <div class="filter-options-grid">
              <div class="filter-dropdowns">
                <select v-model="filters.category" @change="applyFilters" class="filter-select">
                  <option value="">All Categories</option>
                  <option value="Network">Network Issues</option>
                  <option value="Hardware">Hardware Problems</option>
                  <option value="Software">Software Issues</option>
                </select>

  
                <select v-model="filters.status" @change="applyFilters" class="filter-select">
                  <option value="">All Status</option>
                  <option value="Open">Open</option>
                  <option value="Closed">Closed</option>
                </select>
              </div>

              <div class="search-box">
                <svg class="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M21 21L15 15M17 10C17 13.866 13.866 17 10 17C6.13401 17 3 13.866 3 10C3 6.13401 6.13401 3 10 3C13.866 3 17 6.13401 17 10Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <input
                  type="text"
                  v-model="filters.search"
                  placeholder="Search by title, ticket code..."
                  class="search-input"
                  @input="applyFilters"
                >
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Summary Cards -->
      <div class="stats-section">
        <div class="section-header">
          <h2 class="section-title">Report Summary</h2>
          <div class="section-subtitle">Overall ticket performance metrics</div>
        </div>
        <div class="summary-cards">
          <div class="summary-card" v-for="(card, index) in summaryCards" :key="card.title" :style="{ '--delay': index * 0.1 + 's' }">
            <div class="card-background">
              <div class="card-pattern"></div>
            </div>
            <div class="card-icon" :style="{ backgroundColor: card.color + '15', color: card.color }">
              <component :is="card.icon" />
            </div>
            <div class="card-content">
              <div class="card-value-wrapper">
                <h3 class="card-value">{{ card.value }}</h3>
                <div class="card-trend" :class="{ positive: card.trend > 0, negative: card.trend < 0, neutral: card.trend === 0 }">
                  <svg v-if="card.trend > 0" width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 19V5M5 12L12 5L19 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  <svg v-else-if="card.trend < 0" width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 5V19M19 12L12 19L5 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  <span v-if="card.trend !== 0">{{ Math.abs(card.trend) }}%</span>
                </div>
              </div>
              <p class="card-title">{{ card.title }}</p>
            </div>
            <div class="card-glow" :style="{ backgroundColor: card.color + '10' }"></div>
          </div>
        </div>
      </div>

    <!-- Charts Grid -->
    <div class="charts-grid">
      <!-- Ticket Volume by Category Chart -->
      <div class="card chart-card">
        <div class="card-header">
          <h2 class="card-title">Ticket Volume by Category</h2>
          <div class="card-actions">
            <button class="action-button" @click="refreshCategoryStats">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M23 4V10H17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M1 20V14H7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M3.51 9C4.15325 7.99003 5.02055 7.14729 6.04414 6.53788C7.06773 5.92847 8.21931 5.56918 9.4068 5.48856C10.5943 5.40794 11.7844 5.60827 12.882 6.07351C13.9797 6.53875 14.9547 7.25616 15.73 8.17H23M1 4V10H7M20.49 15C19.8468 16.0099 18.9795 16.8527 17.9559 17.4621C16.9323 18.0715 15.7807 18.4308 14.5932 18.5114C13.4057 18.5921 12.2156 18.3917 11.118 17.9265C10.0203 17.4612 9.04534 16.7438 8.27 15.83H1" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>
          </div>
        </div>
        <div class="chart-container">
          <BaseChart
            v-if="categoryChartData && categoryChartData.labels && categoryChartData.labels.length > 0"
            type="doughnut"
            :data="categoryChartData"
          />
          <div v-else class="chart-placeholder">
            <p v-if="categoryStats.value && categoryStats.value.length === 0">No category data available</p>
            <p v-else>Loading chart data...</p>
          </div>
        </div>
      </div>

      <!-- Ticket Status Distribution Chart -->
      <div class="card chart-card">
        <div class="card-header">
          <h2 class="card-title">Ticket Status Distribution</h2>
          <div class="card-actions">
            <button class="action-button" @click="refreshStatusStats">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M23 4V10H17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M1 20V14H7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M3.51 9C4.15325 7.99003 5.02055 7.14729 6.04414 6.53788C7.06773 5.92847 8.21931 5.56918 9.4068 5.48856C10.5943 5.40794 11.7844 5.60827 12.882 6.07351C13.9797 6.53875 14.9547 7.25616 15.73 8.17H23M1 4V10H7M20.49 15C19.8468 16.0099 18.9795 16.8527 17.9559 17.4621C16.9323 18.0715 15.7807 18.4308 14.5932 18.5114C13.4057 18.5921 12.2156 18.3917 11.118 17.9265C10.0203 17.4612 9.04534 16.7438 8.27 15.83H1" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>
          </div>
        </div>
        <div class="chart-container">
          <BaseChart
            v-if="statusChartData && statusChartData.labels && statusChartData.labels.length > 0"
            type="pie"
            :data="statusChartData"
          />
          <div v-else class="chart-placeholder">
            <p v-if="statusStats.value && statusStats.value.length === 0">No status data available</p>
            <p v-else>Loading chart data...</p>
          </div>
        </div>
      </div>

      <!-- Technician Performance Chart -->
      <div class="card chart-card">
        <div class="card-header">
          <h2 class="card-title">Technician Performance</h2>
          <div class="card-actions">
            <select v-model="performanceMetric" class="period-select" @change="refreshTechnicianPerformance">
              <option value="tickets">Resolved Tickets</option>
              <option value="time">Average Time</option>
              <option value="rating">Rating</option>
            </select>
          </div>
        </div>
        <div class="chart-container">
          <BaseChart
            v-if="technicianChartData && technicianChartData.labels && technicianChartData.labels.length > 0"
            type="bar"
            :data="technicianChartData"
            :options="barChartOptions"
          />
          <div v-else class="chart-placeholder">
            <p v-if="technicianStats.value && technicianStats.value.length === 0">No technician data available</p>
            <p v-else>Loading chart data...</p>
          </div>
        </div>
      </div>

    </div>

    <!-- Detailed Reports Table -->
    <div class="card table-card">
      <div class="card-header">
        <h2 class="card-title">Ticket Details</h2>
        <div class="table-info">
          <span class="result-count">Showing {{ pagination.current_page * pagination.items_per_page - pagination.items_per_page + 1 }} - {{ Math.min(pagination.current_page * pagination.items_per_page, pagination.total_items) }} of {{ pagination.total_items }} tickets</span>
        </div>
      </div>
      <div class="table-container">
        <table class="reports-table">
          <thead>
            <tr>
              <th>Ticket Code</th>
              <th>Title</th>
              <th>Category</th>
              <th>Status</th>
              <th>Reporter</th>
              <th>Technician</th>
              <th>Created</th>
              <th>Resolution Time</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="ticket in tickets" :key="ticket.id">
              <td>
                <span class="ticket-code">{{ ticket.ticket_code }}</span>
              </td>
              <td>
                <div class="ticket-title">{{ ticket.title }}</div>
              </td>
              <td>
                <span class="category-badge">{{ getCategoryDisplayName(ticket.category) }}</span>
              </td>
              <td>
                <span class="status-badge" :class="ticket.status.toLowerCase().replace(' ', '-')">
                  {{ ticket.status }}
                </span>
              </td>
              <td>{{ ticket.reporter_name }}</td>
              <td>{{ ticket.assignee || '-' }}</td>
              <td>{{ formatDate(ticket.created_at) }}</td>
              <td>{{ formatResolutionTime(ticket.resolution_time) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="table-footer">
        <div class="pagination">
          <button class="pagination-button" :disabled="pagination.current_page === 1" @click="prevPage">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M15 18L9 12L15 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
          <span class="pagination-info">Page {{ pagination.current_page }} of {{ pagination.total_pages }}</span>
          <button class="pagination-button" :disabled="pagination.current_page === pagination.total_pages" @click="nextPage">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M9 18L15 12L9 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
        </div>
      </div>
    </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, onUnmounted, watch } from 'vue';
import { reportsAPI, type ReportData, type ReportSummary, type ReportTicket, type CategoryStats, type StatusStats, type TechnicianPerformance } from '../api/reportsAPI';
import BaseChart from '../components/BaseChart.vue';
import { Chart, type ChartData, type ChartOptions, registerables } from 'chart.js';

// Register Chart.js components
Chart.register(...registerables);

// State management
const isLoading = ref(true);
const isRefreshing = ref(false);
const isExporting = ref(false);
const error = ref('');
const selectedPreset = ref('7days');
const performanceMetric = ref('tickets');

// Data state
const tickets = ref<ReportTicket[]>([]);
const summary = ref<ReportSummary>({
  total_tickets: 0,
  resolved_tickets: 0,
  open_tickets: 0,
  avg_resolution_time: '0 jam',
  satisfaction_rate: 0
});
const pagination = ref({
  current_page: 1,
  total_pages: 1,
  total_items: 0,
  items_per_page: 10
});

// Chart data
const categoryStats = ref<CategoryStats[]>([]);
const statusStats = ref<StatusStats[]>([]);
const technicianStats = ref<TechnicianPerformance[]>([]);

// Filters
const filters = ref({
  startDate: '',
  endDate: '',
  category: '',
  priority: '',
  status: '',
  search: '',
  page: 1,
  limit: 10
});

// Period presets
const periodPresets = ref([
  { label: '7 Days', value: '7days' },
  { label: '30 Days', value: '30days' },
  { label: '3 Months', value: '3months' },
  { label: '1 Year', value: '1year' }
]);

// Summary cards computed from real data
const summaryCards = computed(() => [
  {
    title: 'Total Tickets',
    value: summary.value.total_tickets.toLocaleString(),
    trend: 12,
    color: '#3b82f6',
    icon: 'TicketIcon'
  },
  {
    title: 'Resolved Tickets',
    value: summary.value.resolved_tickets.toLocaleString(),
    trend: 8,
    color: '#10b981',
    icon: 'CompletedTicketIcon'
  },
  {
    title: 'Average Resolution Time',
    value: summary.value.avg_resolution_time,
    trend: -5,
    color: '#8b5cf6',
    icon: 'TimeIcon'
  }
]);

// Chart data computed properties
const categoryChartData = computed((): ChartData => {
  // Handle null categories by showing as "Uncategorized"
  const processedStats = categoryStats.value.map(stat => ({
    category: getCategoryDisplayName(stat.category),
    count: stat.count
  }));

  return {
    labels: processedStats.map(stat => stat.category),
    datasets: [{
      data: processedStats.map(stat => stat.count),
      backgroundColor: [
        '#3b82f6',
        '#10b981',
        '#f59e0b',
        '#ef4444',
        '#8b5cf6',
        '#ec4899'
      ],
      borderWidth: 2,
      borderColor: '#ffffff'
    }]
  };
});

// Helper function to convert category values to display names
const getCategoryDisplayName = (category: string | null): string => {
  if (!category) return 'Uncategorized';

  switch (category) {
    case 'Network': return 'Network Issues';
    case 'Hardware': return 'Hardware Problems';
    case 'Software': return 'Software Issues';
    default: return category;
  }
};

const statusChartData = computed((): ChartData => ({
  labels: statusStats.value.map(stat => stat.status),
  datasets: [{
    data: statusStats.value.map(stat => stat.count),
    backgroundColor: [
      '#10b981',
      '#f59e0b',
      '#ef4444',
      '#6b7280'
    ],
    borderWidth: 2,
    borderColor: '#ffffff'
  }]
}));

const technicianChartData = computed((): ChartData => {
  // Handle empty technician data
  if (!technicianStats.value || technicianStats.value.length === 0) {
    return {
      labels: ['No Data'],
      datasets: [{
        label: 'No Data Available',
        data: [0],
        backgroundColor: '#e5e7eb',
        borderColor: '#d1d5db',
        borderWidth: 2,
        borderRadius: 6
      }]
    };
  }

  const labels = technicianStats.value.map(stat => stat.technician || 'Unknown Technician');
  let data: number[];
  let label: string;

  switch (performanceMetric.value) {
    case 'tickets':
      data = technicianStats.value.map(stat => stat.resolved_tickets || 0);
      label = 'Resolved Tickets';
      break;
    case 'time':
      // Convert time string to minutes for comparison
      data = technicianStats.value.map(stat => {
        const timeStr = stat.avg_resolution_time || '0m';
        if (timeStr.includes('j')) {
          const [hours, mins] = timeStr.replace('j ', '').replace('m', '').split(' ');
          return parseInt(hours) * 60 + parseInt(mins);
        }
        return parseInt(timeStr.replace('m', ''));
      });
      label = 'Average Resolution Time (minutes)';
      break;
    case 'rating':
      data = technicianStats.value.map(stat => stat.rating || 0);
      label = 'Rating';
      break;
    default:
      data = technicianStats.value.map(stat => stat.resolved_tickets || 0);
      label = 'Resolved Tickets';
  }

  return {
    labels,
    datasets: [{
      label,
      data,
      backgroundColor: '#3b82f6',
      borderColor: '#2563eb',
      borderWidth: 2,
      borderRadius: 6
    }]
  };
});

const barChartOptions: ChartOptions = {
  scales: {
    y: {
      beginAtZero: true,
      grid: {
        display: true,
        color: 'rgba(0, 0, 0, 0.05)'
      }
    },
    x: {
      grid: {
        display: false
      }
    }
  }
};

// Real-time update interval
let updateInterval: NodeJS.Timeout | null = null;


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

const formatResolutionTime = (minutes: number | null) => {
  if (minutes === null || minutes === undefined || minutes === 0) return '-';

  const hours = Math.floor(minutes / 60);
  const mins = minutes % 60;

  if (hours > 0) {
    return `${hours}j ${mins}m`;
  }
  return `${mins}m`;
};

const fetchReportsData = async () => {
  try {
    error.value = '';
    const response = await reportsAPI.getReportsData(filters.value);

    if (response.data) {
      tickets.value = response.data.tickets;
      summary.value = response.data.summary;
      pagination.value = response.data.pagination;
    }
  } catch (err: any) {
    console.error('Error fetching reports data:', err);
    error.value = err.response?.data?.detail || 'Failed to load report data';
  } finally {
    isLoading.value = false;
  }
};

const fetchChartData = async () => {
  try {
    // Fetch each API separately to handle partial failures
    try {
      const categoriesRes = await reportsAPI.getCategoryStats(filters.value);
      categoryStats.value = categoriesRes.data;
    } catch (err) {
      console.error('Error fetching category stats:', err);
      categoryStats.value = [];
    }

    try {
      const statusesRes = await reportsAPI.getStatusStats(filters.value);
      statusStats.value = statusesRes.data;
    } catch (err) {
      console.error('Error fetching status stats:', err);
      statusStats.value = [];
    }

    try {
      const techniciansRes = await reportsAPI.getTechnicianPerformance(filters.value);
      technicianStats.value = techniciansRes.data;
    } catch (err) {
      console.error('Error fetching technician stats:', err);
      technicianStats.value = [];
    }
  } catch (err: any) {
    console.error('Unexpected error in fetchChartData:', err);
  }
};

const applyFilters = async () => {
  filters.value.page = 1;
  await Promise.all([
    fetchReportsData(),
    fetchChartData()
  ]);
};

const selectPreset = async (preset: string) => {
  selectedPreset.value = preset;

  const today = new Date();
  let startDate = new Date(today);

  switch (preset) {
    case '7days':
      startDate.setDate(today.getDate() - 7);
      break;
    case '30days':
      startDate.setDate(today.getDate() - 30);
      break;
    case '3months':
      startDate.setMonth(today.getMonth() - 3);
      break;
    case '1year':
      startDate.setFullYear(today.getFullYear() - 1);
      break;
  }

  filters.value.startDate = startDate.toISOString().split('T')[0];
  filters.value.endDate = today.toISOString().split('T')[0];

  await applyFilters();
};

const refreshData = async () => {
  isRefreshing.value = true;
  try {
    await Promise.all([
      fetchReportsData(),
      fetchChartData()
    ]);
  } finally {
    isRefreshing.value = false;
  }
};

const exportReport = async () => {
  try {
    isExporting.value = true;
    const response = await reportsAPI.exportAllTickets(filters.value);

    // Create a blob and download
    const blob = new Blob([response.data], {
      type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    });

    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `ticket_report_${new Date().toISOString().split('T')[0]}.xlsx`;
    link.click();

    window.URL.revokeObjectURL(url);
  } catch (err: any) {
    console.error('Error exporting report:', err);
    error.value = err.response?.data?.detail || 'Failed to export report';
  } finally {
    isExporting.value = false;
  }
};

const prevPage = async () => {
  if (filters.value.page > 1) {
    filters.value.page--;
    await fetchReportsData();
  }
};

const nextPage = async () => {
  if (filters.value.page < pagination.value.total_pages) {
    filters.value.page++;
    await fetchReportsData();
  }
};

// Chart refresh methods
const refreshCategoryStats = async () => {
  try {
    const response = await reportsAPI.getCategoryStats(filters.value);
    categoryStats.value = response.data;
  } catch (err: any) {
    console.error('Error refreshing category stats:', err);
  }
};

const refreshStatusStats = async () => {
  try {
    const response = await reportsAPI.getStatusStats(filters.value);
    statusStats.value = response.data;
  } catch (err: any) {
    console.error('Error refreshing status stats:', err);
  }
};

const refreshTechnicianPerformance = async () => {
  try {
    const response = await reportsAPI.getTechnicianPerformance(filters.value);
    technicianStats.value = response.data;
  } catch (err: any) {
    console.error('Error refreshing technician performance:', err);
  }
};

// Real-time updates
const startRealTimeUpdates = () => {
  updateInterval = setInterval(() => {
    Promise.all([
      fetchReportsData(),
      fetchChartData()
    ]);
  }, 30000); // Update every 30 seconds
};

const stopRealTimeUpdates = () => {
  if (updateInterval) {
    clearInterval(updateInterval);
    updateInterval = null;
  }
};

// Lifecycle hooks
onMounted(async () => {
  // Set default date range to last 30 days
  await selectPreset('30days');

  // Fetch initial chart data
  await fetchChartData();

  // Start real-time updates
  startRealTimeUpdates();
});

onUnmounted(() => {
  // Clean up interval
  stopRealTimeUpdates();
});
</script>

<style scoped>
* {
  box-sizing: border-box;
}

.reports-container {
  width: 100%;
  min-height: 100vh;
  padding: 1rem;
  background: #ffffff;
  position: relative;
  overflow-x: hidden;
}

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

.export-button,
.refresh-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.export-button {
  background: linear-gradient(135deg, #800000 0%, #5c0000 100%);
  color: white;
}

.export-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(128, 0, 0, 0.3);
}

.export-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.refresh-button {
  background: #f3f4f6;
  color: #374151;
  border: 1px solid #d1d5db;
}

.refresh-button:hover:not(:disabled) {
  background: #e5e7eb;
  border-color: #9ca3af;
}

.refresh-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.refresh-text {
  @media (max-width: 768px) {
    display: none;
  }
}

/* Loading and Error States */
.loading-overlay,
.error-state {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.95);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

.loading-spinner,
.error-icon {
  text-align: center;
  color: #6b7280;
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #e5e7eb;
  border-top: 4px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem auto;
}

.error-icon {
  margin-bottom: 1rem;
}

.error-state h3 {
  margin: 0 0 0.5rem 0;
  color: #1f2937;
  font-size: 1.25rem;
}

.error-state p {
  margin: 0 0 1.5rem 0;
  color: #6b7280;
}

.retry-button {
  padding: 0.75rem 1.5rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s ease;
}

.retry-button:hover {
  background: #2563eb;
}

/* Content */
.reports-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* Cards */
.card {
  background: #ffffff;
  border-radius: 1rem;
  border: 1px solid #e5e7eb;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  overflow: hidden;
}

.card-header {
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.card-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

.card-actions {
  display: flex;
  gap: 0.5rem;
  align-items: center;
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

.period-select {
  padding: 0.5rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  background-color: #fff;
  font-size: 0.875rem;
  color: #374151;
  cursor: pointer;
  transition: all 0.2s ease;
}

.period-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* Filters Section */
.filters-card {
  padding: 0;
  overflow: hidden;
}

.filters-header {
  padding: 1.5rem 2rem;
  background: linear-gradient(135deg, rgba(128, 0, 0, 0.05) 0%, rgba(92, 0, 0, 0.05) 100%);
  border-bottom: 1px solid #e5e7eb;
}

.filters-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.125rem;
  font-weight: 700;
  color: #800000;
  margin: 0;
}

.filters-title svg {
  flex-shrink: 0;
}

.filter-controls {
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.filter-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.section-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #fee2e2;
  display: inline-block;
}

.date-filters {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  align-items: end;
}

.date-filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.date-filter-group label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #475569;
}

.date-input {
  padding: 0.875rem 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 0.875rem;
  color: #1e293b;
  background-color: #f8fafc;
  transition: all 0.3s ease;
  min-width: 150px;
}

.date-input:focus {
  outline: none;
  border-color: #ff4d4f;
  box-shadow: 0 0 0 3px rgba(255, 77, 79, 0.1);
  background-color: #ffffff;
}

.period-presets {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 0.75rem;
}

.preset-button {
  padding: 0.75rem 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  background: #ffffff;
  color: #64748b;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
}

.preset-button:hover {
  border-color: #ff4d4f;
  color: #ff4d4f;
  background: linear-gradient(135deg, rgba(255, 77, 79, 0.05) 0%, rgba(220, 38, 38, 0.05) 100%);
  transform: translateY(-1px);
}

.preset-button.active {
  background: linear-gradient(135deg, #ff4d4f 0%, #dc2626 100%);
  color: white;
  border-color: #ff4d4f;
  box-shadow: 0 4px 12px -2px rgba(255, 77, 79, 0.3);
}

.filter-options-grid {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 1.5rem;
  align-items: end;
}

.filter-dropdowns {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
}

.filter-select {
  padding: 0.875rem 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  background-color: #f8fafc;
  font-size: 0.875rem;
  color: #1e293b;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 150px;
}

.filter-select:focus {
  outline: none;
  border-color: #ff4d4f;
  box-shadow: 0 0 0 3px rgba(255, 77, 79, 0.1);
  background-color: #ffffff;
}

.search-box {
  position: relative;
  min-width: 280px;
}

.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #9ca3af;
  pointer-events: none;
  z-index: 1;
}

.search-input {
  width: 100%;
  padding: 0.875rem 1rem 0.875rem 3rem;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 0.875rem;
  color: #1e293b;
  background-color: #f8fafc;
  transition: all 0.3s ease;
}

.search-input:focus {
  outline: none;
  border-color: #ff4d4f;
  box-shadow: 0 0 0 3px rgba(255, 77, 79, 0.1);
  background-color: #ffffff;
}

.search-input::placeholder {
  color: #9ca3af;
}

/* Stats Section */
.stats-section {
  padding: 2rem;
}

.section-header {
  margin-bottom: 2rem;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 0.5rem 0;
}

.section-subtitle {
  color: #6b7280;
  margin: 0;
  font-size: 0.875rem;
}

.summary-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
}

.summary-card {
  background: #ffffff;
  border-radius: 1rem;
  border: 1px solid #e5e7eb;
  padding: 1.5rem;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
  animation: slideUp 0.6s ease-out;
  animation-delay: var(--delay);
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.summary-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.15);
}

.card-background {
  position: absolute;
  top: 0;
  right: 0;
  width: 100px;
  height: 100px;
  opacity: 0.1;
  pointer-events: none;
}

.card-pattern {
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at center, currentColor 2px, transparent 2px);
  background-size: 20px 20px;
}

.card-icon {
  width: 3.5rem;
  height: 3.5rem;
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
  font-size: 1.5rem;
}

.card-content {
  position: relative;
  z-index: 1;
}

.card-value-wrapper {
  display: flex;
  align-items: baseline;
  gap: 0.75rem;
  margin-bottom: 0.5rem;
}

.card-value {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
  margin: 0;
  line-height: 1;
}

.card-trend {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.875rem;
  font-weight: 500;
}

.card-trend.positive {
  color: #10b981;
}

.card-trend.negative {
  color: #ef4444;
}

.card-trend.neutral {
  color: #6b7280;
}

.card-title {
  font-size: 0.875rem;
  color: #6b7280;
  margin: 0;
  font-weight: 500;
}

.card-glow {
  position: absolute;
  top: -50%;
  right: -50%;
  width: 200%;
  height: 200%;
  border-radius: 50%;
  opacity: 0.1;
  pointer-events: none;
}

/* Charts Grid */
.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 1.5rem;
}

/* With 3 charts, ensure better layout */
@media (min-width: 1200px) {
  .charts-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

.chart-card {
  padding: 0;
}

.chart-card .card-header {
  padding: 1.5rem;
}

.chart-container {
  padding: 1.5rem;
  height: 300px;
  position: relative;
}

.chart-placeholder {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f9fafb;
  border: 2px dashed #e5e7eb;
  border-radius: 0.5rem;
  color: #6b7280;
  font-style: italic;
}

/* Table Card */
.table-card {
  padding: 0;
}

.table-card .card-header {
  padding: 1.5rem;
}

.table-info {
  font-size: 0.875rem;
  color: #6b7280;
}

.result-count {
  font-weight: 500;
}

.table-container {
  overflow-x: auto;
}

.reports-table {
  width: 100%;
  border-collapse: collapse;
  background: #ffffff;
}

.reports-table th {
  text-align: left;
  padding: 0.75rem 1rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
  border-bottom: 2px solid #e5e7eb;
  white-space: nowrap;
  background: #f9fafb;
}

.reports-table td {
  padding: 0.75rem 1rem;
  font-size: 0.875rem;
  color: #374151;
  border-bottom: 1px solid #f3f4f6;
  white-space: nowrap;
}

.reports-table tr:last-child td {
  border-bottom: none;
}

.reports-table tbody tr:hover {
  background-color: #f9fafb;
}

.ticket-code {
  font-family: monospace;
  font-weight: 600;
  color: #3b82f6;
}

.ticket-title {
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.category-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.75rem;
  font-weight: 500;
  background: #f3f4f6;
  color: #374151;
}

.priority-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.75rem;
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
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.75rem;
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

.table-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid #e5e7eb;
  background: #f9fafb;
}

.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

.pagination-button {
  width: 2.5rem;
  height: 2.5rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
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
  font-size: 0.875rem;
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
    padding: 1rem;
  }

  .page-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .header-content {
    flex-direction: column;
    gap: 1rem;
  }

  .header-actions {
    width: 100%;
    justify-content: space-between;
  }

  .filter-controls {
    padding: 1.5rem;
    gap: 1.5rem;
  }

  .date-filters {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .period-presets {
    grid-template-columns: repeat(2, 1fr);
  }

  .filter-options-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .filter-dropdowns {
    grid-template-columns: 1fr;
  }

  .search-box {
    min-width: 100%;
  }

  .summary-cards {
    grid-template-columns: 1fr;
  }

  .stats-section {
    padding: 1rem;
  }

  .reports-table {
    min-width: 800px;
  }

  .pagination {
    flex-direction: column;
    gap: 0.75rem;
  }
}

@media (max-width: 480px) {
  .reports-container {
    padding: 0.5rem;
  }

  .page-title {
    font-size: 1.75rem;
  }

  .export-button {
    width: 100%;
    justify-content: center;
  }

  .period-presets {
    grid-template-columns: 1fr;
  }

  .preset-button {
    width: 100%;
  }

  .filters-header {
    padding: 1rem 1.5rem;
  }

  .filters-title {
    font-size: 1rem;
  }
}

</style>