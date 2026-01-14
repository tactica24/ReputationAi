import React from 'react';
import { useNavigate } from 'react-router-dom';

const PrivacyPage = () => {
  const navigate = useNavigate();

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#0a0a0f', color: '#fff', fontFamily: 'Inter, sans-serif', padding: '6rem 2rem 2rem' }}>
      <div style={{ maxWidth: '900px', margin: '0 auto' }}>
        <button onClick={() => navigate('/')} style={{ background: '#6366f1', color: '#fff', border: 'none', padding: '0.5rem 1rem', borderRadius: '0.5rem', marginBottom: '2rem', cursor: 'pointer' }}>
          ← Back to Home
        </button>
        
        <h1>Privacy Policy</h1>
        <p style={{ color: '#a1a1aa', marginBottom: '2rem' }}>Last updated: December 28, 2025</p>
        
        <section style={{ marginBottom: '2rem' }}>
          <h2>Overview</h2>
          <p>VeriSignal is committed to protecting your privacy. This Privacy Policy explains how we collect, use, and protect your information.</p>
        </section>

        <section style={{ marginBottom: '2rem' }}>
          <h2>Information We Collect</h2>
          <p>We collect information you provide directly to us, such as:</p>
          <ul style={{ marginLeft: '2rem', color: '#a1a1aa' }}>
            <li>Account information (name, email, company)</li>
            <li>Payment information</li>
            <li>Entity information for monitoring</li>
            <li>Communication preferences</li>
          </ul>
        </section>

        <section style={{ marginBottom: '2rem' }}>
          <h2>How We Use Your Information</h2>
          <p>We use your information to:</p>
          <ul style={{ marginLeft: '2rem', color: '#a1a1aa' }}>
            <li>Provide and improve our services</li>
            <li>Send you updates and notifications</li>
            <li>Protect against fraud and abuse</li>
            <li>Comply with legal obligations</li>
          </ul>
        </section>

        <section style={{ marginBottom: '2rem' }}>
          <h2>Contact Us</h2>
          <p>For privacy concerns, please contact us at: privacy@verisignal.com</p>
        </section>
      </div>
    </div>
  );
};

export default PrivacyPage;
