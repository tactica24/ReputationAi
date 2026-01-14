import React from 'react';
import { useNavigate } from 'react-router-dom';

const EnterprisePage = () => {
  const navigate = useNavigate();

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#0a0a0f', color: '#fff', fontFamily: 'Inter, sans-serif', padding: '6rem 2rem 2rem' }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        <button onClick={() => navigate('/')} style={{ background: '#6366f1', color: '#fff', border: 'none', padding: '0.5rem 1rem', borderRadius: '0.5rem', marginBottom: '2rem', cursor: 'pointer' }}>
          ← Back to Home
        </button>
        
        <h1>Enterprise Solutions</h1>
        <p>Unlimited digital reputation and identity protection, dedicated support, and custom solutions for organizations that demand the best.</p>
        
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '2rem', marginTop: '2rem' }}>
          <div style={{ background: '#12121a', padding: '2rem', borderRadius: '12px', border: '1px solid rgba(99, 102, 241, 0.1)' }}>
            <h3>🎯 Unlimited Monitoring</h3>
            <p style={{ color: '#a1a1aa' }}>Monitor unlimited entities and keywords</p>
          </div>
          <div style={{ background: '#12121a', padding: '2rem', borderRadius: '12px', border: '1px solid rgba(99, 102, 241, 0.1)' }}>
            <h3>👥 Dedicated Support</h3>
            <p style={{ color: '#a1a1aa' }}>24/7 premium support team</p>
          </div>
          <div style={{ background: '#12121a', padding: '2rem', borderRadius: '12px', border: '1px solid rgba(99, 102, 241, 0.1)' }}>
            <h3>⚙️ Custom Integration</h3>
            <p style={{ color: '#a1a1aa' }}>API access and custom workflows</p>
          </div>
        </div>
        
        <button onClick={() => navigate('/subscribe')} style={{ background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)', color: '#fff', border: 'none', padding: '1rem 2rem', borderRadius: '0.5rem', marginTop: '2rem', cursor: 'pointer', fontSize: '1rem', fontWeight: '600' }}>
          Contact Us for Enterprise Protection
        </button>
      </div>
    </div>
  );
};

export default EnterprisePage;
