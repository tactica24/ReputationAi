import firebaseService from './firebaseService';

// Entity API using Firebase
export const entityAPI = {
  getAll: async () => {
    const entities = await firebaseService.entities.getAll();
    return { data: entities };
  },
  getById: async (id) => {
    const entity = await firebaseService.entities.getById(id);
    return { data: entity };
  },
  create: async (data) => {
    const entity = await firebaseService.entities.create(data);
    return { data: entity };
  },
  update: async (id, data) => {
    const entity = await firebaseService.entities.update(id, data);
    return { data: entity };
  },
  delete: async (id) => {
    await firebaseService.entities.delete(id);
    return { data: { success: true } };
  },
  getReputation: async (id) => {
    // For now, return a calculated reputation score
    const mentions = await firebaseService.mentions.getAll(id);
    const positive = mentions.filter(m => m.sentiment === 'positive').length;
    const total = mentions.length;
    const score = total > 0 ? Math.round((positive / total) * 100) : 75;
    return { data: { score } };
  },
};

// Mention API
export const mentionAPI = {
  getAll: (params) => api.get('/mentions', { params }).catch(async () => {
    const { mockDataService } = await import('./mockData');
    return mockDataService.getMentions();
  }),
  getById: (id) => api.get(`/mentions/${id}`).catch(() => ({data: null})),
  getByEntity: (entityId, params) => api.get(`/entities/${entityId}/mentions`, { params }).catch(async () => {
    const { mockDataService } = await import('./mockData');
    const mentions = await mockDataService.getMentions();
    return { data: mentions.data.filter(m => m.entity_id === entityId) };
  }),
};

// Alert API
export const alertAPI = {
  getAll: (params) => api.get('/alerts', { params }).catch(async () => {
    const { mockDataService } = await import('./mockData');
    return mockDataService.getAlerts();
  }),
  getById: (id) => api.get(`/alerts/${id}`).catch(() => ({data: null})),
  markAsRead: (id) => api.put(`/alerts/${id}/read`),
  resolve: (id) => api.put(`/alerts/${id}/resolve`),
};

// Dashboard API
export const dashboardAPI = {
  getMetrics: () => api.get('/dashboard/metrics').catch(async () => {
    const { mockDataService } = await import('./mockData');
    return mockDataService.getDashboardStats();
  }),
  getTrends: (timeframe) => api.get('/dashboard/trends', { params: { timeframe } }).catch(() => ({data: {}})),
  getSentimentDistribution: () => api.get('/dashboard/sentiment').catch(() => ({data: {positive: 63, neutral: 20, negative: 17}})),
};

// Analytics API
export const analyticsAPI = {
  getReputationHistory: (entityId, days) => 
    api.get(`/analytics/reputation-history/${entityId}`, { params: { days } }).catch(() => ({data: []})),
  getTrendAnalysis: (entityId) => api.get(`/analytics/trends/${entityId}`).catch(() => ({data: {}})),
  getSourceBreakdown: (entityId) => api.get(`/analytics/sources/${entityId}`).catch(() => ({data: {}})),
  getCompetitorComparison: (entityIds) => 
    api.get('/analytics/comparison', { params: { entity_ids: entityIds.join(',') } }).catch(() => ({data: []})),
  getDashboard: () => api.get('/analytics/dashboard').catch(async () => {
    const { mockDataService } = await import('./mockData');
    return mockDataService.getDashboardStats();
  }),
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
