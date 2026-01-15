import React from 'react';
import PublicHeader from '../components/public/PublicHeader';

const TermsPage = () => {
  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#0a0a0f', color: '#fff', fontFamily: 'Inter, sans-serif', padding: '7rem 2rem 2rem' }}>
      <PublicHeader />
      <div style={{ maxWidth: '900px', margin: '0 auto' }}>
        <h1>Terms of Service</h1>
        <p style={{ color: '#a1a1aa', marginBottom: '2rem' }}>Last updated: December 28, 2025</p>
        <section style={{ marginBottom: '2rem' }}>
          <h2>Acceptance of Terms</h2>
          <p>By accessing or using VeriSignal, you agree to these Terms of Service.</p>
        </section>
        <section style={{ marginBottom: '2rem' }}>
          <h2>Use of Service</h2>
          <p>You agree to use the service responsibly and in compliance with all applicable laws and regulations.</p>
        </section>
        <section style={{ marginBottom: '2rem' }}>
          <h2>Data & Privacy</h2>
          <p>We follow strict data protection practices and provide transparency on our processing policies.</p>
        </section>
        <section style={{ marginBottom: '2rem' }}>
          <h2>Contact</h2>
          <p>Questions about these terms? Contact us at legal@verisignal.com</p>
        </section>
      </div>
    </div>
  );
};

export default TermsPage;
