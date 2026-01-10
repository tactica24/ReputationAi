/**
 * Admin Dashboard - Comprehensive admin control panel
 * Features: User management, application approval, analytics, system monitoring
 */

import React, { useState, useEffect } from 'react';
import { adminScrapingAPI, notificationAPI } from '../../services/adminApi';
import { Line, Bar, Pie } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

function ScrapingTab() {
  const [keys, setKeys] = useState({});
  const [form, setForm] = useState({});
  const [status, setStatus] = useState(null);
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [triggering, setTriggering] = useState(false);
  const [entity, setEntity] = useState("");
  const [source, setSource] = useState("twitter");

  useEffect(() => {
    adminScrapingAPI.getApiKeys().then(setKeys);
    adminScrapingAPI.getScrapingStatus().then((s) => {
      setStatus(s);
      setLogs(s.logs || []);
      setLoading(false);
    });
  }, []);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };
  const handleSave = async () => {
    setSaving(true);
    await adminScrapingAPI.updateApiKeys(form);
    const updated = await adminScrapingAPI.getApiKeys();
    setKeys(updated);
    setSaving(false);
    setForm({});
    alert("API keys updated.");
  };
  const handleTrigger = async () => {
    setTriggering(true);
    await adminScrapingAPI.triggerScraping(source, entity);
    setTriggering(false);
    alert("Scraping triggered.");
  };
  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-2xl font-bold mb-2">Scraping & API Keys</h2>
      <p className="text-gray-600 mb-4">Configure API keys for social/news sources and control scraping jobs.</p>
      <div className="mb-4 grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block font-medium mb-1">Twitter API Key</label>
          <input name="twitter" value={form.twitter ?? ""} onChange={handleChange} className="w-full border rounded px-3 py-2" placeholder={keys.twitter || "Enter Twitter API Key"} />
        </div>
        <div>
          <label className="block font-medium mb-1">NewsAPI Key</label>
          <input name="newsapi" value={form.newsapi ?? ""} onChange={handleChange} className="w-full border rounded px-3 py-2" placeholder={keys.newsapi || "Enter NewsAPI Key"} />
        </div>
        <div>
          <label className="block font-medium mb-1">Reddit Client ID</label>
          <input name="reddit_client_id" value={form.reddit_client_id ?? ""} onChange={handleChange} className="w-full border rounded px-3 py-2" placeholder={keys.reddit_client_id || "Enter Reddit Client ID"} />
        </div>
        <div>
          <label className="block font-medium mb-1">Reddit Client Secret</label>
          <input name="reddit_client_secret" value={form.reddit_client_secret ?? ""} onChange={handleChange} className="w-full border rounded px-3 py-2" placeholder={keys.reddit_client_secret || "Enter Reddit Client Secret"} />
        </div>
        <div>
          <label className="block font-medium mb-1">Reddit User Agent</label>
          <input name="reddit_user_agent" value={form.reddit_user_agent ?? ""} onChange={handleChange} className="w-full border rounded px-3 py-2" placeholder={keys.reddit_user_agent || "Enter Reddit User Agent"} />
        </div>
      </div>
      <button className="px-4 py-2 bg-indigo-600 text-white rounded" onClick={handleSave} disabled={saving}>{saving ? "Saving..." : "Save API Keys"}</button>
      <hr className="my-6" />
      <h3 className="text-lg font-semibold mb-2">Scraping Controls</h3>
      <div className="flex flex-col md:flex-row md:items-end gap-4 mb-4">
        <div>
          <label className="block font-medium mb-1">Source</label>
          <select value={source} onChange={e => setSource(e.target.value)} className="border rounded px-3 py-2">
            <option value="twitter">Twitter</option>
            <option value="reddit">Reddit</option>
            <option value="newsapi">NewsAPI</option>
          </select>
        </div>
        <div>
          <label className="block font-medium mb-1">Entity</label>
          <input value={entity} onChange={e => setEntity(e.target.value)} className="border rounded px-3 py-2" placeholder="Enter entity name or handle" />
        </div>
        <button className="px-4 py-2 bg-green-600 text-white rounded" onClick={handleTrigger} disabled={triggering}>{triggering ? "Triggering..." : "Run Scraper"}</button>
      </div>
      <h4 className="font-semibold mb-2">Scraping Status</h4>
      {loading ? <div>Loading status...</div> : (
        <div>
          <div className="mb-2">Last Run: {status?.last_run}</div>
          <div className="mb-2">Status: {status?.status}</div>
          <div className="mb-2">Logs:</div>
          <ul className="text-sm bg-gray-100 rounded p-2">
            {logs.map((log, i) => <li key={i}>{log}</li>)}
          </ul>
        </div>
      )}
    </div>
  );
}

function NotificationsTab() {
  const [prefs, setPrefs] = useState({ email: true, sms: false, push: true });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [testing, setTesting] = useState(false);

  useEffect(() => {
    notificationAPI.getPreferences().then((data) => {
      setPrefs(data);
      setLoading(false);
    });
  }, []);

  const handleChange = (e) => {
    setPrefs({ ...prefs, [e.target.name]: e.target.checked });
  };
  const handleSave = async () => {
    setSaving(true);
    await notificationAPI.updatePreferences(prefs);
    setSaving(false);
    alert("Preferences saved.");
  };
  const handleTest = async () => {
    setTesting(true);
    await notificationAPI.testNotification();
    setTesting(false);
    alert("Test notification sent.");
  };
  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-2xl font-bold mb-2">Notifications</h2>
      <p className="text-gray-600 mb-4">Manage notification preferences and test notification delivery.</p>
      {loading ? <div>Loading preferences...</div> : (
        <div className="mb-4">
          <label className="block font-medium mb-1">Default Notification Channels</label>
          <div className="flex space-x-4">
            <label><input type="checkbox" name="email" checked={!!prefs.email} onChange={handleChange} /> Email</label>
            <label><input type="checkbox" name="sms" checked={!!prefs.sms} onChange={handleChange} /> SMS</label>
            <label><input type="checkbox" name="push" checked={!!prefs.push} onChange={handleChange} /> Push</label>
          </div>
        </div>
      )}
      <button className="px-4 py-2 bg-indigo-600 text-white rounded" onClick={handleSave} disabled={saving}>{saving ? "Saving..." : "Save Preferences"}</button>
      <hr className="my-6" />
      <h3 className="text-lg font-semibold mb-2">Test Notification</h3>
      <button className="px-4 py-2 bg-green-600 text-white rounded" onClick={handleTest} disabled={testing}>{testing ? "Sending..." : "Send Test Notification"}</button>
    </div>
  );
}

export default function AdminDashboard() {
  const [activeTab, setActiveTab] = useState('overview');
  const [users, setUsers] = useState([]);
  const [applications, setApplications] = useState([]);
  const [systemMetrics, setSystemMetrics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAdminData();
  }, []);

  const fetchAdminData = async () => {
    try {
      // Fetch users
      const usersRes = await fetch('/api/v1/admin/users', {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
      });
      const usersData = await usersRes.json();
      setUsers(usersData);

      // Fetch applications
      const appsRes = await fetch('/api/v1/admin/applications', {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
      });
      const appsData = await appsRes.json();
      setApplications(appsData);

      // Fetch system metrics
      const metricsRes = await fetch('/api/v1/admin/metrics', {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
      });
      const metricsData = await metricsRes.json();
      setSystemMetrics(metricsData);

      setLoading(false);
    } catch (error) {
      console.error('Error fetching admin data:', error);
      setLoading(false);
    }
  };

  const handleApproveApplication = async (applicationId) => {
    try {
      await fetch(`/api/v1/admin/applications/${applicationId}/approve`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
      });
      fetchAdminData();
      alert('Application approved successfully!');
    } catch (error) {
      console.error('Error approving application:', error);
      alert('Failed to approve application');
    }
  };

  const handleRejectApplication = async (applicationId) => {
    try {
      await fetch(`/api/v1/admin/applications/${applicationId}/reject`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
      });
      fetchAdminData();
      alert('Application rejected');
    } catch (error) {
      console.error('Error rejecting application:', error);
    }
  };

  const handleToggleUserStatus = async (userId, currentStatus) => {
    try {
      await fetch(`/api/v1/admin/users/${userId}/toggle-status`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status: currentStatus === 'active' ? 'suspended' : 'active' }),
      });
      fetchAdminData();
    } catch (error) {
      console.error('Error toggling user status:', error);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  const renderOverview = () => (
    <div className="space-y-6">
      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="text-sm font-medium text-gray-600">Total Users</div>
          <div className="mt-2 text-3xl font-bold text-gray-900">{systemMetrics?.totalUsers || 0}</div>
          <div className="mt-2 text-sm text-green-600">+{systemMetrics?.newUsersThisMonth || 0} this month</div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <div className="text-sm font-medium text-gray-600">Pending Applications</div>
          <div className="mt-2 text-3xl font-bold text-orange-600">{systemMetrics?.pendingApplications || 0}</div>
          <div className="mt-2 text-sm text-gray-600">Requires review</div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <div className="text-sm font-medium text-gray-600">Active Subscriptions</div>
          <div className="mt-2 text-3xl font-bold text-green-600">{systemMetrics?.activeSubscriptions || 0}</div>
          <div className="mt-2 text-sm text-gray-600">
            ${systemMetrics?.monthlyRevenue || 0}/mo revenue
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <div className="text-sm font-medium text-gray-600">System Health</div>
          <div className="mt-2 text-3xl font-bold text-green-600">{systemMetrics?.systemHealth || 'Good'}</div>
          <div className="mt-2 text-sm text-gray-600">
            {systemMetrics?.uptime || '99.9'}% uptime
          </div>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold mb-4">User Growth (30 Days)</h3>
          <Line
            data={{
              labels: systemMetrics?.userGrowthLabels || [],
              datasets: [
                {
                  label: 'New Users',
                  data: systemMetrics?.userGrowthData || [],
                  borderColor: 'rgb(99, 102, 241)',
                  backgroundColor: 'rgba(99, 102, 241, 0.1)',
                },
              ],
            }}
            options={{ responsive: true, maintainAspectRatio: true }}
          />
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold mb-4">Subscription Distribution</h3>
          <Pie
            data={{
              labels: ['Basic', 'Pro', 'Enterprise'],
              datasets: [
                {
                  data: systemMetrics?.subscriptionDistribution || [0, 0, 0],
                  backgroundColor: [
                    'rgba(59, 130, 246, 0.8)',
                    'rgba(99, 102, 241, 0.8)',
                    'rgba(139, 92, 246, 0.8)',
                  ],
                },
              ],
            }}
            options={{ responsive: true, maintainAspectRatio: true }}
          />
        </div>
      </div>

      {/* Recent Activity */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold mb-4">Recent Admin Activity</h3>
        <div className="space-y-3">
          {systemMetrics?.recentActivity?.map((activity, index) => (
            <div key={index} className="flex items-center justify-between py-2 border-b">
              <div>
                <span className="font-medium">{activity.action}</span>
                <span className="text-gray-600 ml-2">by {activity.admin}</span>
              </div>
              <span className="text-sm text-gray-500">{activity.timestamp}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const renderApplications = () => (
    <div className="bg-white rounded-lg shadow">
      <div className="p-6 border-b">
        <h2 className="text-2xl font-bold">Application Management</h2>
        <p className="text-gray-600 mt-1">Review and approve new user applications</p>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Applicant</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Plan</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Entities</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Urgency</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {applications
              .filter((app) => app.status === 'pending')
              .map((app) => (
                <tr key={app.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4">
                    <div className="font-medium text-gray-900">
                      {app.firstName} {app.lastName}
                    </div>
                    <div className="text-sm text-gray-600">{app.email}</div>
                  </td>
                  <td className="px-6 py-4">
                    <span className="px-2 py-1 text-xs font-semibold rounded-full bg-indigo-100 text-indigo-800">
                      {app.plan}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-600">{app.entities}</td>
                  <td className="px-6 py-4">
                    <span
                      className={`px-2 py-1 text-xs font-semibold rounded-full ${
                        app.urgency === 'immediate'
                          ? 'bg-red-100 text-red-800'
                          : app.urgency === 'within-week'
                          ? 'bg-orange-100 text-orange-800'
                          : 'bg-green-100 text-green-800'
                      }`}
                    >
                      {app.urgency.replace('-', ' ')}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-600">
                    {new Date(app.submittedAt).toLocaleDateString()}
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex space-x-2">
                      <button
                        onClick={() => handleApproveApplication(app.id)}
                        className="px-3 py-1 bg-green-600 text-white text-sm rounded hover:bg-green-700"
                      >
                        Approve
                      </button>
                      <button
                        onClick={() => handleRejectApplication(app.id)}
                        className="px-3 py-1 bg-red-600 text-white text-sm rounded hover:bg-red-700"
                      >
                        Reject
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
          </tbody>
        </table>
      </div>
    </div>
  );

  const renderUsers = () => (
    <div className="bg-white rounded-lg shadow">
      <div className="p-6 border-b">
        <h2 className="text-2xl font-bold">User Management</h2>
        <p className="text-gray-600 mt-1">Manage all platform users and their accounts</p>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">User</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Plan</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Joined</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Last Active</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {users.map((user) => (
              <tr key={user.id} className="hover:bg-gray-50">
                <td className="px-6 py-4">
                  <div className="font-medium text-gray-900">{user.name}</div>
                  <div className="text-sm text-gray-600">{user.email}</div>
                </td>
                <td className="px-6 py-4">
                  <span className="px-2 py-1 text-xs font-semibold rounded-full bg-indigo-100 text-indigo-800">
                    {user.plan}
                  </span>
                </td>
                <td className="px-6 py-4">
                  <span
                    className={`px-2 py-1 text-xs font-semibold rounded-full ${
                      user.status === 'active'
                        ? 'bg-green-100 text-green-800'
                        : 'bg-red-100 text-red-800'
                    }`}
                  >
                    {user.status}
                  </span>
                </td>
                <td className="px-6 py-4 text-sm text-gray-600">
                  {new Date(user.joinedAt).toLocaleDateString()}
                </td>
                <td className="px-6 py-4 text-sm text-gray-600">
                  {new Date(user.lastActive).toLocaleDateString()}
                </td>
                <td className="px-6 py-4">
                  <button
                    onClick={() => handleToggleUserStatus(user.id, user.status)}
                    className={`px-3 py-1 text-sm rounded ${
                      user.status === 'active'
                        ? 'bg-red-100 text-red-800 hover:bg-red-200'
                        : 'bg-green-100 text-green-800 hover:bg-green-200'
                    }`}
                  >
                    {user.status === 'active' ? 'Suspend' : 'Activate'}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );

  const renderAnalytics = () => (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold mb-4">Platform Analytics</h3>
        <Bar
          data={{
            labels: systemMetrics?.analyticsLabels || [],
            datasets: [
              {
                label: 'Total Mentions Processed',
                data: systemMetrics?.mentionsProcessed || [],
                backgroundColor: 'rgba(99, 102, 241, 0.8)',
              },
              {
                label: 'Alerts Generated',
                data: systemMetrics?.alertsGenerated || [],
                backgroundColor: 'rgba(239, 68, 68, 0.8)',
              },
            ],
          }}
          options={{ responsive: true, maintainAspectRatio: true }}
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <h4 className="text-sm font-medium text-gray-600">Avg Reputation Score</h4>
          <div className="mt-2 text-3xl font-bold text-gray-900">{systemMetrics?.avgReputationScore || 75}</div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h4 className="text-sm font-medium text-gray-600">Total Entities Monitored</h4>
          <div className="mt-2 text-3xl font-bold text-gray-900">{systemMetrics?.totalEntities || 0}</div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h4 className="text-sm font-medium text-gray-600">API Response Time</h4>
          <div className="mt-2 text-3xl font-bold text-green-600">{systemMetrics?.avgResponseTime || 45}ms</div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <div className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <h1 className="text-3xl font-bold text-gray-900">Admin Dashboard</h1>
          <p className="text-gray-600 mt-1">Manage users, applications, and monitor system performance</p>
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex space-x-8" aria-label="Tabs">
            {['overview', 'applications', 'users', 'analytics', 'scraping', 'notifications'].map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`py-4 px-1 border-b-2 font-medium text-sm capitalize ${
                  activeTab === tab
                    ? 'border-indigo-600 text-indigo-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                {tab}
              </button>
            ))}
          </nav>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'overview' && renderOverview()}
        {activeTab === 'applications' && renderApplications()}
        {activeTab === 'users' && renderUsers()}
        {activeTab === 'analytics' && renderAnalytics()}
        {activeTab === 'scraping' && <ScrapingTab />}
        {activeTab === 'notifications' && <NotificationsTab />}
      </div>
    </div>
  );
}
