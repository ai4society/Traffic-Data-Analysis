document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');
    const darkModeToggle = document.getElementById('darkModeToggle');
    const mapFrame = document.getElementById('mapFrame');
    const tabs = document.querySelectorAll('.tab');
    
    const rotationOverlay = document.getElementById('rotationOverlay');
    
    // Function to check device orientation
    function checkOrientation() {
        if (window.innerWidth <= 768) {  // Only check on mobile devices
            if (window.innerHeight > window.innerWidth) {  // Portrait mode
                rotationOverlay.classList.remove('hidden');
            } else {  // Landscape mode
                rotationOverlay.classList.add('hidden');
            }
        } else {  // Hide on desktop
            rotationOverlay.classList.add('hidden');
        }
    }
    
    // Add state for user preference
    let userDismissedRotation = false;

    // Modified check orientation to respect user preference
    function checkOrientation() {
        if (window.innerWidth <= 768 && !userDismissedRotation) {  // Only check if not dismissed
            if (window.innerHeight > window.innerWidth) {  // Portrait mode
                rotationOverlay.classList.remove('hidden');
            } else {  // Landscape mode
                rotationOverlay.classList.add('hidden');
            }
        } else {  // Hide on desktop or if dismissed
            rotationOverlay.classList.add('hidden');
        }
    }

    // Handle dismiss button click
    document.getElementById('dismissRotation').addEventListener('click', () => {
        userDismissedRotation = true;
        rotationOverlay.classList.add('hidden');
    });

    // Check orientation on page load and resize
    checkOrientation();
    window.addEventListener('resize', checkOrientation);
    
    // Also add orientation change event listener
    window.addEventListener('orientationchange', () => {
        setTimeout(checkOrientation, 100);  // Small delay to ensure accurate dimensions
    });

    // Initialize state
    let isSidebarVisible = true;
    let isDarkMode = false;

    // Function to handle sidebar visibility
    function toggleSidebar() {
        if (window.innerWidth <= 768) {
            // Mobile behavior
            sidebar.classList.toggle('active');
            isSidebarVisible = sidebar.classList.contains('active');
        } else {
            // Desktop behavior
            isSidebarVisible = !isSidebarVisible;
            sidebar.classList.toggle('collapsed');
        }
    }

    // Function to handle window resize
    function handleResize() {
        if (window.innerWidth > 768) {
            // Reset mobile classes
            sidebar.classList.remove('active');
            // Restore desktop state
            sidebar.classList.toggle('collapsed', !isSidebarVisible);
        } else {
            // Reset desktop classes
            sidebar.classList.remove('collapsed');
        }
    }

    // Function to load visualization
    function loadVisualization(src) {
        mapFrame.src = src;
    }

    // Function to handle dark mode
    function toggleDarkMode() {
        isDarkMode = !isDarkMode;
        document.body.classList.toggle('dark-mode');
        const icon = darkModeToggle.querySelector('i');
        icon.classList.toggle('fa-moon');
        icon.classList.toggle('fa-sun');
        
        // Save preference to localStorage
        localStorage.setItem('darkMode', isDarkMode);
    }

    // Check for saved dark mode preference
    if (localStorage.getItem('darkMode') === 'true') {
        toggleDarkMode();
    }

    // Event Listeners
    sidebarToggle.addEventListener('click', toggleSidebar);
    darkModeToggle.addEventListener('click', toggleDarkMode);
    window.addEventListener('resize', handleResize);

    // Handle tab switching
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            loadVisualization(tab.dataset.map);
            
            // Auto-hide sidebar on mobile after tab selection
            if (window.innerWidth <= 768 && sidebar.classList.contains('active')) {
                toggleSidebar();
            }
        });
    });

    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', (e) => {
        if (window.innerWidth <= 768 && 
            !sidebar.contains(e.target) && 
            !sidebarToggle.contains(e.target) && 
            sidebar.classList.contains('active')) {
            toggleSidebar();
        }
    });

    // Load default visualization
    loadVisualization('./output/map-visualization/choropleth.html');
    
    // Initial resize handle
    handleResize();
});