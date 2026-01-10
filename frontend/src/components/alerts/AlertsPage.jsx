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

            const getSeverityColor = (severity) => {
              switch (severity) {
                case 'critical': return 'bg-red-100 text-red-800 border-red-200';
                case 'high': return 'bg-orange-100 text-orange-800 border-orange-200';
                case 'medium': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
                case 'low': return 'bg-green-100 text-green-800 border-green-200';
                default: return 'bg-gray-100 text-gray-800 border-gray-200';
              }
            };

            const getSeverityIcon = (severity) => {
              switch (severity) {
                case 'critical': return '🚨';
                case 'high': return '⚠️';
                case 'medium': return '⚡';
                case 'low': return '✅';
                default: return 'ℹ️';
              }
            };

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

// ...existing code...
        </div>
      </div>

      {/* Alerts List */}
      <div className="space-y-4">
        {alerts.length === 0 ? (
          <div className="bg-white rounded-lg shadow-sm p-12 text-center border border-gray-200">
            <p className="text-gray-500 text-lg">No alerts found matching your filters</p>
          </div>
        ) : (
          alerts.map(alert => (
            <div
              key={alert.id}
              className={`bg-white rounded-lg shadow-sm p-6 border-2 transition hover:shadow-md ${
                !alert.read ? 'border-blue-300 bg-blue-50' : 'border-gray-200'
              }`}
            >
              <div className="flex justify-between items-start">
                <div className="flex items-start space-x-4 flex-1">
                  <div className="text-3xl">{getSeverityIcon(alert.severity)}</div>
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-2">
                      <h3 className={`text-lg font-semibold ${!alert.read ? 'text-gray-900' : 'text-gray-700'}`}>
                        {alert.title}
                      </h3>
                      <span className={`px-3 py-1 rounded-full text-xs font-medium uppercase border ${getSeverityColor(alert.severity)}`}>
                        {alert.severity}
                      </span>
                      {!alert.read && (
                        <span className="px-2 py-1 bg-blue-600 text-white rounded-full text-xs font-medium">
                          NEW
                        </span>
                      )}
                    </div>
                    <p className="text-gray-600 mb-3">{alert.description}</p>
                    <div className="flex items-center space-x-4 text-sm text-gray-500">
                      <span>Entity: <span className="text-gray-900 font-medium">{alert.entity}</span></span>
                      <span>•</span>
                      <span>{formatTimestamp(alert.timestamp)}</span>
                      <span>•</span>
                      <span>{alert.sources} sources</span>
                      <span>•</span>
                      <span>Reach: {alert.reach.toLocaleString()}</span>
                    </div>
                    {alert.actionTaken && (
                      <div className="mt-3 flex items-center space-x-2 text-green-600">
                        <span>✓</span>
                        <span className="text-sm font-medium">Action Taken</span>
                      </div>
                    )}
                  </div>
                </div>
              </div>
              <div className="flex space-x-2 pt-4 mt-4 border-t border-gray-100">
                {!alert.read && (
                  <button
                    onClick={() => markAsRead(alert.id)}
                    className="px-4 py-2 bg-blue-50 text-blue-600 rounded hover:bg-blue-100 transition text-sm"
                  >
                    Mark as Read
                  </button>
                )}
                {!alert.actionTaken && (
                  <button
                    onClick={() => markActionTaken(alert.id)}
                    className="px-4 py-2 bg-green-50 text-green-600 rounded hover:bg-green-100 transition text-sm"
                  >
                    Mark Action Taken
                  </button>
                )}
                <button className="px-4 py-2 bg-gray-50 text-gray-700 rounded hover:bg-gray-100 transition text-sm">
                  View Details
                </button>
                <button className="px-4 py-2 bg-gray-50 text-gray-700 rounded hover:bg-gray-100 transition text-sm">
                  Export Report
                </button>
                <button
                  onClick={() => deleteAlert(alert.id)}
                  className="px-4 py-2 bg-red-50 text-red-600 rounded hover:bg-red-100 transition text-sm"
                >
                  Delete
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default AlertsPage;
