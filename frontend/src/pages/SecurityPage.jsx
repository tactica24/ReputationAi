import React from 'react';
import { useNavigate } from 'react-router-dom';

const SecurityPage = () => {
  const navigate = useNavigate();

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#0a0a0f', color: '#fff', fontFamily: 'Inter, sans-serif', padding: '6rem 2rem 2rem' }}>
      <div style={{ maxWidth: '900px', margin: '0 auto' }}>
        <button onClick={() => navigate('/')} style={{ background: '#6366f1', color: '#fff', border: 'none', padding: '0.5rem 1rem', borderRadius: '0.5rem', marginBottom: '2rem', cursor: 'pointer' }}>
          ← Back to Home
        </button>
        
        <h1>Security</h1>
        <p style={{ color: '#a1a1aa', marginBottom: '2rem' }}>How we protect your data</p>
        
        <section style={{ marginBottom: '2rem' }}>
          <h2>🔒 Encryption</h2>
          <p>All data is encrypted in transit using industry-standard TLS 1.3 and at rest using AES-256 encryption.</p>
        </section>

        <section style={{ marginBottom: '2rem' }}>
          <h2>🛡️ Security Audits</h2>
          <p>We conduct regular security audits and penetration testing to ensure the highest standards of protection.</p>
        </section>

        <section style={{ marginBottom: '2rem' }}>
          <h2>🔐 Authentication</h2>
          <p>Multi-factor authentication (MFA) is available for all accounts. We strongly recommend enabling it for enhanced security.</p>
        </section>

        <section style={{ marginBottom: '2rem' }}>
          <h2>📋 Compliance</h2>
          <p>We comply with:</p>
          <ul style={{ marginLeft: '2rem', color: '#a1a1aa' }}>
            <li>GDPR - General Data Protection Regulation</li>
            <li>CCPA - California Consumer Privacy Act</li>
            <li>SOC 2 Type II certification</li>
            <li>ISO 27001 standards</li>
          </ul>
        </section>

        <section style={{ marginBottom: '2rem' }}>
          <h2>🚨 Report Security Issues</h2>
          <p>Found a security vulnerability? Please report it to: security@reputationguard.com</p>
        </section>
      </div>
    </div>
  );
};

export default SecurityPage;
