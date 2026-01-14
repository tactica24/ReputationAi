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
      features: '/features',
      protection: '/protection',
      enterprise: '/enterprise',
      privacy: '/privacy',
      terms: '/terms',
      security: '/security',
      subscribe: '/subscribe'
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
              <text x="18" y="25" fontFamily="Inter, sans-serif" fontSize="18" fontWeight="700" fill="url(#logoText)" textAnchor="middle">VS</text>
              <defs>
                <linearGradient id="logoStroke" x1="0" y1="0" x2="36" y2="36">
                  <stop offset="0%" stopColor="#6366f1"/>
                  <stop offset="100%" stopColor="#8b5cf6"/>
                </linearGradient>
                <linearGradient id="logoText" x1="0" y1="0" x2="36" y2="36">
                  <stop offset="0%" stopColor="#6366f1"/>
                  <stop offset="100%" stopColor="#8b5cf6"/>
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
          <div className="hero-badge">Trusted by Industry Leaders</div>
          <h1 className="hero-heading">
            Protect Your Digital Signal
            <br/>
            <span className="gradient-text">With VeriSignal AI</span>
          </h1>
          <p className="hero-description">
            AI-powered monitoring across platforms. Detect risks instantly, respond effectively, and safeguard your reputation with VeriSignal.
          </p>

          <div className="hero-cta-group">
            <button onClick={() => handleNavClick('subscribe')} className="btn-hero-primary">
              Start Protection Now
            </button>
          </div>

          <div className="hero-trust-bar">
            <div className="trust-stat">
              <span className="trust-number">500+</span>
              <span className="trust-label">Protected Clients</span>
            </div>
            <div className="trust-divider"></div>
            <div className="trust-stat">
              <span className="trust-number">24/7</span>
              <span className="trust-label">Monitoring</span>
            </div>
            <div className="trust-divider"></div>
            <div className="trust-stat">
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
                  <text x="18" y="25" fontFamily="Inter, sans-serif" fontSize="18" fontWeight="700" fill="url(#logoTextFooter)" textAnchor="middle">VS</text>
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
              <p className="footer-tagline">AI-powered digital reputation and identity protection for the modern era. Powered by VeriSignal.</p>
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
