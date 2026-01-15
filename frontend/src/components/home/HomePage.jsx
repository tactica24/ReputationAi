import React from 'react';
import { useNavigate } from 'react-router-dom';
import PublicHeader from '../public/PublicHeader';
import './HomePage.css';

const HomePage = () => {
  const navigate = useNavigate();

  const demoAlerts = [
    {
      title: 'Impersonation claim trending on X',
      source: 'X / Social',
      time: '2m ago',
      risk: 'High',
      score: 82,
      confidence: 'High',
      reasons: ['Impersonation', 'Viral velocity', 'Unverified source'],
      url: 'https://x.com/sample-alert'
    },
    {
      title: 'Blog alleges fraud investigation',
      source: 'Blog / Finance Watch',
      time: '12m ago',
      risk: 'Critical',
      score: 91,
      confidence: 'Medium',
      reasons: ['Accusation', 'Legal risk', 'First-time domain'],
      url: 'https://financewatch.example.com/story'
    },
    {
      title: 'YouTube clip misquotes press release',
      source: 'YouTube / Clip Digest',
      time: '26m ago',
      risk: 'Medium',
      score: 68,
      confidence: 'High',
      reasons: ['Fake quote', 'High engagement', 'New channel'],
      url: 'https://youtube.com/watch?v=example'
    }
  ];

  const handleApply = () => {
    window.location.href = '/application-form.html';
  };

  return (
    <div className="homepage-container">
      <PublicHeader />

      <section className="hero-premium" id="top">
        <div className="hero-content-wrapper">
          <div className="hero-badge">
            <span className="badge-dot"></span>
            Secure-by-design reputation intelligence
          </div>
          <h1 className="hero-heading">
            Prevent reputational damage
            <br />
            <span className="gradient-text">before it spreads.</span>
          </h1>
          <p className="hero-description">
            AI-powered monitoring across platforms. Detect risks instantly, respond effectively, and
            safeguard your reputation with VeriSignal.
          </p>
          <div className="hero-cta-group">
            <button className="btn-hero-primary" onClick={handleApply}>
              Get Protected
            </button>
            <button className="btn-hero-secondary" onClick={() => navigate('/features')}>
              Explore features
            </button>
          </div>
          <div className="hero-metrics">
            <div>
              <strong>15 min</strong>
              <span>fastest scan interval</span>
            </div>
            <div>
              <strong>100M+</strong>
              <span>signals monitored</span>
            </div>
            <div>
              <strong>99.9%</strong>
              <span>alert delivery SLA</span>
            </div>
          </div>
        </div>
        <div className="hero-visual">
          <div className="hero-orbit"></div>
          <div className="hero-stack">
            <div className="hero-card primary">
              <div className="card-header">
                <span className="chip chip-danger">Critical</span>
                <span className="muted">Just now</span>
              </div>
              <h4>Impersonation spike detected</h4>
              <p className="muted">News / Social · Confidence High</p>
              <div className="trust-row">
                <a className="trust-link" href="https://x.com/sample-alert">Source link</a>
                <span>Capture time: 2m ago</span>
                <span>Snapshot</span>
                <span>Reason codes</span>
              </div>
              <div className="badge-row">
                <span className="badge">Impersonation</span>
                <span className="badge">Viral velocity</span>
                <span className="badge">Unverified source</span>
              </div>
              <div className="action-row">
                <button className="ghost-button">Escalate</button>
                <button className="ghost-button">Mark safe</button>
              </div>
            </div>
            <div className="hero-card secondary">
              <div className="card-header">
                <span className="chip chip-info">Monitoring</span>
                <span className="muted">2m ago</span>
              </div>
              <p className="muted">Global scan cycle completed · 438 sources checked</p>
            </div>
          </div>
        </div>
      </section>

      <section className="section" id="demo">
        <div className="section-heading">
          <h2>Demo alert cards</h2>
          <p>Risk chips, explainability, and fast actions in one glance.</p>
        </div>
        <div className="demo-cards">
          {demoAlerts.map((alert, index) => (
            <div key={alert.title} className={`card demo-card demo-card-${index + 1}`}>
              <div className="card-header">
                <span className={`chip chip-${alert.risk.toLowerCase()}`}>{alert.risk}</span>
                <span className="muted">{alert.time}</span>
              </div>
              <h4>{alert.title}</h4>
              <p className="muted">{alert.source}</p>
              <div className="score-row">
                <div>
                  <strong>Risk score</strong>
                  <span>{alert.score}/100</span>
                </div>
                <div>
                  <strong>Confidence</strong>
                  <span>{alert.confidence}</span>
                </div>
              </div>
              <div className="trust-row">
                <a className="trust-link" href={alert.url}>Source link</a>
                <span>Captured {alert.time}</span>
                <span>Snapshot</span>
                <span>Confidence: {alert.confidence}</span>
              </div>
              <div className="badge-row">
                {alert.reasons.map((reason) => (
                  <span key={reason} className="badge">{reason}</span>
                ))}
              </div>
              <div className="action-row">
                <button className="ghost-button">Open</button>
                <button className="ghost-button">Escalate</button>
                <button className="ghost-button">Add evidence</button>
              </div>
            </div>
          ))}
        </div>
      </section>

      <section className="cta-strip" id="docs">
        <div>
          <h3>Get started in 2 minutes</h3>
          <p>Share your monitoring goals and let our team activate your coverage.</p>
        </div>
        <div className="cta-actions">
          <button className="btn-hero-primary" onClick={handleApply}>
            Get Protected
          </button>
        </div>
      </section>

      <footer className="footer-premium">
        <div className="footer-container">
          <div className="footer-grid">
            <div>
              <div className="brand">
                <span className="brand-mark">
                  <span className="brand-mark-glow"></span>
                  <span className="brand-mark-text">VS</span>
                </span>
                <span className="brand-name">VeriSignal</span>
              </div>
            </div>
            <div>
              <h4>Product</h4>
              <button onClick={() => navigate('/features')} className="footer-link">Features</button>
              <button onClick={() => navigate('/protection')} className="footer-link">Protection</button>
              <button onClick={() => navigate('/security')} className="footer-link">Security</button>
            </div>
            <div>
              <h4>Company</h4>
              <button onClick={handleApply} className="footer-link">Get Protected</button>
            </div>
            <div>
              <h4>Resources</h4>
              <button onClick={() => { window.location.hash = 'docs'; }} className="footer-link">Docs</button>
            </div>
          </div>
          <div className="footer-bottom">
            <p>© 2025 VeriSignal. All rights reserved.</p>
            <p className="muted">Secure by design · GDPR-style commitments · Audit logs</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default HomePage;
