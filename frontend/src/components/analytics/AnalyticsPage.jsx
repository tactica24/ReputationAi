import React, { useState } from 'react';
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
  Filler
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
  Legend,
  Filler
);

function AnalyticsPage() {
  const [timeRange, setTimeRange] = useState('7d'); // 7d, 30d, 90d, 1y

  // Sentiment Trend Data
  const sentimentTrendData = {
    labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    datasets: [
      {
        label: 'Sentiment Score',
        data: [72, 75, 68, 78, 82, 79, 85],
        borderColor: 'rgb(59, 130, 246)',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        fill: true,
        tension: 0.4
      }
    ]
  };

  // Mention Volume Data
  const mentionVolumeData = {
    labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    datasets: [
      {
        label: 'Positive',
        data: [45, 52, 48, 65, 72, 68, 78],
        backgroundColor: 'rgb(34, 197, 94)'
      },
      {
        label: 'Neutral',
        data: [28, 32, 35, 28, 25, 30, 32],
        backgroundColor: 'rgb(234, 179, 8)'
      },
      {
        label: 'Negative',
        data: [12, 8, 15, 10, 8, 12, 6],
        backgroundColor: 'rgb(239, 68, 68)'
      }
    ]
  };

  // Platform Distribution
  const platformData = {
    labels: ['Twitter', 'LinkedIn', 'Reddit', 'Google', 'Facebook', 'Other'],
    datasets: [
      {
        data: [35, 25, 15, 12, 8, 5],
        backgroundColor: [
          'rgb(59, 130, 246)',
          'rgb(14, 165, 233)',
          'rgb(239, 68, 68)',
          'rgb(234, 179, 8)',
          'rgb(34, 197, 94)',
          'rgb(156, 163, 175)'
        ]
      }
    ]
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom'
      }
    },
    scales: {
      y: {
        beginAtZero: true
      }
    }
  };

  const pieOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom'
      }
    }
  };

  return (
    <div className="p-6">
      <div className="mb-6 flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Analytics</h1>
          <p className="text-gray-600 mt-1">Comprehensive reputation insights and trends</p>
        </div>
        <select
          value={timeRange}
          onChange={(e) => setTimeRange(e.target.value)}
          className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
        >
          <option value="7d">Last 7 Days</option>
          <option value="30d">Last 30 Days</option>
          <option value="90d">Last 90 Days</option>
          <option value="1y">Last Year</option>
        </select>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
        <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 mb-1">Total Mentions</p>
              <p className="text-3xl font-bold text-gray-900">1,247</p>
              <p className="text-sm text-green-600 mt-1">↑ 12.5% from last week</p>
            </div>
            <div className="text-4xl">📊</div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 mb-1">Avg. Sentiment</p>
              <p className="text-3xl font-bold text-green-600">78%</p>
              <p className="text-sm text-green-600 mt-1">↑ 5.2% from last week</p>
            </div>
            <div className="text-4xl">😊</div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 mb-1">Total Reach</p>
              <p className="text-3xl font-bold text-gray-900">2.4M</p>
              <p className="text-sm text-green-600 mt-1">↑ 18.3% from last week</p>
            </div>
            <div className="text-4xl">🌍</div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 mb-1">Active Alerts</p>
              <p className="text-3xl font-bold text-red-600">3</p>
              <p className="text-sm text-gray-600 mt-1">2 critical, 1 high</p>
            </div>
            <div className="text-4xl">🚨</div>
          </div>
        </div>
      </div>

      {/* Charts Row 1 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Sentiment Trend</h2>
          <div className="h-64">
            <Line data={sentimentTrendData} options={chartOptions} />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Mention Volume by Sentiment</h2>
          <div className="h-64">
            <Bar data={mentionVolumeData} options={chartOptions} />
          </div>
        </div>
      </div>

      {/* Charts Row 2 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Platform Distribution</h2>
          <div className="h-64">
            <Pie data={platformData} options={pieOptions} />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Top Keywords</h2>
          <div className="space-y-3">
            {[
              { keyword: 'innovation', count: 156, sentiment: 92 },
              { keyword: 'leadership', count: 134, sentiment: 88 },
              { keyword: 'product', count: 98, sentiment: 75 },
              { keyword: 'service', count: 87, sentiment: 82 },
              { keyword: 'quality', count: 76, sentiment: 79 }
            ].map((item, index) => (
              <div key={index} className="flex items-center justify-between">
                <div className="flex-1">
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-medium text-gray-900">{item.keyword}</span>
                    <span className="text-sm text-gray-500">{item.count} mentions</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className={`h-2 rounded-full ${
                        item.sentiment >= 70 ? 'bg-green-500' : 
                        item.sentiment >= 40 ? 'bg-yellow-500' : 'bg-red-500'
                      }`}
                      style={{ width: `${item.sentiment}%` }}
                    ></div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Top Influencers */}
      <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Top Influencers</h2>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200">
                <th className="text-left py-3 px-4 text-sm font-medium text-gray-700">Influencer</th>
                <th className="text-left py-3 px-4 text-sm font-medium text-gray-700">Platform</th>
                <th className="text-left py-3 px-4 text-sm font-medium text-gray-700">Mentions</th>
                <th className="text-left py-3 px-4 text-sm font-medium text-gray-700">Reach</th>
                <th className="text-left py-3 px-4 text-sm font-medium text-gray-700">Sentiment</th>
              </tr>
            </thead>
            <tbody>
              {[
                { name: '@techreporter', platform: 'Twitter', mentions: 12, reach: '125K', sentiment: 92 },
                { name: 'Sarah Johnson', platform: 'LinkedIn', mentions: 8, reach: '45K', sentiment: 85 },
                { name: 'u/industry_insider', platform: 'Reddit', mentions: 15, reach: '89K', sentiment: 68 },
                { name: 'Mike Thompson', platform: 'Google', mentions: 6, reach: '12K', sentiment: 95 },
                { name: '@business_news', platform: 'Twitter', mentions: 10, reach: '230K', sentiment: 78 }
              ].map((influencer, index) => (
                <tr key={index} className="border-b border-gray-100 hover:bg-gray-50">
                  <td className="py-3 px-4 font-medium text-gray-900">{influencer.name}</td>
                  <td className="py-3 px-4 text-gray-700">{influencer.platform}</td>
                  <td className="py-3 px-4 text-gray-700">{influencer.mentions}</td>
                  <td className="py-3 px-4 text-gray-700">{influencer.reach}</td>
                  <td className="py-3 px-4">
                    <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                      influencer.sentiment >= 70 ? 'bg-green-100 text-green-800' : 
                      influencer.sentiment >= 40 ? 'bg-yellow-100 text-yellow-800' : 'bg-red-100 text-red-800'
                    }`}>
                      {influencer.sentiment}%
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default AnalyticsPage;
