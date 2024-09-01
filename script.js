document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');
    const darkModeToggle = document.getElementById('darkModeToggle');
    const mapFrame = document.getElementById('mapFrame');
    const tabs = document.querySelectorAll('.tab');

    // Function to load a visualization
    function loadVisualization(src) {
        mapFrame.src = src;
    }

    // Load default visualization
    loadVisualization('./output/map-visualization/choropleth.html');

    // Sidebar toggle
    sidebarToggle.addEventListener('click', () => {
        sidebar.style.display = sidebar.style.display === 'none' ? 'block' : 'none';
    });

    // Dark mode toggle
    darkModeToggle.addEventListener('click', () => {
        document.body.classList.toggle('dark-mode');
        const icon = darkModeToggle.querySelector('i');
        icon.classList.toggle('fa-moon');
        icon.classList.toggle('fa-sun');
    });

    // Tab switching
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            loadVisualization(tab.dataset.map);
        });
    });

    // Social share functionality (placeholder)
    const shareButtons = document.querySelectorAll('.social-share button');
    shareButtons.forEach(button => {
        button.addEventListener('click', () => {
            alert('Sharing functionality to be implemented');
        });
    });
});