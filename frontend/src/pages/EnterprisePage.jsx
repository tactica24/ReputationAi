import React from 'react';
import PublicHeader from '../components/public/PublicHeader';

const EnterprisePage = () => {
  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#0a0a0f', color: '#fff', fontFamily: 'Inter, sans-serif', padding: '7rem 2rem 2rem' }}>
      <PublicHeader />
      <div style={{ maxWidth: '1100px', margin: '0 auto' }}>
        <h1>Enterprise</h1>
        <p style={{ color: '#a1a1aa', marginBottom: '2rem' }}>Advanced protection for global teams.</p>
        <section style={{ marginBottom: '2rem' }}>
          <h2>Enterprise-grade monitoring</h2>
          <p>Custom coverage, team workflows, and compliance-ready reporting for large organizations.</p>
        </section>
        <section style={{ marginBottom: '2rem' }}>
          <h2>Dedicated response workflows</h2>
          <p>Escalations, audit trails, and role-based access controls tailored to your organization.</p>
        </section>
        <section style={{ marginBottom: '2rem' }}>
          <h2>Talk to our team</h2>
          <p>Contact enterprise@verisignal.com to schedule a private demo.</p>
        </section>
      </div>
    </div>
  );
};

export default EnterprisePage;
