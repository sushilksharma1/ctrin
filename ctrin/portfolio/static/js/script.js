/**
 * Ctrin Interiors - Custom JavaScript
 */

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', function() {
    initNavbar();
    initSmoothScroll();
    initFormValidation();
    initLazyLoad();
    initAnimations();
});

/**
 * Navbar Active Link
 */
function initNavbar() {
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    const currentLocation = location.pathname;

    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentLocation || currentLocation.startsWith(href) && href !== '/') {
            link.classList.add('active');
            link.setAttribute('aria-current', 'page');
        } else {
            link.classList.remove('active');
        }
    });
}

/**
 * Smooth Scrolling for Anchor Links
 */
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href === '#') return;

            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/**
 * Form Validation
 */
function initFormValidation() {
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
}

/**
 * Lazy Load Images
 */
function initLazyLoad() {
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.classList.add('loaded');
                    }
                    observer.unobserve(img);
                }
            });
        });

        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
}

/**
 * Scroll Animations
 */
function initAnimations() {
    if ('IntersectionObserver' in window) {
        const animationObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in-up');
                    animationObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });

        document.querySelectorAll('.card, .service-card, .project-card').forEach(element => {
            animationObserver.observe(element);
        });
    }
}

/**
 * Contact Form - Show Success Message
 */
function handleContactFormSuccess() {
    const form = document.querySelector('.contact-form');
    if (form) {
        form.addEventListener('submit', function() {
            setTimeout(() => {
                const alert = document.querySelector('.alert-success');
                if (alert) {
                    alert.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }, 500);
        });
    }
}

/**
 * Mobile Menu Close on Link Click
 */
function initMobileMenu() {
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');

    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (navbarCollapse.classList.contains('show')) {
                navbarToggler.click();
            }
        });
    });
}

/**
 * Image Gallery Lightbox Effect (Optional)
 */
function initGalleryLightbox() {
    const galleryImages = document.querySelectorAll('.project-gallery img, .gallery img');

    galleryImages.forEach(img => {
        img.style.cursor = 'pointer';
        img.addEventListener('click', function() {
            showImageModal(this.src, this.alt);
        });
    });
}

/**
 * Show Image in Modal
 */
function showImageModal(src, alt) {
    const modal = document.createElement('div');
    modal.className = 'modal fade';
    modal.id = 'imageModal';
    modal.tabIndex = '-1';
    modal.innerHTML = `
        <div class="modal-dialog modal-xl modal-dialog-centered">
            <div class="modal-content bg-dark">
                <div class="modal-header bg-dark border-secondary">
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body p-0">
                    <img src="${src}" alt="${alt}" class="img-fluid w-100">
                </div>
            </div>
        </div>
    `;

    document.body.appendChild(modal);
    const bsModal = new bootstrap.Modal(modal);
    bsModal.show();

    modal.addEventListener('hidden.bs.modal', () => {
        modal.remove();
    });
}

/**
 * Scroll to Top Button
 */
function initScrollToTop() {
    const scrollButton = document.createElement('button');
    scrollButton.id = 'scrollToTop';
    scrollButton.className = 'btn btn-primary rounded-circle';
    scrollButton.innerHTML = '<i class="fas fa-arrow-up"></i>';
    scrollButton.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        display: none;
        z-index: 99;
        width: 50px;
        height: 50px;
        border: none;
        cursor: pointer;
        opacity: 0.7;
        transition: opacity 0.3s ease;
    `;

    document.body.appendChild(scrollButton);

    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 300) {
            scrollButton.style.display = 'block';
        } else {
            scrollButton.style.display = 'none';
        }
    });

    scrollButton.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    scrollButton.addEventListener('mouseenter', () => {
        scrollButton.style.opacity = '1';
    });

    scrollButton.addEventListener('mouseleave', () => {
        scrollButton.style.opacity = '0.7';
    });
}

/**
 * Format Phone Number
 */
function formatPhoneNumber(input) {
    input.addEventListener('input', function() {
        let value = this.value.replace(/\D/g, '');
        if (value.length > 10) {
            value = value.slice(0, 10);
        }
        if (value.length === 10) {
            value = `(${value.slice(0, 3)}) ${value.slice(3, 6)}-${value.slice(6)}`;
        }
        this.value = value;
    });
}

/**
 * Filter Projects by Category
 */
function initProjectFilter() {
    const filterButtons = document.querySelectorAll('.filter-btn');

    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');

            const filterValue = this.getAttribute('data-filter');
            const projectCards = document.querySelectorAll('.project-card');

            projectCards.forEach(card => {
                if (filterValue === '*' || card.getAttribute('data-category') === filterValue) {
                    card.style.display = 'block';
                    setTimeout(() => card.classList.add('fade-in-up'), 10);
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
}

/**
 * Initialize all on page load
 */
document.addEventListener('DOMContentLoaded', function() {
    initNavbar();
    initSmoothScroll();
    initFormValidation();
    initMobileMenu();
    initGalleryLightbox();
    initScrollToTop();
    handleContactFormSuccess();

    // Format phone inputs
    const phoneInputs = document.querySelectorAll('input[type="tel"]');
    phoneInputs.forEach(input => {
        formatPhoneNumber(input);
    });
});

/**
 * Console Log on Page Load
 */
console.log('%c Ctrin Interiors', 'font-size: 20px; font-weight: bold; color: #1e40af;');
console.log('%c Premium Interior Design Solutions', 'font-size: 14px; color: #6b7280;');
