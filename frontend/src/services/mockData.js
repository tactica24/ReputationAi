/**
 * Mock Data Service
 * Provides sample data for dashboard when backend is not available
 */

export const mockDataService = {
  // Dashboard stats
  getDashboardStats: async () => {
    return {
      data: {
        applications: {
          total: 12,
          pending: 5,
          approved: 6,
          rejected: 1
        },
        users: {
          total: 8,
          active: 7,
          admins: 2
        },
        entities: {
          total: 15,
          active: 14
        },
        mentions: {
          total: 247,
          positive: 156,
          negative: 42,
          neutral: 49
        },
        timestamp: new Date().toISOString()
      }
    };
  },

  // Applications
  getApplications: async () => {
    return {
      data: [
        {
          id: '1',
          company_name: 'VeriSignal Inc',
          email: 'contact@verisignal.com',
          industry: 'Technology',
          company_size: '50-100',
          use_case: 'AI-powered digital reputation and identity protection for our SaaS product',
          status: 'pending',
          created_at: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString()
        },
        {
          id: '2',
          company_name: 'VeriSignal Finance',
          email: 'info@verisignal.com',
          industry: 'Finance',
          company_size: '100-500',
          use_case: 'Executive digital reputation and identity protection',
          status: 'approved',
          created_at: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString()
        },
        {
          id: '3',
          company_name: 'VeriSignal Health',
          email: 'hello@verisignal.com',
          industry: 'Healthcare',
          company_size: '10-50',
          use_case: 'Medical practice digital reputation management',
          status: 'rejected',
          created_at: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString()
        }
      ]
    };
  },

  // Users
  getUsers: async () => {
    return {
      data: [
        {
          id: '1',
          email: 'admin@verisignal.com',
          name: 'Admin User',
          company: 'VeriSignal',
          role: 'admin',
          is_active: true,
          created_at: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString()
        },
        {
          id: '2',
          email: 'john@verisignal.com',
          name: 'John Smith',
          company: 'VeriSignal',
          role: 'user',
          is_active: true,
          created_at: new Date(Date.now() - 15 * 24 * 60 * 60 * 1000).toISOString()
        },
        {
          id: '3',
          email: 'sarah@verisignal.com',
          name: 'Sarah Johnson',
          company: 'VeriSignal',
          role: 'user',
          is_active: true,
          created_at: new Date(Date.now() - 10 * 24 * 60 * 60 * 1000).toISOString()
        }
      ]
    };
  },

  // Entities
  getEntities: async () => {
    return {
      data: [
        {
          id: '1',
          user_id: '2',
          name: 'Tech Corp',
          entity_type: 'company',
          description: 'Leading technology company',
          is_active: true,
          created_at: new Date(Date.now() - 20 * 24 * 60 * 60 * 1000).toISOString()
        },
        {
          id: '2',
          user_id: '2',
          name: 'John Smith',
          entity_type: 'person',
          description: 'CEO of Tech Corp',
          is_active: true,
          created_at: new Date(Date.now() - 20 * 24 * 60 * 60 * 1000).toISOString()
        },
        {
          id: '3',
          user_id: '3',
          name: 'Innovation Inc',
          entity_type: 'company',
          description: 'Innovation consulting firm',
          is_active: true,
          created_at: new Date(Date.now() - 15 * 24 * 60 * 60 * 1000).toISOString()
        }
      ]
    };
  },

  // Mentions
  getMentions: async () => {
    return {
      data: [
        {
          id: '1',
          entity_id: '1',
          source: 'Twitter',
          content: 'Tech Corp just released an amazing new feature! Love the innovation.',
          sentiment: 'positive',
          url: 'https://twitter.com/example/status/123',
          created_at: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString()
        },
        {
          id: '2',
          entity_id: '1',
          source: 'Reddit',
          content: 'Has anyone tried Tech Corp products? Thinking of switching.',
          sentiment: 'neutral',
          url: 'https://reddit.com/r/tech/comments/abc',
          created_at: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString()
        },
        {
          id: '3',
          entity_id: '2',
          source: 'LinkedIn',
          content: 'Great insights from John Smith at the tech conference today.',
          sentiment: 'positive',
          url: 'https://linkedin.com/posts/example',
          created_at: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString()
        },
        {
          id: '4',
          entity_id: '1',
          source: 'Twitter',
          content: 'Tech Corp customer service is terrible. Been waiting 3 days for response.',
          sentiment: 'negative',
          url: 'https://twitter.com/example/status/456',
          created_at: new Date(Date.now() - 4 * 24 * 60 * 60 * 1000).toISOString()
        }
      ]
    };
  },

  // Alerts
  getAlerts: async () => {
    return {
      data: [
        {
          id: '1',
          entity_id: '1',
          alert_type: 'negative_sentiment',
          severity: 'high',
          message: 'Negative mention detected on Twitter regarding customer service',
          is_read: false,
          created_at: new Date(Date.now() - 1 * 60 * 60 * 1000).toISOString()
        },
        {
          id: '2',
          entity_id: '2',
          alert_type: 'mention_spike',
          severity: 'medium',
          message: 'Unusual increase in mentions detected (50% above baseline)',
          is_read: false,
          created_at: new Date(Date.now() - 3 * 60 * 60 * 1000).toISOString()
        },
        {
          id: '3',
          entity_id: '1',
          alert_type: 'brand_crisis',
          severity: 'critical',
          message: 'Multiple negative mentions detected in short timeframe',
          is_read: true,
          created_at: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString()
        }
      ]
    };
  }
};
