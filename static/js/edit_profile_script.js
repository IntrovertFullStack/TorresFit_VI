document.addEventListener('DOMContentLoaded', function() {
    // Get current year for footer
    document.getElementById('current-year').textContent = new Date().getFullYear();

    // Sidebar toggle functionality
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('mainContent');
    const sidebarToggle = document.getElementById('sidebarToggle');
    const mobileSidebarToggle = document.getElementById('mobileSidebarToggle');
    const toggleIcon = document.getElementById('toggleIcon');

    // Function to toggle sidebar
    function toggleSidebar() {
        sidebar.classList.toggle('active');
        mainContent.classList.toggle('sidebar-open');
        
        // Change toggle icon direction
        if (sidebar.classList.contains('active')) {
            toggleIcon.classList.remove('fa-chevron-left');
            toggleIcon.classList.add('fa-chevron-right');
        } else {
            toggleIcon.classList.remove('fa-chevron-right');
            toggleIcon.classList.add('fa-chevron-left');
        }
    }

    // Desktop sidebar toggle
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', toggleSidebar);
    }

    // Mobile sidebar toggle
    if (mobileSidebarToggle) {
        mobileSidebarToggle.addEventListener('click', toggleSidebar);
    }

    // Close sidebar on mobile when clicking outside
    document.addEventListener('click', function(event) {
        const isMobile = window.innerWidth < 768;
        if (isMobile && 
            !event.target.closest('.sidebar') && 
            !event.target.closest('.mobile-sidebar-toggle') &&
            sidebar.classList.contains('active')) {
            toggleSidebar();
        }
    });

    // Handle message alerts
    $('.django-message').each(function() {
        var level = $(this).data('level');
        var message = $(this).text().trim();
        
        // Create Bootstrap alerts
        if(message) {
            var alertClass = 'alert-info';
            if(level === 'success') alertClass = 'alert-success';
            if(level === 'error') alertClass = 'alert-danger';
            if(level === 'warning') alertClass = 'alert-warning';
            
            $('body').append(
                '<div class="alert ' + alertClass + ' alert-dismissible fade show position-fixed" style="top: 20px; right: 20px; z-index: 9999;" role="alert">' +
                message +
                '<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
                '<span aria-hidden="true">&times;</span>' +
                '</button>' +
                '</div>'
            );
        }
    });
    
    // Auto dismiss alerts after 5 seconds
    setTimeout(function() {
        $('.alert').alert('close');
    }, 5000);

    // Initialize WOW.js animations
    if (typeof WOW !== 'undefined') {
        new WOW().init();
    }
});