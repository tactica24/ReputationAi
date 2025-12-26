import React, { useState, useEffect } from 'react';

function EntitiesPage() {
  const [entities, setEntities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showAddModal, setShowAddModal] = useState(false);
  const [newEntity, setNewEntity] = useState({
    name: '',
    type: 'person',
    description: '',
    platforms: []
  });

  useEffect(() => {
    fetchEntities();
  }, []);

  const fetchEntities = async () => {
    try {
      setLoading(true);
      // Simulate API call - replace with actual endpoint
      const mockEntities = [
        {
          id: 1,
          name: 'John Doe',
          type: 'person',
          description: 'CEO & Founder',
          platforms: ['LinkedIn', 'Twitter', 'Instagram'],
          monitored: true,
          mentions: 234,
          sentiment: 85
        },
        {
          id: 2,
          name: 'Acme Corporation',
          type: 'company',
          description: 'Main company brand',
          platforms: ['LinkedIn', 'Twitter', 'Facebook', 'Google'],
          monitored: true,
          mentions: 1432,
          sentiment: 72
        }
      ];
      
      setTimeout(() => {
        setEntities(mockEntities);
        setLoading(false);
      }, 800);
    } catch (error) {
      console.error('Error fetching entities:', error);
      setLoading(false);
    }
  };

  const handleAddEntity = async (e) => {
    e.preventDefault();
    try {
      // Add entity logic - replace with actual API call
      const entity = {
        id: entities.length + 1,
        ...newEntity,
        monitored: true,
        mentions: 0,
        sentiment: 0
      };
      
      setEntities([...entities, entity]);
      setShowAddModal(false);
      setNewEntity({
        name: '',
        type: 'person',
        description: '',
        platforms: []
      });
    } catch (error) {
      console.error('Error adding entity:', error);
    }
  };

  const toggleMonitoring = (id) => {
    setEntities(entities.map(entity => 
      entity.id === id ? { ...entity, monitored: !entity.monitored } : entity
    ));
  };

  const deleteEntity = (id) => {
    if (window.confirm('Are you sure you want to delete this entity?')) {
      setEntities(entities.filter(entity => entity.id !== id));
    }
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
      <div className="mb-6 flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Monitored Entities</h1>
          <p className="text-gray-600 mt-1">Manage the people, brands, and organizations you're protecting</p>
        </div>
        <button
          onClick={() => setShowAddModal(true)}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition"
        >
          + Add Entity
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {entities.map(entity => (
          <div key={entity.id} className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
            <div className="flex justify-between items-start mb-4">
              <div className="flex items-center space-x-3">
                <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center text-2xl">
                  {entity.type === 'person' ? '👤' : '🏢'}
                </div>
                <div>
                  <h3 className="font-semibold text-lg text-gray-900">{entity.name}</h3>
                  <p className="text-sm text-gray-500 capitalize">{entity.type}</p>
                </div>
              </div>
              <div className="flex items-center space-x-2">
                <button
                  onClick={() => toggleMonitoring(entity.id)}
                  className={`w-10 h-6 rounded-full transition ${
                    entity.monitored ? 'bg-green-500' : 'bg-gray-300'
                  }`}
                >
                  <div className={`w-4 h-4 bg-white rounded-full transition transform ${
                    entity.monitored ? 'translate-x-5' : 'translate-x-1'
                  }`}></div>
                </button>
              </div>
            </div>

            <p className="text-gray-600 text-sm mb-4">{entity.description}</p>

            <div className="mb-4">
              <p className="text-xs text-gray-500 mb-2">Platforms</p>
              <div className="flex flex-wrap gap-2">
                {entity.platforms.map(platform => (
                  <span key={platform} className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">
                    {platform}
                  </span>
                ))}
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4 mb-4">
              <div>
                <p className="text-xs text-gray-500">Mentions</p>
                <p className="text-xl font-semibold text-gray-900">{entity.mentions}</p>
              </div>
              <div>
                <p className="text-xs text-gray-500">Sentiment</p>
                <p className={`text-xl font-semibold ${
                  entity.sentiment >= 70 ? 'text-green-600' : 
                  entity.sentiment >= 40 ? 'text-yellow-600' : 'text-red-600'
                }`}>
                  {entity.sentiment}%
                </p>
              </div>
            </div>

            <div className="flex space-x-2">
              <button className="flex-1 bg-blue-50 text-blue-600 py-2 rounded hover:bg-blue-100 transition text-sm">
                View Details
              </button>
              <button
                onClick={() => deleteEntity(entity.id)}
                className="px-4 bg-red-50 text-red-600 py-2 rounded hover:bg-red-100 transition text-sm"
              >
                Delete
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Add Entity Modal */}
      {showAddModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h2 className="text-2xl font-bold mb-4">Add New Entity</h2>
            <form onSubmit={handleAddEntity}>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">Name *</label>
                <input
                  type="text"
                  required
                  value={newEntity.name}
                  onChange={(e) => setNewEntity({ ...newEntity, name: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  placeholder="Person or organization name"
                />
              </div>

              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">Type *</label>
                <select
                  required
                  value={newEntity.type}
                  onChange={(e) => setNewEntity({ ...newEntity, type: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                >
                  <option value="person">Person</option>
                  <option value="company">Company</option>
                  <option value="brand">Brand</option>
                  <option value="product">Product</option>
                </select>
              </div>

              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">Description</label>
                <textarea
                  value={newEntity.description}
                  onChange={(e) => setNewEntity({ ...newEntity, description: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  rows="3"
                  placeholder="Brief description"
                ></textarea>
              </div>

              <div className="flex space-x-3">
                <button
                  type="button"
                  onClick={() => setShowAddModal(false)}
                  className="flex-1 bg-gray-200 text-gray-700 py-2 rounded-lg hover:bg-gray-300 transition"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="flex-1 bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition"
                >
                  Add Entity
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default EntitiesPage;
