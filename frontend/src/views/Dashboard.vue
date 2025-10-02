<template>
  <div class="dashboard-container">

    <!-- Page Header -->
    <div class="page-header">
      <div class="header-content">
        <div class="title-section">
          <h1 class="page-title">
            <span class="title-gradient">Dashboard</span>
          </h1>
          <p class="page-subtitle">Welcome back! Here's what's happening with your tickets today.</p>
        </div>
        <div class="header-stats">
          <div class="live-indicator">
            <div class="live-dot"></div>
            <span>Live</span>
          </div>
        </div>
      </div>
      <div class="header-actions">
        <div class="date-filter">
          <label class="filter-label">Time Period</label>
          <select v-model="selectedPeriod" class="period-selector" @change="updateDashboardData">
            <option value="today">Today</option>
            <option value="week">This Week</option>
            <option value="month">This Month</option>
            <option value="year">This Year</option>
          </select>
        </div>
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

    <!-- Loading State -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="loading-spinner">
        <div class="spinner"></div>
        <p>Loading dashboard data...</p>
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
      <h3>Unable to load dashboard</h3>
      <p>{{ error }}</p>
      <button @click="updateDashboardData" class="retry-button">Try Again</button>
    </div>

    <!-- Dashboard Content -->
    <div v-else class="dashboard-content">
      <!-- Stats Overview -->
      <div class="stats-section">
        <div class="section-header">
          <h2 class="section-title">Overview</h2>
          <div class="section-subtitle">Key metrics at a glance</div>
        </div>
        <div class="stats-grid">
          <div class="stat-card" v-for="(stat, index) in stats" :key="stat.title" :style="{ '--delay': index * 0.1 + 's' }">
            <div class="stat-background">
              <div class="stat-pattern"></div>
            </div>
            <div class="stat-icon" :style="{ backgroundColor: stat.color + '15', color: stat.color }">
              <component :is="stat.icon" />
            </div>
            <div class="stat-content">
              <div class="stat-value-wrapper">
                <h3 class="stat-value">{{ stat.value }}</h3>
                <div class="stat-trend" :class="{ positive: stat.trend > 0, negative: stat.trend < 0, neutral: stat.trend === 0 }">
                  <svg v-if="stat.trend > 0" width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 19V5M5 12L12 5L19 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  <svg v-else-if="stat.trend < 0" width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 5V19M19 12L12 19L5 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  <span v-if="stat.trend !== 0">{{ Math.abs(stat.trend) }}%</span>
                </div>
              </div>
              <p class="stat-title">{{ stat.title }}</p>
            </div>
            <div class="stat-glow" :style="{ backgroundColor: stat.color + '10' }"></div>
          </div>
        </div>
      </div>

      <!-- Charts and Analytics Section -->
      <div class="analytics-section">
        <div class="section-header">
          <h2 class="section-title">Analytics</h2>
          <div class="section-subtitle">Detailed insights and trends</div>
        </div>

        <div class="content-grid">
          <!-- Ticket Status Chart -->
          <div class="chart-card enhanced-card">
            <div class="card-header">
              <div class="card-title-group">
                <div class="card-icon">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M9 11H15M21 11C21 16.5228 16.5228 21 11 21C5.47715 21 1 16.5228 1 11C1 5.47715 5.47715 1 11 1C16.5228 1 21 5.47715 21 11Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
                <div>
                  <h3 class="card-title">Ticket Status</h3>
                  <p class="card-subtitle">Current distribution</p>
                </div>
              </div>
              <div class="card-actions">
                <button class="action-button enhanced-button">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="12" cy="12" r="1" fill="currentColor"/>
                    <circle cx="12" cy="5" r="1" fill="currentColor"/>
                    <circle cx="12" cy="19" r="1" fill="currentColor"/>
                  </svg>
                </button>
              </div>
            </div>
            <div class="chart-container">
              <canvas ref="statusChart" data-testid="status-chart"></canvas>
              <div v-if="!dashboardData || !dashboardData.status_distribution || dashboardData.status_distribution.length === 0" class="chart-placeholder">
                <div class="placeholder-icon">
                  <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M9 11H15M21 11C21 16.5228 16.5228 21 11 21C5.47715 21 1 16.5228 1 11C1 5.47715 5.47715 1 11 1C16.5228 1 21 5.47715 21 11Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
                <p>No status data available</p>
              </div>
            </div>
          </div>

          <!-- Priority Distribution Chart -->
          <div class="chart-card enhanced-card">
            <div class="card-header">
              <div class="card-title-group">
                <div class="card-icon priority-icon">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
                <div>
                  <h3 class="card-title">Priority Distribution</h3>
                  <p class="card-subtitle">By urgency level</p>
                </div>
              </div>
              <div class="card-actions">
                <button class="action-button enhanced-button">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="12" cy="12" r="1" fill="currentColor"/>
                    <circle cx="12" cy="5" r="1" fill="currentColor"/>
                    <circle cx="12" cy="19" r="1" fill="currentColor"/>
                  </svg>
                </button>
              </div>
            </div>
            <div class="chart-container">
              <canvas ref="priorityChart" data-testid="priority-chart"></canvas>
              <div v-if="!dashboardData || !dashboardData.priority_distribution || dashboardData.priority_distribution.length === 0" class="chart-placeholder">
                <div class="placeholder-icon">
                  <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
                <p>No priority data available</p>
              </div>
            </div>
          </div>

          <!-- Recent Tickets Table -->
          <div class="table-card enhanced-card">
            <div class="card-header">
              <div class="card-title-group">
                <div class="card-icon recent-icon">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 8V12L15 15M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
                <div>
                  <h3 class="card-title">Recent Tickets</h3>
                  <p class="card-subtitle">Latest updates</p>
                </div>
              </div>
              <div class="card-actions">
                <button class="action-button enhanced-button">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="12" cy="12" r="1" fill="currentColor"/>
                    <circle cx="12" cy="5" r="1" fill="currentColor"/>
                    <circle cx="12" cy="19" r="1" fill="currentColor"/>
                  </svg>
                </button>
              </div>
            </div>
            <div class="table-container">
              <table class="data-table enhanced-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Title</th>
                    <th>Status</th>
                    <th>Priority</th>
                    <th>Created</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="ticket in recentTickets" :key="ticket.id" class="table-row">
                    <td><span class="ticket-id">#{{ ticket.ticket_code }}</span></td>
                    <td><span class="ticket-title">{{ ticket.title }}</span></td>
                    <td>
                      <span class="status-badge enhanced-badge" :class="ticket.status.toLowerCase().replace(' ', '-')">
                        {{ ticket.status }}
                      </span>
                    </td>
                    <td>
                      <span class="priority-badge enhanced-badge" :class="ticket.priority.toLowerCase()">
                        {{ ticket.priority }}
                      </span>
                    </td>
                    <td><span class="ticket-date">{{ formatDate(ticket.created_at) }}</span></td>
                  </tr>
                  <tr v-if="recentTickets.length === 0">
                    <td colspan="5" class="empty-state">
                      <div class="empty-icon">
                        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                          <path d="M9 12H15M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                      </div>
                      No recent tickets
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Top Categories -->
          <div class="categories-card enhanced-card">
            <div class="card-header">
              <div class="card-title-group">
                <div class="card-icon category-icon">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M19 11H5M19 11L13 5M19 11L13 17M5 11L11 5M5 11L11 17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
                <div>
                  <h3 class="card-title">Top Categories</h3>
                  <p class="card-subtitle">Most active areas</p>
                </div>
              </div>
              <div class="card-actions">
                <button class="action-button enhanced-button">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="12" cy="12" r="1" fill="currentColor"/>
                    <circle cx="12" cy="5" r="1" fill="currentColor"/>
                    <circle cx="12" cy="19" r="1" fill="currentColor"/>
                  </svg>
                </button>
              </div>
            </div>
            <div class="categories-list">
              <div class="category-item" v-for="(category, index) in topCategories" :key="category.name" :style="{ '--delay': index * 0.1 + 's' }">
                <div class="category-rank">{{ index + 1 }}</div>
                <div class="category-info">
                  <h3 class="category-name">{{ category.name }}</h3>
                  <div class="category-progress">
                    <div class="progress-bar">
                      <div class="progress-fill" :style="{ width: category.percentage + '%', backgroundColor: category.color || '#3b82f6' }"></div>
                    </div>
                  </div>
                </div>
                <div class="category-stats">
                  <span class="category-count">{{ category.count }}</span>
                  <span class="category-percentage">{{ category.percentage }}%</span>
                </div>
              </div>
              <div v-if="topCategories.length === 0" class="empty-state">
                <div class="empty-icon">
                  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M9 12H15M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
                No categories available
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, markRaw, h } from 'vue';
import { Chart, registerables } from 'chart.js';
import { dashboardAPI, type DashboardData } from '../api/dashboardAPI';

// Register Chart.js components
Chart.register(...registerables);

// State management
const selectedPeriod = ref('week');
const isRefreshing = ref(false);
const dashboardData = ref<DashboardData | null>(null);

// Loading state
const isLoading = ref(true);
const error = ref<string | null>(null);

// Flag untuk mencegah multiple updates
const isUpdating = ref(false);

// Icon components using render function
const OpenTicketIcon = markRaw({
  render() {
    return h('svg', {
      width: 24,
      height: 24,
      viewBox: '0 0 24 24',
      fill: 'none',
      xmlns: 'http://www.w3.org/2000/svg'
    }, [
      h('path', {
        d: 'M21 15C21 15.5304 20.7893 16.0391 20.4142 16.4142C20.0391 16.7893 19.5304 17 19 17H7L3 21V5C3 4.46957 3.21071 3.96086 3.58579 3.58579C3.96086 3.21071 4.46957 3 5 3H19C19.5304 3 20.0391 3.21071 20.4142 3.58579C20.7893 3.96086 21 4.46957 21 5V15Z',
        stroke: 'currentColor',
        'stroke-width': 2,
        'stroke-linecap': 'round',
        'stroke-linejoin': 'round'
      })
    ]);
  }
});

const CompletedTicketIcon = markRaw({
  render() {
    return h('svg', {
      width: 24,
      height: 24,
      viewBox: '0 0 24 24',
      fill: 'none',
      xmlns: 'http://www.w3.org/2000/svg'
    }, [
      h('path', {
        d: 'M9 12L11 14L15 10M21 12C21 13.1819 20.7672 14.3522 20.3141 15.4442C19.861 16.5361 19.1971 17.5282 18.3608 18.3645C17.5245 19.2008 16.5324 19.8647 15.4405 20.3178C14.3485 20.7709 13.1782 21 12 21C10.8218 21 9.65152 20.7709 8.55957 20.3178C7.46763 19.8647 6.47553 19.2008 5.6392 18.3645C4.80288 17.5282 4.13898 16.5361 3.68588 15.4442C3.23279 14.3522 3.00003 13.1819 3 12C3.00003 10.8181 3.23279 9.64781 3.68588 8.55585C4.13898 7.4639 4.80288 6.4718 5.6392 5.63547C6.47553 4.79915 7.46763 4.13525 8.55957 3.68216C9.65152 3.22907 10.8218 3 12 3C13.1782 3 14.3485 3.22907 15.4405 3.68216C16.5324 4.13525 17.5245 4.79915 18.3608 5.63547C19.1971 6.4718 19.861 7.4639 20.3141 8.55585C20.7672 9.64781 20.9999 10.8181 21 12Z',
        stroke: 'currentColor',
        'stroke-width': 2,
        'stroke-linecap': 'round',
        'stroke-linejoin': 'round'
      })
    ]);
  }
});

const TimeIcon = markRaw({
  render() {
    return h('svg', {
      width: 24,
      height: 24,
      viewBox: '0 0 24 24',
      fill: 'none',
      xmlns: 'http://www.w3.org/2000/svg'
    }, [
      h('circle', {
        cx: 12,
        cy: 12,
        r: 10,
        stroke: 'currentColor',
        'stroke-width': 2
      }),
      h('path', {
        d: 'M12 6V12L16 14',
        stroke: 'currentColor',
        'stroke-width': 2,
        'stroke-linecap': 'round',
        'stroke-linejoin': 'round'
      })
    ]);
  }
});

const RemoteIcon = markRaw({
  render() {
    return h('svg', {
      width: 24,
      height: 24,
      viewBox: '0 0 24 24',
      fill: 'none',
      xmlns: 'http://www.w3.org/2000/svg'
    }, [
      h('path', {
        d: 'M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM12 6V12L16 14',
        stroke: 'currentColor',
        'stroke-width': 2,
        'stroke-linecap': 'round',
        'stroke-linejoin': 'round'
      })
    ]);
  }
});

// Reactive data refs
const stats = ref([
  {
    title: 'Open Tickets',
    value: '0',
    trend: 0,
    color: '#ef4444',
    icon: OpenTicketIcon
  },
  {
    title: 'Completed Tickets',
    value: '0',
    trend: 0,
    color: '#10b981',
    icon: CompletedTicketIcon
  },
  {
    title: 'Avg. Resolution Time',
    value: '0',
    trend: 0,
    color: '#8b5cf6',
    icon: TimeIcon
  },
  {
    title: 'Total Remotes',
    value: '0',
    trend: 0,
    color: '#f59e0b',
    icon: RemoteIcon
  }
]);

const recentTickets = ref<any[]>([]);
const topCategories = ref<any[]>([]);

// Chart references
const statusChart = ref<HTMLCanvasElement | null>(null);
const priorityChart = ref<HTMLCanvasElement | null>(null);
let statusChartInstance: Chart | null = null;
let priorityChartInstance: Chart | null = null;

// Methods
const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    day: '2-digit',
    month: 'short',
    year: 'numeric'
  });
};

const updateDashboardData = async () => {
  // Cegah multiple updates
  if (isUpdating.value) {
    console.log('Update already in progress, skipping...');
    return;
  }

  isUpdating.value = true;
  isLoading.value = true;
  error.value = null;

  try {
    console.log('Fetching dashboard data for period:', selectedPeriod.value);
    const response = await dashboardAPI.getDashboardData(selectedPeriod.value);
    console.log('Dashboard API response:', response.data);
    dashboardData.value = response.data;
    
    // Update stats with real data
    stats.value = [
      {
        title: 'Open Tickets',
        value: response.data.stats.open_tickets.toString(),
        trend: 0,
        color: '#ef4444',
        icon: OpenTicketIcon
      },
      {
        title: 'Completed Tickets',
        value: response.data.stats.completed_tickets.toString(),
        trend: 0,
        color: '#10b981',
        icon: CompletedTicketIcon
      },
      {
        title: 'Avg. Resolution Time',
        value: response.data.stats.avg_resolution_time,
        trend: 0,
        color: '#8b5cf6',
        icon: TimeIcon
      },
      {
        title: 'Total Remotes',
        value: response.data.stats.total_remotes.toString(),
        trend: 0,
        color: '#f59e0b',
        icon: RemoteIcon
      }
    ];
    
    // Update recent tickets
    recentTickets.value = response.data.recent_tickets;
    
    // Update top categories
    topCategories.value = response.data.top_categories;
    
  } catch (err) {
    console.error('Error fetching dashboard data:', err);
    error.value = 'Failed to load dashboard data. Please try again.';
  } finally {
    isLoading.value = false;
    isUpdating.value = false;
  }
};

const refreshData = async () => {
  isRefreshing.value = true;
  await updateDashboardData();
  isRefreshing.value = false;
};

// Initialize charts with real data
const initCharts = () => {
  console.log('Initializing charts...', { dashboardData: dashboardData.value });

  // Add a small delay to ensure DOM is ready
  setTimeout(() => {
    // Status distribution chart (doughnut)
    if (statusChart.value && dashboardData.value) {
      console.log('Creating status chart...');
      const ctx = statusChart.value.getContext('2d');
      if (ctx) {
      // Destroy existing chart if it exists
      if (statusChartInstance) {
        statusChartInstance.destroy();
      }
      
      // Status colors mapping
      const statusColors: Record<string, string> = {
        'Open': '#ef4444',
        'In Progress': '#f59e0b',
        'Closed': '#10b981',
        'On Hold': '#6b7280'
      };
      
      // Default colors for unknown statuses
      const defaultColors = ['#800000', '#a52a2a', '#dc143c', '#b22222'];
      
      const labels = dashboardData.value.status_distribution.map(item => item.status);
      const data = dashboardData.value.status_distribution.map(item => item.count);
      const backgroundColors = labels.map((label, index) => 
        statusColors[label] || defaultColors[index % defaultColors.length]
      );
      
      console.log('Status chart data:', { labels, data, backgroundColors });

      statusChartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: labels,
          datasets: [{
            data: data,
            backgroundColor: backgroundColors,
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

      console.log('Status chart created successfully');
      } else {
        console.error('Failed to get context for status chart');
      }
    } else {
      console.log('Status chart not initialized:', {
        hasStatusChart: !!statusChart.value,
        hasDashboardData: !!dashboardData.value,
        statusChartElement: statusChart.value
      });
    }

    // Priority distribution chart (bar)
    if (priorityChart.value && dashboardData.value) {
      console.log('Creating priority chart...');
      const ctx = priorityChart.value.getContext('2d');
      if (ctx) {
      // Destroy existing chart if it exists
      if (priorityChartInstance) {
        priorityChartInstance.destroy();
      }
      
      // Priority colors mapping
      const priorityColors: Record<string, string> = {
        'High': '#ef4444',
        'Medium': '#f59e0b',
        'Low': '#10b981'
      };
      
      const labels = dashboardData.value.priority_distribution.map(item => item.priority);
      const data = dashboardData.value.priority_distribution.map(item => item.count);
      const backgroundColors = labels.map(label =>
        priorityColors[label] || '#800000'
      );
      
      console.log('Priority chart data:', { labels, data, backgroundColors });

      priorityChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [{
            label: 'Number of Tickets',
            data: data,
            backgroundColor: backgroundColors,
            borderRadius: 4
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: false
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

      console.log('Priority chart created successfully');
      } else {
        console.error('Failed to get context for priority chart');
      }
    } else {
      console.log('Priority chart not initialized:', {
        hasPriorityChart: !!priorityChart.value,
        hasDashboardData: !!dashboardData.value,
        priorityChartElement: priorityChart.value
      });
    }
  }, 100); // Small delay to ensure DOM is ready
};

// Reactive data for interval
const refreshIntervalId = ref<number | null>(null);


// Performance optimization: Visibility change handler
const handleVisibilityChange = () => {
  if (document.hidden) {
    // Pause refresh when tab is not visible
    if (refreshIntervalId.value !== null) {
      clearInterval(refreshIntervalId.value);
      refreshIntervalId.value = null;
    }
  } else {
    // Resume refresh when tab becomes visible - hanya jika interval tidak ada
    if (refreshIntervalId.value === null) {
      refreshIntervalId.value = setInterval(() => {
        updateDashboardData();
      }, 60000); // Refresh setiap 1 menit
    }
  }
};

// Lifecycle hooks
onMounted(() => {
  updateDashboardData();

  // Set up automatic refresh every 60 seconds (1 menit) bukan 10 detik
  refreshIntervalId.value = setInterval(() => {
    updateDashboardData();
  }, 60000); // Refresh setiap 1 menit

  // Add visibility change listener for performance optimization
  document.addEventListener('visibilitychange', handleVisibilityChange);
});

onUnmounted(() => {
  // Clear the interval when the component is unmounted
  if (refreshIntervalId.value !== null) {
    clearInterval(refreshIntervalId.value);
  }

  // Clear timeout if exists
  if (periodChangeTimeout) {
    clearTimeout(periodChangeTimeout);
  }

  // Remove event listener
  document.removeEventListener('visibilitychange', handleVisibilityChange);
});

// Watch for data changes to update charts
watch(dashboardData, (newData) => {
  console.log('Dashboard data changed:', newData);
  if (dashboardData.value && !isUpdating.value) {
    initCharts();
  }
});

// Watch for period changes - debounced
let periodChangeTimeout: number | null = null;
watch(selectedPeriod, () => {
  // Clear existing timeout
  if (periodChangeTimeout) {
    clearTimeout(periodChangeTimeout);
  }

  // Debounced update
  periodChangeTimeout = setTimeout(() => {
    if (!isUpdating.value) {
      updateDashboardData();
    }
  }, 300) as unknown as number;
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
  background: #ffffff;
  position: relative;
  overflow-x: hidden;
}

.page-header {
  background: #ffffff;
  border-radius: 1rem;
  padding: 2rem;
  margin-bottom: 2rem;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
  flex-wrap: wrap;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  border: 1px solid #e5e7eb;
}

.header-content {
  flex: 1;
  min-width: 250px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 2rem;
}

.title-section {
  flex: 1;
}

.page-title {
  font-size: clamp(2rem, 4vw, 3rem);
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
  gap: 1rem;
}

.live-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: rgba(128, 0, 0, 0.1);
  border-radius: 2rem;
  color: #800000;
  font-size: 0.875rem;
  font-weight: 500;
}

.live-dot {
  width: 8px;
  height: 8px;
  background: #800000;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.header-actions {
  display: flex;
  align-items: flex-end;
  gap: 1rem;
  flex-wrap: wrap;
}

.date-filter {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-label {
  font-size: 0.75rem;
  color: #64748b;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.period-selector {
  padding: 0.75rem 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 0.75rem;
  background: #ffffff;
  font-size: 0.875rem;
  color: #374151;
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 140px;
  font-weight: 500;
}

.period-selector:focus {
  outline: none;
  border-color: #800000;
  box-shadow: 0 0 0 3px rgba(128, 0, 0, 0.1);
}

.refresh-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border: 2px solid #e2e8f0;
  border-radius: 0.75rem;
  background: #ffffff;
  color: #374151;
  cursor: pointer;
  transition: all 0.2s ease;
  font-weight: 500;
  font-size: 0.875rem;
}

.refresh-button:hover:not(:disabled) {
  border-color: #800000;
  color: #800000;
  background: linear-gradient(135deg, rgba(128, 0, 0, 0.05) 0%, rgba(92, 0, 0, 0.05) 100%);
  transform: translateY(-1px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

.refresh-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.refresh-text {
  font-weight: 500;
}

/* Loading and Error States */
.loading-overlay, .error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  text-align: center;
  background: #ffffff;
  border-radius: 1rem;
  margin: 2rem 0;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  border: 1px solid #e5e7eb;
}

.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e2e8f0;
  border-top: 4px solid #800000;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-state h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #374151;
  margin: 1rem 0 0.5rem 0;
}

.error-state p {
  color: #64748b;
  margin: 0 0 1.5rem 0;
}

.error-icon {
  color: #ef4444;
  margin-bottom: 1rem;
}

.retry-button {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #800000 0%, #5c0000 100%);
  color: white;
  border: none;
  border-radius: 0.75rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.retry-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
}

/* Section Headers */
.stats-section, .analytics-section {
  background: #ffffff;
  border-radius: 1rem;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  border: 1px solid #e5e7eb;
}

.section-header {
  margin-bottom: 2rem;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
  line-height: 1.2;
}

.section-subtitle {
  font-size: 1rem;
  color: #64748b;
  margin: 0;
  line-height: 1.4;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}

.stat-card {
  position: relative;
  background: #ffffff;
  border-radius: 1rem;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: all 0.3s ease;
  min-height: 120px;
  border: 1px solid rgba(226, 232, 240, 0.5);
  animation: slideInUp 0.5s ease-out;
  animation-delay: var(--delay);
  animation-fill-mode: both;
  overflow: hidden;
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.15), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.stat-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  opacity: 0.03;
  z-index: 0;
}

.stat-pattern {
  width: 100%;
  height: 100%;
  background-image: radial-gradient(circle, currentColor 1px, transparent 1px);
  background-size: 20px 20px;
}

.stat-icon {
  width: 4rem;
  height: 4rem;
  border-radius: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  position: relative;
  z-index: 1;
  font-size: 1.5rem;
}

.stat-content {
  flex: 1;
  min-width: 0;
  position: relative;
  z-index: 1;
}

.stat-value-wrapper {
  display: flex;
  align-items: baseline;
  gap: 0.75rem;
  margin-bottom: 0.25rem;
}

.stat-value {
  font-size: clamp(1.5rem, 3vw, 2rem);
  font-weight: 800;
  color: #1e293b;
  margin: 0;
  line-height: 1.1;
}

.stat-trend {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.875rem;
  font-weight: 600;
  padding: 0.25rem 0.5rem;
  border-radius: 0.375rem;
}

.stat-trend.positive {
  color: #059669;
  background: rgba(16, 185, 129, 0.1);
}

.stat-trend.negative {
  color: #dc2626;
  background: rgba(239, 68, 68, 0.1);
}

.stat-trend.neutral {
  color: #64748b;
  background: rgba(100, 116, 139, 0.1);
}

.stat-title {
  font-size: 0.875rem;
  color: #64748b;
  margin: 0;
  line-height: 1.4;
  font-weight: 500;
}

.stat-glow {
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  border-radius: 50%;
  z-index: 0;
  filter: blur(40px);
  opacity: 0.4;
}

/* Content Grid */
.content-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
  gap: 1.5rem;
}

.enhanced-card {
  background: #ffffff;
  border-radius: 1rem;
  padding: 2rem;
  transition: all 0.3s ease;
  min-height: 400px;
  border: 1px solid rgba(226, 232, 240, 0.5);
  position: relative;
  overflow: hidden;
}

.enhanced-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(135deg, #800000 0%, #5c0000 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.enhanced-card:hover::before {
  opacity: 1;
}

.enhanced-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.15), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
  gap: 1rem;
}

.card-title-group {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  flex: 1;
}

.card-icon {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  background: linear-gradient(135deg, rgba(128, 0, 0, 0.1) 0%, rgba(92, 0, 0, 0.1) 100%);
  color: #800000;
}

.card-icon.priority-icon {
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(239, 68, 68, 0.1) 100%);
  color: #f59e0b;
}

.card-icon.recent-icon {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.1) 100%);
  color: #10b981;
}

.card-icon.category-icon {
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(124, 58, 237, 0.1) 100%);
  color: #8b5cf6;
}

.card-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 0.25rem 0;
  line-height: 1.2;
}

.card-subtitle {
  font-size: 0.875rem;
  color: #64748b;
  margin: 0;
  line-height: 1.4;
  font-weight: 400;
}

.card-actions {
  display: flex;
  gap: 0.5rem;
  flex-shrink: 0;
}

.enhanced-button {
  width: 2.5rem;
  height: 2.5rem;
  border: 1px solid rgba(226, 232, 240, 0.5);
  border-radius: 0.75rem;
  background: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s ease;
}

.enhanced-button:hover {
  border-color: #800000;
  color: #800000;
  background: linear-gradient(135deg, rgba(128, 0, 0, 0.05) 0%, rgba(92, 0, 0, 0.05) 100%);
  transform: scale(1.05);
}

.chart-container {
  height: 300px;
  min-height: 250px;
  position: relative;
  width: 100%;
  background: #ffffff;
  border-radius: 0.75rem;
  border: 1px solid #e5e7eb;
  padding: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chart-container canvas {
  max-width: 100%;
  max-height: 100%;
  display: block;
}

.chart-placeholder {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #9ca3af;
  background: #f9fafb;
  border-radius: 0.75rem;
}

.placeholder-icon {
  margin-bottom: 1rem;
  opacity: 0.5;
}

.chart-placeholder p {
  margin: 0;
  font-size: 0.875rem;
  font-weight: 500;
}

.table-container {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  border-radius: 0.75rem;
  border: 1px solid rgba(226, 232, 240, 0.5);
}

.enhanced-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 500px;
}

.enhanced-table th {
  text-align: left;
  padding: 1rem;
  font-size: 0.75rem;
  font-weight: 600;
  color: #64748b;
  background: rgba(248, 250, 252, 0.8);
  border-bottom: 1px solid rgba(226, 232, 240, 0.5);
  white-space: nowrap;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.enhanced-table td {
  padding: 1rem;
  font-size: 0.875rem;
  color: #374151;
  border-bottom: 1px solid rgba(226, 232, 240, 0.3);
  white-space: nowrap;
}

.enhanced-table tr:last-child td {
  border-bottom: none;
}

.table-row {
  transition: background-color 0.2s ease;
}

.table-row:hover td {
  background-color: rgba(128, 0, 0, 0.02);
}

.ticket-id {
  font-family: 'Courier New', monospace;
  font-weight: 600;
  color: #800000;
}

.ticket-title {
  font-weight: 500;
  color: #1e293b;
}

.ticket-date {
  color: #64748b;
  font-size: 0.875rem;
}

.enhanced-badge {
  padding: 0.375rem 0.75rem;
  border-radius: 0.5rem;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  white-space: nowrap;
  letter-spacing: 0.05em;
  border: 1px solid transparent;
  transition: all 0.2s ease;
}

.status-badge.enhanced-badge.open {
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(220, 38, 38, 0.1) 100%);
  color: #dc2626;
  border-color: rgba(239, 68, 68, 0.2);
}

.status-badge.enhanced-badge.in-progress {
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(217, 119, 6, 0.1) 100%);
  color: #d97706;
  border-color: rgba(245, 158, 11, 0.2);
}

.status-badge.enhanced-badge.closed {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.1) 100%);
  color: #059669;
  border-color: rgba(16, 185, 129, 0.2);
}

.status-badge.enhanced-badge.on-hold {
  background: linear-gradient(135deg, rgba(107, 114, 128, 0.1) 0%, rgba(55, 65, 81, 0.1) 100%);
  color: #374151;
  border-color: rgba(107, 114, 128, 0.2);
}

.priority-badge.enhanced-badge.high {
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(220, 38, 38, 0.1) 100%);
  color: #dc2626;
  border-color: rgba(239, 68, 68, 0.2);
}

.priority-badge.enhanced-badge.medium {
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(217, 119, 6, 0.1) 100%);
  color: #d97706;
  border-color: rgba(245, 158, 11, 0.2);
}

.priority-badge.enhanced-badge.low {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.1) 100%);
  color: #059669;
  border-color: rgba(16, 185, 129, 0.2);
}

.categories-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.category-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(248, 250, 252, 0.5);
  border-radius: 0.75rem;
  border: 1px solid rgba(226, 232, 240, 0.3);
  transition: all 0.3s ease;
  animation: slideInLeft 0.5s ease-out;
  animation-delay: var(--delay);
  animation-fill-mode: both;
}

@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.category-item:hover {
  background: rgba(102, 126, 234, 0.02);
  border-color: rgba(102, 126, 234, 0.2);
  transform: translateX(4px);
}

.category-rank {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 0.75rem;
  background: linear-gradient(135deg, #800000 0%, #5c0000 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1rem;
  flex-shrink: 0;
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
  font-weight: 600;
  color: #1e293b;
  margin: 0;
  line-height: 1.2;
}

.category-progress {
  width: 100%;
}

.progress-bar {
  height: 0.75rem;
  background-color: rgba(226, 232, 240, 0.5);
  border-radius: 0.375rem;
  overflow: hidden;
  position: relative;
}

.progress-fill {
  height: 100%;
  border-radius: 0.375rem;
  transition: width 1s ease-out;
  position: relative;
  background: linear-gradient(135deg, var(--progress-color, '#800000') 0%, var(--progress-color-dark, '#5c0000') 100%);
}

.progress-fill::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  animation: shimmer 2s infinite;
}

@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.category-stats {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.25rem;
  flex-shrink: 0;
}

.category-count {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1e293b;
  white-space: nowrap;
}

.category-percentage {
  font-size: 0.875rem;
  color: #64748b;
  font-weight: 500;
  white-space: nowrap;
}

/* Empty States */
.empty-state {
  text-align: center;
  padding: 3rem 2rem;
  color: #64748b;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.empty-icon {
  color: #cbd5e1;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Animations */
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.animate-spin {
  animation: spin 1s linear infinite;
}

.loading .stat-value,
.loading .stat-title {
  background-color: #e5e7eb;
  color: transparent;
  border-radius: 0.25rem;
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

/* Responsive adjustments for more cards */
@media (min-width: 1400px) {
  .content-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .chart-card:first-child,
  .table-card,
  .categories-card {
    grid-column: span 1;
  }
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