// Admin Scraping/API Key and Notification API
// Calls backend endpoints for admin scraping and notification management

const API_BASE = "/api/v1/admin/scraping";

export const adminScrapingAPI = {
  getApiKeys: async () => {
    const res = await fetch(`${API_BASE}/keys`, { credentials: 'include' });
    return res.json();
  },
  updateApiKeys: async (keys) => {
    const res = await fetch(`${API_BASE}/keys/update`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify(keys)
    });
    return res.json();
  },
  triggerScraping: async (source, entity) => {
    const res = await fetch(`${API_BASE}/trigger`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ source, entity })
    });
    return res.json();
  },
  getScrapingStatus: async () => {
    const res = await fetch(`${API_BASE}/status`, { credentials: 'include' });
    return res.json();
  }
};

// Notification API (user preferences)
const USER_API_BASE = "/api/v1/user";
export const notificationAPI = {
  getPreferences: async () => {
    const res = await fetch(`${USER_API_BASE}/notification-preferences`, { credentials: 'include' });
    return res.json();
  },
  updatePreferences: async (prefs) => {
    const res = await fetch(`${USER_API_BASE}/notification-preferences`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify(prefs)
    });
    return res.json();
  },
  testNotification: async () => {
    const res = await fetch(`${USER_API_BASE}/test-notification`, { credentials: 'include' });
    return res.json();
  }
};
