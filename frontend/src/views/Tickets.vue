<template>
  <div class="tickets-page">
    <!-- Page Header -->
    <header class="page-header">
      <div class="header-content">
        <div class="title-section">
          <h1 class="page-title">
            <span class="title-gradient">Ticket Management</span>
          </h1>
          <p class="page-subtitle">Manage, track, and resolve all issue tickets here.</p>
        </div>
        <div class="header-stats">
          <div class="live-indicator">
            <div class="live-dot"></div>
            <span>Live</span>
          </div>
          <div class="header-actions">
            <router-link to="/tickets/create" class="primary-button">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 5V19M5 12H19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <span>Create New Ticket</span>
            </router-link>
          </div>
        </div>
      </div>
    </header>

    <!-- Filters and Search Section -->
    <div class="card filters-card">
      <div class="filter-controls">
        <div class="search-box">
          <svg class="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M21 21L15 15M17 10C17 13.866 13.866 17 10 17C6.13401 17 3 13.866 3 10C3 6.13401 6.13401 3 10 3C13.866 3 17 6.13401 17 10Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <input 
            type="text" 
            v-model="searchQuery" 
            placeholder="Search by ID, title..." 
            class="search-input"
            @input="applyFilters"
          >
        </div>
        
        <div class="date-filters">
          <div class="date-filter-group">
            <label for="date-from">From Date:</label>
            <input 
              type="date" 
              id="date-from" 
              v-model="dateFilterFrom" 
              class="date-input"
              @change="applyFilters"
            >
          </div>
          
          <div class="date-filter-group">
            <label for="date-to">To Date:</label>
            <input 
              type="date" 
              id="date-to" 
              v-model="dateFilterTo" 
              class="date-input"
              @change="applyFilters"
            >
          </div>
        </div>
        
        <div class="view-options">
          <a :href="getBulkExportUrl('excel')" class="secondary-button export-all-excel" target="_blank">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M14 2v7h7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M4 11a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1H5a1 1 0 01-1-1v-4z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M22 13v7a2 2 0 01-2 2H9a2 2 0 01-2-2v-7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M15 22v-5a1 1 0 011-1h5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
            <span>Export Filtered to Excel</span>
          </a>
          <div class="toggle-switch">
            <input type="checkbox" id="show-closed" v-model="showClosedTickets" @change="applyFilters">
            <label for="show-closed" class="slider"></label>
            <span>Show Closed Tickets</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Tickets Table -->
    <div class="card tickets-table-card">
      <div class="table-responsive">
        <table class="tickets-table">
          <thead>
            <tr>
              <th>Ticket ID</th>
              <th>Title</th>
              <th>Status</th>
              <th>Priority</th>
              <th>Reporter</th>
              <th>Date Created</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="loading">
                <td colspan="7" class="loading-state">Loading tickets...</td>
            </tr>
            <tr v-else-if="filteredTickets.length === 0">
              <td colspan="7" class="empty-state">
                <p>No tickets match your criteria.</p>
              </td>
            </tr>
            <tr v-for="ticket in paginatedTickets" :key="ticket.id">
              <td class="ticket-id">{{ ticket.ticket_code }}</td>
              <td>
                <div class="ticket-title">{{ ticket.title }}</div>
                <div class="ticket-updated">Updated: {{ formatDate(ticket.closed_at || ticket.created_at) }}</div>
              </td>
              <td>
                <span class="status-badge" :class="`status-${ticket.status.toLowerCase().replace(' ', '-')}`">
                  {{ ticket.status }}
                </span>
              </td>
              <td>
                <span class="priority-badge" :class="`priority-${ticket.priority.toLowerCase()}`">
                  {{ ticket.priority }}
                </span>
              </td>
              <td>{{ ticket.reporter_name }}</td>
              <td>{{ formatDate(ticket.created_at) }}</td>
              <td>
                <div class="action-buttons">
                  <button class="action-button view" @click="viewTicket(ticket)" title="View Details">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M1 12C1 12 5 4 12 4C19 4 23 12 23 12C23 12 19 20 12 20C5 20 1 12 1 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M12 15C13.6569 15 15 13.6569 15 12C15 10.3431 13.6569 9 12 9C10.3431 9 9 10.3431 9 12C9 13.6569 10.3431 15 12 15Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                  </button>
                  <router-link :to="`/tickets/${ticket.id}/action-taken`" class="action-button action-taken" title="View Actions">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M13 3H12C9.23858 3 7 5.23858 7 8V11C7 13.7614 9.23858 16 12 16H13V20H15V16H16C17.6569 16 19 14.6569 19 13V8C19 6.34315 17.6569 5 16 5H15V3H13Z" stroke="currentColor" stroke-width="2"/><path d="M5 9H9" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M5 13H7" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M9 5V9" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M5 17H7" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
                  </router-link>
                  <a :href="getExportUrlForTicket(ticket, 'pdf')" class="action-button export-pdf" title="Export to PDF" target="_blank">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M14 2v7h7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M4 11a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1H5a1 1 0 01-1-1v-4z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M22 13v7a2 2 0 01-2 2H9a2 2 0 01-2-2v-7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M15 22v-5a1 1 0 011-1h5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                  </a>
                  <button
                    class="action-button delete"
                    :class="{ 'disabled-delete': ticket.status === 'Open' }"
                    @click="deleteTicket(ticket)"
                    :title="ticket.status === 'Open' ? 'Cannot delete Open ticket - must close first' : 'Delete Ticket'"
                  >
                   <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3 6H5H21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M8 6V4C8 3.46957 8.21071 2.96086 8.58579 2.58579C8.96086 2.21071 9.46957 2 10 2H14C14.5304 2 15.0391 2.21071 15.4142 2.58579C15.7893 2.96086 16 3.46957 16 4V6M19 6V20C19 20.5304 18.7893 21.0391 18.4142 21.4142C18.0391 21.7893 17.5304 22 17 22H7C6.46957 22 5.96086 21.7893 5.58579 21.4142C5.21071 21.0391 5 20.5304 5 20V6H19Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M10 11V17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M14 11V17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
       <!-- Pagination -->
      <div class="pagination">
        <button class="pagination-button" :disabled="currentPage === 1" @click="prevPage">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M15 18L9 12L15 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span>Previous</span>
        </button>
        <span class="pagination-info">Page {{ currentPage }} of {{ totalPages }}</span>
        <button class="pagination-button" :disabled="currentPage === totalPages" @click="nextPage">
          <span>Next</span>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M9 18L15 12L9 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
      </div>
    </div>
  </div>

  
  <!-- View Ticket Detail Modal (Redesigned) -->
  <transition name="modal-fade">
    <div v-if="showDetailModal" class="modal-overlay" @click="closeDetailModal">
      <div class="modal-content detail-view-modal" @click.stop>
        <div class="detail-view-header">
            <div class="header-icon">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M21.707 11.293l-9-9a.999.999 0 00-1.414 0l-9 9A1 1 0 003 13h1v7c0 1.103.897 2 2 2h12c1.103 0 2-.897 2-2v-7h1a1 1 0 00.707-1.707zM12 20c-1.103 0-2-.897-2-2v-7h4v7c0 1.103-.897 2-2 2z"/></svg>
            </div>
            <div>
                <h2 class="detail-view-title">{{ selectedTicket.title }}</h2>
                <p class="detail-view-subtitle">Ticket ID: {{ selectedTicket.ticket_code }}</p>
            </div>
            <button class="close-button" @click="closeDetailModal">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </button>
        </div>

        <div class="detail-view-body">
            <div class="detail-section description-section">
                <p>{{ selectedTicket.description }}</p>
            </div>

            <div class="detail-section info-grid">
                <div class="info-item">
                    <div class="item-icon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.486 2 2 6.486 2 12s4.486 10 10 10 10-4.486 10-10S17.514 2 12 2zm0 18c-4.411 0-8-3.589-8-8s3.589-8 8-8 8 3.589 8 8-3.589 8-8 8z"/><path d="M13 7h-2v6h2V7zm0 8h-2v2h2v-2z"/></svg></div>
                    <div class="item-content">
                        <span class="item-label">Status</span>
                        <span class="status-badge" :class="`status-${selectedTicket.status.toLowerCase().replace(' ', '-')}`">{{ selectedTicket.status }}</span>
                    </div>
                </div>
                <div class="info-item">
                    <div class="item-icon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M11.707 2.293A.997.997 0 0011 2H6a.997.997 0 00-.707.293l-3 3A.996.996 0 002 6v5c0 .266.105.52.293.707l10 10a.997.997 0 001.414 0l8-8a.999.999 0 000-1.414l-7-7zM13 19.586L4.414 11H10c.552 0 1-.449 1-1V4.414L13 3.828V10c0 .551.448 1 1 1h5.586L13 19.586z"/><circle cx="6.5" cy="6.5" r="1.5"/></svg></div>
                    <div class="item-content">
                        <span class="item-label">Priority</span>
                        <span class="priority-badge" :class="`priority-${selectedTicket.priority.toLowerCase()}`">{{ selectedTicket.priority }}</span>
                    </div>
                </div>
                <div class="info-item">
                    <div class="item-icon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M10 3H4a1 1 0 00-1 1v6a1 1 0 001 1h6a1 1 0 001-1V4a1 1 0 00-1-1zM9 9H5V5h4v4zm11 4h-6a1 1 0 00-1 1v6a1 1 0 001 1h6a1 1 0 001-1v-6a1 1 0 00-1-1zm-1 6h-4v-4h4v4zM10 13H4a1 1 0 00-1 1v6a1 1 0 001 1h6a1 1 0 001-1v-6a1 1 0 00-1-1zm-1 6H5v-4h4v4zm11-13h-6a1 1 0 00-1 1v6a1 1 0 001 1h6a1 1 0 001-1V4a1 1 0 00-1-1zm-1 6h-4V5h4v4z"/></svg></div>
                    <div class="item-content">
                        <span class="item-label">Category</span>
                        <span class="item-value">{{ selectedTicket.category }}</span>
                    </div>
                </div>
                <div class="info-item">
                    <div class="item-icon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2.002c-5.522 0-10 4.477-10 10s4.478 10 10 10 10-4.477 10-10-4.478-10-10-10zm0 18c-4.411 0-8-3.589-8-8s3.589-8 8-8 8 3.589 8 8-3.589 8-8 8z"/><path d="M12 7.002c-2.757 0-5 2.243-5 5s2.243 5 5 5 5-2.243 5-5-2.243-5-5-5zm0 8c-1.654 0-3-1.346-3-3s1.346-3 3-3 3 1.346 3 3-1.346 3-3 3z"/></svg></div>
                    <div class="item-content">
                        <span class="item-label">Reporter</span>
                        <span class="item-value">{{ selectedTicket.reporter_name }}</span>
                    </div>
                </div>
                 <div class="info-item">
                    <div class="item-icon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M17.724 14.158c-.226-.12-1.232-.604-1.424-.673s-.331-.104-.473.104c-.142.208-.538.673-.66 812s-.245.156-.452.052c-.208-.104-.879-.324-1.673-.998-.623-.53-1.036-1.185-1.158-1.392s-.015-.318.09-.422c.09-.09.208-.235.313-.357.104-.122.139-.208.208-.345s.035-.26-.018-.364c-.052-.104-.473-1.14-.645-1.559s-.338-.35-.473-.357c-.122 0-.26.005-.396.005s-.357.052-.538.26c-.182.208-.691.673-.898 1.645s-.538 1.914-.617 2.04c-.078.126-.156.131-.288.078-.4-.162-1.357-.5-2.584-1.596-1.04-.92-1.743-2.05-2.04-2.4s-.226-.288-.015-.452c.182-.147.381-.229.513-.324.131-.095.176-.156.245-.288.07-.131.06-.26-.015-.364s-1.424-3.43-1.95-4.692c-.486-1.14-.972-1-.737-1.035.208-.035.452-.035.645-.035.208 0 .497.015.737.364.24.349.785 2.275.898 2.45.113.176.208.26.313.26.104 0 .208-.052.287-.113.276-.208.313-.235.422-.381.122-.156.208-.345.287-.513.078-.167.052-.313-.015-.422s-.208-.208-.287-.26c-.09-.06-.182-.131-.208-.182-.035-.052-.052-.113-.052-.156 0-.052.018-.104.035-.156.182-.452.972-1.26 1.357-1.645.357-.35.702-.482.972-.513.26-.035.523.005.691.005.182 0 .452.052.645.104.208.052.313.156.357.288.035.113.035.673-.156 1.71-.182 1.035-.182 1.914-.126 2.04.052.126.182.208.357.235.182.035.589-.078.691-.131.104-.052.422-.208.513-.381s.156-.334.182-.381c.035-.06.052-.113.052-.167s-.005-.104-.005-.104c0-.052-.018-.104-.018-.156l-.005-.095c-.018-.167-.052-.334-.09-.482-.156-.589-.331-1.158-.409-1.329-.167-.35-.331-.645-.331-.864 0-.208.104-.381.208-.513.104-.131.235-.26.381-.357.122-.078.26-.131.381-.156.288-.052.564.005.785.005.229 0 .617-.052.972.617.349.645.422 1.232.438 1.357.015.126.015 2.6-.452 5.104-.473 2.504-1.95 4.88-2.258 5.104-.287.208-.564.313-.84.313-.208 0-.4-.052-.564-.104z"/></svg></div>
                    <div class="item-content">
                        <span class="item-label">Reporter Contact</span>
                        <span class="item-value">{{ selectedTicket.reporter_contact || 'N/A' }}</span>
                    </div>
                </div>
                 <div class="info-item">
                    <div class="item-icon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M12 10c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z"/><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-5-8c0-1.07.25-2.07.7-2.94l1.73 1.73C9.16 11.46 9 11.72 9 12c0 1.65 1.35 3 3 3s3-1.35 3-3c0-.28-.04-.54-.1-.79l1.73-1.73c.45.87.7 1.87.7 2.94l-3.91-3.91C12.54 9.04 12.28 9 12 9c-.28 0-.54.04-.79.1L7 7.06z"/></svg></div>
                    <div class="item-content">
                        <span class="item-label">Assigned To</span>
                        <span class="item-value">{{ selectedTicket.assigned_to || 'Not assigned' }}</span>
                    </div>
                </div>
            </div>

            <div class="detail-section time-info">
                <div class="info-item">
                    <div class="item-icon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.486 2 2 6.486 2 12s4.486 10 10 10 10-4.486 10-10S17.514 2 12 2zm0 18c-4.411 0-8-3.589-8-8s3.589-8 8-8 8 3.589 8 8-3.589 8-8 8z"/><path d="M13 7h-2v5.414l3.293 3.293 1.414-1.414L13 11.586V7z"/></svg></div>
                    <div class="item-content">
                        <span class="item-label">Created At</span>
                        <span class="item-value">{{ formatDate(selectedTicket.created_at) }}</span>
                    </div>
                </div>
                <div class="info-item">
                    <div class="item-icon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.486 2 2 6.486 2 12s4.486 10 10 10 10-4.486 10-10S17.514 2 12 2zm0 18c-4.411 0-8-3.589-8-8s3.589-8 8-8 8 3.589 8 8-3.589 8-8 8z"/><path d="M13 7h-2v5.414l3.293 3.293 1.414-1.414L13 11.586V7z"/></svg></div>
                    <div class="item-content">
                        <span class="item-label">Last Updated</span>
                        <span class="item-value">{{ formatDate(selectedTicket.closed_at || selectedTicket.created_at) }}</span>
                    </div>
                </div>
            </div>

            <div class="detail-section export-section">
                <a :href="getExportUrl('pdf')" class="secondary-button" target="_blank">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4 7V4a2 2 0 0 1 2-2h8.586a2 2 0 0 1 1.414.586l4.414 4.414A2 2 0 0 1 21 8.586V19a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2v-3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M14 2v7h7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M9 15.5a1.5 1.5 0 0 0 1.5 1.5h1a1.5 1.5 0 0 0 1.5-1.5v-2a1.5 1.5 0 0 0-3 0v2z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M18 14h-1a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1h1v-3z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M4 14h1v3h1.5v-3h1v3H9v-4a1 1 0 0 0-1-1H4v1z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                    <span>Export to PDF</span>
                </a>
                <a :href="getExportUrl('excel')" class="secondary-button" target="_blank">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4 7V4a2 2 0 0 1 2-2h8.586a2 2 0 0 1 1.414.586l4.414 4.414A2 2 0 0 1 21 8.586V19a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2v-3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M14 2v7h7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M14.5 13.5h-3a1 1 0 0 1 0-2h3a1 1 0 0 1 0 2zm-3 4h3a1 1 0 0 0 0-2h-3a1 1 0 0 0 0 2z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                    <span>Export to Excel</span>
                </a>
            </div>
        </div>
      </div>
    </div>
  </transition>
  
    <!-- Delete Confirmation Modal -->
  <transition name="modal-fade">
    <div v-if="showDeleteModal" class="modal-overlay" @click="closeDeleteModal">
      <div class="modal-content confirmation-modal" @click.stop>
        <div class="modal-header">
          <h2 class="modal-title">Confirm Ticket Deletion</h2>
        </div>
        <div class="modal-body">
          <p v-if="ticketToDelete">
            Are you sure you want to delete ticket <strong>{{ ticketToDelete.ticket_code }} - {{ ticketToDelete.title }}</strong>?
          </p>
          <p class="warning-text">This action cannot be undone.</p>
        </div>
        <div class="modal-actions">
          <button type="button" class="secondary-button" @click="closeDeleteModal">Cancel</button>
          <button type="button" class="primary-button delete-confirm-button" @click="confirmDelete">Yes, Delete</button>
        </div>
      </div>
    </div>
  </transition>

  <!-- Cannot Delete Modal (for Open tickets) -->
  <transition name="modal-fade">
    <div v-if="showCannotDeleteModal" class="modal-overlay" @click="closeCannotDeleteModal">
      <div class="modal-content warning-modal" @click.stop>
        <div class="modal-header warning-header">
          <div class="warning-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 9v4M12 17h.01M5.07183 19H18.9282C19.5528 19 20.0565 18.4451 19.9952 17.8235L19.0718 8.82353C19.0182 8.27657 18.5568 7.85714 18.0068 7.85714H5.9932C5.44324 7.85714 4.98184 8.27657 4.92818 8.82353L4.00478 17.8235C3.94349 18.4451 4.44719 19 5.07183 19Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <h2 class="modal-title">Cannot Delete Open Ticket</h2>
          <button class="close-button" @click="closeCannotDeleteModal">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <div v-if="cannotDeleteTicket" class="warning-content">
            <p class="warning-message">
              <strong>Tiket {{ cannotDeleteTicket.ticket_code }} tidak dapat dihapus karena statusnya masih <span class="status-highlight">Open</span>.</strong>
            </p>
            <div class="requirement-box">
              <h4>Persyaratan untuk menghapus tiket:</h4>
              <ul>
                <li>Tiket harus memiliki status <strong>Closed</strong> terlebih dahulu</li>
                <li>Status tiket dapat diubah melalui halaman <strong>Action Taken</strong></li>
                <li>Pastikan semua penyelesaian masalah telah dicatat</li>
              </ul>
            </div>
            <div class="suggestion-box">
              <p><strong>Saran:</strong> Kunjungi halaman <strong>Action Taken</strong> untuk menutup tiket ini terlebih dahulu.</p>
              <router-link :to="`/tickets/${cannotDeleteTicket.id}/action-taken`" class="primary-button" @click="closeCannotDeleteModal">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M13 3H12C9.23858 3 7 5.23858 7 8V11C7 13.7614 9.23858 16 12 16H13V20H15V16H16C17.6569 16 19 14.6569 19 13V8C19 6.34315 17.6569 5 16 5H15V3H13Z" stroke="currentColor" stroke-width="2"/>
                  <path d="M5 9H9" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                  <path d="M5 13H7" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                  <path d="M9 5V9" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                  <path d="M5 17H7" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                </svg>
                <span>Go to Action Taken</span>
              </router-link>
            </div>
          </div>
        </div>
        <div class="modal-actions">
          <button type="button" class="secondary-button" @click="closeCannotDeleteModal">Mengerti</button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue';
import type { Ticket } from '../api/ticketAPI';
import { ticketAPI } from '../api/ticketAPI';

// State management
const showDetailModal = ref(false);
const showDeleteModal = ref(false);
const showCannotDeleteModal = ref(false); // New modal for tickets that can't be deleted
const showClosedTickets = ref(false);

const ticketToDelete = ref<Ticket | null>(null);
const cannotDeleteTicket = ref<Ticket | null>(null);
const searchQuery = ref('');
const dateFilterFrom = ref('');
const dateFilterTo = ref('');
const currentPage = ref(1);
const itemsPerPage = ref(10);
const loading = ref(false);

const allTickets = ref<Ticket[]>([]);
const filteredTickets = ref<Ticket[]>([]);

interface ExtendedTicket extends Ticket {
  category?: string;
  assigned_to?: string;
  reporter_contact?: string;
}

const selectedTicket = ref<ExtendedTicket>({
  id: 0,
  ticket_code: '',
  title: '',
  description: '',
  status: 'Open',
  priority: 'Medium',
  reporter_name: '',
  reporter_contact: '',
  assignee_id: undefined,
  created_at: '',
  closed_at: undefined,
  downtime: undefined,
  summary_problem: undefined,
  summary_action: undefined,
  actions: [],
  assignee: undefined,
  category: 'Network',
  assigned_to: '',
});


// Computed properties for pagination
const totalPages = computed(() => Math.ceil(filteredTickets.value.length / itemsPerPage.value));
const paginatedTickets = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value;
  const end = start + itemsPerPage.value;
  return filteredTickets.value.slice(start, end);
});

const formatDate = (dateString: string | undefined) => {
  if (!dateString) return '-';
  const date = new Date(dateString);
  if (isNaN(date.getTime())) {
    return '-';
  }
  return date.toLocaleDateString('en-US', { day: '2-digit', month: 'long', year: 'numeric' });
};

const applyFilters = () => {
  let tempTickets = allTickets.value;

  // Filter by closed status
  if (!showClosedTickets.value) {
    tempTickets = tempTickets.filter(ticket => ticket.status !== 'Closed');
  }
  
  // Filter by search query
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    tempTickets = tempTickets.filter(ticket => 
      (ticket.title || '').toLowerCase().includes(query) || 
      (ticket.ticket_code || '').toLowerCase().includes(query)
    );
  }
  
  // Filter by date range
  if (dateFilterFrom.value) {
    const fromDate = new Date(dateFilterFrom.value);
    tempTickets = tempTickets.filter(ticket => {
      const ticketDate = new Date(ticket.created_at || ticket.closed_at || new Date());
      return ticketDate >= fromDate;
    });
  }
  
  if (dateFilterTo.value) {
    const toDate = new Date(dateFilterTo.value);
    toDate.setHours(23, 59, 59, 999); // Set to end of the day
    tempTickets = tempTickets.filter(ticket => {
      const ticketDate = new Date(ticket.created_at || ticket.closed_at || new Date());
      return ticketDate <= toDate;
    });
  }
  
  filteredTickets.value = tempTickets;
  currentPage.value = 1; // Reset to first page when filters change
};


const closeDetailModal = () => {
  showDetailModal.value = false;
};



const viewTicket = async (ticket: Ticket) => {
  try {
    const response = await ticketAPI.getTicketById(ticket.id);
    selectedTicket.value = { 
      ...response.data,
      category: 'Network', // Example category, adjust as needed
      assigned_to: response.data.assignee ? response.data.assignee.username : 'Not assigned',
      reporter_contact: response.data.reporter_contact,
    };
    showDetailModal.value = true;
  } catch (error) {
    console.error('Error loading ticket details:', error);
  }
};

const deleteTicket = (ticket: Ticket) => {
  // Check if ticket status is "Open" - if so, show a different modal
  if (ticket.status === 'Open') {
    // Show warning modal for open tickets
    showCannotDeleteModal.value = true;
    cannotDeleteTicket.value = ticket;
  } else {
    // Show normal delete confirmation for non-open tickets
    ticketToDelete.value = ticket;
    showDeleteModal.value = true;
  }
};

const closeDeleteModal = () => {
  showDeleteModal.value = false;
  ticketToDelete.value = null;
};

const closeCannotDeleteModal = () => {
  showCannotDeleteModal.value = false;
  cannotDeleteTicket.value = null;
};

const confirmDelete = async () => {
  if (!ticketToDelete.value) return;

  try {
    await ticketAPI.deleteTicket(ticketToDelete.value.id);
    await loadTickets();
  } catch (error: any) {
    console.error('Error deleting ticket:', error);
  } finally {
    closeDeleteModal();
  }
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

const loadTickets = async () => {
  loading.value = true;
  try {
    const response = await ticketAPI.getAllTickets(0, 500); // Fetch more to allow for frontend filtering
    allTickets.value = response.data;
    applyFilters();
  } catch (error: any) {
    console.error('Error loading tickets:', error);
  } finally {
    loading.value = false;
  }
};


const getExportUrl = (format: 'pdf' | 'excel'): string => {
  if (!selectedTicket.value?.id) {
    return '#';
  }
  // Use the correct backend API endpoint for exports
  if (format === 'pdf') {
    return `/api/tickets/${selectedTicket.value.id}/export/pdf`;
  } else {
    return `/api/tickets/${selectedTicket.value.id}/export/excel`;
  }
};

const getExportUrlForTicket = (ticket: Ticket, _format: 'pdf'): string => {
  if (!ticket?.id) {
    return '#';
  }
  // Use the correct backend API endpoint for PDF exports (only individual tickets)
  return `/api/tickets/${ticket.id}/export/pdf`;
};

const getBulkExportUrl = (format: 'excel'): string => {
  // Use the correct backend API endpoint for bulk exports with filters
  const params = new URLSearchParams();
  
  if (showClosedTickets.value) {
    params.append('showClosed', 'true');
  }
  
  if (dateFilterFrom.value) {
    params.append('dateFrom', dateFilterFrom.value);
  }
  
  if (dateFilterTo.value) {
    params.append('dateTo', dateFilterTo.value);
  }
  
  if (searchQuery.value) {
    params.append('search', searchQuery.value);
  }
  
  let url = `/api/tickets/export/${format}`;
  if (params.toString()) {
    url += `?${params.toString()}`;
  }
  
  return url;
};

onMounted(async () => {
  await loadTickets();
});

watch([searchQuery, showClosedTickets], () => {
  applyFilters();
});
</script>

<style scoped>
.tickets-page {
  background-color: #f8fafc;
  padding: 2rem;
  font-family: 'Inter', sans-serif;
  width: 100%;
  box-sizing: border-box;
}

.card {
  background-color: #ffffff;
  border-radius: 16px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  border: 1px solid #e2e8f0;
  margin-bottom: 1.5rem;
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
.primary-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #800000 0%, #5c0000 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
}

.primary-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(128, 0, 0, 0.3);
}

.secondary-button {
  padding: 0.75rem 1.5rem;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  background: #ffffff;
  color: #64748b;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
}

.secondary-button:hover {
  border-color: #800000;
  color: #800000;
  background: linear-gradient(135deg, rgba(128, 0, 0, 0.05) 0%, rgba(92, 0, 0, 0.05) 100%);
}

/* Filters & Options */
.filters-card {
  padding: 1rem 1.5rem;
}
.filter-controls {
  display: flex;
  justify-content: space-between;
  align-items: end;
  width: 100%;
  gap: 1rem;
  flex-wrap: wrap;
}
.search-box { position: relative; flex-grow: 1; max-width: 400px; }
.search-icon { position: absolute; left: 1rem; top: 50%; transform: translateY(-50%); color: #9ca3af; }
.search-input { width: 100%; padding: 0.75rem 1rem 0.75rem 2.75rem; border: 1px solid #e2e8f0; border-radius: 12px; font-size: 1rem; color: #1e293b; background-color: #f8fafc; transition: all 0.3s ease; box-sizing: border-box; }
.search-input:focus { outline: none; border-color: #ff4d4f; box-shadow: 0 0 0 3px rgba(255, 77, 79, 0.2); background-color: #ffffff; }

.view-options { display: flex; align-items: center; gap: 1rem; }
.toggle-switch {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: #475569;
}
.toggle-switch input { display: none; }
.toggle-switch .slider {
  position: relative;
  cursor: pointer;
  width: 40px;
  height: 22px;
  background-color: #cbd5e1;
  border-radius: 22px;
  transition: background-color 0.3s;
}
.toggle-switch .slider::before {
  position: absolute;
  content: "";
  height: 16px;
  width: 16px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  border-radius: 50%;
  transition: transform 0.3s;
}
.toggle-switch input:checked + .slider {
  background-color: #ff4d4f;
}
.toggle-switch input:checked + .slider::before {
  transform: translateX(18px);
}

/* Table */
.tickets-table-card { overflow: hidden; }
.table-responsive { overflow-x: auto; }
.tickets-table { width: 100%; border-collapse: collapse; text-align: left; }
.tickets-table th, .tickets-table td { padding: 1.25rem 1.5rem; border-bottom: 1px solid #e2e8f0; }
.tickets-table th { font-size: 0.875rem; font-weight: 600; color: #64748b; text-transform: uppercase; background-color: #f8fafc; }
.tickets-table tr:last-child td { border-bottom: none; }
.ticket-id { font-weight: 600; color: #d9363e; }
.ticket-title { font-weight: 600; color: #1e293b; }
.ticket-updated { font-size: 0.875rem; color: #64748b; margin-top: 0.25rem; }
.loading-state, .empty-state { text-align: center; padding: 4rem; color: #64748b; }

/* Badges */
.status-badge, .priority-badge { padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; display: inline-block; }
.status-open { background-color: #fee2e2; color: #dc2626; }
.status-in-progress { background-color: #fef3c7; color: #d97706; }
.status-closed { background-color: #d1fae5; color: #059669; }
.status-on-hold { background-color: #e5e7eb; color: #374151; }
.priority-high { background-color: #fecaca; color: #b91c1c; }
.priority-medium { background-color: #fed7aa; color: #c2410c; }
.priority-low { background-color: #bfdbfe; color: #1d4ed8; }

/* Actions */
.action-buttons { display: flex; gap: 0.5rem; }
.action-button { width: 36px; height: 36px; border-radius: 8px; background: transparent; border: none; display: flex; align-items: center; justify-content: center; color: #64748b; cursor: pointer; transition: all 0.2s ease; }
.action-button:hover { background-color: #f1f5f9; color: #1e293b; }
.action-button.view:hover { color: #3b82f6; }
.action-button.action-taken:hover { color: #10b981; }
.action-button.delete:hover { color: #ef4444; }
.action-button.delete.disabled-delete {
  color: #d1d5db;
  cursor: not-allowed;
  opacity: 0.5;
}
.action-button.delete.disabled-delete:hover {
  color: #d1d5db;
  background-color: transparent;
}
.action-button.export-pdf:hover { color: #f59e0b; }
.action-button.export-excel:hover { color: #10b981; }

/* Pagination */
.pagination { display: flex; align-items: center; justify-content: center; padding: 1.5rem; flex-wrap: wrap; gap: 1rem; }
.pagination-button { display: flex; align-items: center; gap: 0.5rem; padding: 0.5rem 1rem; border: 1px solid #e2e8f0; border-radius: 8px; background: #ffffff; color: #64748b; cursor: pointer; transition: all 0.2s ease; }
.pagination-button:hover:not(:disabled) { border-color: #ff4d4f; color: #ff4d4f; }
.pagination-button:disabled { opacity: 0.5; cursor: not-allowed; }
.pagination-info { font-size: 1rem; font-weight: 500; color: #1e293b; }

/* --- Modal Styles --- */
.modal-fade-enter-active, .modal-fade-leave-active { transition: opacity 0.4s cubic-bezier(0.25, 0.8, 0.25, 1); }
.modal-fade-enter-from, .modal-fade-leave-to { opacity: 0; }
.modal-fade-enter-active .modal-content, .modal-fade-leave-active .modal-content { transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1); }
.modal-fade-enter-from .modal-content, .modal-fade-leave-to .modal-content { opacity: 0; transform: scale(0.95) translateY(20px); }
.modal-overlay { position: fixed; inset: 0; background: rgba(17, 24, 39, 0.8); display: flex; align-items: center; justify-content: center; z-index: 1000; backdrop-filter: blur(8px); }

/* Base Modal Content for Create/Edit & Delete */
.modal-content { background-color: #f8fafc; border-radius: 20px; width: 100%; max-width: 600px; max-height: 90vh; display: flex; flex-direction: column; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25); border: 1px solid #334155; }
.modal-header { display: flex; justify-content: space-between; align-items: center; padding: 1.5rem 2rem; background-color: #1f2937; color: #fff; border-top-left-radius: 20px; border-top-right-radius: 20px; border-bottom: 1px solid #334155; }
.modal-title { font-size: 1.25rem; font-weight: 600; }
.close-button { background: transparent; border: none; color: #9ca3af; cursor: pointer; padding: 0.5rem; border-radius: 50%; transition: all 0.2s; }
.close-button:hover { color: #fff; background-color: rgba(255, 255, 255, 0.1); }
.modal-form, .modal-body { padding: 2rem; overflow-y: auto; background-color: #ffffff; }
.form-group { margin-bottom: 1.5rem; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }
.form-group label { display: block; font-size: 0.875rem; font-weight: 600; color: #1e293b; margin-bottom: 0.5rem; }
.form-group input, .form-group textarea, .form-group select { width: 100%; padding: 0.75rem 1rem; border: 1px solid #e2e8f0; border-radius: 12px; font-size: 1rem; transition: all 0.3s ease; background-color: #f8fafc; box-sizing: border-box; }
.form-group input:focus, .form-group textarea:focus, .form-group select:focus { outline: none; border-color: #ff4d4f; box-shadow: 0 0 0 3px rgba(255, 77, 79, 0.2); background-color: #ffffff; }
.modal-actions { display: flex; justify-content: flex-end; gap: 1rem; padding: 1.5rem 2rem; border-top: 1px solid #e2e8f0; background-color: #f8fafc; border-bottom-left-radius: 20px; border-bottom-right-radius: 20px; }

/* Delete Confirmation Modal Specifics */
.confirmation-modal { max-width: 450px; }
.confirmation-modal .modal-body { font-size: 1.1rem; color: #334155; line-height: 1.6; }
.confirmation-modal .warning-text { font-size: 1rem; font-weight: 600; color: #ef4444; margin-top: 1rem; }
.delete-confirm-button { background-color: #ef4444; }
.delete-confirm-button:hover { background-color: #dc2626; }

/* --- NEW Detail View Modal Styles --- */
.detail-view-modal { background-color: #ffffff; max-width: 700px; border-radius: 16px; border: 1px solid #e2e8f0; }
.detail-view-header { display: flex; align-items: flex-start; gap: 1rem; padding: 2rem; position: relative; }
.detail-view-header .close-button { position: absolute; top: 1rem; right: 1rem; color: #9ca3af; }
.detail-view-header .close-button:hover { color: #1e293b; background-color: #f1f5f9; }
.detail-view-header .header-icon { flex-shrink: 0; background-color: #fee2e2; color: #ef4444; width: 48px; height: 48px; border-radius: 12px; display: flex; align-items: center; justify-content: center; }
.header-icon svg { width: 28px; height: 28px; }
.detail-view-title { font-size: 1.75rem; font-weight: 800; color: #1e293b; margin: 0; line-height: 1.2; }
.detail-view-subtitle { font-size: 1rem; color: #64748b; margin: 0.25rem 0 0 0; font-family: 'Courier New', Courier, monospace; }
.detail-view-body { padding: 0 2rem 2rem 2rem; overflow-y: auto; max-height: calc(90vh - 120px); }
.detail-section { margin-top: 2rem; padding-top: 2rem; border-top: 1px solid #f1f5f9; }
.detail-section:first-child { margin-top: 0; padding-top: 0; border-top: none; }
.description-section p { font-size: 1rem; line-height: 1.7; color: #334155; background-color: #f8fafc; padding: 1rem; border-radius: 12px; border: 1px solid #e2e8f0; }
.info-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; }
.info-item { display: flex; align-items: flex-start; gap: 1rem; }
.item-icon { flex-shrink: 0; color: #9ca3af; width: 20px; height: 20px; margin-top: 2px; }
.item-content { display: flex; flex-direction: column; }
.item-label { font-size: 0.875rem; font-weight: 500; color: #64748b; margin-bottom: 0.25rem; }
.item-value { font-size: 1rem; font-weight: 600; color: #334155; }
.time-info { display: flex; gap: 2rem; }

.export-section {
    display: flex;
    gap: 1rem;
    justify-content: center;
}
.export-section .secondary-button {
    flex-grow: 1;
    justify-content: center;
}

.filters-card .view-options {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.filters-card .view-options .export-all-excel {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
}

.date-filters {
    display: flex;
    gap: 1rem;
    align-items: end;
}

.date-filter-group {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
}

.date-filter-group label {
    font-size: 0.875rem;
    font-weight: 600;
    color: #475569;
}

.date-input {
    padding: 0.75rem 1rem;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    font-size: 1rem;
    background-color: #f8fafc;
    transition: all 0.3s ease;
    min-width: 150px;
}

.date-input:focus {
    outline: none;
    border-color: #ff4d4f;
    box-shadow: 0 0 0 3px rgba(255, 77, 79, 0.2);
    background-color: #ffffff;
}

/* Warning Modal Styles */
.warning-modal { max-width: 550px; }
.warning-header {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
}
.warning-icon {
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.5rem;
}
.warning-content {
  font-size: 1rem;
  line-height: 1.6;
  color: #334155;
}
.warning-message {
  font-size: 1.1rem;
  margin-bottom: 1.5rem;
  text-align: center;
}
.status-highlight {
  background: #fef3c7;
  color: #92400e;
  padding: 0.25rem 0.5rem;
  border-radius: 6px;
  font-weight: 600;
}
.requirement-box {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}
.requirement-box h4 {
  margin: 0 0 1rem 0;
  color: #1e293b;
  font-size: 1.1rem;
}
.requirement-box ul {
  margin: 0;
  padding-left: 1.5rem;
}
.requirement-box li {
  margin-bottom: 0.5rem;
  color: #475569;
}
.suggestion-box {
  background: #ecfdf5;
  border: 1px solid #d1fae5;
  border-radius: 12px;
  padding: 1.5rem;
  text-align: center;
}
.suggestion-box p {
  margin: 0 0 1rem 0;
  color: #065f46;
}
.suggestion-box .primary-button {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}
.suggestion-box .primary-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(16, 185, 129, 0.3);
}

/* Responsive */
@media (max-width: 768px) {
  .tickets-page { padding: 1rem; }
  .page-header { flex-direction: column; align-items: flex-start; }
  .filters-card { flex-direction: column; }
  .form-row { grid-template-columns: 1fr; }
  .tickets-table th:nth-child(5), .tickets-table td:nth-child(5) { display: none; }
}
@media (max-width: 480px) {
  .page-title { font-size: 1.75rem; }
  .modal-content { margin: 1rem; max-height: calc(100vh - 2rem); }
  .modal-form, .detail-view-body { padding: 1.5rem; }
  .detail-view-header { padding: 1.5rem; }
}
</style>