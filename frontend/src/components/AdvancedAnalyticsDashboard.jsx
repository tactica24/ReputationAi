/**
 * Advanced Analytics Dashboard
 * Real-time data visualization with custom report builder
 */

import React, { useState, useEffect } from 'react';
import {
  BarChart, Bar, LineChart, Line, PieChart, Pie, Cell,
  AreaChart, Area, RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';
import { Download, Filter, Calendar, TrendingUp, AlertCircle } from 'lucide-react';

const COLORS = ['#6366f1', '#8b5cf6', '#10b981', '#f59e0b', '#ef4444'];

export default function AdvancedAnalyticsDashboard() {
  const [dateRange, setDateRange] = useState('7days');
  const [selectedEntities, setSelectedEntities] = useState([]);
  const [metrics, setMetrics] = useState({});
  const [isLoading, setIsLoading] = useState(false);

  // Sample data (would be fetched from API)
  const reputationTrendData = [
    { date: '12/19', score: 72, mentions: 45 },
    { date: '12/20', score: 74, mentions: 52 },
    { date: '12/21', score: 71, mentions: 38 },
    { date: '12/22', score: 76, mentions: 61 },
    { date: '12/23', score: 78, mentions: 58 },
    { date: '12/24', score: 75, mentions: 49 },
    { date: '12/25', score: 79, mentions: 67 },
  ];

  const sentimentData = [
    { name: 'Positive', value: 65, count: 234 },
    { name: 'Neutral', value: 25, count: 89 },
    { name: 'Negative', value: 10, count: 36 },
  ];

  const sourceDistribution = [
    { source: 'Twitter', mentions: 145, engagement: 23400 },
    { source: 'Reddit', mentions: 89, engagement: 15600 },
    { source: 'News', mentions: 67, engagement: 45200 },
    { source: 'Blogs', mentions: 54, engagement: 8900 },
    { source: 'Forums', mentions: 38, engagement: 6700 },
  ];

  const topicsData = [
    { topic: 'Product', positive: 78, negative: 12, neutral: 10 },
    { topic: 'Service', positive: 65, negative: 20, neutral: 15 },
    { topic: 'Price', positive: 45, negative: 35, neutral: 20 },
    { topic: 'Support', positive: 82, negative: 8, neutral: 10 },
    { topic: 'Quality', positive: 88, negative: 5, neutral: 7 },
  ];

  const geographicData = [
    { region: 'North America', mentions: 145, sentiment: 78 },
    { region: 'Europe', mentions: 89, sentiment: 72 },
    { region: 'Asia Pacific', mentions: 67, sentiment: 81 },
    { region: 'Latin America', mentions: 34, sentiment: 69 },
    { region: 'Middle East', mentions: 24, sentiment: 75 },
  ];

  const exportReport = (format) => {
    // Would generate and download report in specified format
    console.log(`Exporting report in ${format} format`);
  };

  return (
    <div className="analytics-dashboard">
      {/* Header */}
      <div className="dashboard-header">
        <div>
          <h1>Advanced Analytics</h1>
          <p className="subtitle">Comprehensive insights and predictive analytics</p>
        </div>
        
        <div className="header-actions">
          <select 
            value={dateRange} 
            onChange={(e) => setDateRange(e.target.value)}
            className="date-select"
          >
            <option value="7days">Last 7 Days</option>
            <option value="30days">Last 30 Days</option>
            <option value="90days">Last 90 Days</option>
            <option value="custom">Custom Range</option>
          </select>
          
          <button className="btn-secondary">
            <Filter size={18} />
            Filters
          </button>
          
          <button className="btn-primary" onClick={() => exportReport('pdf')}>
            <Download size={18} />
            Export Report
          </button>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="metrics-grid">
        <div className="metric-card">
          <div className="metric-icon" style={{background: '#e0e7ff'}}>
            <TrendingUp color="#6366f1" size={24} />
          </div>
          <div className="metric-content">
            <h3>Average Reputation Score</h3>
            <p className="metric-value">75.4</p>
            <p className="metric-change positive">+5.2% from last period</p>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon" style={{background: '#d1fae5'}}>
            <AlertCircle color="#10b981" size={24} />
          </div>
          <div className="metric-content">
            <h3>Total Mentions</h3>
            <p className="metric-value">359</p>
            <p className="metric-change positive">+12.3% from last period</p>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon" style={{background: '#fef3c7'}}>
            <Calendar color="#f59e0b" size={24} />
          </div>
          <div className="metric-content">
            <h3>Engagement Rate</h3>
            <p className="metric-value">8.7%</p>
            <p className="metric-change negative">-2.1% from last period</p>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon" style={{background: '#fce7f3'}}>
            <TrendingUp color="#8b5cf6" size={24} />
          </div>
          <div className="metric-content">
            <h3>Sentiment Score</h3>
            <p className="metric-value">+0.72</p>
            <p className="metric-change positive">+8.5% from last period</p>
          </div>
        </div>
      </div>

      {/* Charts Grid */}
      <div className="charts-grid">
        {/* Reputation Trend */}
        <div className="chart-card full-width">
          <div className="chart-header">
            <h2>Reputation Score Trend</h2>
            <span className="chart-subtitle">7-day moving average with mention volume</span>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={reputationTrendData}>
              <defs>
                <linearGradient id="colorScore" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#6366f1" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="#6366f1" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis dataKey="date" stroke="#64748b" />
              <YAxis yAxisId="left" stroke="#64748b" />
              <YAxis yAxisId="right" orientation="right" stroke="#8b5cf6" />
              <Tooltip />
              <Legend />
              <Area 
                yAxisId="left"
                type="monotone" 
                dataKey="score" 
                stroke="#6366f1" 
                fill="url(#colorScore)"
                name="Reputation Score"
              />
              <Line 
                yAxisId="right"
                type="monotone" 
                dataKey="mentions" 
                stroke="#8b5cf6" 
                name="Mention Count"
                strokeWidth={2}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Sentiment Distribution */}
        <div className="chart-card">
          <div className="chart-header">
            <h2>Sentiment Distribution</h2>
            <span className="chart-subtitle">Overall sentiment breakdown</span>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={sentimentData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({name, percent}) => `${name}: ${(percent * 100).toFixed(0)}%`}
                outerRadius={100}
                fill="#8884d8"
                dataKey="value"
              >
                {sentimentData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Source Distribution */}
        <div className="chart-card">
          <div className="chart-header">
            <h2>Source Distribution</h2>
            <span className="chart-subtitle">Mentions by platform</span>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={sourceDistribution}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis dataKey="source" stroke="#64748b" />
              <YAxis stroke="#64748b" />
              <Tooltip />
              <Legend />
              <Bar dataKey="mentions" fill="#6366f1" name="Mentions" />
              <Bar dataKey="engagement" fill="#8b5cf6" name="Engagement" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Topic Analysis */}
        <div className="chart-card">
          <div className="chart-header">
            <h2>Topic Analysis</h2>
            <span className="chart-subtitle">Sentiment by topic</span>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <RadarChart data={topicsData}>
              <PolarGrid stroke="#e2e8f0" />
              <PolarAngleAxis dataKey="topic" stroke="#64748b" />
              <PolarRadiusAxis stroke="#64748b" />
              <Radar name="Positive" dataKey="positive" stroke="#10b981" fill="#10b981" fillOpacity={0.3} />
              <Radar name="Negative" dataKey="negative" stroke="#ef4444" fill="#ef4444" fillOpacity={0.3} />
              <Legend />
            </RadarChart>
          </ResponsiveContainer>
        </div>

        {/* Geographic Distribution */}
        <div className="chart-card">
          <div className="chart-header">
            <h2>Geographic Distribution</h2>
            <span className="chart-subtitle">Mentions and sentiment by region</span>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={geographicData} layout="horizontal">
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis type="number" stroke="#64748b" />
              <YAxis type="category" dataKey="region" stroke="#64748b" width={100} />
              <Tooltip />
              <Legend />
              <Bar dataKey="mentions" fill="#6366f1" name="Mentions" />
              <Bar dataKey="sentiment" fill="#10b981" name="Sentiment Score" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Predictive Insights */}
      <div className="insights-section">
        <h2>Predictive Insights</h2>
        
        <div className="insights-grid">
          <div className="insight-card">
            <div className="insight-header">
              <h3>7-Day Forecast</h3>
              <span className="confidence-badge">85% Confidence</span>
            </div>
            <p className="insight-value">Predicted Score: 81.2</p>
            <p className="insight-trend positive">Expected improvement of +2.8 points</p>
            <ul className="insight-factors">
              <li>Positive sentiment trend continuing</li>
              <li>Increasing mention volume</li>
              <li>High engagement on recent content</li>
            </ul>
          </div>

          <div className="insight-card">
            <div className="insight-header">
              <h3>Crisis Assessment</h3>
              <span className="confidence-badge low">Low Risk</span>
            </div>
            <p className="insight-value">Risk Score: 15/100</p>
            <p className="insight-trend stable">No significant threats detected</p>
            <ul className="insight-factors">
              <li>Normal mention patterns</li>
              <li>Stable sentiment distribution</li>
              <li>No viral negative content</li>
            </ul>
          </div>

          <div className="insight-card">
            <div className="insight-header">
              <h3>Emerging Trends</h3>
              <span className="confidence-badge">3 Detected</span>
            </div>
            <div className="trending-topics">
              <div className="trend-item">
                <span className="trend-name">Product launch</span>
                <span className="trend-velocity">+245% velocity</span>
              </div>
              <div className="trend-item">
                <span className="trend-name">Customer service</span>
                <span className="trend-velocity">+128% velocity</span>
              </div>
              <div className="trend-item">
                <span className="trend-name">Innovation</span>
                <span className="trend-velocity">+96% velocity</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <style jsx>{`
        .analytics-dashboard {
          padding: 24px;
          background: #f8fafc;
          min-height: 100vh;
        }

        .dashboard-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 24px;
        }

        .dashboard-header h1 {
          font-size: 32px;
          font-weight: 700;
          color: #1e293b;
          margin: 0;
        }

        .subtitle {
          color: #64748b;
          margin-top: 4px;
        }

        .header-actions {
          display: flex;
          gap: 12px;
        }

        .date-select {
          padding: 8px 16px;
          border: 1px solid #e2e8f0;
          border-radius: 8px;
          font-size: 14px;
          cursor: pointer;
        }

        .btn-secondary, .btn-primary {
          display: flex;
          align-items: center;
          gap: 8px;
          padding: 8px 16px;
          border: none;
          border-radius: 8px;
          font-size: 14px;
          font-weight: 500;
          cursor: pointer;
          transition: all 0.2s;
        }

        .btn-secondary {
          background: white;
          color: #64748b;
          border: 1px solid #e2e8f0;
        }

        .btn-primary {
          background: #6366f1;
          color: white;
        }

        .btn-primary:hover {
          background: #4f46e5;
        }

        .metrics-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
          gap: 20px;
          margin-bottom: 24px;
        }

        .metric-card {
          background: white;
          border-radius: 12px;
          padding: 20px;
          display: flex;
          gap: 16px;
          box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }

        .metric-icon {
          width: 48px;
          height: 48px;
          border-radius: 10px;
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .metric-content h3 {
          font-size: 14px;
          color: #64748b;
          margin: 0 0 8px 0;
        }

        .metric-value {
          font-size: 32px;
          font-weight: 700;
          color: #1e293b;
          margin: 0 0 4px 0;
        }

        .metric-change {
          font-size: 13px;
          margin: 0;
        }

        .metric-change.positive {
          color: #10b981;
        }

        .metric-change.negative {
          color: #ef4444;
        }

        .charts-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
          gap: 20px;
          margin-bottom: 24px;
        }

        .chart-card {
          background: white;
          border-radius: 12px;
          padding: 24px;
          box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }

        .chart-card.full-width {
          grid-column: 1 / -1;
        }

        .chart-header {
          margin-bottom: 20px;
        }

        .chart-header h2 {
          font-size: 18px;
          font-weight: 600;
          color: #1e293b;
          margin: 0 0 4px 0;
        }

        .chart-subtitle {
          font-size: 13px;
          color: #64748b;
        }

        .insights-section {
          margin-top: 24px;
        }

        .insights-section h2 {
          font-size: 24px;
          font-weight: 600;
          color: #1e293b;
          margin-bottom: 16px;
        }

        .insights-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
          gap: 20px;
        }

        .insight-card {
          background: white;
          border-radius: 12px;
          padding: 24px;
          box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }

        .insight-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 16px;
        }

        .insight-header h3 {
          font-size: 16px;
          font-weight: 600;
          color: #1e293b;
          margin: 0;
        }

        .confidence-badge {
          padding: 4px 12px;
          border-radius: 12px;
          font-size: 12px;
          font-weight: 500;
          background: #e0e7ff;
          color: #6366f1;
        }

        .confidence-badge.low {
          background: #d1fae5;
          color: #10b981;
        }

        .insight-value {
          font-size: 28px;
          font-weight: 700;
          color: #1e293b;
          margin: 0 0 8px 0;
        }

        .insight-trend {
          font-size: 14px;
          margin: 0 0 16px 0;
        }

        .insight-trend.positive {
          color: #10b981;
        }

        .insight-trend.stable {
          color: #64748b;
        }

        .insight-factors {
          list-style: none;
          padding: 0;
          margin: 0;
        }

        .insight-factors li {
          padding: 8px 0;
          color: #64748b;
          font-size: 14px;
          border-bottom: 1px solid #f1f5f9;
        }

        .insight-factors li:last-child {
          border-bottom: none;
        }

        .trending-topics {
          display: flex;
          flex-direction: column;
          gap: 12px;
        }

        .trend-item {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 12px;
          background: #f8fafc;
          border-radius: 8px;
        }

        .trend-name {
          font-size: 14px;
          color: #1e293b;
          font-weight: 500;
        }

        .trend-velocity {
          font-size: 13px;
          color: #10b981;
          font-weight: 600;
        }
      `}</style>
    </div>
  );
}
