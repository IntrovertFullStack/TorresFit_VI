// Page loader functionality
document.addEventListener('DOMContentLoaded', function() {
    const loaderContainer = document.getElementById('loaderContainer');
    
    // Hide loader after page loads
    setTimeout(function() {
      loaderContainer.classList.add('hidden');
    }, 1500); // 1.5 second delay
  });
  
  // Show loader when navigating away
  window.addEventListener('beforeunload', function() {
    const loaderContainer = document.getElementById('loaderContainer');
    loaderContainer.classList.remove('hidden');
  });

  // Page loader functionality
document.addEventListener('DOMContentLoaded', function() {
    const loaderContainer = document.getElementById('loaderContainer');
    
    // Hide loader after page loads
    setTimeout(function() {
      loaderContainer.classList.add('hidden');
    }, 1500); // 1.5 second delay
});

// Show loader when navigating away
window.addEventListener('beforeunload', function() {
    const loaderContainer = document.getElementById('loaderContainer');
    loaderContainer.classList.remove('hidden');
});

// Hide loader when navigating back to the page
window.addEventListener('pageshow', function(event) {
    if (event.persisted) {
        const loaderContainer = document.getElementById('loaderContainer');
        loaderContainer.classList.add('hidden');
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const loaderContainer = document.getElementById('loaderContainer');
    const loaderText = document.getElementById('loaderText');
    
    // Hide loader after page loads
    setTimeout(function() {
        loaderContainer.classList.add('hidden');
    }, 1500); // 1.5 second delay

    // Change loader text if logging out
    if (document.body.classList.contains('logging-out')) {
        loaderText.innerHTML = 'Cerrando <span>Sesión</span>';
    }
});

// Add class to body when logout link is clicked
document.querySelectorAll('.logout-link').forEach(function(link) {
    link.addEventListener('click', function() {
        document.body.classList.add('logging-out');
    });
});