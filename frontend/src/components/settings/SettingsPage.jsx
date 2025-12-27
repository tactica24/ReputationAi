import React, { useState } from 'react';
import { useAuthStore } from '../../store/authStore';

function SettingsPage() {
  const { user } = useAuthStore();
  const [activeTab, setActiveTab] = useState('profile');
  
  const [profile, setProfile] = useState({
    firstName: user?.firstName || 'John',
    lastName: user?.lastName || 'Doe',
    email: user?.email || 'john@example.com',
    phone: '+1 (555) 123-4567',
    company: 'Acme Corporation',
    title: 'CEO & Founder'
  });

  const [notifications, setNotifications] = useState({
    emailAlerts: true,
    smsAlerts: true,
    pushNotifications: true,
    weeklyReport: true,
    criticalOnly: false,
    mentionAlerts: true,
    sentimentAlerts: true
  });

  const [security, setSecurity] = useState({
    twoFactorEnabled: false,
    sessionTimeout: '30',
    allowedIPs: ''
  });

  const handleProfileSave = (e) => {
    e.preventDefault();
    alert('Profile updated successfully!');
  };

  const handleNotificationsSave = (e) => {
    e.preventDefault();
    alert('Notification preferences updated!');
  };

  const handleSecuritySave = (e) => {
    e.preventDefault();
    alert('Security settings updated!');
  };

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Settings</h1>
        <p className="text-gray-600 mt-1">Manage your account preferences and security</p>
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 mb-6">
        <div className="flex border-b border-gray-200">
          <button
            onClick={() => setActiveTab('profile')}
            className={`px-6 py-3 font-medium transition ${
              activeTab === 'profile'
                ? 'text-blue-600 border-b-2 border-blue-600'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            Profile
          </button>
          <button
            onClick={() => setActiveTab('notifications')}
            className={`px-6 py-3 font-medium transition ${
              activeTab === 'notifications'
                ? 'text-blue-600 border-b-2 border-blue-600'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            Notifications
          </button>
          <button
            onClick={() => setActiveTab('security')}
            className={`px-6 py-3 font-medium transition ${
              activeTab === 'security'
                ? 'text-blue-600 border-b-2 border-blue-600'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            Security
          </button>
        </div>

        <div className="p-6">
          {/* Profile Tab */}
          {activeTab === 'profile' && (
            <form onSubmit={handleProfileSave}>
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Profile Information</h2>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">First Name</label>
                  <input
                    type="text"
                    value={profile.firstName}
                    onChange={(e) => setProfile({ ...profile, firstName: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Last Name</label>
                  <input
                    type="text"
                    value={profile.lastName}
                    onChange={(e) => setProfile({ ...profile, lastName: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Email</label>
                  <input
                    type="email"
                    value={profile.email}
                    onChange={(e) => setProfile({ ...profile, email: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Phone</label>
                  <input
                    type="tel"
                    value={profile.phone}
                    onChange={(e) => setProfile({ ...profile, phone: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Company</label>
                  <input
                    type="text"
                    value={profile.company}
                    onChange={(e) => setProfile({ ...profile, company: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Title</label>
                  <input
                    type="text"
                    value={profile.title}
                    onChange={(e) => setProfile({ ...profile, title: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>

              <button
                type="submit"
                className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition"
              >
                Save Changes
              </button>
            </form>
          )}

          {/* Notifications Tab */}
          {activeTab === 'notifications' && (
            <form onSubmit={handleNotificationsSave}>
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Notification Preferences</h2>
              
              <div className="space-y-4 mb-6">
                <div className="flex items-center justify-between py-3 border-b border-gray-200">
                  <div>
                    <p className="font-medium text-gray-900">Email Alerts</p>
                    <p className="text-sm text-gray-600">Receive alerts via email</p>
                  </div>
                  <button
                    type="button"
                    onClick={() => setNotifications({ ...notifications, emailAlerts: !notifications.emailAlerts })}
                    className={`w-12 h-6 rounded-full transition ${
                      notifications.emailAlerts ? 'bg-blue-600' : 'bg-gray-300'
                    }`}
                  >
                    <div className={`w-4 h-4 bg-white rounded-full transition transform ${
                      notifications.emailAlerts ? 'translate-x-7' : 'translate-x-1'
                    }`}></div>
                  </button>
                </div>

                <div className="flex items-center justify-between py-3 border-b border-gray-200">
                  <div>
                    <p className="font-medium text-gray-900">SMS Alerts</p>
                    <p className="text-sm text-gray-600">Receive urgent alerts via SMS</p>
                  </div>
                  <button
                    type="button"
                    onClick={() => setNotifications({ ...notifications, smsAlerts: !notifications.smsAlerts })}
                    className={`w-12 h-6 rounded-full transition ${
                      notifications.smsAlerts ? 'bg-blue-600' : 'bg-gray-300'
                    }`}
                  >
                    <div className={`w-4 h-4 bg-white rounded-full transition transform ${
                      notifications.smsAlerts ? 'translate-x-7' : 'translate-x-1'
                    }`}></div>
                  </button>
                </div>

                <div className="flex items-center justify-between py-3 border-b border-gray-200">
                  <div>
                    <p className="font-medium text-gray-900">Push Notifications</p>
                    <p className="text-sm text-gray-600">Browser push notifications</p>
                  </div>
                  <button
                    type="button"
                    onClick={() => setNotifications({ ...notifications, pushNotifications: !notifications.pushNotifications })}
                    className={`w-12 h-6 rounded-full transition ${
                      notifications.pushNotifications ? 'bg-blue-600' : 'bg-gray-300'
                    }`}
                  >
                    <div className={`w-4 h-4 bg-white rounded-full transition transform ${
                      notifications.pushNotifications ? 'translate-x-7' : 'translate-x-1'
                    }`}></div>
                  </button>
                </div>

                <div className="flex items-center justify-between py-3 border-b border-gray-200">
                  <div>
                    <p className="font-medium text-gray-900">Weekly Report</p>
                    <p className="text-sm text-gray-600">Get a summary every week</p>
                  </div>
                  <button
                    type="button"
                    onClick={() => setNotifications({ ...notifications, weeklyReport: !notifications.weeklyReport })}
                    className={`w-12 h-6 rounded-full transition ${
                      notifications.weeklyReport ? 'bg-blue-600' : 'bg-gray-300'
                    }`}
                  >
                    <div className={`w-4 h-4 bg-white rounded-full transition transform ${
                      notifications.weeklyReport ? 'translate-x-7' : 'translate-x-1'
                    }`}></div>
                  </button>
                </div>

                <div className="flex items-center justify-between py-3 border-b border-gray-200">
                  <div>
                    <p className="font-medium text-gray-900">Critical Only</p>
                    <p className="text-sm text-gray-600">Only notify for critical alerts</p>
                  </div>
                  <button
                    type="button"
                    onClick={() => setNotifications({ ...notifications, criticalOnly: !notifications.criticalOnly })}
                    className={`w-12 h-6 rounded-full transition ${
                      notifications.criticalOnly ? 'bg-blue-600' : 'bg-gray-300'
                    }`}
                  >
                    <div className={`w-4 h-4 bg-white rounded-full transition transform ${
                      notifications.criticalOnly ? 'translate-x-7' : 'translate-x-1'
                    }`}></div>
                  </button>
                </div>
              </div>

              <button
                type="submit"
                className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition"
              >
                Save Preferences
              </button>
            </form>
          )}

          {/* Security Tab */}
          {activeTab === 'security' && (
            <form onSubmit={handleSecuritySave}>
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Security Settings</h2>
              
              <div className="space-y-6 mb-6">
                <div className="flex items-center justify-between py-3 border-b border-gray-200">
                  <div>
                    <p className="font-medium text-gray-900">Two-Factor Authentication</p>
                    <p className="text-sm text-gray-600">Add an extra layer of security</p>
                  </div>
                  <button
                    type="button"
                    onClick={() => setSecurity({ ...security, twoFactorEnabled: !security.twoFactorEnabled })}
                    className={`w-12 h-6 rounded-full transition ${
                      security.twoFactorEnabled ? 'bg-blue-600' : 'bg-gray-300'
                    }`}
                  >
                    <div className={`w-4 h-4 bg-white rounded-full transition transform ${
                      security.twoFactorEnabled ? 'translate-x-7' : 'translate-x-1'
                    }`}></div>
                  </button>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Session Timeout (minutes)</label>
                  <select
                    value={security.sessionTimeout}
                    onChange={(e) => setSecurity({ ...security, sessionTimeout: e.target.value })}
                    className="w-full md:w-64 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="15">15 minutes</option>
                    <option value="30">30 minutes</option>
                    <option value="60">1 hour</option>
                    <option value="120">2 hours</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Change Password</label>
                  <button
                    type="button"
                    className="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-200 transition"
                  >
                    Update Password
                  </button>
                </div>
              </div>

              <button
                type="submit"
                className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition"
              >
                Save Security Settings
              </button>
            </form>
          )}
        </div>
      </div>
    </div>
  );
}

export default SettingsPage;
