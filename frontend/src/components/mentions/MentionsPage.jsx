import React, { useState, useEffect } from 'react';

function MentionsPage() {
  const [mentions, setMentions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all'); // all, positive, neutral, negative
  const [sortBy, setSortBy] = useState('recent'); // recent, sentiment, relevance

  useEffect(() => {
    fetchMentions();
  }, [filter, sortBy]);

  const fetchMentions = async () => {
    try {
      setLoading(true);
      // Simulate API call - replace with actual endpoint
      const mockMentions = [
        {
          id: 1,
          entity: 'John Doe',
          platform: 'Twitter',
          author: '@techreporter',
          content: 'John Doe\'s leadership has transformed the industry. Incredible vision!',
          url: 'https://twitter.com/example/123',
          sentiment: 92,
          timestamp: new Date(Date.now() - 3600000).toISOString(),
          reach: 12500,
          verified: true
        },
        {
          id: 2,
          entity: 'Acme Corporation',
          platform: 'LinkedIn',
          author: 'Sarah Johnson',
          content: 'Had a mixed experience with Acme Corp\'s latest product release.',
          url: 'https://linkedin.com/posts/example',
          sentiment: 45,
          timestamp: new Date(Date.now() - 7200000).toISOString(),
          reach: 3200,
          verified: false
        },
        {
          id: 3,
          entity: 'John Doe',
          platform: 'Reddit',
          author: 'u/industry_insider',
          content: 'Disappointed by the recent decision from John Doe. Expected better.',
          url: 'https://reddit.com/r/example',
          sentiment: 25,
          timestamp: new Date(Date.now() - 10800000).toISOString(),
          reach: 8900,
          verified: false
        },
        {
          id: 4,
          entity: 'Acme Corporation',
          platform: 'Google Reviews',
          author: 'Mike Thompson',
          content: 'Outstanding service! Acme Corporation exceeded all expectations.',
          url: 'https://google.com/reviews/example',
          sentiment: 95,
          timestamp: new Date(Date.now() - 14400000).toISOString(),
          reach: 450,
          verified: true
        }
      ];

      setTimeout(() => {
        let filtered = mockMentions;
        
        if (filter === 'positive') filtered = mockMentions.filter(m => m.sentiment >= 70);
        else if (filter === 'neutral') filtered = mockMentions.filter(m => m.sentiment >= 40 && m.sentiment < 70);
        else if (filter === 'negative') filtered = mockMentions.filter(m => m.sentiment < 40);

        setMentions(filtered);
        setLoading(false);
      }, 600);
    } catch (error) {
      console.error('Error fetching mentions:', error);
      setLoading(false);
    }
  };

  const getSentimentColor = (sentiment) => {
    if (sentiment >= 70) return 'text-green-600 bg-green-50';
    if (sentiment >= 40) return 'text-yellow-600 bg-yellow-50';
    return 'text-red-600 bg-red-50';
  };

  const getSentimentLabel = (sentiment) => {
    if (sentiment >= 70) return 'Positive';
    if (sentiment >= 40) return 'Neutral';
    return 'Negative';
  };

  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diff = now - date;
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);

    if (hours < 1) return 'Just now';
    if (hours < 24) return `${hours}h ago`;
    if (days < 7) return `${days}d ago`;
    return date.toLocaleDateString();
  };

  const getPlatformIcon = (platform) => {
    const icons = {
      'Twitter': '🐦',
      'LinkedIn': '💼',
      'Reddit': '🔴',
      'Google Reviews': '⭐',
      'Facebook': '📘',
      'Instagram': '📷'
    };
    return icons[platform] || '🌐';
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Mentions</h1>
        <p className="text-gray-600 mt-1">Track what people are saying about your entities</p>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-lg shadow-sm p-4 mb-6 border border-gray-200">
        <div className="flex flex-wrap gap-4 items-center justify-between">
          <div className="flex space-x-2">
            <button
              onClick={() => setFilter('all')}
              className={`px-4 py-2 rounded-lg transition ${
                filter === 'all' 
                  ? 'bg-blue-600 text-white' 
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              All
            </button>
            <button
              onClick={() => setFilter('positive')}
              className={`px-4 py-2 rounded-lg transition ${
                filter === 'positive' 
                  ? 'bg-green-600 text-white' 
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              Positive
            </button>
            <button
              onClick={() => setFilter('neutral')}
              className={`px-4 py-2 rounded-lg transition ${
                filter === 'neutral' 
                  ? 'bg-yellow-600 text-white' 
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              Neutral
            </button>
            <button
              onClick={() => setFilter('negative')}
              className={`px-4 py-2 rounded-lg transition ${
                filter === 'negative' 
                  ? 'bg-red-600 text-white' 
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              Negative
            </button>
          </div>

          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          >
            <option value="recent">Most Recent</option>
            <option value="sentiment">By Sentiment</option>
            <option value="relevance">By Relevance</option>
          </select>
        </div>
      </div>

      {/* Mentions List */}
      <div className="space-y-4">
        {mentions.length === 0 ? (
          <div className="bg-white rounded-lg shadow-sm p-12 text-center border border-gray-200">
            <p className="text-gray-500 text-lg">No mentions found matching your filters</p>
          </div>
        ) : (
          mentions.map(mention => (
            <div key={mention.id} className="bg-white rounded-lg shadow-sm p-6 border border-gray-200 hover:shadow-md transition">
              <div className="flex justify-between items-start mb-4">
                <div className="flex items-start space-x-4 flex-1">
                  <div className="text-3xl">{getPlatformIcon(mention.platform)}</div>
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-2">
                      <h3 className="font-semibold text-gray-900">{mention.author}</h3>
                      {mention.verified && (
                        <span className="text-blue-500" title="Verified">✓</span>
                      )}
                      <span className="text-gray-400">•</span>
                      <span className="text-sm text-gray-500">{mention.platform}</span>
                      <span className="text-gray-400">•</span>
                      <span className="text-sm text-gray-500">{formatTimestamp(mention.timestamp)}</span>
                    </div>
                    <p className="text-gray-700 mb-3">{mention.content}</p>
                    <div className="flex items-center space-x-4 text-sm">
                      <span className="text-gray-500">Entity: <span className="text-gray-900 font-medium">{mention.entity}</span></span>
                      <span className="text-gray-500">Reach: <span className="text-gray-900 font-medium">{mention.reach.toLocaleString()}</span></span>
                    </div>
                  </div>
                </div>
                <div className="flex flex-col items-end space-y-2">
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${getSentimentColor(mention.sentiment)}`}>
                    {getSentimentLabel(mention.sentiment)} ({mention.sentiment}%)
                  </span>
                </div>
              </div>
              <div className="flex space-x-2 pt-4 border-t border-gray-100">
                <a
                  href={mention.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="px-4 py-2 bg-blue-50 text-blue-600 rounded hover:bg-blue-100 transition text-sm"
                >
                  View Original
                </a>
                <button className="px-4 py-2 bg-gray-50 text-gray-700 rounded hover:bg-gray-100 transition text-sm">
                  Create Alert
                </button>
                <button className="px-4 py-2 bg-gray-50 text-gray-700 rounded hover:bg-gray-100 transition text-sm">
                  Export
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default MentionsPage;
