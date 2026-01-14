import React from 'react';
import { useNavigate } from 'react-router-dom';

const ProtectionPage = () => {
  const navigate = useNavigate();

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#0a0a0f', color: '#fff', fontFamily: 'Inter, sans-serif', padding: '6rem 2rem 2rem' }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        <button onClick={() => navigate('/')} style={{ background: '#6366f1', color: '#fff', border: 'none', padding: '0.5rem 1rem', borderRadius: '0.5rem', marginBottom: '2rem', cursor: 'pointer' }}>
          ← Back to Home
        </button>
        
        <h1>How Protection Works</h1>
        <p>Real-time monitoring and threat detection across the entire internet.</p>
        
        <section id="how-it-works" style={{ marginTop: '2rem' }}>
          <h2>The VeriSignal Process</h2>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '2rem', marginTop: '2rem' }}>
            {['Monitor', 'Analyze', 'Protect', 'Report'].map((feature, i) => (
              <div key={i} style={{ background: '#12121a', padding: '2rem', borderRadius: '12px', border: '1px solid rgba(99, 102, 241, 0.1)' }}>
                <h3>{feature}</h3>
                <p style={{ color: '#a1a1aa' }}>24/7 AI-powered monitoring and protection</p>
              </div>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
};

export default ProtectionPage;
