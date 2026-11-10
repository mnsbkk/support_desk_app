document.addEventListener("DOMContentLoaded", () => {
    // Keep the description count and required-field checks in sync.

    // Client-side form validation
    const form = document.querySelector(".ticket-form");
    if (form) {
        form.addEventListener("submit", (e) => {
            let firstInvalid = null;

            form.querySelectorAll("input, textarea").forEach((field) => {
                field.classList.remove("invalid");
                const valid = field.checkValidity();
                if (!valid) {
                    field.classList.add("invalid");
                    if (!firstInvalid) firstInvalid = field;
                }
            });

            // Custom email validation
            const email = form.querySelector("#email");
            if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim())) {
                email.classList.add("invalid");
                if (!firstInvalid) firstInvalid = email;
            }

            if (firstInvalid) {
                e.preventDefault();
                firstInvalid.focus();
                alert("Please fill in all required fields correctly.");
            }
        });
    }
});