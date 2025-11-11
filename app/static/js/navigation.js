/**
 * Enhanced Navigation System
 * Handles sidebar collapse/expand for desktop and mobile
 * With localStorage persistence and smooth animations
 */

(function() {
    'use strict';

    // Configuration
    const STORAGE_KEY = 'sidebar_collapsed';
    const MOBILE_BREAKPOINT = 768;
    
    // DOM Elements
    const sidebar = document.getElementById('sidebar');
    const adminContainer = document.getElementById('adminContainer');
    const mainContent = document.getElementById('mainContent');
    const mobileToggle = document.getElementById('mobileToggle');
    const desktopCollapseBtn = document.getElementById('desktopCollapseBtn');
    const overlay = document.getElementById('sidebarOverlay');
    
    // State
    let isMobile = window.innerWidth <= MOBILE_BREAKPOINT;
    let isCollapsed = false;
    let isMobileMenuOpen = false;

    /**
     * Initialize navigation system
     */
    function init() {
        // Load saved collapse state for desktop
        loadCollapseState();
        
        // Setup event listeners
        setupEventListeners();
        
        // Handle initial window size
        handleResize();
        
        console.log('✅ Navigation system initialized');
    }

    /**
     * Load collapse state from localStorage
     */
    function loadCollapseState() {
        if (isMobile) return; // Don't apply collapse state on mobile
        
        const savedState = localStorage.getItem(STORAGE_KEY);
        if (savedState === 'true') {
            setCollapsed(true, false); // false = no animation on initial load
        }
    }

    /**
     * Save collapse state to localStorage
     */
    function saveCollapseState(collapsed) {
        localStorage.setItem(STORAGE_KEY, collapsed.toString());
    }

    /**
     * Set sidebar collapsed state (desktop only)
     */
    function setCollapsed(collapsed, animate = true) {
        if (isMobile) return; // Ignore on mobile
        
        isCollapsed = collapsed;
        
        // Add/remove transition temporarily if no animation needed
        if (!animate) {
            sidebar.style.transition = 'none';
            mainContent.style.transition = 'none';
        }
        
        if (collapsed) {
            sidebar.classList.add('collapsed');
            adminContainer.classList.add('sidebar-collapsed');
        } else {
            sidebar.classList.remove('collapsed');
            adminContainer.classList.remove('sidebar-collapsed');
        }
        
        // Restore transition
        if (!animate) {
            setTimeout(() => {
                sidebar.style.transition = '';
                mainContent.style.transition = '';
            }, 50);
        }
        
        // Save state
        saveCollapseState(collapsed);
        
        // Trigger resize event for charts/tables that might need to adjust
        setTimeout(() => {
            window.dispatchEvent(new Event('resize'));
        }, 300);
    }

    /**
     * Toggle desktop collapse state
     */
    function toggleDesktopCollapse() {
        setCollapsed(!isCollapsed, true);
    }

    /**
     * Toggle mobile menu
     */
    function toggleMobileMenu() {
        if (!isMobile) return;
        
        isMobileMenuOpen = !isMobileMenuOpen;
        
        if (isMobileMenuOpen) {
            sidebar.classList.add('mobile-active');
            overlay.classList.add('active');
            document.body.style.overflow = 'hidden'; // Prevent background scroll
        } else {
            sidebar.classList.remove('mobile-active');
            overlay.classList.remove('active');
            document.body.style.overflow = '';
        }
    }

    /**
     * Close mobile menu
     */
    function closeMobileMenu() {
        if (!isMobile || !isMobileMenuOpen) return;
        toggleMobileMenu();
    }

    /**
     * Handle window resize
     */
    function handleResize() {
        const wasMobile = isMobile;
        isMobile = window.innerWidth <= MOBILE_BREAKPOINT;
        
        // Switched from mobile to desktop
        if (wasMobile && !isMobile) {
            // Clean up mobile state
            sidebar.classList.remove('mobile-active');
            overlay.classList.remove('active');
            document.body.style.overflow = '';
            isMobileMenuOpen = false;
            
            // Restore desktop collapse state
            loadCollapseState();
        }
        
        // Switched from desktop to mobile
        if (!wasMobile && isMobile) {
            // Remove desktop collapse state
            sidebar.classList.remove('collapsed');
            adminContainer.classList.remove('sidebar-collapsed');
            isCollapsed = false;
        }
    }

    /**
     * Setup all event listeners
     */
    function setupEventListeners() {
        // Desktop collapse button
        if (desktopCollapseBtn) {
            desktopCollapseBtn.addEventListener('click', function(e) {
                e.preventDefault();
                toggleDesktopCollapse();
            });
        }
        
        // Mobile toggle button
        if (mobileToggle) {
            mobileToggle.addEventListener('click', function(e) {
                e.preventDefault();
                toggleMobileMenu();
            });
        }
        
        // Overlay click - close mobile menu
        if (overlay) {
            overlay.addEventListener('click', closeMobileMenu);
        }
        
        // Close mobile menu when clicking on a link
        const menuLinks = sidebar.querySelectorAll('.sidebar-menu a');
        menuLinks.forEach(link => {
            link.addEventListener('click', function() {
                if (isMobile && isMobileMenuOpen) {
                    // Small delay for smooth transition
                    setTimeout(closeMobileMenu, 150);
                }
            });
        });
        
        // Window resize handler with debounce
        let resizeTimer;
        window.addEventListener('resize', function() {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(handleResize, 150);
        });
        
        // Keyboard shortcuts
        document.addEventListener('keydown', function(e) {
            // ESC key - close mobile menu
            if (e.key === 'Escape' && isMobile && isMobileMenuOpen) {
                closeMobileMenu();
            }
            
            // Ctrl/Cmd + B - toggle sidebar (desktop only)
            if ((e.ctrlKey || e.metaKey) && e.key === 'b' && !isMobile) {
                e.preventDefault();
                toggleDesktopCollapse();
            }
        });
    }

    /**
     * Public API (if needed for other scripts)
     */
    window.NavigationSystem = {
        toggleCollapse: toggleDesktopCollapse,
        toggleMobile: toggleMobileMenu,
        closeMobile: closeMobileMenu,
        isCollapsed: () => isCollapsed,
        isMobileOpen: () => isMobileMenuOpen,
        isMobileView: () => isMobile
    };

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
