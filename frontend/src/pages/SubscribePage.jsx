import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const SubscribePage = () => {
  const navigate = useNavigate();
  const [selected, setSelected] = useState('pro');

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#0a0a0f', color: '#fff', fontFamily: 'Inter, sans-serif', padding: '6rem 2rem 2rem' }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        <button onClick={() => navigate('/')} style={{ background: '#6366f1', color: '#fff', border: 'none', padding: '0.5rem 1rem', borderRadius: '0.5rem', marginBottom: '2rem', cursor: 'pointer' }}>
          ← Back to Home
        </button>
        
        <h1 style={{ textAlign: 'center', marginBottom: '1rem' }}>Choose Your Plan</h1>
        <p style={{ textAlign: 'center', color: '#a1a1aa', marginBottom: '3rem' }}>Select the perfect plan for your reputation protection needs</p>
        
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '2rem', marginTop: '2rem' }}>
          {[
            { id: 'starter', name: 'Starter', price: '$99', features: ['Up to 5 entities', 'Basic monitoring', 'Email alerts', 'Monthly reports'] },
            { id: 'pro', name: 'Professional', price: '$299', features: ['Up to 25 entities', 'Advanced monitoring', 'Real-time alerts', 'Weekly reports', 'API access'], featured: true },
            { id: 'enterprise', name: 'Enterprise', price: 'Custom', features: ['Unlimited entities', 'Premium monitoring', 'Instant alerts', 'Custom reports', 'Dedicated support'] }
          ].map((plan) => (
            <div 
              key={plan.id} 
              onClick={() => setSelected(plan.id)}
              style={{ 
                background: '#12121a', 
                padding: '2rem', 
                borderRadius: '12px', 
                border: `2px solid ${selected === plan.id ? '#6366f1' : 'rgba(99, 102, 241, 0.1)'}`,
                cursor: 'pointer',
                transition: 'all 0.2s',
                transform: plan.featured ? 'scale(1.05)' : 'scale(1)',
                position: 'relative'
              }}
            >
              {plan.featured && <span style={{ position: 'absolute', top: '1rem', right: '1rem', background: '#6366f1', padding: '0.25rem 0.75rem', borderRadius: '9999px', fontSize: '0.75rem', fontWeight: '600' }}>POPULAR</span>}
              <h3>{plan.name}</h3>
              <p style={{ fontSize: '2rem', fontWeight: '700', color: '#6366f1', margin: '1rem 0' }}>{plan.price}</p>
              <ul style={{ listStyle: 'none', color: '#a1a1aa', marginBottom: '1.5rem' }}>
                {plan.features.map((feature, i) => (
                  <li key={i} style={{ marginBottom: '0.5rem' }}>✓ {feature}</li>
                ))}
              </ul>
              <button style={{ width: '100%', background: '#6366f1', color: '#fff', border: 'none', padding: '0.75rem', borderRadius: '0.5rem', cursor: 'pointer', fontWeight: '600' }}>
                Choose Plan
              </button>
            </div>
          ))}
        </div>

        <div style={{ marginTop: '4rem', padding: '2rem', background: '#12121a', borderRadius: '12px', border: '1px solid rgba(99, 102, 241, 0.1)' }}>
          <h3 style={{ marginBottom: '1rem' }}>All Plans Include:</h3>
          <ul style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '1rem', listStyle: 'none', color: '#a1a1aa' }}>
            {['24/7 AI Monitoring', '100M+ Sources', 'Instant Alerts', 'Sentiment Analysis', 'Threat Detection', 'Monthly Reports'].map((feature, i) => (
              <li key={i} style={{ marginBottom: '0.5rem' }}>✓ {feature}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default SubscribePage;
