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
    // Calculate reputation score from mentions
    const mentions = await firebaseService.mentions.getAll(id);
    const positive = mentions.filter(m => m.sentiment === 'positive').length;
    const total = mentions.length;
    const score = total > 0 ? Math.round((positive / total) * 100) : 75;
    return { data: { score } };
  },
};

// Mention API using Firebase
export const mentionAPI = {
  getAll: async (params) => {
    const mentions = await firebaseService.mentions.getAll(params?.entity_id);
    return { data: mentions };
  },
  getById: async (id) => {
    const mention = await firebaseService.mentions.getById(id);
    return { data: mention };
  },
  getByEntity: async (entityId, params) => {
    const mentions = await firebaseService.mentions.getAll(entityId);
    return { data: mentions };
  },
  analyze: async (id) => {
    // Placeholder for AI analysis
    return { data: { sentiment: 'positive', score: 0.8 } };
  },
};

// Alert API using Firebase
export const alertAPI = {
  getAll: async (params) => {
    const alerts = await firebaseService.alerts.getAll(params?.user_id);
    return { data: alerts };
  },
  getById: async (id) => {
    // Firestore doesn't have getById for alerts, so we'll skip it
    return { data: null };
  },
  markAsRead: async (id) => {
    await firebaseService.alerts.markAsRead(id);
    return { data: { success: true } };
  },
  resolve: async (id) => {
    await firebaseService.alerts.markAsRead(id);
    return { data: { success: true } };
  },
};

// Dashboard API using Firebase
export const dashboardAPI = {
  getMetrics: async () => {
    const stats = await firebaseService.analytics.getDashboardStats();
    return { data: stats };
  },
  getTrends: async (timeframe) => {
    // Placeholder for trends analysis
    return { data: {} };
  },
  getSentimentDistribution: async () => {
    const stats = await firebaseService.analytics.getDashboardStats();
    return { 
      data: {
        positive: stats.mentions.positive,
        neutral: stats.mentions.neutral,
        negative: stats.mentions.negative
      }
    };
  },
};

// Analytics API using Firebase
export const analyticsAPI = {
  getReputationHistory: async (entityId, days) => {
    // Placeholder for historical data
    return { data: [] };
  },
  getTrendAnalysis: async (entityId) => {
    return { data: {} };
  },
  getSourceBreakdown: async (entityId) => {
    return { data: {} };
  },
  getCompetitorComparison: async (entityIds) => {
    return { data: [] };
  },
  getDashboard: async () => {
    const stats = await firebaseService.analytics.getDashboardStats();
    return { data: stats };
  },
};

// Auth API using Firebase
export const authAPI = {
  login: async (email, password) => {
    const result = await firebaseService.auth.login(email, password);
    return { data: result };
  },
  register: async (data) => {
    const user = await firebaseService.auth.register(data.email, data.password, data);
    return { data: user };
  },
  logout: async () => {
    await firebaseService.auth.logout();
    return { data: { success: true } };
  },
  getCurrentUser: () => {
    const user = firebaseService.auth.getCurrentUser();
    return Promise.resolve({ data: user });
  },
  refreshToken: async () => {
    const user = firebaseService.auth.getCurrentUser();
    if (user) {
      const token = await user.getIdToken(true);
      return { data: { token } };
    }
    return { data: { token: null } };
  },
};

// User API using Firebase
export const userAPI = {
  getProfile: async () => {
    const user = firebaseService.auth.getCurrentUser();
    if (user) {
      const profile = await firebaseService.users.getById(user.uid);
      return { data: profile };
    }
    return { data: null };
  },
  updateProfile: async (data) => {
    const user = firebaseService.auth.getCurrentUser();
    if (user) {
      const updated = await firebaseService.users.update(user.uid, data);
      return { data: updated };
    }
    return { data: null };
  },
  changePassword: async (oldPassword, newPassword) => {
    // Placeholder for password change
    return { data: { success: true } };
  },
  getNotificationPreferences: async () => {
    return { data: { email: true, push: false, sms: false } };
  },
  updateNotificationPreferences: async (data) => {
    return { data };
  },
};

export default firebaseService;
