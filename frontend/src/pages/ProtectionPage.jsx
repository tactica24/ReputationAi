import React from 'react';
import PublicHeader from '../components/public/PublicHeader';

const ProtectionPage = () => {
  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#0a0a0f', color: '#fff', fontFamily: 'Inter, sans-serif', padding: '7rem 2rem 2rem' }}>
      <PublicHeader />
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        <h1>How VeriSignal Protects You</h1>
        <p>AI-powered, real-time monitoring and threat detection across the entire digital landscape. Stay ahead of risks and protect your reputation and identity 24/7.</p>
        <section id="how-it-works" style={{ marginTop: '2rem' }}>
          <h2>The VeriSignal Process</h2>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '2rem', marginTop: '2rem' }}>
            <div style={{ background: '#12121a', padding: '2rem', borderRadius: '12px', border: '1px solid rgba(99, 102, 241, 0.1)' }}>
              <h3>🌐 Monitor</h3>
              <p style={{ color: '#a1a1aa' }}>24/7 scanning of 100M+ sources for threats and mentions.</p>
            </div>
            <div style={{ background: '#12121a', padding: '2rem', borderRadius: '12px', border: '1px solid rgba(99, 102, 241, 0.1)' }}>
              <h3>⚡ Analyze</h3>
              <p style={{ color: '#a1a1aa' }}>AI-driven sentiment and context analysis for every mention.</p>
            </div>
            <div style={{ background: '#12121a', padding: '2rem', borderRadius: '12px', border: '1px solid rgba(99, 102, 241, 0.1)' }}>
              <h3>🛡️ Protect</h3>
              <p style={{ color: '#a1a1aa' }}>Instant alerts and automated threat response to keep you safe.</p>
            </div>
            <div style={{ background: '#12121a', padding: '2rem', borderRadius: '12px', border: '1px solid rgba(99, 102, 241, 0.1)' }}>
              <h3>📊 Report</h3>
              <p style={{ color: '#a1a1aa' }}>Custom monthly and on-demand reporting for actionable insights.</p>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
};

export default ProtectionPage;
