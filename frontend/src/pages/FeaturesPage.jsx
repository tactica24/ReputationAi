import React from 'react';
import { useNavigate } from 'react-router-dom';

const FeaturesPage = () => {
  const navigate = useNavigate();

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#0a0a0f', color: '#fff', fontFamily: 'Inter, sans-serif', padding: '6rem 2rem 2rem' }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        <button onClick={() => navigate('/')} style={{ background: '#6366f1', color: '#fff', border: 'none', padding: '0.5rem 1rem', borderRadius: '0.5rem', marginBottom: '2rem', cursor: 'pointer' }}>
          ← Back to Home
        </button>
        <h1>Features</h1>
        <p>Discover the advanced features that set VeriSignal apart in digital reputation and identity protection.</p>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '2rem', marginTop: '2rem' }}>
          <div style={{ background: '#12121a', padding: '2rem', borderRadius: '12px', border: '1px solid rgba(99, 102, 241, 0.1)' }}>
            <h3>🌐 24/7 Monitoring</h3>
            <p style={{ color: '#a1a1aa' }}>Continuous scanning of 100M+ sources for threats and mentions.</p>
          </div>
          <div style={{ background: '#12121a', padding: '2rem', borderRadius: '12px', border: '1px solid rgba(99, 102, 241, 0.1)' }}>
            <h3>⚡ Instant Alerts</h3>
            <p style={{ color: '#a1a1aa' }}>Real-time notifications for critical risks and opportunities.</p>
          </div>
          <div style={{ background: '#12121a', padding: '2rem', borderRadius: '12px', border: '1px solid rgba(99, 102, 241, 0.1)' }}>
            <h3>🔍 Sentiment Analysis</h3>
            <p style={{ color: '#a1a1aa' }}>AI-powered sentiment and context analysis for every mention.</p>
          </div>
          <div style={{ background: '#12121a', padding: '2rem', borderRadius: '12px', border: '1px solid rgba(99, 102, 241, 0.1)' }}>
            <h3>🛡️ Threat Detection</h3>
            <p style={{ color: '#a1a1aa' }}>Advanced algorithms to detect and prioritize digital threats.</p>
          </div>
          <div style={{ background: '#12121a', padding: '2rem', borderRadius: '12px', border: '1px solid rgba(99, 102, 241, 0.1)' }}>
            <h3>📊 Custom Reports</h3>
            <p style={{ color: '#a1a1aa' }}>Monthly and on-demand reporting for actionable insights.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FeaturesPage;
