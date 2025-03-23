// Set current year for copyright
document.getElementById('current-year').textContent = new Date().getFullYear();

// Add animation class to contact items on scroll
const contactItems = document.querySelectorAll('.contact-item');

// Initialize WOW.js animations if not already initialized
if (typeof WOW === 'function' && !window.wowInitialized) {
    new WOW().init();
    window.wowInitialized = true;
}

// Add hover animation for social icons
document.querySelectorAll('.social-icon').forEach(icon => {
    icon.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-8px) scale(1.1)';
    });

    icon.addEventListener('mouseleave', function() {
        this.style.transform = '';
    });
});

// Newsletter form submission handler
const newsletterForm = document.querySelector('.newsletter-form');
if (newsletterForm) {
    newsletterForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const emailInput = this.querySelector('input[type="email"]');
        const email = emailInput.value.trim();

        if (email) {
            // Show success message
            const formGroup = this.querySelector('.input-group');

            // Create success message
            const successMsg = document.createElement('div');
            successMsg.className = 'alert alert-success mt-2 animate__animated animate__fadeIn';
            successMsg.textContent = '¡Gracias por suscribirte! Pronto recibirás nuestras novedades.';

            // Insert message after form
            formGroup.parentNode.insertBefore(successMsg, formGroup.nextSibling);

            // Clear input
            emailInput.value = '';

            // Remove success message after 5 seconds
            setTimeout(() => {
                successMsg.classList.replace('animate__fadeIn', 'animate__fadeOut');
                setTimeout(() => successMsg.remove(), 500);
            }, 5000);
        }
    });
}

// Initialize WOW animations
new WOW().init();

// Smooth scrolling for internal links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();

        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Back to top button
window.onscroll = function() {
    if (document.body.scrollTop > 200 || document.documentElement.scrollTop > 200) {
        document.querySelector('.back-to-top').style.display = "flex";
    } else {
        document.querySelector('.back-to-top').style.display = "none";
    }
};

// Sidebar toggle functionality for mobile
document.getElementById('sidebarToggle').addEventListener('click', function() {
    document.getElementById('sidebar').classList.toggle('show');
    document.querySelector('.main-content').classList.toggle('shifted');
});

// Highlight current page in sidebar
document.addEventListener('DOMContentLoaded', function() {
    const currentPage = window.location.pathname;
    const sidebarLinks = document.querySelectorAll('.sidebar__link');

    sidebarLinks.forEach(link => {
        if (link.getAttribute('href') === currentPage) {
            link.classList.add('active');
        }
    });
});

// Enhanced sidebar functionality
document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');
    const toggleIcon = document.getElementById('toggleIcon');
    const mainContent = document.querySelector('.main-content');
    const mobileSidebarToggle = document.getElementById('mobileSidebarToggle');
    const sidebarLinks = document.querySelectorAll('.sidebar__link');

    // Function to collapse sidebar
    function collapseSidebar() {
        sidebar.classList.add('collapsed');
        mainContent.classList.add('expanded');
        sidebarToggle.classList.add('collapsed');
        toggleIcon.classList.remove('fa-chevron-left');
        toggleIcon.classList.add('fa-chevron-right');

        // Save state to localStorage
        localStorage.setItem('sidebarState', 'collapsed');
    }

    // Function to expand sidebar
    function expandSidebar() {
        sidebar.classList.remove('collapsed');
        mainContent.classList.remove('expanded');
        sidebarToggle.classList.remove('collapsed');
        toggleIcon.classList.remove('fa-chevron-right');
        toggleIcon.classList.add('fa-chevron-left');

        // Save state to localStorage
        localStorage.setItem('sidebarState', 'expanded');
    }

    // Toggle sidebar on button click
    sidebarToggle.addEventListener('click', function() {
        if (sidebar.classList.contains('collapsed')) {
            expandSidebar();
        } else {
            collapseSidebar();
        }
    });

    // Mobile toggle
    mobileSidebarToggle.addEventListener('click', function() {
        sidebar.classList.toggle('show');
        mainContent.classList.toggle('shifted');
    });

    // Add hover effects to sidebar items
    sidebarLinks.forEach(link => {
        // Add bounce effect on hover
        link.addEventListener('mouseenter', function() {
            this.classList.add('animate__animated', 'animate__pulse');

            // If sidebar is collapsed, show a tooltip with the menu item text
            if (sidebar.classList.contains('collapsed') && window.innerWidth > 991) {
                const tooltipText = this.querySelector('span').textContent.trim();

                // Create tooltip element
                const tooltip = document.createElement('div');
                tooltip.className = 'sidebar-tooltip';
                tooltip.textContent = tooltipText;

                // Apply styles to tooltip
                Object.assign(tooltip.style, {
                    position: 'absolute',
                    left: '60px',
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    color: 'white',
                    padding: '5px 10px',
                    borderRadius: '4px',
                    zIndex: '1050',
                    fontSize: '0.9rem',
                    whiteSpace: 'nowrap'
                });

                // Position tooltip vertically centered with the link
                const linkRect = this.getBoundingClientRect();
                tooltip.style.top = (linkRect.top + window.scrollY + linkRect.height/2 - 15) + 'px';

                // Add tooltip to body
                document.body.appendChild(tooltip);
                this.dataset.tooltip = 'true';
            }
        });

        // Remove animation and tooltip when mouse leaves
        link.addEventListener('mouseleave', function() {
            this.classList.remove('animate__animated', 'animate__pulse');

            // Remove tooltip if exists
            if (this.dataset.tooltip) {
                const tooltip = document.querySelector('.sidebar-tooltip');
                if (tooltip) {
                    document.body.removeChild(tooltip);
                }
                delete this.dataset.tooltip;
            }
        });

        // Add active class to current page link
        if (link.getAttribute('href') === window.location.pathname) {
            link.classList.add('active');
        }
    });

    // Auto-collapse for mobile on page load
    if (window.innerWidth <= 991) {
        sidebar.classList.remove('show');
    } else {
        // For desktop, restore previous state from localStorage or default to expanded
        const savedState = localStorage.getItem('sidebarState');
        if (savedState === 'collapsed') {
            collapseSidebar();
        } else {
            expandSidebar();
        }
    }

    // Smart auto-hide based on scrolling behavior
    let lastScrollTop = 0;
    let scrollingDown = false;

    window.addEventListener('scroll', function() {
        const currentScroll = window.pageYOffset || document.documentElement.scrollTop;

        // Determine scroll direction
        scrollingDown = currentScroll > lastScrollTop;
        lastScrollTop = currentScroll;

        // Only apply for desktop view
        if (window.innerWidth > 991) {
            // Auto-collapse when scrolling down past threshold
            if (scrollingDown && currentScroll > 300 && !sidebar.classList.contains('collapsed')) {
                collapseSidebar();
            }
        }
    });

    // Add smooth hover expansion on collapsed sidebar
    if (window.innerWidth > 991) {
        sidebar.addEventListener('mouseenter', function() {
            if (sidebar.classList.contains('collapsed')) {
                // Create transition effect for hover expansion
                sidebar.style.transition = 'width 0.3s ease';
                sidebar.style.width = '180px'; // Partially expand on hover

                // Make menu text visible
                sidebarLinks.forEach(link => {
                    const span = link.querySelector('span');
                    span.style.opacity = '1';
                    span.style.width = 'auto';
                    span.style.height = 'auto';
                });
            }
        });

        sidebar.addEventListener('mouseleave', function() {
            if (sidebar.classList.contains('collapsed')) {
                // Return to collapsed state
                sidebar.style.width = '60px';

                // Hide menu text again
                sidebarLinks.forEach(link => {
                    const span = link.querySelector('span');
                    span.style.opacity = '0';
                    span.style.width = '0';
                    span.style.height = '0';
                });
            }
        });
    }

    // Update on window resize
    window.addEventListener('resize', function() {
        if (window.innerWidth <= 991) {
            sidebar.classList.remove('show');
            mainContent.classList.remove('shifted');

            // Reset hover styles for mobile
            sidebar.style.width = '';
            sidebarLinks.forEach(link => {
                const span = link.querySelector('span');
                span.style = '';
            });
        }
    });

    // Hide sidebar when clicking outside of it on mobile
    document.addEventListener('click', function(event) {
        const isClickInsideSidebar = sidebar.contains(event.target);
        const isClickOnToggle = mobileSidebarToggle.contains(event.target);

        if (!isClickInsideSidebar && !isClickOnToggle && sidebar.classList.contains('show') && window.innerWidth <= 991) {
            sidebar.classList.remove('show');
            mainContent.classList.remove('shifted');
        }
    });
});