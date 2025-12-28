import axios from 'axios';
import { mockAuthService } from './mockAuth';

// Use Firebase Functions URL or fall back to localhost for development
const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://us-central1-reputationai-df869.cloudfunctions.net/api';
const USE_MOCK_AUTH = import.meta.env.VITE_USE_MOCK_AUTH === 'true';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('auth_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Entity API
export const entityAPI = {
  getAll: () => api.get('/entities'),
  getById: (id) => api.get(`/entities/${id}`),
  create: (data) => api.post('/entities', data),
  update: (id, data) => api.put(`/entities/${id}`, data),
  delete: (id) => api.delete(`/entities/${id}`),
  getReputation: (id) => api.get(`/entities/${id}/reputation`),
};

// Mention API
export const mentionAPI = {
  getAll: (params) => api.get('/mentions', { params }),
  getById: (id) => api.get(`/mentions/${id}`),
  getByEntity: (entityId, params) => api.get(`/entities/${entityId}/mentions`, { params }),
};

// Alert API
export const alertAPI = {
  getAll: (params) => api.get('/alerts', { params }),
  getById: (id) => api.get(`/alerts/${id}`),
  markAsRead: (id) => api.put(`/alerts/${id}/read`),
  resolve: (id) => api.put(`/alerts/${id}/resolve`),
};

// Dashboard API
export const dashboardAPI = {
  getMetrics: () => api.get('/dashboard/metrics'),
  getTrends: (timeframe) => api.get('/dashboard/trends', { params: { timeframe } }),
  getSentimentDistribution: () => api.get('/dashboard/sentiment'),
};

// Analytics API
export const analyticsAPI = {
  getReputationHistory: (entityId, days) => 
    api.get(`/analytics/reputation-history/${entityId}`, { params: { days } }),
  getTrendAnalysis: (entityId) => api.get(`/analytics/trends/${entityId}`),
  getSourceBreakdown: (entityId) => api.get(`/analytics/sources/${entityId}`),
  getCompetitorComparison: (entityIds) => 
    api.get('/analytics/comparison', { params: { entity_ids: entityIds.join(',') } }),
};

// Auth API
export const authAPI = {
  login: (email, password) => {
    // Always use mock auth for now until Firebase Auth is configured
    return mockAuthService.login(email, password);
  },
  register: (data) => {
    return mockAuthService.register(data);
  },
  logout: () => {
    return mockAuthService.logout();
  },
  getCurrentUser: () => {
    return mockAuthService.getCurrentUser();
  },
  refreshToken: () => Promise.resolve({ data: { token: localStorage.getItem('auth_token') } }),
};

// User API
export const userAPI = {
  getProfile: () => api.get('/users/profile'),
  updateProfile: (data) => api.put('/users/profile', data),
  changePassword: (oldPassword, newPassword) => 
    api.put('/users/password', { old_password: oldPassword, new_password: newPassword }),
  getNotificationPreferences: () => api.get('/users/notifications'),
  updateNotificationPreferences: (data) => api.put('/users/notifications', data),
};

export default api;
