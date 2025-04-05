document.addEventListener('DOMContentLoaded', function() {
    const modeToggleButton = document.getElementById('mode-toggle');
    const fileInput = document.getElementById('file');
    const dataCleaningOptions = document.getElementById('data-cleaning-options');
    let dropArea = document.getElementById("drop-area");
    let fileNameDisplay = document.getElementById("file-name"); // Ensure there's an element for file name
    const chickyImage = document.getElementById("chicky-image"); // Get the image element

    // Function to toggle images based on mode
    function updateChickyImage(mode) {
        if (mode === 'dark') {
            chickyImage.src = "/static/images/chicky-dark-mode.png"; // Dark mode image
        } else {
            chickyImage.src = "/static/images/chicky-file-upload.png"; // Light mode image
        }
    }

    // Load mode from local storage
    const currentMode = localStorage.getItem('mode') || 'light';
    document.body.classList.add(`${currentMode}-mode`);
    updateChickyImage(currentMode);

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
            updateFileName(fileInput.files[0]); // Display file name
            dataCleaningOptions.style.display = 'block';
        }
        const scrollTarget = document.getElementById("handle-missing-values");
        if (scrollTarget) {
            setTimeout(() => {
                scrollTarget.scrollIntoView({ behavior: "smooth", block: "start" });
            }, 300); // Slight delay to allow form to render
        }
    });

    // Prevent default behavior for drag events
    ["dragenter", "dragover", "dragleave", "drop"].forEach(event => {
        dropArea.addEventListener(event, e => e.preventDefault(), false);
    });

    // Highlight drop area
    dropArea.addEventListener("dragover", () => dropArea.classList.add("highlight"));
    dropArea.addEventListener("dragleave", () => dropArea.classList.remove("highlight"));

    // Handle file drop
    dropArea.addEventListener("drop", e => {
        dropArea.classList.remove("highlight");

        let files = e.dataTransfer.files;
        if (files.length > 0) {
            // Workaround for browser security restrictions
            let fileList = new DataTransfer();
            fileList.items.add(files[0]); // Only first file allowed
            fileInput.files = fileList.files;

            updateFileName(files[0]); // Display file name
            fileInput.dispatchEvent(new Event("change")); // Ensure change event triggers
        }
    });

    // Open file browser on click
    dropArea.addEventListener("click", () => fileInput.click());

    // Function to update file name display
    function updateFileName(file) {
        fileNameDisplay.textContent = `Selected File: ${file.name}`;
    }

    // Tooltip initialization for bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.forEach(function (tooltipTriggerEl) {
        new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Scroll to "Original Data" if cleaning just happened
    const scrollFlag = document.getElementById("scroll-flag");
    if (scrollFlag && scrollFlag.dataset.scroll === "original-data") {
        const target = document.getElementById("original-data");
        if (target) {
            setTimeout(() => {
                target.scrollIntoView({ behavior: "smooth", block: "start" });
            }, 300);
        }
    }

    // Scroll to "Data Visualization" section when clicking "Generate Chart"
    const generateChartButton = document.getElementById("generate-chart");
    if (generateChartButton) {
        generateChartButton.addEventListener("click", function() {
            const target = document.getElementById("charts-container");
            if (target) {
                setTimeout(() => {
                    target.scrollIntoView({ behavior: "smooth", block: "start" });
                }, 300);
            }
        });
    }
});
