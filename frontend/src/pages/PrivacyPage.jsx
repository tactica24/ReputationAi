import React from 'react';
import PublicHeader from '../components/public/PublicHeader';

const PrivacyPage = () => {
  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#0a0a0f', color: '#fff', fontFamily: 'Inter, sans-serif', padding: '7rem 2rem 2rem' }}>
      <PublicHeader />
      <div style={{ maxWidth: '900px', margin: '0 auto' }}>
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
          <h2>Data Security</h2>
          <p>We implement strong security measures to protect your data, including encryption, access controls, and regular audits.</p>
        </section>
        <section style={{ marginBottom: '2rem' }}>
          <h2>Contact Us</h2>
          <p>Questions about privacy? Contact us at privacy@verisignal.com</p>
        </section>
      </div>
    </div>
  );
};

export default PrivacyPage;
