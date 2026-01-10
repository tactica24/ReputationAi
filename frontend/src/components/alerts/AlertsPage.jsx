import React, { useState, useEffect } from 'react';

function AlertsPage() {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all'); // all, unread, critical, high, medium, low

  useEffect(() => {
    fetchAlerts();
  }, [filter]);

  const fetchAlerts = async () => {
    try {
      setLoading(true);
      // Simulate API call - replace with actual endpoint
      const mockAlerts = [
        {
          id: 1,
          title: 'Coordinated negative campaign detected',
          description: 'Multiple fake accounts posting similar negative content about John Doe',
          severity: 'critical',
          entity: 'John Doe',
          timestamp: new Date(Date.now() - 1800000).toISOString(),
          read: false,
          actionTaken: false,
          sources: 15,
          reach: 45000
        },
        // ...existing mockAlerts...
      ];

      // Filter alerts based on the selected filter
      const filteredAlerts = mockAlerts.filter(alert => {
        if (filter === 'all') return true;
        if (filter === 'unread' && !alert.read) return true;
        if (filter === 'critical' && alert.severity === 'critical') return true;
        if (filter === 'high' && alert.severity === 'high') return true;
        if (filter === 'medium' && alert.severity === 'medium') return true;
        if (filter === 'low' && alert.severity === 'low') return true;
        return false;
      });

      setAlerts(filteredAlerts);
    } catch (error) {
      console.error('Error fetching alerts:', error);
    } finally {
      setLoading(false);
    }
  };

  function getSeverityColor(severity) {
    switch (severity) {
      case 'critical': return 'bg-red-100 text-red-800 border-red-200';
      case 'high': return 'bg-orange-100 text-orange-800 border-orange-200';
      case 'medium': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'low': return 'bg-green-100 text-green-800 border-green-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  }

  function getSeverityIcon(severity) {
    switch (severity) {
      case 'critical': return '🚨';
      case 'high': return '⚠️';
      case 'medium': return '⚡';
      case 'low': return '✅';
      default: return 'ℹ️';
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-red-600"></div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Alerts</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {alerts.map(alert => (
          <div key={alert.id} className={`bg-white rounded-lg shadow-md p-6 border-2 ${getSeverityColor(alert.severity)}`}>
            <div className="flex items-center mb-2">
              <span className="text-2xl mr-2">{getSeverityIcon(alert.severity)}</span>
              <div className="font-semibold text-lg">{alert.title}</div>
            </div>
            <div className="flex justify-between items-center text-xs text-gray-500 mt-2">
              <span>{new Date(alert.timestamp).toLocaleString()}</span>
              {alert.url && (
                <a href={alert.url} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">View Source</a>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default AlertsPage;
