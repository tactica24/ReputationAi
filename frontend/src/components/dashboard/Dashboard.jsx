import React, { useState, useEffect } from 'react';
import {
  LineChart, Line, BarChart, Bar, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';

/**
 * Main Dashboard Component
 * Interactive reputation monitoring dashboard with real-time insights
 */
const Dashboard = ({ entityId }) => {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [timeframe, setTimeframe] = useState('24h');

  useEffect(() => {
    fetchDashboardData();
  }, [entityId, timeframe]);

  const fetchDashboardData = async () => {
    try {
      const response = await fetch(`/api/v1/dashboard/${entityId}?timeframe=${timeframe}`);
      const data = await response.json();
      setDashboardData(data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return <LoadingSpinner />;
  }

  return (
    <div className="dashboard-container">
      {/* Header Section */}
      <DashboardHeader
        reputationScore={dashboardData.reputation_score}
        timeframe={timeframe}
        onTimeframeChange={setTimeframe}
      />

      {/* Key Metrics Grid */}
      <MetricsGrid data={dashboardData} />

      {/* Charts Section */}
      <div className="charts-grid">
        <SentimentTrendChart data={dashboardData.sentiment_trend} />
        <SentimentDistributionChart data={dashboardData.sentiment_distribution} />
        <SourceBreakdownChart data={dashboardData.source_breakdown} />
        <MentionVolumeChart data={dashboardData.mention_volume} />
      </div>

      {/* Trending Keywords */}
      <TrendingKeywords keywords={dashboardData.trending_keywords} />

      {/* Recent Alerts */}
      <AlertsPanel alerts={dashboardData.recent_alerts} />
    </div>
  );
};

/**
 * Dashboard Header with Score Display
 */
const DashboardHeader = ({ reputationScore, timeframe, onTimeframeChange }) => {
  const getScoreColor = (score) => {
    if (score >= 80) return '#10b981';
    if (score >= 65) return '#3b82f6';
    if (score >= 45) return '#f59e0b';
    return '#ef4444';
  };

  return (
    <div className="dashboard-header">
      <div className="score-display">
        <div className="score-circle" style={{ borderColor: getScoreColor(reputationScore) }}>
          <span className="score-value">{reputationScore.toFixed(1)}</span>
          <span className="score-label">Reputation Score</span>
        </div>
      </div>

      <div className="timeframe-selector">
        {['24h', '7d', '30d'].map((tf) => (
          <button
            key={tf}
            className={`timeframe-btn ${timeframe === tf ? 'active' : ''}`}
            onClick={() => onTimeframeChange(tf)}
          >
            {tf}
          </button>
        ))}
      </div>
    </div>
  );
};

/**
 * Key Metrics Grid
 */
const MetricsGrid = ({ data }) => {
  const metrics = [
    {
      title: 'Total Mentions',
      value: data.mention_volume.current.toLocaleString(),
      change: data.mention_volume.change_percentage,
      icon: '📊'
    },
    {
      title: 'Positive Sentiment',
      value: `${data.sentiment_distribution.positive.toFixed(1)}%`,
      change: null,
      icon: '😊'
    },
    {
      title: 'Negative Sentiment',
      value: `${data.sentiment_distribution.negative.toFixed(1)}%`,
      change: null,
      icon: '😟'
    },
    {
      title: 'Active Alerts',
      value: data.recent_alerts.length,
      change: null,
      icon: '🔔'
    }
  ];

  return (
    <div className="metrics-grid">
      {metrics.map((metric, index) => (
        <MetricCard key={index} {...metric} />
      ))}
    </div>
  );
};

/**
 * Individual Metric Card
 */
const MetricCard = ({ title, value, change, icon }) => (
  <div className="metric-card">
    <div className="metric-icon">{icon}</div>
    <div className="metric-content">
      <h3 className="metric-title">{title}</h3>
      <div className="metric-value">{value}</div>
      {change !== null && (
        <div className={`metric-change ${change >= 0 ? 'positive' : 'negative'}`}>
          {change >= 0 ? '↑' : '↓'} {Math.abs(change).toFixed(1)}%
        </div>
      )}
    </div>
  </div>
);

/**
 * Sentiment Trend Line Chart
 */
const SentimentTrendChart = ({ data }) => (
  <div className="chart-container">
    <h3 className="chart-title">Sentiment Trend</h3>
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="date" />
        <YAxis domain={[0, 100]} />
        <Tooltip />
        <Legend />
        <Line
          type="monotone"
          dataKey="score"
          stroke="#6366f1"
          strokeWidth={2}
          dot={{ r: 4 }}
          activeDot={{ r: 6 }}
        />
      </LineChart>
    </ResponsiveContainer>
  </div>
);

/**
 * Sentiment Distribution Pie Chart
 */
const SentimentDistributionChart = ({ data }) => {
  const chartData = [
    { name: 'Positive', value: data.positive, color: '#10b981' },
    { name: 'Neutral', value: data.neutral, color: '#6b7280' },
    { name: 'Negative', value: data.negative, color: '#ef4444' }
  ];

  return (
    <div className="chart-container">
      <h3 className="chart-title">Sentiment Distribution</h3>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(1)}%`}
            outerRadius={80}
            fill="#8884d8"
            dataKey="value"
          >
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Pie>
          <Tooltip />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
};

/**
 * Source Breakdown Bar Chart
 */
const SourceBreakdownChart = ({ data }) => {
  const chartData = Object.entries(data).map(([source, count]) => ({
    source: source.charAt(0).toUpperCase() + source.slice(1),
    mentions: count
  }));

  return (
    <div className="chart-container">
      <h3 className="chart-title">Mentions by Source</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="source" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="mentions" fill="#8b5cf6" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

/**
 * Mention Volume Comparison
 */
const MentionVolumeChart = ({ data }) => (
  <div className="chart-container">
    <h3 className="chart-title">Mention Volume</h3>
    <div className="volume-comparison">
      <div className="volume-bar-container">
        <div className="volume-label">Current Period</div>
        <div className="volume-bar" style={{ width: '100%', background: '#6366f1' }}>
          <span className="volume-value">{data.current.toLocaleString()}</span>
        </div>
      </div>
      <div className="volume-bar-container">
        <div className="volume-label">Previous Period</div>
        <div
          className="volume-bar"
          style={{ width: `${(data.previous / data.current) * 100}%`, background: '#94a3b8' }}
        >
          <span className="volume-value">{data.previous.toLocaleString()}</span>
        </div>
      </div>
      <div className="volume-change">
        <span className={data.change_percentage >= 0 ? 'positive' : 'negative'}>
          {data.change_percentage >= 0 ? '↑' : '↓'} {Math.abs(data.change_percentage).toFixed(1)}% change
        </span>
      </div>
    </div>
  </div>
);

/**
 * Trending Keywords Section
 */
const TrendingKeywords = ({ keywords }) => (
  <div className="trending-keywords">
    <h3>Trending Keywords</h3>
    <div className="keywords-grid">
      {keywords.map((keyword, index) => (
        <div key={index} className="keyword-tag" data-sentiment={keyword.sentiment}>
          <span className="keyword-text">{keyword.keyword}</span>
          <span className="keyword-count">{keyword.count}</span>
        </div>
      ))}
    </div>
  </div>
);

/**
 * Alerts Panel
 */
const AlertsPanel = ({ alerts }) => (
  <div className="alerts-panel">
    <h3>Recent Alerts</h3>
    {alerts.length === 0 ? (
      <div className="no-alerts">✅ No active alerts - all systems normal</div>
    ) : (
      <div className="alerts-list">
        {alerts.map((alert) => (
          <AlertCard key={alert.alert_id} alert={alert} />
        ))}
      </div>
    )}
  </div>
);

/**
 * Individual Alert Card
 */
const AlertCard = ({ alert }) => {
  const getLevelColor = (level) => {
    const colors = {
      info: '#3b82f6',
      warning: '#f59e0b',
      critical: '#ef4444',
      opportunity: '#10b981'
    };
    return colors[level] || '#6b7280';
  };

  return (
    <div className="alert-card" style={{ borderLeftColor: getLevelColor(alert.level) }}>
      <div className="alert-header">
        <span className="alert-level" style={{ background: getLevelColor(alert.level) }}>
          {alert.level.toUpperCase()}
        </span>
        <span className="alert-time">{new Date(alert.timestamp).toLocaleString()}</span>
      </div>
      <div className="alert-message">{alert.message}</div>
      {alert.recommendations && alert.recommendations.length > 0 && (
        <div className="alert-recommendations">
          <strong>Recommendations:</strong>
          <ul>
            {alert.recommendations.map((rec, index) => (
              <li key={index}>{rec}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

/**
 * Loading Spinner Component
 */
const LoadingSpinner = () => (
  <div className="loading-spinner">
    <div className="spinner"></div>
    <p>Loading dashboard data...</p>
  </div>
);

export default Dashboard;
