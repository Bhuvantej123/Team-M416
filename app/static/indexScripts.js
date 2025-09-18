document.addEventListener("DOMContentLoaded", () => {
    const uploadBtn = document.getElementById("uploadBtn");
    const pdfUpload = document.getElementById("pdfUpload");
    const featuresSection = document.querySelector(".features-grid-section");

    uploadBtn.addEventListener("click", () => {
        // Check if a file is selected
        if (pdfUpload.files.length > 0) {
            // Smoothly scroll down to features section
            featuresSection.scrollIntoView({ behavior: "smooth" });
        } else {
            // Optional: alert or highlight that user must select a file
            alert("Please select a PDF file before continuing!");
        }
    });
});
