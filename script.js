// Mobile Menu Toggle
const mobileToggle = document.querySelector('.mobile-toggle');
const navLinks = document.querySelector('.nav-links');

if (mobileToggle) {
    mobileToggle.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        mobileToggle.classList.toggle('active');
    });
}

// Smooth Scrolling
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
            // Close mobile menu if open
            navLinks?.classList.remove('active');
            mobileToggle?.classList.remove('active');
        }
    });
});

// FAQ Accordion
document.querySelectorAll('.faq-question').forEach(question => {
    question.addEventListener('click', function() {
        const faqItem = this.parentElement;
        const isActive = faqItem.classList.contains('active');
        
        // Close all FAQ items
        document.querySelectorAll('.faq-item').forEach(item => {
            item.classList.remove('active');
        });
        
        // Open clicked item if it wasn't active
        if (!isActive) {
            faqItem.classList.add('active');
        }
    });
});

// Application Form Submission
const applicationForm = document.getElementById('applicationForm');
const successMessage = document.getElementById('successMessage');

if (applicationForm) {
    applicationForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Collect form data
        const formData = new FormData(this);
        const data = Object.fromEntries(formData.entries());
        
        // Validate required fields
        const requiredFields = ['firstName', 'lastName', 'email', 'phone', 'title', 'entities', 'urgency'];
        let isValid = true;
        
        requiredFields.forEach(field => {
            const input = this.querySelector(`[name="${field}"]`);
            if (!input.value.trim()) {
                isValid = false;
                input.style.borderColor = 'var(--danger)';
            } else {
                input.style.borderColor = 'var(--border)';
            }
        });
        
        if (!isValid) {
            alert('Please fill in all required fields marked with *');
            return;
        }
        
        // Check agreement checkbox
        if (!this.querySelector('#agreement').checked || !this.querySelector('#privacy').checked) {
            alert('Please accept the terms to continue');
            return;
        }
        
        // Show loading state
        const submitBtn = this.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;
        submitBtn.textContent = 'Submitting...';
        submitBtn.disabled = true;
        
        try {
            // Send to backend API
            const response = await fetch('http://localhost:8080/api/v1/applications', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Submission failed');
            }
            
            const result = await response.json();
            
            // Hide form and show success message
            this.style.display = 'none';
            successMessage.style.display = 'block';
            
            // Update success message with application ID
            const successNote = successMessage.querySelector('.success-note');
            if (successNote) {
                successNote.textContent = `Application ID: ${result.application_id}. ${result.message}`;
            }
            
            // Scroll to success message
            successMessage.scrollIntoView({ behavior: 'smooth', block: 'center' });
            
        } catch (error) {
            console.error('Error:', error);
            alert('There was an error submitting your application. Please try again or contact us directly.');
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        }
    });
}

// Scroll-based navbar background
let lastScroll = 0;
const nav = document.querySelector('.nav');

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    if (currentScroll > 100) {
        nav.style.background = 'rgba(10, 10, 15, 0.95)';
        nav.style.boxShadow = '0 4px 6px -1px rgb(0 0 0 / 0.3)';
    } else {
        nav.style.background = 'rgba(10, 10, 15, 0.8)';
        nav.style.boxShadow = 'none';
    }
    
    lastScroll = currentScroll;
});

// Intersection Observer for Animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe all cards for animation
document.querySelectorAll('.threat-card, .protection-card, .pricing-card').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(card);
});

// Real-time urgency counter (simulated)
function updateUrgencyStats() {
    const stats = document.querySelectorAll('.urgency-stat .big');
    stats.forEach(stat => {
        const current = parseInt(stat.textContent);
        const change = Math.floor(Math.random() * 10) - 5; // Random change
        const newValue = Math.max(0, current + change);
        stat.textContent = newValue;
    });
}

// Update stats every 5 seconds
if (document.querySelector('.urgency-banner')) {
    setInterval(updateUrgencyStats, 5000);
}
            console.log('Start Free Trial clicked');
            // Redirect to signup or show modal
        } else if (this.textContent.includes('Demo')) {
            console.log('Watch Demo clicked');
            // Open demo video or schedule demo
        } else if (this.textContent.includes('Sales')) {
            console.log('Contact Sales clicked');
            // Open contact form
        }
    });
});

// Stats Counter Animation
const animateCounter = (element, target, duration = 2000) => {
    let start = 0;
    const increment = target / (duration / 16);
    
    const updateCounter = () => {
        start += increment;
        if (start < target) {
            element.textContent = Math.floor(start).toLocaleString();
            requestAnimationFrame(updateCounter);
        } else {
            element.textContent = target.toLocaleString();
        }
    };
    
    updateCounter();
};

// Observe stats
const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const statValue = entry.target.querySelector('.stat-value');
            const text = statValue.textContent;
            
            // Don't animate if already animated
            if (statValue.dataset.animated) return;
            statValue.dataset.animated = 'true';
            
            // Keep original text for non-numeric values
            if (text.includes('%')) {
                const value = parseFloat(text);
                let current = 0;
                const timer = setInterval(() => {
                    current += 0.1;
                    if (current >= value) {
                        statValue.textContent = text;
                        clearInterval(timer);
                    } else {
                        statValue.textContent = current.toFixed(1) + '%';
                    }
                }, 20);
            }
        }
    });
}, { threshold: 0.5 });

document.querySelectorAll('.stat').forEach(stat => {
    statsObserver.observe(stat);
});
