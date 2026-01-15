import React, { useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../home/HomePage.css';

const PublicHeader = () => {
  const navigate = useNavigate();
  const [mobileNavOpen, setMobileNavOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 24);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const navigation = useMemo(
    () => [
      { label: 'Features', href: '/features' },
      { label: 'Protection', href: '/protection' },
      { label: 'Security', href: '/security' },
      { label: 'Docs', href: '#docs' }
    ],
    []
  );

  const toggleMobileNav = () => {
    setMobileNavOpen((prev) => !prev);
    document.body.classList.toggle('nav-open');
  };

  const handleNav = (href) => {
    setMobileNavOpen(false);
    document.body.classList.remove('nav-open');
    if (href.startsWith('#')) {
      const element = document.querySelector(href);
      element?.scrollIntoView({ behavior: 'smooth' });
    } else {
      navigate(href);
    }
  };

  const handleApply = () => {
    window.location.href = '/application-form.html';
  };

  return (
    <>
      <nav className={`nav-premium ${scrolled ? 'scrolled' : ''}`}>
        <div className="nav-wrapper">
          <a className="brand" href="#top">
            <span className="brand-mark">
              <span className="brand-mark-glow"></span>
              <span className="brand-mark-text">VS</span>
            </span>
            <span className="brand-name">VeriSignal</span>
          </a>
          <div className="nav-links">
            {navigation.map((link) => (
              <button
                key={link.label}
                className="nav-link"
                onClick={() => handleNav(link.href)}
              >
                {link.label}
              </button>
            ))}
            <button className="nav-link nav-cta" onClick={handleApply}>
              Get Protected
            </button>
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

      <div className={`mobile-nav ${mobileNavOpen ? 'active' : ''}`}>
        <button className="mobile-nav-close" onClick={toggleMobileNav}>&times;</button>
        <div className="mobile-nav-content">
          {navigation.map((link) => (
            <button
              key={link.label}
              className="mobile-nav-link"
              onClick={() => handleNav(link.href)}
            >
              {link.label}
            </button>
          ))}
          <button className="mobile-nav-link" onClick={handleApply}>
            Get Protected
          </button>
        </div>
      </div>
    </>
  );
};

export default PublicHeader;
