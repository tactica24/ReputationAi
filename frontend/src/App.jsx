import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/layout/Layout';
import HomePage from './components/home/HomePage';
import Dashboard from './components/dashboard/Dashboard';
import EntitiesPage from './components/entities/EntitiesPage';
import MentionsPage from './components/mentions/MentionsPage';
import AlertsPage from './components/alerts/AlertsPage';
import AnalyticsPage from './components/analytics/AnalyticsPage';
import SettingsPage from './components/settings/SettingsPage';
import AdminDashboard from './components/admin/AdminDashboard';
import LoginPage from './components/auth/LoginPage';
import ProtectionPage from './pages/ProtectionPage';
import EnterprisePage from './pages/EnterprisePage';
import SubscribePage from './pages/SubscribePage';
import PrivacyPage from './pages/PrivacyPage';
import TermsPage from './pages/TermsPage';
import SecurityPage from './pages/SecurityPage';
import { useAuthStore } from './store/authStore';

function App() {
  const { isAuthenticated, user } = useAuthStore();

  return (
    <Routes>
      {/* Public pages */}
      <Route path="/" element={<HomePage />} />
      <Route path="/protection" element={<ProtectionPage />} />
      <Route path="/enterprise" element={<EnterprisePage />} />
      <Route path="/subscribe" element={<SubscribePage />} />
      <Route path="/privacy" element={<PrivacyPage />} />
      <Route path="/terms" element={<TermsPage />} />
      <Route path="/security" element={<SecurityPage />} />
      
      {/* Login page */}
      <Route path="/login" element={<LoginPage />} />

      {/* Protected routes */}
      {isAuthenticated ? (
        <>
          <Route path="/dashboard" element={<Layout><Dashboard /></Layout>} />
          <Route path="/entities" element={<Layout><EntitiesPage /></Layout>} />
          <Route path="/mentions" element={<Layout><MentionsPage /></Layout>} />
          <Route path="/alerts" element={<Layout><AlertsPage /></Layout>} />
          <Route path="/analytics" element={<Layout><AnalyticsPage /></Layout>} />
          <Route path="/settings" element={<Layout><SettingsPage /></Layout>} />
          
          {/* Admin-only route */}
          {user?.role === 'admin' && (
            <Route path="/admin" element={<AdminDashboard />} />
          )}
        </>
      ) : null}
      
      {/* Catch-all */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default App;
