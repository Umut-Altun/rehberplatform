document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const toggleButton = document.querySelector('.toggle-sidebar');
    const sidebar = document.querySelector('.sidebar');
    const body = document.body;
    
    // Create overlay for mobile
    const overlay = document.createElement('div');
    overlay.className = 'sidebar-overlay';
    document.body.appendChild(overlay);
    
    // Toggle sidebar
    function toggleSidebar() {
        sidebar.classList.toggle('active');
        overlay.classList.toggle('active');
        body.classList.toggle('sidebar-open');
    }
    
    // Event listeners
    if (toggleButton) {
        toggleButton.addEventListener('click', toggleSidebar);
    }
    
    // Close sidebar when clicking on overlay
    overlay.addEventListener('click', toggleSidebar);
    
    // Close sidebar when pressing escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && sidebar.classList.contains('active')) {
            toggleSidebar();
        }
    });
    
    // Close sidebar when window is resized to desktop size
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768 && sidebar.classList.contains('active')) {
            toggleSidebar();
        }
    });

    // Highlight active menu item based on current URL
    function setActiveMenuItem() {
        const currentPath = window.location.pathname;
        const navItems = document.querySelectorAll('.nav-item');
        
        // Remove active class from all items
        navItems.forEach(item => {
            item.classList.remove('active');
        });
        
        // Find matching nav item
        navItems.forEach(item => {
            const link = item.querySelector('.nav-link');
            if (!link) return;
            
            const href = link.getAttribute('href');
            
            // Skip root path match for non-root links
            if (currentPath === '/' && href !== '/') return;
            
            // Check if current path starts with the link's href
            if (href !== '/' && currentPath.startsWith(href)) {
                item.classList.add('active');
            } else if (href === '/' && currentPath === '/') {
                item.classList.add('active');
            }
        });
    }
    
    // Set active menu item on page load
    setActiveMenuItem();
});