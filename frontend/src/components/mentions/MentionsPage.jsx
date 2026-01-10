import React, { useState, useEffect } from 'react';
function MentionsPage() {
  const [mentions, setMentions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchMentions();
  }, []);

  const fetchMentions = async () => {
    try {
      setLoading(true);
      // Simulate API call - replace with actual endpoint
      const mockMentions = [
        {
          id: 1,
          platform: 'Twitter',
          content: "Your name was mentioned in a tweet.",
          url: 'https://twitter.com/example/123',
          timestamp: new Date(Date.now() - 3600000).toISOString(),
        },
        {
          id: 2,
          platform: 'LinkedIn',
          content: "Mentioned in a LinkedIn post.",
          url: 'https://linkedin.com/posts/example',
          timestamp: new Date(Date.now() - 7200000).toISOString(),
        },
        {
          id: 3,
          platform: 'Reddit',
          content: "Your name appeared in a Reddit discussion.",
          url: 'https://reddit.com/r/example',
          timestamp: new Date(Date.now() - 10800000).toISOString(),
        },
        {
          id: 4,
          platform: 'Google Reviews',
          content: "Mentioned in a Google review.",
          url: 'https://google.com/reviews/example',
          timestamp: new Date(Date.now() - 14400000).toISOString(),
        }
      ];
      setTimeout(() => {
        setMentions(mockMentions);
        setLoading(false);
      }, 600);
    } catch (error) {
      setLoading(false);
    }
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

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Mentions</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {mentions.map(mention => (
          <div key={mention.id} className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
            <div className="font-semibold text-lg mb-2">{mention.platform}</div>
            <div className="text-gray-800 mb-2 line-clamp-2">{mention.content}</div>
            <div className="flex justify-between items-center text-xs text-gray-500">
              <span>{formatTimestamp(mention.timestamp)}</span>
              <a href={mention.url} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">View Source</a>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-6">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-4">
          <div className="flex space-x-2">
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
