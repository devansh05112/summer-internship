document.addEventListener("DOMContentLoaded", () => {

    /* ==========================================
       Greeting Based On Time
    ========================================== */

    const heading = document.querySelector(".header h1");

    if (heading) {

        const hour = new Date().getHours();

        let greeting = "Welcome back";

        if (hour < 12) {

            greeting = "Good Morning";

        } else if (hour < 17) {

            greeting = "Good Afternoon";

        } else {

            greeting = "Good Evening";

        }

        const profile = heading.textContent.split(",")[1] || "";

        heading.innerHTML = `${greeting},${profile}`;

    }

    /* ==========================================
       Animated Stat Counters
    ========================================== */

    const counters = document.querySelectorAll(".stat-card h3");

    counters.forEach(counter => {

        const original = counter.innerText;

        const number = parseInt(original);

        if (isNaN(number)) return;

        let current = 0;

        const step = Math.max(1, Math.ceil(number / 40));

        const interval = setInterval(() => {

            current += step;

            if (current >= number) {

                current = number;

                clearInterval(interval);

            }

            counter.innerText = current;

        }, 25);

    });

    /* ==========================================
       Show Selected PDF Name
    ========================================== */

    const fileInput = document.querySelector('input[type="file"]');

    const uploadTitle = document.querySelector(".upload-box h3");

    const uploadText = document.querySelector(".upload-box p");

    if (fileInput) {

        fileInput.addEventListener("change", () => {

            if (fileInput.files.length > 0) {

                uploadTitle.innerHTML = fileInput.files[0].name;

                uploadText.innerHTML = "Ready to upload";

            }

        });

    }

    /* ==========================================
       Notification Bell Animation
    ========================================== */

    const bell = document.querySelector(".icon-btn");

    if (bell) {

        bell.addEventListener("click", () => {

            bell.style.transform = "rotate(20deg)";

            setTimeout(() => {

                bell.style.transform = "rotate(-20deg)";

            }, 100);

            setTimeout(() => {

                bell.style.transform = "rotate(0deg)";

            }, 200);

        });

    }

    /* ==========================================
       Card Hover Effect
    ========================================== */

    const cards = document.querySelectorAll(".stat-card");

    cards.forEach(card => {

        card.addEventListener("mouseenter", () => {

            card.style.transform = "translateY(-8px) scale(1.02)";

        });

        card.addEventListener("mouseleave", () => {

            card.style.transform = "translateY(0px) scale(1)";

        });

    });

    /* ==========================================
       Upload Button Loading Effect
    ========================================== */

    const form = document.querySelector("form");

    const uploadBtn = document.querySelector(".upload-btn");

    if (form && uploadBtn) {

        form.addEventListener("submit", () => {

            uploadBtn.disabled = true;

            uploadBtn.innerHTML =

                '<i class="fas fa-spinner fa-spin"></i> Uploading...';

        });

    }

});