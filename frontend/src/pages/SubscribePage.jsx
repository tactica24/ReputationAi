import React from 'react';
import PublicHeader from '../components/public/PublicHeader';

const SubscribePage = () => {
  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#0a0a0f', color: '#fff', fontFamily: 'Inter, sans-serif', padding: '7rem 2rem 2rem' }}>
      <PublicHeader />
      <div style={{ maxWidth: '900px', margin: '0 auto' }}>
        <h1>Subscribe</h1>
        <p style={{ color: '#a1a1aa', marginBottom: '2rem' }}>Choose the plan that fits your monitoring needs.</p>
        <section style={{ marginBottom: '2rem' }}>
          <h2>Starter</h2>
          <p>Ideal for individuals and emerging brands.</p>
        </section>
        <section style={{ marginBottom: '2rem' }}>
          <h2>Growth</h2>
          <p>For teams that need escalations and deeper monitoring.</p>
        </section>
        <section style={{ marginBottom: '2rem' }}>
          <h2>Enterprise</h2>
          <p>Custom coverage, workflows, and integrations for global orgs.</p>
        </section>
      </div>
    </div>
  );
};

export default SubscribePage;
