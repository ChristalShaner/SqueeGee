document.addEventListener('DOMContentLoaded', function() {
    // Get the toggle button
    const modeToggleButton = document.getElementById('mode-toggle');
    
    // Check for the user's saved theme in localStorage
    const currentMode = localStorage.getItem('mode') || 'light'; // default to light mode

    // Apply the saved mode on page load
    document.body.classList.add(`${currentMode}-mode`);

    // Toggle mode when the button is clicked
    modeToggleButton.addEventListener('click', function() {
        // Toggle between light and dark mode
        if (document.body.classList.contains('light-mode')) {
            document.body.classList.remove('light-mode');
            document.body.classList.add('dark-mode');
            localStorage.setItem('mode', 'dark');  // Save the current mode in localStorage
            modeToggleButton.innerHTML = '<i class="fas fa-sun"></i>'; // Change icon to sun
        } else {
            document.body.classList.remove('dark-mode');
            document.body.classList.add('light-mode');
            localStorage.setItem('mode', 'light');  // Save the current mode in localStorage
            modeToggleButton.innerHTML = '<i class="fas fa-moon"></i>'; // Change icon to moon
        }
    });
});

