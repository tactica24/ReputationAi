import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';
import './HomePage.css';

const HomePage = () => {
  const navigate = useNavigate();
  const { user, isAuthenticated } = useAuthStore();
  const [mobileNavOpen, setMobileNavOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const [showForm, setShowForm] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 50) {
        setScrolled(true);
      } else {
        setScrolled(false);
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const toggleMobileNav = () => {
    setMobileNavOpen(!mobileNavOpen);
    document.body.classList.toggle('nav-open');
  };

  const handleNavClick = (path) => {
    setMobileNavOpen(false);
    document.body.classList.remove('nav-open');
    const urlMap = {
      features: '/protection',
      protection: '/application-form',
      enterprise: '/enterprise',
      privacy: '/privacy',
      terms: '/terms',
      security: '/security'
    };

    const target = urlMap[path] || path;

    if (target.startsWith('#')) {
      const element = document.querySelector(target);
      element?.scrollIntoView({ behavior: 'smooth' });
    } else if (target.startsWith('http')) {
      window.location.href = target;
    } else {
      navigate(target);
    }
  };

  const handleDashboard = () => {
    setMobileNavOpen(false);
    document.body.classList.remove('nav-open');
    if (isAuthenticated) {
      if (user?.role === 'admin') {
        navigate('/admin');
      } else {
        navigate('/dashboard');
      }
    } else {
      navigate('/login');
    }
  };

  const handleLogin = () => {
    setMobileNavOpen(false);
    document.body.classList.remove('nav-open');
    navigate('/login');
  };

  return (
    <div className="homepage-container">
      {/* Premium Navigation */}
      <nav className={`nav-premium ${scrolled ? 'scrolled' : ''}`}>
        <div className="nav-wrapper">
          <a href="/" className="brand">
            <svg className="brand-icon" width="36" height="36" viewBox="0 0 36 36" fill="none">
              <rect width="36" height="36" rx="8" fill="#0a0a0f" stroke="url(#logoStroke)" strokeWidth="1.5"/>
              <g>
                <path d="M18 7 L30 12 V19 C30 27 22 32 18 33 C14 32 6 27 6 19 V12 L18 7 Z" fill="#00c3a0" fillOpacity="0.18" stroke="#00c3a0" strokeWidth="1.5"/>
                <circle cx="18" cy="18" r="4" fill="#6366f1" fillOpacity="0.7" />
              </g>
              <text x="18" y="25" fontFamily="Inter, sans-serif" fontSize="15" fontWeight="700" fill="#fff" textAnchor="middle">VS</text>
              <defs>
                <linearGradient id="logoStroke" x1="0" y1="0" x2="36" y2="36">
                  <stop offset="0%" stopColor="#00c3a0"/>
                  <stop offset="100%" stopColor="#6366f1"/>
                </linearGradient>
              </defs>
            </svg>
            <span className="brand-name">VeriSignal</span>
          </a>

          <div className="nav-links">
            <button onClick={() => handleNavClick('features')} className="nav-link">Features</button>
            <button onClick={() => handleNavClick('protection')} className="nav-link">Protection</button>
            <button onClick={() => handleNavClick('enterprise')} className="nav-link">Enterprise</button>
            <button onClick={handleDashboard} className="nav-link-dash">Dashboard</button>
          </div>

          <button 
            className={`mobile-nav-toggle ${mobileNavOpen ? 'active' : ''}`}
            onClick={toggleMobileNav}
            aria-label="Menu"
          >
            <span></span>
            <span></span>
            <span></span>
          </button>
        </div>
      </nav>

      {/* Mobile Navigation */}
      <div className={`mobile-nav ${mobileNavOpen ? 'active' : ''}`}>
        <button className="mobile-nav-close" onClick={toggleMobileNav}>&times;</button>
        <div className="mobile-nav-content">
          <button onClick={() => handleNavClick('features')} className="mobile-nav-link">Features</button>
          <button onClick={() => handleNavClick('protection')} className="mobile-nav-link">Protection</button>
          <button onClick={() => handleNavClick('enterprise')} className="mobile-nav-link">Enterprise</button>
          <button onClick={handleDashboard} className="mobile-nav-link">Dashboard</button>
        </div>
      </div>

      {/* Hero Section */}
      <section className="hero-premium">
        <div className="hero-content-wrapper">
          <div className="hero-badge">Reputation Security for the Age of Deepfakes</div>
          <h1 className="hero-heading">
            VeriSignal — <span className="gradient-text">Cutting-Edge Reputation Guard</span>
          </h1>
          <p className="hero-description">
            Defend your brand, identity, and legacy with 24/7 cutting-edge technology monitoring.<br/>
            Detect deepfakes, misinformation, and threats before they go viral.<br/>
            <span style={{color:'#00c3a0', fontWeight:600}}>Enterprise-grade security. Real-time alerts. Peace of mind.</span>
          </p>
          <div className="hero-cta-group">
            <button onClick={() => navigate('/application-form')} className="btn-hero-primary">
              Get Protected Now
            </button>
          </div>
          <div className="hero-trust-bar">
            <div className="trust-stat">
              <span className="trust-icon" role="img" aria-label="shield">🛡️</span>
              <span className="trust-number">Enterprise</span>
              <span className="trust-label">Grade Security</span>
            </div>
            <div className="trust-divider"></div>
            <div className="trust-stat">
              <span className="trust-icon" role="img" aria-label="clock">⏱️</span>
              <span className="trust-number">24/7</span>
              <span className="trust-label">Cutting-Edge Monitoring</span>
            </div>
            <div className="trust-divider"></div>
            <div className="trust-stat">
              <span className="trust-icon" role="img" aria-label="globe">🌐</span>
              <span className="trust-number">100M+</span>
              <span className="trust-label">Sources Scanned</span>
            </div>
          </div>
        </div>
      </section>

      {/* Contact Us Section */}
      <section className="contact-us">
        <h2>Contact Us</h2>
        <button className="btn-contact-us" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Hide Form' : 'Contact Us'}
        </button>
        {showForm && (
          <form className="contact-form">
            <label htmlFor="name">Name</label>
            <input type="text" id="name" name="name" required />

            <label htmlFor="email">Email</label>
            <input type="email" id="email" name="email" required />

            <label htmlFor="message">Message</label>
            <textarea id="message" name="message" rows="4" required></textarea>

            <button type="submit" className="btn-submit">Submit</button>
          </form>
        )}
      </section>

      {/* Footer */}
      <footer className="footer-premium">
        <div className="footer-container">
          <div className="footer-grid">
            <div className="footer-brand">
              <div className="brand">
                <svg className="brand-icon" width="32" height="32" viewBox="0 0 36 36" fill="none">
                  <rect width="36" height="36" rx="8" fill="#0a0a0f" stroke="url(#logoStrokeFooter)" strokeWidth="1.5"/>
                  <text x="18" y="25" fontFamily="Inter, sans-serif" fontSize="18" fontWeight="700" fill="url(#logoTextFooter)" textAnchor="middle">RG</text>
                  <defs>
                    <linearGradient id="logoStrokeFooter" x1="0" y1="0" x2="36" y2="36">
                      <stop offset="0%" stopColor="#6366f1"/>
                      <stop offset="100%" stopColor="#8b5cf6"/>
                    </linearGradient>
                    <linearGradient id="logoTextFooter" x1="0" y1="0" x2="36" y2="36">
                      <stop offset="0%" stopColor="#6366f1"/>
                      <stop offset="100%" stopColor="#8b5cf6"/>
                    </linearGradient>
                  </defs>
                </svg>
                <span className="brand-name">VeriSignal</span>
              </div>
              <p className="footer-tagline">Enterprise-grade AI reputation security for those who can't afford risk.</p>
            </div>

            <div className="footer-links">
              <h4>Product</h4>
              <button onClick={() => handleNavClick('features')} className="footer-link">Features</button>
              <button onClick={() => handleNavClick('protection')} className="footer-link">How It Works</button>
              <button onClick={() => handleNavClick('enterprise')} className="footer-link">Enterprise</button>
            </div>

            <div className="footer-links">
              <h4>Company</h4>
              <button onClick={handleDashboard} className="footer-link">Dashboard</button>
              <a href="tel:+18005551234" className="footer-link">Contact</a>
            </div>

            <div className="footer-links">
              <h4>Legal</h4>
              <button onClick={() => handleNavClick('privacy')} className="footer-link">Privacy Policy</button>
              <button onClick={() => handleNavClick('terms')} className="footer-link">Terms of Service</button>
              <button onClick={() => handleNavClick('security')} className="footer-link">Security</button>
            </div>
          </div>

          <div className="footer-bottom">
            <p>&copy; 2025 VeriSignal. All rights reserved.</p>
            <p className="footer-emergency">🚨 Crisis Hotline: <a href="tel:+18005551234">1-800-555-1234</a></p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default HomePage;
