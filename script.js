document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');
    const darkModeToggle = document.getElementById('darkModeToggle');
    const mapFrame = document.getElementById('mapFrame');
    const tabs = document.querySelectorAll('.tab');

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
            mapFrame.src = tab.dataset.map;
        });
    });

    // Lazy loading
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const iframe = entry.target;
                iframe.src = iframe.dataset.src;
                observer.unobserve(iframe);
            }
        });
    });

    observer.observe(mapFrame);

    // Social share functionality (placeholder)
    const shareButtons = document.querySelectorAll('.social-share button');
    shareButtons.forEach(button => {
        button.addEventListener('click', () => {
            alert('Sharing functionality to be implemented');
        });
    });
});