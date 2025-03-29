document.addEventListener('DOMContentLoaded', function() {
    const modeToggleButton = document.getElementById('mode-toggle');
    const fileInput = document.getElementById('file');
    const dataCleaningOptions = document.getElementById('data-cleaning-options');
    
    const currentMode = localStorage.getItem('mode') || 'light';
    document.body.classList.add(`${currentMode}-mode`);

    modeToggleButton.addEventListener('click', function() {
        if (document.body.classList.contains('light-mode')) {
            document.body.classList.remove('light-mode');
            document.body.classList.add('dark-mode');
            localStorage.setItem('mode', 'dark');
            modeToggleButton.innerHTML = '<i class="fas fa-sun"></i>';
        } else {
            document.body.classList.remove('dark-mode');
            document.body.classList.add('light-mode');
            localStorage.setItem('mode', 'light');
            modeToggleButton.innerHTML = '<i class="fas fa-moon"></i>';
        }
    });

    // Show data cleaning options after a file is uploaded
    fileInput.addEventListener('change', function() {
        if (fileInput.files.length > 0) {
            dataCleaningOptions.style.display = 'block';
        }
    });
});
