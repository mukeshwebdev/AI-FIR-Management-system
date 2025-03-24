document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript Loaded!");

    // Navigation Menu Highlight
    let navLinks = document.querySelectorAll(".nav-link");
    navLinks.forEach(link => {
        link.addEventListener("click", function () {
            navLinks.forEach(nav => nav.classList.remove("active"));
            this.classList.add("active");
        });
    });

    // Signup Form Validation
    const signupForm = document.getElementById("signupForm");
    if (signupForm) {
        signupForm.addEventListener("submit", function (event) {
            let username = document.getElementById("username").value.trim();
            let password = document.getElementById("password").value.trim();
            let role = document.getElementById("role").value;

            if (username === "" || password === "" || role === "") {
                alert("All fields are required!");
                event.preventDefault();
            }
        });
    }

    // Login Form Validation
    const loginForm = document.getElementById("loginForm");
    if (loginForm) {
        loginForm.addEventListener("submit", function (event) {
            let username = document.getElementById("loginUsername").value.trim();
            let password = document.getElementById("loginPassword").value.trim();

            if (username === "" || password === "") {
                alert("Please enter both username and password!");
                event.preventDefault();
            }
        });
    }

    // File Upload Preview
    const fileInput = document.getElementById("fileUpload");
    const filePreview = document.getElementById("filePreview");

    if (fileInput && filePreview) {
        fileInput.addEventListener("change", function () {
            let file = fileInput.files[0];
            if (file) {
                let reader = new FileReader();
                reader.onload = function (e) {
                    filePreview.innerHTML = `<img src="${e.target.result}" alt="Uploaded File" style="max-width: 200px; border: 2px solid #ddd; padding: 5px;">`;
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // Smooth Scroll to Sections
    document.querySelectorAll(".scroll-link").forEach(anchor => {
        anchor.addEventListener("click", function (e) {
            e.preventDefault();
            let targetId = this.getAttribute("href").substring(1);
            document.getElementById(targetId).scrollIntoView({ behavior: "smooth" });
        });
    });

    // Speech-to-Text Audio Preview
    const audioInput = document.getElementById("audioUpload");
    const audioPreview = document.getElementById("audioPreview");

    if (audioInput && audioPreview) {
        audioInput.addEventListener("change", function () {
            let audioFile = audioInput.files[0];
            if (audioFile) {
                let audioURL = URL.createObjectURL(audioFile);
                audioPreview.innerHTML = `<audio controls><source src="${audioURL}" type="audio/wav">Your browser does not support the audio element.</audio>`;
            }
        });
    }
});
