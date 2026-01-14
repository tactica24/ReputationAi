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
        
        <h1>How VeriSignal Protects You</h1>
        <p>Cutting-edge, real-time monitoring and deepfake threat detection across the entire digital world.</p>
        <section id="how-it-works" style={{ marginTop: '2rem' }}>
          <h2>The VeriSignal Process</h2>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '2rem', marginTop: '2rem' }}>
            <div style={{ background: '#12121a', padding: '2rem', borderRadius: '12px', border: '1px solid #00c3a0' }}>
              <h3>🔎 Cutting-Edge Monitoring</h3>
              <p style={{ color: '#a1a1aa' }}>24/7 scanning of news, social media, and the dark web for threats and deepfakes using advanced technology.</p>
            </div>
            <div style={{ background: '#12121a', padding: '2rem', borderRadius: '12px', border: '1px solid #00c3a0' }}>
              <h3>⚡ Instant Alerts</h3>
              <p style={{ color: '#a1a1aa' }}>Get notified the moment a risk or impersonation is detected.</p>
            </div>
            <div style={{ background: '#12121a', padding: '2rem', borderRadius: '12px', border: '1px solid #00c3a0' }}>
              <h3>🛡️ Automated Protection</h3>
              <p style={{ color: '#a1a1aa' }}>Automated response tools to help you counter threats and misinformation fast.</p>
            </div>
            <div style={{ background: '#12121a', padding: '2rem', borderRadius: '12px', border: '1px solid #00c3a0' }}>
              <h3>📊 Evidence & Reports</h3>
              <p style={{ color: '#a1a1aa' }}>Actionable reports and evidence for legal, PR, or takedown requests.</p>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
};

export default ProtectionPage;
