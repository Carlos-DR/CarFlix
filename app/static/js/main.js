// ============================================
// CARFLIX - JAVASCRIPT PRINCIPAL
// ============================================

document.addEventListener('DOMContentLoaded', function() {

    // ========== NAVBAR SCROLL EFFECT ==========
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }

    // ========== AUTO-CLOSE FLASH MESSAGES ==========
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        // Cerrar automáticamente después de 5 segundos
        setTimeout(function() {
            alert.style.animation = 'slideOut 0.3s ease';
            setTimeout(function() {
                alert.remove();
            }, 300);
        }, 5000);

        // Cerrar al hacer click en el botón
        const closeBtn = alert.querySelector('.close-alert');
        if (closeBtn) {
            closeBtn.addEventListener('click', function() {
                alert.style.animation = 'slideOut 0.3s ease';
                setTimeout(function() {
                    alert.remove();
                }, 300);
            });
        }
    });

    // ========== CONTENT ROW SCROLL ==========
    const contentRows = document.querySelectorAll('.content-row');
    contentRows.forEach(function(row) {
        let isDown = false;
        let startX;
        let scrollLeft;

        row.addEventListener('mousedown', function(e) {
            isDown = true;
            row.style.cursor = 'grabbing';
            startX = e.pageX - row.offsetLeft;
            scrollLeft = row.scrollLeft;
        });

        row.addEventListener('mouseleave', function() {
            isDown = false;
            row.style.cursor = 'default';
        });

        row.addEventListener('mouseup', function() {
            isDown = false;
            row.style.cursor = 'default';
        });

        row.addEventListener('mousemove', function(e) {
            if (!isDown) return;
            e.preventDefault();
            const x = e.pageX - row.offsetLeft;
            const walk = (x - startX) * 2;
            row.scrollLeft = scrollLeft - walk;
        });
    });

    // ========== FORMS VALIDATION ==========
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"], input[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Procesando...';

                // Re-habilitar después de 5 segundos por si hay error
                setTimeout(function() {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = submitBtn.getAttribute('data-original-text') || 'Enviar';
                }, 5000);
            }
        });
    });

    // ========== IMAGE LAZY LOADING ==========
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver(function(entries, observer) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                observer.unobserve(img);
            }
        });
    });

    images.forEach(function(img) {
        imageObserver.observe(img);
    });

    // ========== CONFIRM DELETIONS ==========
    const deleteLinks = document.querySelectorAll('a[href*="delete"]');
    deleteLinks.forEach(function(link) {
        if (!link.hasAttribute('onclick')) {
            link.addEventListener('click', function(e) {
                if (!confirm('¿Estás seguro de que quieres eliminar esto? Esta acción no se puede deshacer.')) {
                    e.preventDefault();
                }
            });
        }
    });

    // ========== SMOOTH SCROLL ==========
    const smoothScrollLinks = document.querySelectorAll('a[href^="#"]');
    smoothScrollLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#' && document.querySelector(href)) {
                e.preventDefault();
                document.querySelector(href).scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // ========== DROPDOWN MENU MOBILE ==========
    const userBtn = document.querySelector('.user-btn');
    const dropdownMenu = document.querySelector('.dropdown-menu');

    if (userBtn && dropdownMenu && window.innerWidth <= 768) {
        userBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            dropdownMenu.style.opacity = dropdownMenu.style.opacity === '1' ? '0' : '1';
            dropdownMenu.style.visibility = dropdownMenu.style.visibility === 'visible' ? 'hidden' : 'visible';
        });

        document.addEventListener('click', function() {
            dropdownMenu.style.opacity = '0';
            dropdownMenu.style.visibility = 'hidden';
        });
    }

    // ========== FILE INPUT PREVIEW ==========
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(function(input) {
        input.addEventListener('change', function(e) {
            const fileName = e.target.files[0]?.name;
            if (fileName) {
                const label = input.nextElementSibling;
                if (label && label.classList.contains('form-text')) {
                    const originalText = label.textContent;
                    label.textContent = `Archivo seleccionado: ${fileName}`;
                    label.style.color = 'var(--success-color)';
                }

                // Preview para imágenes
                if (input.accept && input.accept.includes('image')) {
                    const file = e.target.files[0];
                    const reader = new FileReader();

                    reader.onload = function(event) {
                        let preview = input.parentElement.querySelector('.preview-image');
                        if (!preview) {
                            preview = document.createElement('img');
                            preview.className = 'preview-image';
                            input.parentElement.appendChild(preview);
                        }
                        preview.src = event.target.result;
                    };

                    reader.readAsDataURL(file);
                }
            }
        });
    });

    // ========== SEARCH AUTO-SUBMIT ==========
    const searchInput = document.querySelector('.search-input-large');
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            // Auto-submit después de 500ms de inactividad
            // searchTimeout = setTimeout(function() {
            //     searchInput.form.submit();
            // }, 500);
        });
    }

    // ========== LOADING STATES ==========
    window.showLoading = function(element) {
        if (element) {
            element.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Cargando...';
            element.disabled = true;
        }
    };

    window.hideLoading = function(element, originalText) {
        if (element) {
            element.innerHTML = originalText;
            element.disabled = false;
        }
    };

    // ========== TOOLTIPS SIMPLE ==========
    const tooltipElements = document.querySelectorAll('[title]');
    tooltipElements.forEach(function(element) {
        element.addEventListener('mouseenter', function() {
            const title = this.getAttribute('title');
            if (title) {
                this.setAttribute('data-title', title);
                this.removeAttribute('title');

                const tooltip = document.createElement('div');
                tooltip.className = 'custom-tooltip';
                tooltip.textContent = title;
                tooltip.style.cssText = `
                    position: absolute;
                    background: rgba(0,0,0,0.9);
                    color: white;
                    padding: 8px 12px;
                    border-radius: 4px;
                    font-size: 14px;
                    z-index: 10000;
                    pointer-events: none;
                    white-space: nowrap;
                `;

                document.body.appendChild(tooltip);

                const rect = this.getBoundingClientRect();
                tooltip.style.top = (rect.top - tooltip.offsetHeight - 5) + 'px';
                tooltip.style.left = (rect.left + rect.width / 2 - tooltip.offsetWidth / 2) + 'px';

                this.tooltipElement = tooltip;
            }
        });

        element.addEventListener('mouseleave', function() {
            if (this.tooltipElement) {
                this.tooltipElement.remove();
                this.tooltipElement = null;
            }
            if (this.getAttribute('data-title')) {
                this.setAttribute('title', this.getAttribute('data-title'));
                this.removeAttribute('data-title');
            }
        });
    });

    console.log('🎬 Carflix initialized successfully!');
});

// ========== ANIMACIÓN SLIDEOUT PARA ALERTS ==========
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);