document.addEventListener("DOMContentLoaded", () => {
    const uploadForm = document.querySelector("form");
    const pdfUpload = document.getElementById("pdfUpload");
    const featuresSection = document.querySelector(".features-grid-section");

    if (!uploadForm || !pdfUpload) {
        console.error("Form or PDF input not found!");
        return;
    }

    uploadForm.addEventListener("submit", async (e) => {
        e.preventDefault(); // stop default submit

        console.log("Submit clicked"); // DEBUG

        if (!pdfUpload.files || pdfUpload.files.length === 0) {
            console.log("No file selected"); // DEBUG
            alert("⚠ Please select a PDF file before submitting!");
            return;
        }

        console.log("File is selected, submitting..."); // DEBUG

        const formData = new FormData(uploadForm);

        try {
            const response = await fetch(uploadForm.action, {
                method: "POST",
                body: formData
            });

            const html = await response.text();

            // Replace page content
            document.open();
            document.write(html);
            document.close();

            // Scroll to features section
            const newFeaturesSection = document.querySelector(".features-grid-section");
            if (newFeaturesSection) {
                newFeaturesSection.scrollIntoView({ behavior: "smooth" });
            }
        } catch (err) {
            console.error("Error uploading file:", err);
            alert("There was an error uploading the file. Please try again.");
        }
    });
});
