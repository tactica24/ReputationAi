import React from 'react';
import { useNavigate } from 'react-router-dom';

const TermsPage = () => {
  const navigate = useNavigate();

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#0a0a0f', color: '#fff', fontFamily: 'Inter, sans-serif', padding: '6rem 2rem 2rem' }}>
      <div style={{ maxWidth: '900px', margin: '0 auto' }}>
        <button onClick={() => navigate('/')} style={{ background: '#6366f1', color: '#fff', border: 'none', padding: '0.5rem 1rem', borderRadius: '0.5rem', marginBottom: '2rem', cursor: 'pointer' }}>
          ← Back to Home
        </button>
        
        <h1>Terms of Service</h1>
        <p style={{ color: '#a1a1aa', marginBottom: '2rem' }}>Last updated: December 28, 2025</p>
        
        <section style={{ marginBottom: '2rem' }}>
          <h2>1. Acceptance of Terms</h2>
          <p>By using ReputationGuard, you agree to these terms and conditions. If you do not agree, please do not use our services.</p>
        </section>

        <section style={{ marginBottom: '2rem' }}>
          <h2>2. Use License</h2>
          <p>We grant you a limited, non-exclusive, revocable license to use ReputationGuard for lawful purposes only. You may not:</p>
          <ul style={{ marginLeft: '2rem', color: '#a1a1aa' }}>
            <li>Reproduce or duplicate any content</li>
            <li>Use our services for illegal purposes</li>
            <li>Harass or harm other users</li>
            <li>Attempt to gain unauthorized access</li>
          </ul>
        </section>

        <section style={{ marginBottom: '2rem' }}>
          <h2>3. Limitation of Liability</h2>
          <p>ReputationGuard is provided "as is" without warranties. We are not liable for indirect, incidental, or consequential damages arising from your use of our services.</p>
        </section>

        <section style={{ marginBottom: '2rem' }}>
          <h2>4. Contact</h2>
          <p>For questions about these terms, contact us at: legal@reputationguard.com</p>
        </section>
      </div>
    </div>
  );
};

export default TermsPage;
